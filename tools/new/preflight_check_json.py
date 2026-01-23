#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys
from typing import Any, Dict, List, Tuple

# Reuse the exact same content rules function + Issue dataclass
from validate_one_exercises_file import run_content_rules, Issue


def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def preflight(data: Any, source_label: str) -> Tuple[bool, List[Issue]]:
    issues: List[Issue] = []

    if not isinstance(data, list):
        issues.append(Issue("ERROR", "PREFLIGHT-FAIL", "Top-level must be a JSON array of exercises."))
        return False, issues

    if len(data) == 0:
        issues.append(Issue("WARN", "PREFLIGHT-WARN", "Empty array (placeholder)."))
        return True, issues

    for idx, ex in enumerate(data):
        if not isinstance(ex, dict):
            issues.append(Issue("ERROR", "PREFLIGHT-FAIL", f"Item[{idx}] is not an object."))
            continue

        # Apply content rules (same as validator)
        issues.extend(run_content_rules(ex, source_label))

    ok = not any(i.kind == "ERROR" for i in issues)
    return ok, issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_file", help="Path to a generated JSON file (array) or exercises.json")
    args = ap.parse_args()

    try:
        data = read_json(args.json_file)
    except Exception as e:
        print(f"[{args.json_file}] [PREFLIGHT-FAIL] JSON parse error: {e}")
        sys.exit(1)

    ok, issues = preflight(data, args.json_file)

    for i in issues:
        print(f"[{args.json_file}] [{i.code}] {i.message}")

    if ok:
        print("Result: ✅ OK (preflight).")
        sys.exit(0)

    err_count = sum(1 for i in issues if i.kind == "ERROR")
    warn_count = sum(1 for i in issues if i.kind == "WARN")
    print(f"Result: ❌ FAIL (preflight) — {err_count} error(s), {warn_count} warning(s).")
    sys.exit(1)


if __name__ == "__main__":
    main()
