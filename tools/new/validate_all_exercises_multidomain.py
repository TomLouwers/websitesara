#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from typing import List, Tuple

# We import the one-file validator so rules are guaranteed identical
from validate_one_exercises_file import validate_one_file, Issue


def find_exercises_files(content_root: str) -> List[str]:
    matches: List[str] = []
    for root, dirs, files in os.walk(content_root):
        for fn in files:
            if fn == "exercises.json":
                matches.append(os.path.join(root, fn))
    return sorted(matches)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content-root", required=True, help="Root folder containing content/")
    ap.add_argument("--schema", required=True, help="Path to ExerciseSchema.json")
    ap.add_argument("--taskforms", required=True, help="Path to taskvormen-canon.json")
    ap.add_argument("--fail-on-warn", action="store_true", help="Treat warnings as errors (optional)")
    args = ap.parse_args()

    files = find_exercises_files(args.content_root)
    if not files:
        print("Result: ❌ FAIL — no exercises.json files found.")
        sys.exit(1)

    total_errors = 0
    total_warnings = 0
    failed_files = 0

    for path in files:
        ok, issues = validate_one_file(path, args.schema, args.taskforms)

        errors = [i for i in issues if i.kind == "ERROR"]
        warns = [i for i in issues if i.kind == "WARN"]

        total_errors += len(errors)
        total_warnings += len(warns)

        if (not ok) or (args.fail_on_warn and warns):
            failed_files += 1
            for i in issues:
                print(f"[{path}] [{i.code}] {i.message}")

    if total_errors == 0 and (total_warnings == 0 or not args.fail_on_warn):
        msg = f"Result: ✅ OK — validated {len(files)} files"
        if total_warnings:
            msg += f", with {total_warnings} warning(s)"
        msg += "."
        print(msg)
        sys.exit(0)

    print(f"Result: ❌ FAIL — {total_errors} error(s), {total_warnings} warning(s) across {failed_files} file(s).")
    sys.exit(1)


if __name__ == "__main__":
    main()
