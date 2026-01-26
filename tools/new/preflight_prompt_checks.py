from __future__ import annotations
import argparse
import json
import os
import sys
from typing import Any, Dict, List, Tuple

from validators.content_rules import get_rules


def infer_level_topic(text: str) -> Tuple[str | None, str | None]:
    # extremely simple inference from batch prompt text
    level = None
    topic = None
    for lv in ["n1", "n2", "n3", "n4"]:
        if f"level: \"{lv}\"" in text or f"level\": \"{lv}\"" in text:
            level = lv
            break
    # topic line could be: topic: "..."
    import re
    m = re.search(r"topic\s*:\s*\"([a-z0-9\-]+)\"", text)
    if m:
        topic = m.group(1)
    return level, topic


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-file", required=True, help="Path to a .txt file containing the batch prompt.")
    args = ap.parse_args()

    if not os.path.exists(args.prompt_file):
        print(f"❌ prompt-file not found: {args.prompt_file}")
        return 2

    text = open(args.prompt_file, "r", encoding="utf-8").read()
    level, topic = infer_level_topic(text)

    rules = get_rules(level=level, topic=topic)

    fails: List[Dict[str, Any]] = []
    warns: List[Dict[str, Any]] = []

    for r in rules:
        hits = list(r.pattern.finditer(text))
        if not hits:
            continue
        entry = {
            "code": r.code,
            "severity": r.severity,
            "description": r.description,
            "count": len(hits),
        }
        if r.severity == "FAIL":
            fails.append(entry)
        else:
            warns.append(entry)

    print("PRE-FLIGHT PROMPT CHECKS")
    print(f"- inferred level: {level}")
    print(f"- inferred topic: {topic}")
    print(f"- FAILS: {len(fails)} | WARNS: {len(warns)}")

    for e in fails:
        print(f"❌ [{e['code']}] {e['description']} (hits={e['count']})")
    for e in warns:
        print(f"⚠️ [{e['code']}] {e['description']} (hits={e['count']})")

    if fails:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
