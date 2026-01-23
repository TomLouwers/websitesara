#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import re
import sys
import hashlib
from collections import Counter, defaultdict
from typing import Any, Dict, List, Tuple, Optional

NUM_PATTERN = re.compile(r"-?\d+(?:[.,]\d+)?")
WORD_PATTERN = re.compile(r"\b[a-zA-Z]{4,}\b")

# Global stopwords + template woorden die in educatieve prompts onvermijdelijk zijn.
# (Deze woorden mogen NOOIT een pack laten falen op context-dominantie.)
STOPWORDS = {
    # generiek
    "bereken","welke","welk","wat","hoeveel","hier","deze","dit",
    "rekent","betekent","komt","staat","zijn","heeft","klopt","goed",
    "lees","kijk","kies","ongeveer","past","beste","antwoord",

    # routes/templates
    "beweegt","gaat","stappen","stap","daarna","eerst","routezin","hierbij",
    "vooruit","achteruit","links","rechts",

    # n3 explain templates
    "wordt","maakt","doet","gebeurt",

    # meten templates
    "gebruik","meten","meet","past","beste","logisch","uitspraak","eenheid"
}

def norm_rel(path: str, content_root: str) -> str:
    # absolute -> relative to content_root; normalize slashes
    ap = os.path.abspath(path)
    cr = os.path.abspath(content_root)
    if ap.startswith(cr):
        rel = os.path.relpath(ap, cr)
    else:
        rel = path
    return rel.replace("\\", "/")

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def parse_pack_meta(path: str) -> Dict[str, Any]:
    p = path.replace("\\", "/")
    parts = p.split("/")

    meta = {"domain": "", "grade": None, "level": "", "topic": ""}

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

def extract_numeric_core(prompt: str) -> Tuple[str, ...]:
    # Normaliseer komma naar punt om "2,5" en "2.5" gelijk te trekken
    nums = NUM_PATTERN.findall(prompt.replace(",", "."))
    return tuple(nums)

def extract_context_words(prompt: str) -> List[str]:
    # Alleen iets "informatieve" woorden: >=5 letters en niet in stopwords
    words = [w.lower() for w in WORD_PATTERN.findall(prompt)]
    words = [w for w in words if len(w) >= 5]
    return [w for w in words if w not in STOPWORDS]

def check_pack(path: str, max_context_ratio: float) -> List[str]:
    try:
        data = load_json(path)
    except Exception as e:
        return [f"parse error: {e}"]

    if not isinstance(data, list) or len(data) == 0:
        # lege pack: geen duplicate fail (dit wordt elders als warning gerapporteerd)
        return []

    errors: List[str] = []

    numeric_cores = Counter()
    mcq_sets = Counter()
    context_prompt_counts = Counter()  # telt in hoeveel prompts een woord voorkomt (niet hoe vaak)

    for ex in data:
        prompt = ex.get("prompt", "") or ""

        # Numeric core duplicates: gebaseerd op cijfers in prompt
        core = extract_numeric_core(prompt)
        if core:
            numeric_cores[core] += 1

        # MCQ duplicates: options + solution.index
        if (ex.get("interaction") or {}).get("type") == "mcq":
            opts = tuple(ex.get("options", []) or [])
            idx = (ex.get("solution") or {}).get("index")
            mcq_sets[(opts, idx)] += 1

        # Context dominance: tel per prompt UNIQUE woorden
        uniq_words = set(extract_context_words(prompt))
        for w in uniq_words:
            context_prompt_counts[w] += 1

    # 1) Numeric duplicates
    for core, cnt in numeric_cores.items():
        if cnt > 1:
            errors.append(f"Duplicate numeric core {core} occurs {cnt}x")

    # 2) MCQ duplicates
    for (opts, idx), cnt in mcq_sets.items():
        if cnt > 1:
            errors.append(f"Duplicate MCQ options+index occurs {cnt}x (index {idx})")

    # 3) Context dominance
    total_prompts = len(data)
    for w, cnt in context_prompt_counts.items():
        if total_prompts > 0 and (cnt / total_prompts) > max_context_ratio:
            errors.append(f"Context word '{w}' dominates {cnt}/{total_prompts} prompts (> {max_context_ratio:.2f})")

    return errors

