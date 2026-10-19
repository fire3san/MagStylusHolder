#!/usr/bin/env python3
"""Mirror canonical frontend files into site/; use --check for read-only validation."""
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if the mirror needs updating')
    args = parser.parse_args()
    sources = [ROOT / 'index.html', ROOT / 'README.md']
    for directory in ('css', 'js', 'docs'):
        sources.extend(sorted(path for path in (ROOT / directory).rglob('*') if path.is_file()))

    changed = []
    for source in sources:
        relative = source.relative_to(ROOT)
        target = ROOT / 'site' / relative
        if target.is_file() and source.read_bytes() == target.read_bytes():
            continue
        changed.append(str(relative))
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

    if args.check and changed:
        print('Site mirror is out of date:\n' + '\n'.join(changed))
        return 1
    print(f'{len(changed)} file(s) synchronized.' if changed else 'Site mirror is up to date.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
