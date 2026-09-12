"""Read-only consumer interfaces. No action executor exists."""
import argparse
import json
from pathlib import Path
import sys

from .audit import audit, proposals, registry, text_report
from .consumer import ROOT, render, verify
from .safety import Denied, MAX_BYTES


class Parser(argparse.ArgumentParser):
    def error(self, message):
        # argparse's default includes untrusted arguments in diagnostics.
        raise Denied('CLI_ARGUMENTS')


def main():
    try:
        parser = Parser(description=__doc__)
        parser.add_argument('command', choices=('validate', 'render', 'inventory', 'audit', 'drift', 'propose'))
        parser.add_argument('--fleet-root', type=Path, default=ROOT.parent)
        parser.add_argument('--pilot', action='store_true')
        parser.add_argument('--repository', help='Restrict an already selected enrolled/pilot scope')
        parser.add_argument('--text', action='store_true')
        args = parser.parse_args()
        if args.command == 'render':
            output = render(sys.stdin.buffer.read(MAX_BYTES + 1))
            status = 0
        else:
            verify()
            data = registry()
            if args.command == 'validate':
                data = {'status': 'PASS', 'foundation_integrity': 'PASS', 'enrollment_schema': 'PASS',
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
    except (Denied, OSError, ValueError, TypeError, KeyError, RecursionError, ImportError):
        # No partial stdout, traceback, rejected payload, paths or command text.
        sys.stderr.write('BLOCKER=REPO_CP_NONCONFORMANCE\n')
        return 2
    sys.stdout.write(output)
    return status
