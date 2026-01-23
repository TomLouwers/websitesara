#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, json, os, re, sys
from collections import Counter

NUM_PATTERN = re.compile(r"-?\d+(?:[.,]\d+)?")
WORD_PATTERN = re.compile(r"\b[a-zA-Z]{4,}\b")

STOPWORDS = {
    "bereken", "welke", "wat", "hoeveel", "hier", "deze", "dit",
    "rekent", "betekent", "komt", "staat", "zijn", "heeft"
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_numeric_core(prompt: str):
    nums = NUM_PATTERN.findall(prompt.replace(",", "."))
    return tuple(nums)


def extract_context_words(prompt: str):
    words = [w.lower() for w in WORD_PATTERN.findall(prompt)]
    return [w for w in words if w not in STOPWORDS]


def check_pack(path: str, max_context_ratio: float, allow_flags=None):
    """
    allow_flags: optional dict per pack with booleans:
      - allow_numeric_duplicates
      - allow_context_dominance
      - allow_mcq_duplicates
    """
    allow_flags = allow_flags or {}

    data = load_json(path)
    if not isinstance(data, list) or not data:
        return []

    errors = []

    numeric_cores = Counter()
    mcq_sets = Counter()
    context_words = Counter()

    for ex in data:
        prompt = ex.get("prompt", "")

        # Numeric core
        core = extract_numeric_core(prompt)
        if core:
            numeric_cores[core] += 1

        # MCQ set
        if ex.get("interaction", {}).get("type") == "mcq":
            opts = tuple(ex.get("options", []))
            idx = ex.get("solution", {}).get("index")
            mcq_sets[(opts, idx)] += 1

        # Context words
        for w in extract_context_words(prompt):
            context_words[w] += 1

    # Numeric duplicates
    if not allow_flags.get("allow_numeric_duplicates"):
        for core, cnt in numeric_cores.items():
            if cnt > 1:
                errors.append(f"Duplicate numeric core {core} occurs {cnt}x")

    # MCQ duplicates
    if not allow_flags.get("allow_mcq_duplicates"):
        for (opts, idx), cnt in mcq_sets.items():
            if cnt > 1:
                errors.append(f"Duplicate MCQ options+index occurs {cnt}x: {opts} / index {idx}")

    # Context dominance
    if not allow_flags.get("allow_context_dominance"):
        total_prompts = len(data)
        for w, cnt in context_words.items():
            if cnt / total_prompts > max_context_ratio:
                errors.append(f"Context word '{w}' dominates {cnt}/{total_prompts} prompts")

    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content-root", required=True)
    ap.add_argument("--max-context-ratio", type=float, default=0.4)
    ap.add_argument("--baseline", help="Path to duplicate baseline JSON")
    args = ap.parse_args()

    baseline = {}
    if args.baseline:
        try:
            blob = load_json(args.baseline)
            for p, flags in blob.get("packs", {}).items():
                baseline[os.path.normpath(p)] = flags
        except Exception as e:
            print(f"[DUP-FAIL] Could not load baseline {args.baseline}: {e}")
            sys.exit(1)

    failed = False

    for root, _, files in os.walk(args.content_root):
        if "exercises.json" in files:
            path = os.path.join(root, "exercises.json")
            allow_flags = baseline.get(os.path.normpath(path), {})
            try:
                errors = check_pack(path, args.max_context_ratio, allow_flags)
            except Exception as e:
                print(f"[DUP-FAIL] {path}: parse error {e}")
                failed = True
                continue

            for err in errors:
                print(f"[DUP-FAIL] {path}: {err}")
                failed = True

    if failed:
        print("\n✖ HARD DUPLICATE GATE FAILED")
        sys.exit(1)
    else:
        print("✅ HARD DUPLICATE GATE PASSED")


if __name__ == "__main__":
    main()
