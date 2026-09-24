#!/usr/bin/env python3
"""Prefix each session folder with the date of its oldest file.

Pro Tools and Ableton session folders get copied, renamed and backed up until
nobody remembers when the music was actually made. The oldest file inside a
session is the best record of that date. This script finds it and renames the
folder to "YYYY-MM-DD <original name>".

Runs as a dry run by default. Add --apply to rename.
"""
import argparse
import os
import re
import sys
from datetime import datetime

DATED = re.compile(r"^\d{4}-\d{2}-\d{2} ")
SKIP = {".DS_Store", "Thumbs.db", "desktop.ini"}


def file_date(path):
    """Creation time where the OS records it (macOS, Windows), else modification time."""
    st = os.stat(path)
    return datetime.fromtimestamp(getattr(st, "st_birthtime", st.st_mtime))


def oldest_date(folder):
    oldest = None
    for root, _dirs, files in os.walk(folder):
        for name in files:
            if name in SKIP or name.startswith("._"):
                continue
            try:
                d = file_date(os.path.join(root, name))
            except OSError as e:
                print(f"  skip {name}: {e}", file=sys.stderr)
                continue
            if oldest is None or d < oldest:
                oldest = d
    return oldest


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("parent", help="folder that contains the session folders")
    p.add_argument("--apply", action="store_true", help="rename (default is a dry run)")
    args = p.parse_args()

    for item in sorted(os.listdir(args.parent)):
        folder = os.path.join(args.parent, item)
        if not os.path.isdir(folder) or DATED.match(item):
            continue
        d = oldest_date(folder)
        if d is None:
            print(f"no files:   {item}")
            continue
        new = os.path.join(args.parent, f"{d:%Y-%m-%d} {item}")
        if os.path.exists(new):
            print(f"exists:     {os.path.basename(new)}")
            continue
        print(f"{'rename' if args.apply else 'would rename'}: {item} -> {os.path.basename(new)}")
        if args.apply:
            os.rename(folder, new)


if __name__ == "__main__":
    main()
