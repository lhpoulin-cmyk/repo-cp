"""Allowlisted reason codes, the denial-site inventory and hostile exceptions."""
import ast
import contextlib
import io
from pathlib import Path
import sys
import textwrap
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from repocp import cli
from repocp.diagnostics import CANONICAL, INTERNAL, PUBLIC, blocker, public_reason
from repocp.publication import Outcome, PublicationFailure
from repocp.safety import Denied

SOURCES = (*sorted((ROOT / 'src/repocp').glob('*.py')),
           *(ROOT / 'tools' / name for name in ('validate', 'repo-cp', 'audit-hardlinks')))
GENERIC = 'BLOCKER=REPO_CP_NONCONFORMANCE\n'


def inventory(sources):
    """Structural (AST) denial inventory; no text matching.

    Finds every class derived from Denied, then classifies every reference to
    those classes by its syntactic role. Allowed roles: a call, an except
    clause, a class base, isinstance's class argument or an is/is-not type
    identity comparison. Any other reference
    (aliasing, assignment, passing the class around) is reported, because a
    detector cannot follow it. Denied calls must pass one str literal.
    """
    trees = {str(path): ast.parse(source) for path, source in sources.items()}
    classes = {'Denied'}
    changed = True
    while changed:
        changed = False
        for tree in trees.values():
            for node in ast.walk(tree):
                if (isinstance(node, ast.ClassDef) and node.name not in classes
                        and any(name_of(base) in classes for base in node.bases)):
                    classes.add(node.name)
                    changed = True
    codes, subclass_sites, problems = {}, [], []
    for path, tree in trees.items():
        parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    if alias.name.split('.')[-1] in classes and alias.asname not in (None, alias.name):
                        problems.append((path, node.lineno, 'ALIASED_IMPORT'))
                continue
            if name_of(node) not in classes or not hasattr(node, 'ctx'):
                continue
            if not isinstance(node.ctx, ast.Load):
                problems.append((path, node.lineno, 'REBOUND_NAME'))  # Shadowing hides sites.
                continue
            parent = parents[node]
            role = parent
            if isinstance(parent, ast.Tuple):
                role = parents[parent]
            if isinstance(parent, ast.Call) and parent.func is node:
                if name_of(node) != 'Denied':
                    subclass_sites.append((path, node.lineno, name_of(node)))
                elif (len(parent.args) == 1 and not parent.keywords
                      and isinstance(parent.args[0], ast.Constant) and type(parent.args[0].value) is str):
                    codes.setdefault(parent.args[0].value, []).append((path, node.lineno))
                else:
                    problems.append((path, node.lineno, 'NON_LITERAL_DENIAL'))
            elif isinstance(role, ast.ExceptHandler) or (isinstance(parent, ast.ClassDef) and node in parent.bases):
                continue
            elif (isinstance(role, ast.Call) and name_of(role.func) == 'isinstance'
                  and len(role.args) == 2 and (role.args[1] is node or role.args[1] is parent)):
                continue
            elif (isinstance(parent, ast.Compare) and node in parent.comparators
                  and all(isinstance(op, (ast.Is, ast.IsNot)) for op in parent.ops)):
                continue  # Exact type identity checks cannot construct a denial.
            else:
                problems.append((path, node.lineno, 'ESCAPED_REFERENCE'))
    return codes, subclass_sites, problems


