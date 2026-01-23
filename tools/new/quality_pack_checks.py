#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from typing import Any, Dict, List, Tuple


# -----------------------------
# Helpers
# -----------------------------

def find_exercises_files(content_root: str) -> List[str]:
    matches: List[str] = []
    for root, _, files in os.walk(content_root):
        for fn in files:
            if fn == "exercises.json":
                matches.append(os.path.join(root, fn))
    return sorted(matches)


def load_json_safe(path: str) -> Tuple[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        if raw.strip() == "":
            return "empty_file", None
        data = json.loads(raw)
        return "ok", data
    except Exception:
        return "parse_error", None


def extract_core_math(prompt: str) -> str:
    """
    Rough heuristic to extract the mathematical core from a prompt.
    Used for duplicate detection in numeric-style tasks.
    """
    p = prompt.lower()
    # remove words, keep digits and operators
    p = re.sub(r"[^\d÷x\+\-\*/]", "", p)
    return p.strip()


def extract_context_words(prompt: str) -> List[str]:
    words = re.findall(r"[a-zA-Z]+", prompt.lower())
    stop = {
        "bereken", "hoeveel", "wat", "is", "zijn", "de", "het", "een",
        "schrijf", "als", "rest", "over", "ieder", "elk"
    }
    return [w for w in words if w not in stop and len(w) > 3]


def parse_path_meta(path: str) -> Dict[str, str]:
    p = path.replace("\\", "/")
    parts = p.split("/")
    meta = {"domain": "", "group": "", "level": "", "topic": ""}

    if "nl-NL" in parts:
        i = parts.index("nl-NL")
        if i + 1 < len(parts):
            meta["domain"] = parts[i + 1]

    for part in parts:
        if part.startswith("groep-"):
            meta["group"] = part
        if part in ("n1", "n2", "n3", "n4"):
            meta["level"] = part

    if "topics" in parts:
        j = parts.index("topics")
        if j + 1 < len(parts):
            meta["topic"] = parts[j + 1]

    return meta


# -----------------------------
# Quality checks
# -----------------------------

def check_duplicates(exercises: List[Dict[str, Any]], path: str) -> List[str]:
    warnings: List[str] = []

    prompts = Counter()
    math_cores = Counter()
    mcq_signatures = Counter()

    for ex in exercises:
        prompt = ex.get("prompt", "").strip()
        prompts[prompt] += 1

        interaction = (ex.get("interaction") or {}).get("type")
        if interaction == "numeric":
            core = extract_core_math(prompt)
            if core:
                math_cores[core] += 1

        if interaction == "mcq":
            opts = tuple((ex.get("options") or []))
            sol = (ex.get("solution") or {}).get("index")
            mcq_signatures[(opts, sol)] += 1

    for p, c in prompts.items():
        if c > 1:
            warnings.append(
                f"[PROMPT-DUP-WARN] Prompt duplicated {c}× in {path}"
            )

    for core, c in math_cores.items():
        if c > 1:
            warnings.append(
                f"[MATH-DUP-WARN] Same numeric core '{core}' occurs {c}× in {path}"
            )

    for sig, c in mcq_signatures.items():
        if c > 1:
            warnings.append(
                f"[OPTIONS-DUP-WARN] Identical MCQ options+answer {c}× in {path}"
            )

    return warnings


def check_distribution(exercises: List[Dict[str, Any]], path: str) -> List[str]:
    warnings: List[str] = []

    delers = Counter()
    context_words = Counter()

    for ex in exercises:
        prompt = ex.get("prompt", "").lower()
        interaction = (ex.get("interaction") or {}).get("type")

        if interaction == "numeric":
            m = re.findall(r"÷\s*(\d+)", prompt)
            for d in m:
                delers[int(d)] += 1

        if interaction in ("numeric", "fill_blanks", "mcq"):
            for w in extract_context_words(prompt):
                context_words[w] += 1

    if delers:
        most_common = delers.most_common(1)[0]
        if most_common[1] > len(exercises) * 0.4:
            warnings.append(
                f"[DISTRIBUTION-WARN] Deler '{most_common[0]}' used in {most_common[1]} of {len(exercises)} items ({path})"
            )

    if context_words:
        word, count = context_words.most_common(1)[0]
        if count > len(exercises) * 0.4:
            warnings.append(
                f"[CONTEXT-DUP-WARN] Context word '{word}' dominates ({count}×) in {path}"
            )

    return warnings


def check_pack_size(exercises: List[Dict[str, Any]], path: str) -> List[str]:
    if len(exercises) == 0:
        return [f"[PACK-EMPTY-WARN] Empty pack ([]) {path}"]
    if len(exercises) < 20:
        return [f"[PACK-SMALL-WARN] Only {len(exercises)} exercises in {path}"]
    return []


# -----------------------------
# Main
# -----------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content-root", required=True, help="Root folder containing content/")
    args = ap.parse_args()

    files = find_exercises_files(args.content_root)
    if not files:
        print("No exercises.json files found.")
        return

    total_warns = 0
    by_domain = defaultdict(int)

    for path in files:
        status, data = load_json_safe(path)
        if status != "ok" or not isinstance(data, list):
            continue

        meta = parse_path_meta(path)
        domain = meta["domain"] or "unknown"

        warns: List[str] = []
        warns += check_pack_size(data, path)
        warns += check_duplicates(data, path)
        warns += check_distribution(data, path)

        if warns:
            by_domain[domain] += len(warns)
            total_warns += len(warns)
            for w in warns:
                print(w)

    print()
    print("=== QUALITY CHECK SUMMARY ===")
    print(f"Total warnings: {total_warns}")
    for d, c in sorted(by_domain.items(), key=lambda x: -x[1]):
        print(f"{d:25} {c:>5} warnings")


if __name__ == "__main__":
    main()
