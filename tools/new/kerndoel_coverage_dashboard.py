#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, json, os
from collections import defaultdict, Counter
from typing import Dict, List, Any, Tuple

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_files(root: str, filename: str) -> List[str]:
    out = []
    for r, _, files in os.walk(root):
        if filename in files:
            out.append(os.path.join(r, filename))
    return sorted(out)

def parse_pack_meta(path: str) -> Dict[str, Any]:
    p = path.replace("\\", "/")
    parts = p.split("/")

    meta = {
        "path": path,
        "domain": "",
        "grade": None,
        "level": "",
        "topic": ""
    }

    if "nl-NL" in parts:
        i = parts.index("nl-NL")
        if i + 1 < len(parts):
            meta["domain"] = parts[i + 1]

    for part in parts:
        if part.startswith("groep-"):
            try:
                meta["grade"] = int(part.split("-")[1])
            except Exception:
                meta["grade"] = None
        if part in ("n1", "n2", "n3", "n4"):
            meta["level"] = part

    if "topics" in parts:
        j = parts.index("topics")
        if j + 1 < len(parts):
            meta["topic"] = parts[j + 1]

    return meta

def load_topic_canons(topic_canon_dir: str) -> Dict[str, Dict[str, Any]]:
    """
    Returns mapping: domain -> topic_slug -> topic_entry
    Expected canon file shape:
      { "domain": "...", "version": "...", "topics": [ { "topic": "slug", "kerndoelen":[...], ... }, ... ] }
    """
    domain_map: Dict[str, Dict[str, Any]] = defaultdict(dict)
    canon_files = []
    for r, _, files in os.walk(topic_canon_dir):
        for fn in files:
            if fn.endswith(".json") and "topic-canon" in fn:
                canon_files.append(os.path.join(r, fn))
    canon_files = sorted(canon_files)

    for path in canon_files:
        doc = load_json(path)

        # Variant A: dict with domain+topics
        if isinstance(doc, dict):
            domain = doc.get("domain")
            topics = doc.get("topics", [])
            if domain and isinstance(topics, list):
                for t in topics:
                    slug = t.get("topic")
                    if slug:
                        domain_map[domain][slug] = t
                continue

        # Variant B: flat list of topic entries (legacy topic-canon.json)
        if isinstance(doc, list):
            for t in doc:
                if not isinstance(t, dict):
                    continue
                domain = t.get("domain")
                slug = t.get("topic")
                if domain and slug:
                    domain_map[domain][slug] = t
            continue

    return domain_map

def load_group_gate(group_gate_path: str) -> Dict[int, List[int]]:
    """
    Expected shape:
      { "version": "...", "groups": [ { "group": 1, "kerndoelen":[23,26,...], "focus":"..." }, ... ] }
    Returns { groupNum: [kerndoelen] }
    """
    doc = load_json(group_gate_path)
    groups = doc.get("groups", [])
    out: Dict[int, List[int]] = {}
    for g in groups:
        try:
            gn = int(g.get("group"))
            ks = g.get("kerndoelen", [])
            if isinstance(ks, list):
                out[gn] = [int(x) for x in ks]
        except Exception:
            continue
    return out