def name_of(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def repository_inventory():
    return inventory({path: path.read_text() for path in SOURCES})


class InventoryTests(unittest.TestCase):
    def test_every_denial_code_is_literal_and_classified_once(self):
        codes, subclass_sites, problems = repository_inventory()
        self.assertEqual(problems, [])
        self.assertEqual(PUBLIC & INTERNAL, frozenset())
        self.assertEqual(sorted(set(codes) - PUBLIC - INTERNAL), [], 'unclassified denial code')
        self.assertEqual(sorted((PUBLIC | INTERNAL) - set(codes)), [], 'stale classification')
        # The only subclass construction is the publication reference, which the
        # exact-type rule keeps generic (tested below).
        self.assertEqual({name for _, _, name in subclass_sites}, {'PublicationFailure'})

    def test_inventory_detects_new_and_evasive_sites(self):
        def scan(source):
            return inventory({'synthetic.py': textwrap.dedent(source)})
        codes, _, problems = scan('''
            from .safety import Denied
            def f(x):
                if x:
                    raise Denied('BRAND_NEW_CODE')
                raise safety.Denied('ATTRIBUTE_CODE') from None
            ''')
        self.assertEqual(set(codes), {'BRAND_NEW_CODE', 'ATTRIBUTE_CODE'})
        self.assertEqual(problems, [])
        for allowed in ('type(e) is Denied', 'type(e) is not Denied', 'isinstance(e, (OSError, Denied))',
                        'try:\n    pass\nexcept (Denied, OSError):\n    pass'):
            self.assertEqual(scan(allowed)[2], [], allowed)
        self.assertNotEqual(scan('type(e) == Denied')[2], [])  # Equality is not an allowed role.
        for label, source in [
                ('non-literal', 'raise Denied(code)'),
                ('formatted', "raise Denied(f'CODE_{x}')"),
                ('two arguments', "raise Denied('CODE', detail)"),
                ('keyword', "raise Denied(reason='CODE')"),
                ('aliased import', 'from .safety import Denied as Refused'),
                ('assigned alias', 'Refused = Denied'),
                ('passed around', 'factory(Denied)'),
                ('rebound', 'Denied = ValueError'),
                ('subclass alias', "class Refused(Denied):\n    pass\nR = Refused")]:
            with self.subTest(label):
                self.assertNotEqual(scan(source)[2], [], label)
        # New subclasses are discovered transitively and reported as subclass sites.
        codes, subclass_sites, problems = scan(
            "class A(Denied):\n    pass\nclass B(A):\n    pass\nraise B('X')\n")
        self.assertEqual((codes, problems), ({}, []))
        self.assertEqual([site[2] for site in subclass_sites], ['B'])


class ReasonTests(unittest.TestCase):
    def test_public_codes_emit_one_constant_reason_line(self):
        for code in sorted(PUBLIC):
            with self.subTest(code):
                self.assertEqual(blocker('REPO_CP_NONCONFORMANCE', Denied(code)),
                                 GENERIC + 'REASON=' + code + '\n')
                self.assertIs(public_reason(Denied(code)), CANONICAL[code])

    def test_internal_codes_keep_generic_fallback(self):
        for code in sorted(INTERNAL):
            with self.subTest(code):
                self.assertEqual(blocker('REPO_CP_NONCONFORMANCE', Denied(code)), GENERIC)

    def test_unknown_and_malformed_codes_keep_generic_fallback(self):
        for code in ('NOT_A_REGISTERED_CODE', 'FOUNDATION_PIN_INVALID_EXTRA', 'foundation_pin_invalid',
                     ' FOUNDATION_PIN_INVALID', 'FOUNDATION_PIN_INVALID\n', '', 'A' * 4096):
            with self.subTest(code=code[:40]):
                self.assertEqual(blocker('REPO_CP_NONCONFORMANCE', Denied(code)), GENERIC)

    def hostile(self):
        marker = 'HOSTILE_MARKER'

        class EqualsEverything(str):
            def __eq__(self, other):
                return True
            def __hash__(self):
                return hash('FOUNDATION_PIN_INVALID')
            def __str__(self):
                return marker

        class PublicSubclass(Denied):
            def __str__(self):
                return marker

        secret = 'tok' + 'en=' + 'SYNTHETIC' * 3
        return marker, [
            Denied('FOUNDATION_PIN_INVALID\nREASON=' + marker),
            Denied(marker + ' /private/path ' + secret),
            Denied('FOUNDATION_PIN_INVALID', marker),
            Denied(),
            Denied(b'FOUNDATION_PIN_INVALID'),
            Denied(EqualsEverything('FOUNDATION_PIN_INVALID')),
            PublicSubclass('FOUNDATION_PIN_INVALID'),
            PublicationFailure(Outcome('FAILED', marker, 'CONCURRENCY_CONFLICT')),
            OSError(2, marker, '/private/' + marker),
            ValueError(secret + marker),
            KeyError(marker),
            TypeError(marker),
            RecursionError(marker),
            ImportError(marker),
        ]

    def test_hostile_exceptions_never_reach_stderr(self):
        marker, errors = self.hostile()
        for error in errors:
            with self.subTest(error=type(error).__name__):
                self.assertEqual(blocker('REPO_CP_NONCONFORMANCE', error), GENERIC)

    def test_cli_hostile_exception_keeps_status_and_empty_stdout(self):
        marker, errors = self.hostile()
        for error in errors:
            with self.subTest(error=type(error).__name__):
                stdout, stderr = io.StringIO(), io.StringIO()
                with patch.object(sys, 'argv', ['repo-cp', 'validate']), \
                        patch.object(cli, 'verify', side_effect=error), \
                        contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    status = cli.main()
                self.assertEqual((status, stdout.getvalue(), stderr.getvalue()), (2, '', GENERIC))
                self.assertNotIn(marker, stderr.getvalue())

    def test_cli_public_code_in_process(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(sys, 'argv', ['repo-cp', 'inventory']), \
                patch.object(cli, 'verify', side_effect=Denied('FOUNDATION_PIN_INVALID')), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            status = cli.main()
        self.assertEqual((status, stdout.getvalue(), stderr.getvalue()),
                         (2, '', GENERIC + 'REASON=FOUNDATION_PIN_INVALID\n'))


if __name__ == '__main__':
    unittest.main()
