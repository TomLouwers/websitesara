#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
from collections import defaultdict
from typing import Any, Dict, List, Tuple


def find_exercises_files(content_root: str) -> List[str]:
    matches: List[str] = []
    for root, _, files in os.walk(content_root):
        for fn in files:
            if fn == "exercises.json":
                matches.append(os.path.join(root, fn))
    return sorted(matches)


def safe_load_json(path: str) -> Tuple[str, Any]:
    """
    Returns (status, data)
    status: "ok" | "empty_file" | "parse_error"
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        if raw.strip() == "":
            return "empty_file", None
        data = json.loads(raw)
        return "ok", data
    except Exception:
        return "parse_error", None


def parse_path_metadata(path: str) -> Dict[str, str]:
    """
    Extract domain, groep, level, topic from:
    content/nl-NL/<domain>/groep-6/n2/topics/<topic>/exercises.json
    """
    p = path.replace("\\", "/")
    parts = p.split("/")

    meta = {"domain": "", "group": "", "level": "", "topic": ""}

    # domain is after nl-NL
    if "nl-NL" in parts:
        i = parts.index("nl-NL")
        if i + 1 < len(parts):
            meta["domain"] = parts[i + 1]

    # group and level
    for part in parts:
        if part.startswith("groep-"):
            meta["group"] = part
        if part in ("n1", "n2", "n3", "n4"):
            meta["level"] = part

    # topic slug
    if "topics" in parts:
        j = parts.index("topics")
        if j + 1 < len(parts):
            meta["topic"] = parts[j + 1]

    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content-root", required=True, help="Root folder containing content/")
    ap.add_argument("--top", type=int, default=20, help="Show top N topics by exercise count")
    args = ap.parse_args()

    files = find_exercises_files(args.content_root)
    if not files:
        print("No exercises.json files found.")
        return

    totals = {
        "files": 0,
        "ok": 0,
        "empty_array": 0,
        "empty_file": 0,
        "parse_error": 0,
        "exercises": 0,
    }

    # breakdowns
    by_domain = defaultdict(lambda: {"files": 0, "exercises": 0, "empty_array": 0, "empty_file": 0, "parse_error": 0})
    by_group = defaultdict(lambda: {"files": 0, "exercises": 0, "empty_array": 0, "empty_file": 0, "parse_error": 0})
    by_level = defaultdict(lambda: {"files": 0, "exercises": 0, "empty_array": 0, "empty_file": 0, "parse_error": 0})
    by_topic_key = defaultdict(lambda: {"files": 0, "exercises": 0, "empty_array": 0, "empty_file": 0, "parse_error": 0})

    empty_paths: List[str] = []
    parse_error_paths: List[str] = []

    totals["files"] = len(files)

    for path in files:
        meta = parse_path_metadata(path)
        domain = meta["domain"] or "(unknown-domain)"
        group = meta["group"] or "(unknown-group)"
        level = meta["level"] or "(unknown-level)"
        topic = meta["topic"] or "(unknown-topic)"
        topic_key = f"{domain}/{group}/{level}/{topic}"

        status, data = safe_load_json(path)

        # common increments
        by_domain[domain]["files"] += 1
        by_group[group]["files"] += 1
        by_level[level]["files"] += 1
        by_topic_key[topic_key]["files"] += 1

        if status == "empty_file":
            totals["empty_file"] += 1
            by_domain[domain]["empty_file"] += 1
            by_group[group]["empty_file"] += 1
            by_level[level]["empty_file"] += 1
            by_topic_key[topic_key]["empty_file"] += 1
            empty_paths.append(path)
            continue

        if status == "parse_error":
            totals["parse_error"] += 1
            by_domain[domain]["parse_error"] += 1
            by_group[group]["parse_error"] += 1
            by_level[level]["parse_error"] += 1
            by_topic_key[topic_key]["parse_error"] += 1
            parse_error_paths.append(path)
            continue

        # ok JSON
        totals["ok"] += 1

        if isinstance(data, list):
            n = len(data)
            totals["exercises"] += n
            by_domain[domain]["exercises"] += n
            by_group[group]["exercises"] += n
            by_level[level]["exercises"] += n
            by_topic_key[topic_key]["exercises"] += n

            if n == 0:
                totals["empty_array"] += 1
                by_domain[domain]["empty_array"] += 1
                by_group[group]["empty_array"] += 1
                by_level[level]["empty_array"] += 1
                by_topic_key[topic_key]["empty_array"] += 1
                empty_paths.append(path)
        else:
            # not an array -> treat as parse_error-ish for reporting
            totals["parse_error"] += 1
            by_domain[domain]["parse_error"] += 1
            by_group[group]["parse_error"] += 1
            by_level[level]["parse_error"] += 1
            by_topic_key[topic_key]["parse_error"] += 1
            parse_error_paths.append(path)

    # ---- Print summary
    print("=== CONTENT PROGRESS REPORT ===")
    print(f"Files found:          {totals['files']}")
    print(f"Valid JSON files:     {totals['ok']}")
    print(f"Total exercises:      {totals['exercises']}")
    print(f"Empty arrays ([]):    {totals['empty_array']}")
    print(f"Empty files:          {totals['empty_file']}")
    print(f"Parse errors:         {totals['parse_error']}")
    print()

    def print_table(title: str, dct: Dict[str, Dict[str, int]], key_order: List[str]):
        print(title)
        print("-" * len(title))
        header = f"{'Key':45}  " + "  ".join([f"{k:>10}" for k in key_order])
        print(header)
        print("-" * len(header))
        for k, v in sorted(dct.items(), key=lambda kv: (-kv[1]["exercises"], kv[0]))[:50]:
            row = f"{k:45}  " + "  ".join([f"{v.get(kk,0):>10}" for kk in key_order])
            print(row)
        print()

    print_table(
        "By domain (top 50)",
        by_domain,
        ["files", "exercises", "empty_array", "empty_file", "parse_error"]
    )
    print_table(
        "By group (top 50)",
        by_group,
        ["files", "exercises", "empty_array", "empty_file", "parse_error"]
    )
    print_table(
        "By level (top 10)",
        by_level,
        ["files", "exercises", "empty_array", "empty_file", "parse_error"]
    )

    # Top topics by exercise count
    print(f"Top {args.top} topic packs by exercise count")
    print("-" * 40)
    top_topics = sorted(by_topic_key.items(), key=lambda kv: (-kv[1]["exercises"], kv[0]))[:args.top]
    for k, v in top_topics:
        print(f"{v['exercises']:>5}  {k}")
    print()

    # Lists (limited)
    if empty_paths:
        print("First 30 empty packs (empty file or []):")
        for p in empty_paths[:30]:
            print(" - " + p)
        if len(empty_paths) > 30:
            print(f" ... and {len(empty_paths) - 30} more")
        print()

    if parse_error_paths:
        print("First 30 parse-error packs:")
        for p in parse_error_paths[:30]:
            print(" - " + p)
        if len(parse_error_paths) > 30:
            print(f" ... and {len(parse_error_paths) - 30} more")
        print()


if __name__ == "__main__":
    main()