def count_pack_exercises(pack_path: str) -> Tuple[int, Counter]:
    """
    Returns (n_exercises, interaction_counter)
    """
    try:
        data = load_json(pack_path)
    except Exception:
        return (0, Counter())

    if not isinstance(data, list):
        return (0, Counter())

    interactions = Counter()
    for ex in data:
        it = (ex.get("interaction") or {}).get("type")
        if it:
            interactions[it] += 1
    return (len(data), interactions)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content-root", required=True)
    ap.add_argument("--topic-canon-dir", required=True, help="Directory containing topic-canon*.json files")
    ap.add_argument("--group-gate", required=True, help="Kerndoelen per groep gate JSON")
    ap.add_argument("--out-json", default="docs/new/reports/kerndoel_coverage.json")
    ap.add_argument("--out-md", default="docs/new/reports/kerndoel_coverage.md")
    ap.add_argument("--min-per-kerndoel", type=int, default=30, help="Coverage threshold per kerndoel per group")
    args = ap.parse_args()

    topic_canons = load_topic_canons(args.topic_canon_dir)
    group_gate = load_group_gate(args.group_gate)

    packs = find_files(args.content_root, "exercises.json")

    # Aggregates
    # group -> kerndoel -> count
    gk_counts = defaultdict(lambda: defaultdict(int))
    # group -> domain -> kerndoel -> count
    gdk_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    # group -> domain -> total
    gd_totals = defaultdict(lambda: defaultdict(int))
    # domain -> kerndoel -> count
    dk_counts = defaultdict(lambda: defaultdict(int))
    # topic trace: group -> kerndoel -> list of contributing topics
    trace = defaultdict(lambda: defaultdict(list))

    missing_in_canon = []

    total_exercises = 0
    empty_packs = 0

    for p in packs:
        meta = parse_pack_meta(p)
        domain = meta["domain"]
        grade = meta["grade"]
        topic = meta["topic"]

        n, interactions = count_pack_exercises(p)
        total_exercises += n
        if n == 0:
            empty_packs += 1

        if not domain or not grade or not topic:
            continue

        canon_entry = topic_canons.get(domain, {}).get(topic)
        if not canon_entry:
            missing_in_canon.append(p)
            continue

        kerndoelen = canon_entry.get("kerndoelen", [])
        if not isinstance(kerndoelen, list) or not kerndoelen:
            continue

        for k in kerndoelen:
            try:
                kk = int(k)
            except Exception:
                continue
            gk_counts[grade][kk] += n
            gdk_counts[grade][domain][kk] += n
            dk_counts[domain][kk] += n
            gd_totals[grade][domain] += n
            trace[grade][kk].append({
                "topic": topic,
                "domain": domain,
                "count": n,
                "path": p,
                "interaction_breakdown": dict(interactions)
            })

    # Coverage evaluation per group (based on allowed kerndoelen for that group)
    coverage = []
    for group_num, allowed_ks in sorted(group_gate.items()):
        for k in allowed_ks:
            cnt = gk_counts[group_num].get(k, 0)
            status = "OK" if cnt >= args.min_per_kerndoel else ("LOW" if cnt > 0 else "NONE")
            coverage.append({
                "group": group_num,
                "kerndoel": k,
                "count": cnt,
                "status": status,
                "min_threshold": args.min_per_kerndoel
            })

    # Summaries
    under = [c for c in coverage if c["status"] != "OK"]
    under.sort(key=lambda x: (x["group"], x["status"], x["count"]))

    # Output JSON
    os.makedirs(os.path.dirname(args.out_json), exist_ok=True)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0.0",
            "min_per_kerndoel": args.min_per_kerndoel,
            "stats": {
                "total_packs": len(packs),
                "empty_packs": empty_packs,
                "total_exercises": total_exercises,
                "packs_missing_in_topic_canon": len(missing_in_canon)
            },
            "coverage": coverage,
            "undercoverage": under,
            "domain_kerndoel_counts": {d: dict(kc) for d, kc in dk_counts.items()},
            "trace": trace  # can get big; but useful for drill-down
        }, f, ensure_ascii=False, indent=2)

    # Output Markdown (human friendly)
    lines = []
    lines.append("# Kerndoel coverage dashboard\n")
    lines.append(f"- Min threshold per kerndoel per group: **{args.min_per_kerndoel}** oefeningen\n")
    lines.append("## Stats\n")
    lines.append(f"- Total packs: **{len(packs)}**\n")
    lines.append(f"- Empty packs: **{empty_packs}**\n")
    lines.append(f"- Total exercises: **{total_exercises}**\n")
    lines.append(f"- Packs missing in topic canon: **{len(missing_in_canon)}**\n")

    lines.append("\n## Undercoverage (groepen × kerndoelen)\n")
    lines.append("| Groep | Kerndoel | Aantal oefeningen | Status |\n")
    lines.append("|---:|---:|---:|---|\n")
    for c in under[:200]:
        lines.append(f"| {c['group']} | {c['kerndoel']} | {c['count']} | {c['status']} |\n")
    if len(under) > 200:
        lines.append(f"\n> (Toont 200 van {len(under)} undercoverage-rijen. Zie JSON voor volledig.)\n")

    lines.append("\n## Domein → kerndoel verdeling (totaal)\n")
    for dom in sorted(dk_counts.keys()):
        lines.append(f"\n### {dom}\n")
        lines.append("| Kerndoel | Aantal oefeningen |\n")
        lines.append("|---:|---:|\n")
        for k, cnt in sorted(dk_counts[dom].items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"| {k} | {cnt} |\n")

    if missing_in_canon:
        lines.append("\n## Packs missing in topic-canon (fix warnings)\n")
        for p in missing_in_canon[:100]:
            lines.append(f"- {p}\n")
        if len(missing_in_canon) > 100:
            lines.append(f"\n> (Toont 100 van {len(missing_in_canon)}.)\n")

    os.makedirs(os.path.dirname(args.out_md), exist_ok=True)
    with open(args.out_md, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"✅ Wrote JSON: {args.out_json}")
    print(f"✅ Wrote MD:   {args.out_md}")

if __name__ == "__main__":
    main()