def load_baseline(baseline_path: Optional[str]) -> Dict[str, Any]:
    if not baseline_path:
        return {}
    if not os.path.exists(baseline_path):
        return {}

    try:
        baseline = load_json(baseline_path)
    except Exception:
        return {}

    packs = baseline.get("packs")
    if not isinstance(packs, dict):
        return baseline

    # Normalize keys:
    # - backslashes -> slashes
    # - strip leading "content/" if present
    newpacks = {}
    for k, v in packs.items():
        nk = k.replace("\\", "/")
        if nk.startswith("content/"):
            nk = nk[len("content/"):]
        newpacks[nk] = v

    baseline["packs"] = newpacks
    return baseline

def load_overrides(overrides_path: Optional[str]) -> Dict[str, Any]:
    if not overrides_path:
        return {}
    if not os.path.exists(overrides_path):
        return {}
    try:
        return load_json(overrides_path)
    except Exception:
        return {}

def get_topic_override_ratio(overrides: Dict[str, Any], topic: str, default_ratio: float) -> float:
    arr = overrides.get("topicOverrides", [])
    if not isinstance(arr, list):
        return default_ratio
    for it in arr:
        if it.get("topic") == topic and isinstance(it.get("maxContextRatio"), (int, float)):
            return float(it["maxContextRatio"])
    return default_ratio

def baseline_entry(baseline: Dict[str, Any], pack_path: str, content_root: str) -> Optional[Dict[str, Any]]:
    packs = baseline.get("packs")
    if not isinstance(packs, dict):
        return None

    key = norm_rel(pack_path, content_root)  # e.g. nl-NL/.../exercises.json

    # direct match
    if key in packs:
        return packs[key]

    # fallback: some baselines may still include "content/" prefix
    if f"content/{key}" in packs:
        return packs[f"content/{key}"]

    # fallback: raw
    raw = pack_path.replace("\\", "/")
    if raw in packs:
        return packs[raw]

    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content-root", required=True)
    ap.add_argument("--baseline", default=None, help="Path to duplicate_baseline.json (optional)")
    ap.add_argument("--overrides", default=None, help="Path to duplicate_gate_overrides.json (optional)")
    ap.add_argument("--max-context-ratio", type=float, default=0.40, help="Default context dominance threshold")
    args = ap.parse_args()

    baseline = load_baseline(args.baseline)
    overrides = load_overrides(args.overrides)

    failed = False
    warn_count = 0
    fail_count = 0

    for root, _, files in os.walk(args.content_root):
        if "exercises.json" not in files:
            continue

        path = os.path.join(root, "exercises.json")
        meta = parse_pack_meta(path)
        topic = meta.get("topic") or ""

        # topic-aware ratio (optioneel)
        ratio = get_topic_override_ratio(overrides, topic, args.max_context_ratio)

        errors = check_pack(path, ratio)
        if not errors:
            continue

        # baseline behavior:
        # - If pack is listed in baseline:
        #   - If baseline has sha256 and file hash matches -> WARN only
        #   - Else (hash missing OR changed) -> FAIL (changed legacy must improve)
        # - If pack not in baseline -> FAIL
        be = baseline_entry(baseline, path, args.content_root)

        if be is not None:
            baseline_hash = be.get("sha256")
            current_hash = None
            if isinstance(baseline_hash, str) and baseline_hash:
                current_hash = sha256_file(path)
                if current_hash == baseline_hash:
                    for err in errors:
                        print(f"[DUP-WARN][BASELINE] {path}: {err}")
                        warn_count += 1
                else:
                    for err in errors:
                        print(f"[DUP-FAIL][CHANGED] {path}: {err}")
                        fail_count += 1
                        failed = True
            else:
                # hash ontbreekt: behandel als WARN om legacy niet te blokkeren
                # (maar adviseer baseline hashes later te fixen)
                for err in errors:
                    print(f"[DUP-WARN][BASELINE-NOHASH] {path}: {err}")
                    warn_count += 1
        else:
            for err in errors:
                print(f"[DUP-FAIL] {path}: {err}")
                fail_count += 1
                failed = True

    if failed:
        print(f"\n HARD DUPLICATE GATE FAILED - {fail_count} fail(s), {warn_count} warn(s).")
        print("Tip: voeg topicOverrides toe of baseline sha256 voor legacy packs; nieuwe/gewijzigde packs moeten schoon zijn.")
        sys.exit(1)

    print(f" HARD DUPLICATE GATE PASSED - {warn_count} warn(s) (baseline-only).")
    sys.exit(0)

if __name__ == "__main__":
    main()

