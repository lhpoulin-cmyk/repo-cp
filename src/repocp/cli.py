"""Repository governance: read-only audits and explicit local repository creation."""
import argparse
import json
from pathlib import Path
import sys

from .audit import audit, proposals, registry, text_report
from .consumer import ROOT, render, verify
from .diagnostics import blocker
from .file_integrity import INVARIANT
from .safety import Denied, MAX_BYTES
from .work_protocol import CLEAN_EXECUTION_BASELINE, schemas as protocol_schemas, validate as validate_work


class Parser(argparse.ArgumentParser):
    def error(self, message):
        # argparse's default includes untrusted arguments in diagnostics.
        raise Denied('CLI_ARGUMENTS')


def main():
    if sys.argv[1:2] == ['create']:
        from .create import main as create_main
        return create_main(sys.argv[2:])
    try:
        parser = Parser(description=__doc__, epilog='Create a local repository: repo-cp create --help')
        parser.add_argument('command', choices=('validate', 'render', 'inventory', 'audit', 'drift', 'propose',
                                                'check-work-entry', 'check-work-result'))
        parser.add_argument('--fleet-root', type=Path, default=ROOT.parent)
        parser.add_argument('--pilot', action='store_true')
        parser.add_argument('--repository', help='Restrict an already selected enrolled/pilot scope')
        parser.add_argument('--text', action='store_true')
        args = parser.parse_args()
        if args.command == 'render':
            output = render(sys.stdin.buffer.read(MAX_BYTES + 1))
            status = 0
        elif args.command in ('check-work-entry', 'check-work-result'):
            verify()
            kind = 'entry' if args.command == 'check-work-entry' else 'result'
            data = validate_work(kind, sys.stdin.buffer.read(MAX_BYTES + 1))
            output = json.dumps(data, indent=2, sort_keys=True) + '\n'
            status = 1 if kind == 'entry' and data['mutation_gate'] == 'CLOSED' else 0
        else:
            verify()
            data = registry()
            if args.command == 'validate':
                protocol_schemas()
                data = {'status': 'PASS', 'foundation_integrity': 'PASS', 'enrollment_schema': 'PASS',
                        'file_integrity_schema': 'PASS', 'work_entry_schema': 'PASS',
                        'work_result_schema': 'PASS', 'invariant_id': INVARIANT,
                        'clean_execution_invariant_id': CLEAN_EXECUTION_BASELINE,
                        'automatic_execution': False, 'live_mutation': 'NONE'}
            elif args.command != 'inventory':
                data = audit(args.fleet_root, pilot=args.pilot, repository=args.repository)
                if args.command == 'propose':
                    data = proposals(data)
            status = 0
            if args.command in ('audit', 'drift'):
                status = {'PASS': 0, 'DRIFT': 1, 'UNKNOWN': 1, 'BLOCKED': 2}[data['status']]
            output = (text_report(data) if args.text and args.command in ('audit', 'drift')
                      else json.dumps(data, indent=2, sort_keys=True) + '\n')
    except (Denied, OSError, ValueError, TypeError, KeyError, RecursionError, ImportError) as error:
        # No partial stdout, traceback, rejected payload, paths or command text;
        # only an allowlisted constant reason code may follow the blocker.
        sys.stderr.write(blocker('REPO_CP_NONCONFORMANCE', error))
        return 2
    sys.stdout.write(output)
    return status
