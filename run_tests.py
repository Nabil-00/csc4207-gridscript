#!/usr/bin/env python3
import sys
import os
import glob
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

GRIDSCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gridscript.py')
TEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')

GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'


def run_test(test_file, expected_file, kind):
    name = os.path.basename(test_file).replace('.gsc', '')
    with open(expected_file) as f:
        expected = f.read().strip()
    proc = subprocess.run(
        [sys.executable, GRIDSCRIPT, test_file],
        capture_output=True, text=True, timeout=30,
    )
    if kind == 'valid':
        actual = proc.stdout.strip()
        if actual == expected:
            print(f"  {GREEN}PASS{RESET} {name}")
            return True
        else:
            print(f"  {RED}FAIL{RESET} {name}")
            print(f"    expected: {expected!r}")
            print(f"    actual:   {actual!r}")
            if proc.stderr:
                print(f"    stderr:   {proc.stderr.strip()}")
            return False
    else:
        combined = proc.stderr.strip() + '\n' + proc.stdout.strip()
        if expected in combined:
            print(f"  {GREEN}PASS{RESET} {name}")
            return True
        else:
            print(f"  {RED}FAIL{RESET} {name}")
            print(f"    expected error: {expected!r}")
            print(f"    got:            {combined!r}")
            return False


def main():
    passed = 0
    failed = 0

    print("\n=== Valid tests ===")
    valid_dir = os.path.join(TEST_DIR, 'valid')
    for f in sorted(glob.glob(os.path.join(valid_dir, '*.gsc'))):
        expected = f.replace('.gsc', '.expected')
        if os.path.exists(expected):
            if run_test(f, expected, 'valid'):
                passed += 1
            else:
                failed += 1
        else:
            print(f"  ? SKIP {os.path.basename(f).replace('.gsc', '')} (no .expected file)")

    print("\n=== Invalid tests ===")
    invalid_dir = os.path.join(TEST_DIR, 'invalid')
    for f in sorted(glob.glob(os.path.join(invalid_dir, '*.gsc'))):
        expected = f.replace('.gsc', '.error')
        if os.path.exists(expected):
            if run_test(f, expected, 'invalid'):
                passed += 1
            else:
                failed += 1
        else:
            print(f"  ? SKIP {os.path.basename(f).replace('.gsc', '')} (no .error file)")

    total = passed + failed
    print(f"\n{'=' * 40}")
    print(f"  {passed}/{total} passed", end="")
    if failed:
        print(f", {RED}{failed} failed{RESET}")
    else:
        print(f", all {GREEN}PASS{RESET}")
    print()
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())