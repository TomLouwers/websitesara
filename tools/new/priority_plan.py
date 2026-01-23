#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, json, os
from typing import Any, Dict, List, Tuple

def find_exercises_files(root: str) -> List[str]:
    out = []
    for r, _, files in os.walk(root):
        for fn in files:
            if fn == "exercises.json":
                out.append(os.path.join(r, fn))
    return sorted(out)

def load_json_safe(path: str) -> Tuple[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        if raw.strip() == "":
            return "empty_file", None
        return "ok", json.loads(raw)
    except Exception:
        return "parse_error", None

def parse_meta(path: str) -> Dict[str, Any]:
    p = path.replace("\\", "/")
    parts = p.split("/")
    meta = {"domain": "", "group": "", "level": "", "topic": "", "path": path}
    if "nl-NL" in parts:
        i = parts.index("nl-NL")
        if i + 1 < len(parts): meta["domain"] = parts[i + 1]
    for part in parts:
        if part.startswith("groep-"):
            meta["group"] = part
            try:
                meta["group_num"] = int(part.split("-")[1])
            except Exception:
                meta["group_num"] = 0
        if part in ("n1","n2","n3","n4"):
            meta["level"] = part
    if "topics" in parts:
        j = parts.index("topics")
        if j + 1 < len(parts): meta["topic"] = parts[j + 1]
    if "group_num" not in meta: meta["group_num"] = 0
    return meta

def score(meta: Dict[str, Any], status: str, n_items: int) -> int:
    g = meta["group_num"]
    lvl = meta["level"]
    dom = meta["domain"]

    # base: empty > small > ok
    s = 0
    if status in ("empty_file", "parse_error"): s += 1000
    elif status == "ok" and n_items == 0: s += 900
    elif status == "ok" and n_items < 30: s += 600
    else: s += 0

    # group priority: focus 4–6
    if 4 <= g <= 6: s += 300
    elif g in (3,7): s += 150
    else: s += 50

    # level priority
    if lvl == "n2": s += 120
    elif lvl == "n3": s += 80
    elif lvl == "n1": s += 60
    else: s += 40

    # domain bump (meetkunde was underfilled in your report)
    if dom == "meten-en-meetkunde": s += 200
    elif dom == "verhoudingen": s += 120
    elif dom == "getal-en-bewerkingen": s += 100

    # pack size urgency
    if status == "ok" and 0 < n_items < 30:
        s += (30 - n_items)  # slightly prioritize very small packs

    return s

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content-root", required=True)
    ap.add_argument("--min-target", type=int, default=30, help="Target exercises per pack")
    ap.add_argument("--out", default="docs/new/reports/priority_plan.json")
    ap.add_argument("--top", type=int, default=80)
    args = ap.parse_args()

    files = find_exercises_files(args.content_root)
    rows = []

    for path in files:
        meta = parse_meta(path)
        st, data = load_json_safe(path)
        n = 0
        if st == "ok" and isinstance(data, list):
            n = len(data)
        elif st == "ok":
            st = "parse_error"

        if st == "ok" and n >= args.min_target:
            status = "OK"
        elif st == "ok" and n == 0:
            status = "EMPTY"
        elif st == "ok" and 0 < n < args.min_target:
            status = "SMALL"
        elif st == "empty_file":
            status = "EMPTY_FILE"
        else:
            status = "PARSE_ERROR"

        sc = score(meta, st, n)

        rows.append({
            "score": sc,
            "status": status,
            "count": n,
            "domain": meta["domain"],
            "group": meta["group"],
            "level": meta["level"],
            "topic": meta["topic"],
            "path": path
        })

    rows.sort(key=lambda r: (-r["score"], r["domain"], r["group"], r["level"], r["topic"]))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({
            "min_target": args.min_target,
            "total_packs": len(rows),
            "top": rows[:args.top]
        }, f, ensure_ascii=False, indent=2)

    # Also print a compact top list
    print("=== PRIORITY PLAN (top) ===")
    for r in rows[:args.top]:
        print(f"{r['score']:>4}  {r['status']:<10}  {r['domain']}/{r['group']}/{r['level']}/{r['topic']}  ({r['count']} items)")
    print(f"\nSaved: {args.out}")

if __name__ == "__main__":
    main()
