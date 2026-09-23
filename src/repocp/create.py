"""Explicit local repository creation, separate from read-only audit commands.

Linux, ordinary user, public metadata only. Build in a private sibling directory,
fsync it, then publish with renameat2(NOREPLACE). Existing targets are never
modified. Interrupted staging is retained for inspection, never glob-cleaned.
"""
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys

from .agent_contract import verify_agent_contract
from .consumer import ROOT
from .diagnostics import blocker
from .publication import (absolute_file, check_directory_path, exists, locked_directory,
                          rename_exclusive, require_unprivileged, termination_control, Interrupted)
from .safety import Denied, open_directory, read_public, require_single_regular
from .scaffold import TEMPLATE_VERSION, scaffold

INTENT = '.repo-cp-create.json'
GENERATOR_FILES = ('src/repocp/create.py', 'src/repocp/scaffold.py',
                   'src/repocp/agent_contract.py', 'src/repocp/publication.py',
                   'src/repocp/safety.py')


def git_init(directory):
    """Ignore ambient Git config/env/templates; never invoke a shell or hooks."""
    git = shutil.which('git', path=os.defpath)
    if git is None:
        raise Denied('CREATE_GIT_UNAVAILABLE')
    try:
        subprocess.run([git, 'init', '--quiet', '--template=', '--initial-branch=main',
                        '--object-format=sha1', '.'],
                       cwd=f'/proc/self/fd/{directory}', pass_fds=(directory,),
                       env={'PATH': os.defpath, 'HOME': '/nonexistent', 'LC_ALL': 'C',
                            'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull},
                       stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, check=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        raise Denied('CREATE_GIT_FAILED') from None


def write_file(directory, name, raw):
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                 0o600, dir_fd=directory)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def verify_tree(path, files, intent):
    """Verify generated public files and Git's initial state independently."""
    for name, raw in {**files, INTENT: intent}.items():
        if read_public(path, name) != raw:
            raise Denied('CREATE_CONTENT_MISMATCH')
    if read_public(path, '.git/HEAD') != b'ref: refs/heads/main\n':
        raise Denied('CREATE_CONTENT_MISMATCH')
    # Inspect only fixed directories through no-follow descriptors. An altered
    # recovery tree must never redirect inspection through a symlink or hide
    # commits in packed refs, reflogs, alternate object stores or loose objects.
    directories = {
        '': set(files) | {INTENT, '.git'},
        '.git': {'HEAD', 'config', 'objects', 'refs'},
        '.git/refs': {'heads', 'tags'},
        '.git/refs/heads': set(),
        '.git/refs/tags': set(),
        '.git/objects': {'info', 'pack'},
        '.git/objects/info': set(),
        '.git/objects/pack': set(),
    }
    for relative, expected in directories.items():
        fd = open_directory(Path(path) / relative)
        try:
            if set(os.listdir(fd)) != expected:
                raise Denied('CREATE_CONTENT_MISMATCH')
        finally:
            os.close(fd)
    # This is a strict fresh-init format check, not a general Git config parser.
    # Reject all other sections/keys, including case variants and include files,
    # without asking Git to interpret potentially executable configuration.
    lines = read_public(path, '.git/config').decode('ascii').splitlines()
    if not lines or lines[0] != '[core]':
        raise Denied('CREATE_CONTENT_MISMATCH')
    config = {}
    for line in lines[1:]:
        key, separator, value = line.strip().partition(' = ')
        if not separator or key in config:
            raise Denied('CREATE_CONTENT_MISMATCH')
        config[key] = value
    required = {'repositoryformatversion': {'0'}, 'filemode': {'true', 'false'},
                'bare': {'false'}, 'logallrefupdates': {'true'}}
    allowed = {**required, 'ignorecase': {'true'}, 'symlinks': {'false'}}
    if (not set(required) <= set(config) <= set(allowed)
            or any(value not in allowed[key] for key, value in config.items())):
        raise Denied('CREATE_CONTENT_MISMATCH')


def sync_tree(path):
    """Only traverse our private, generated tree; validate files before fsync."""
    for root, dirs, files in os.walk(path, topdown=False, followlinks=False):
        for name in dirs:
            if (Path(root) / name).is_symlink():
                raise Denied('CREATE_CONTENT_MISMATCH')
        for name in files:
            fd = os.open(Path(root) / name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            try:
                info = os.fstat(fd)
                require_single_regular(info)
                if info.st_uid != os.geteuid():
                    raise Denied('CREATE_CONTENT_MISMATCH')
                os.fsync(fd)
            finally:
                os.close(fd)
        fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def create_repository(destination, *, purpose, owner='Louis', dry_run=False, source=ROOT):
    require_unprivileged()
    target = absolute_file(destination)
    files = scaffold(target.name, purpose, owner)
    verify_agent_contract(source)
    generator = {name: hashlib.sha256(read_public(source, name)).hexdigest()
                 for name in GENERATOR_FILES}
    parent_info = target.parent.stat()
    committed = False
    try:
        with locked_directory(target.parent, parent_info.st_dev) as parent:
            if exists(parent, target.name):
                raise Denied('CREATE_DESTINATION_EXISTS')
            result = {'schema_version': 1, 'status': 'PLANNED' if dry_run else 'CREATED',
                      'repository': str(target), 'branch': 'main', 'files': sorted(files),
                      'initial_commit': False, 'remote_created': False, 'enrolled': False,
                      'project_settings': 'MANUAL_INSTALL_REQUIRED',
                      'instructions_file': 'OPENAI_PROJECT_INSTRUCTIONS.md',
                      'local_mutation': 'NONE' if dry_run else 'NEW_REPOSITORY'}
            if dry_run:
                result['contents'] = {name: raw.decode() for name, raw in files.items()}
                return result
            staging = '.repo-cp-create-' + secrets.token_hex(16)
            intent_data = {'schema_version': 1, 'template_version': TEMPLATE_VERSION,
                           'target': target.name, 'staging': staging, 'generator_sha256': generator,
                           'purpose': purpose, 'owner': owner,
                           'files': {name: hashlib.sha256(raw).hexdigest() for name, raw in files.items()}}
            intent = (json.dumps(intent_data, sort_keys=True, indent=2) + '\n').encode()
            directory = None
            try:
                with termination_control():
                    os.mkdir(staging, 0o700, dir_fd=parent)
                    directory = os.open(staging, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
                    # The durable intent survives cancellation; contains public inputs only.
                    write_file(directory, INTENT, intent)
                    os.fsync(directory)
                    os.fsync(parent)
                    for name, raw in files.items():
                        write_file(directory, name, raw)
                    git_init(directory)
                    stage_path = target.parent / staging
                    check_directory_path(stage_path, directory)
                    verify_tree(stage_path, files, intent)
                    sync_tree(stage_path)
                    check_directory_path(target.parent, parent)
                    committed = True  # From here, an error may follow a successful rename.
                    rename_exclusive(parent, staging, target.name)
                    os.fsync(parent)
                    check_directory_path(target, directory)
                    verify_tree(target, files, intent)
                return result
            except (Interrupted, KeyboardInterrupt):
                if committed:
                    raise Denied('CREATE_RECOVERY_REQUIRED') from None
                raise Denied('CREATE_INTERRUPTED') from None
            except Exception:
                # No cleanup: preserve uncertain state and the original public inputs.
                if committed:
                    raise Denied('CREATE_RECOVERY_REQUIRED') from None
                raise Denied('CREATE_PREPARATION_FAILED') from None
            finally:
                if directory is not None:
                    os.close(directory)
    except (Denied, OSError, KeyboardInterrupt):
        # The parent lock's exit checks also run after publication. Preserve the
        # possibly-committed outcome even if those final checks fail.
        if committed:
            raise Denied('CREATE_RECOVERY_REQUIRED') from None
        raise


def inspect_repository(path):
    """Read-only recovery inspection; never resumes, overwrites or deletes state."""
    from .safety import load
    require_unprivileged()
    target = absolute_file(path)
    raw = read_public(target, INTENT)
    data = load(raw)
    if (type(data) is not dict
            or set(data) != {'schema_version', 'template_version', 'target', 'staging', 'purpose', 'owner', 'files', 'generator_sha256'}
            or type(data['schema_version']) is not int or data['schema_version'] != 1
            or data['template_version'] != TEMPLATE_VERSION):
        raise Denied('CREATE_INTENT_INVALID')
    import re
    if (type(data['generator_sha256']) is not dict
            or set(data['generator_sha256']) != set(GENERATOR_FILES)
            or any(type(digest) is not str or re.fullmatch('[0-9a-f]{64}', digest) is None
                   for digest in data['generator_sha256'].values())
            or type(data['staging']) is not str
            or re.fullmatch(r'\.repo-cp-create-[0-9a-f]{32}', data['staging']) is None):
        raise Denied('CREATE_INTENT_INVALID')
    files = scaffold(data['target'], data['purpose'], data['owner'])
    if (data['files'] != {name: hashlib.sha256(body).hexdigest() for name, body in files.items()}
            or target.name not in (data['target'], data['staging'])):
        raise Denied('CREATE_INTENT_INVALID')
    try:
        verify_tree(target, files, raw)
        content = 'VERIFIED'
    except (Denied, OSError, UnicodeError):
        content = 'INCOMPLETE_OR_CHANGED'
    return {'schema_version': 1, 'status': 'RECOVERY_REQUIRED', 'content': content,
            'location': 'TARGET' if target.name == data['target'] else 'STAGING',
            'durability': 'UNCONFIRMED', 'local_mutation': 'NONE',
            'next_action': 'Review retained state before cleanup or a new creation; no automatic resume.'}


def main(argv):
    from .cli import Parser
    try:
        parser = Parser(prog='repo-cp create', description=__doc__, allow_abbrev=False)
        parser.add_argument('destination', help='Absolute new repository path; parent must already exist')
        parser.add_argument('--purpose', help='Public one-line repository purpose (required for creation)')
        parser.add_argument('--owner', default='Louis', help='Public repository steward; default Louis')
        actions = parser.add_mutually_exclusive_group()
        actions.add_argument('--dry-run', action='store_true', help='Print generated content without writing')
        actions.add_argument('--inspect', action='store_true', help='Inspect retained creation state without writing')
        args = parser.parse_args(argv)
        if args.inspect:
            if args.purpose is not None or args.owner != 'Louis':
                raise Denied('CLI_ARGUMENTS')
            result = inspect_repository(args.destination)
        else:
            if args.purpose is None:
                raise Denied('CLI_ARGUMENTS')
            result = create_repository(args.destination, purpose=args.purpose,
                                       owner=args.owner, dry_run=args.dry_run)
    except (Denied, OSError, ValueError, TypeError, KeyError) as error:
        sys.stderr.write(blocker('REPOSITORY_CREATION_FAILED', error))
        return 2
    sys.stdout.write(json.dumps(result, sort_keys=True, indent=2) + '\n')
    return 1 if args.inspect else 0
