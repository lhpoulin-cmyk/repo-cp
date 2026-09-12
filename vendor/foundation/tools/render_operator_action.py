#!/usr/bin/env python3
"""Render a public action declaration on stdin. Never invokes its command."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from operator_action import MAX_INPUT_BYTES, OperatorActionError, load_action, render_action


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--foundation-revision', required=True)
    parser.add_argument('--doctrine-revision', required=True)
    args = parser.parse_args()
    try:
        action = load_action(sys.stdin.buffer.read(MAX_INPUT_BYTES + 1))
        rendered = render_action(action, expected_source={
            'repository_revision': args.foundation_revision,
            'doctrine_revision': args.doctrine_revision})
    except OperatorActionError as error:
        print('BLOCKER=OPERATOR_ACTION_NONCONFORMANCE reason=' + str(error), file=sys.stderr)
        return 2
    sys.stdout.write(rendered)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
