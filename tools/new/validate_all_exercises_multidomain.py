#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Batch validator for Learn & Play static exercise packs.

Validates:
- JSON parse + schema (ExerciseSchema.json)
- Taskform canon constraints (allowed/disallowed by level)
- Canon consistency (all taskforms referenced exist in taskFormDefinitions)
- MCQ structure + index bounds
- Numeric solution must be numeric
- taskForm <-> interaction type consistency (select_single <-> mcq)
- n2 MCQ wording guardrail (prevents error-analysis drift)
- Misconcept keys existence (shared misconcepts packs)
- (Optional) Canon lock enforcement
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple, Set

try:
    import jsonschema
except ImportError:
    print("Missing dependency: jsonschema. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(2)


# --------------------------
# Helpers
# --------------------------

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def is_numeric_value(v: Any) -> bool:
    if isinstance(v, (int, float)):
        return True
    if isinstance(v, str):
        try:
            float(v.replace(",", "."))  # allow "0,5" too
            return True
        except ValueError:
            return False
    return False

def find_all_exercise_files(content_root: Path) -> List[Path]:
    # We intentionally validate only files called exercises.json
    return sorted(content_root.rglob("exercises.json"))

def normalize_domain_key(domain: str) -> str:
    # Keep it simple; user can standardize later
    return domain.strip()


# --------------------------
# Canon loading
# --------------------------

def load_taskform_canon(taskforms_path: Path) -> Dict[str, Any]:
    if not taskforms_path.exists():
        raise FileNotFoundError(f"Taskforms canon not found: {taskforms_path}")
    return read_json(taskforms_path)

def load_topic_canon(topic_canon_path: Path) -> Dict[str, Any] | None:
    if not topic_canon_path.exists():
        return None
    return read_json(topic_canon_path)

def load_misconcept_keys(shared_misconcepts_root: Path) -> Set[str]:
    keys: Set[str] = set()
    if not shared_misconcepts_root.exists():
        return keys

    for p in sorted(shared_misconcepts_root.glob("*.json")):
        try:
            data = read_json(p)
        except Exception:
            continue

        # expected:
        # { "version": "...", "domain": "...", "misconcepts": { "KEY": {...}, ... } }
        misconcepts = data.get("misconcepts", {})
        if isinstance(misconcepts, dict):
            for k in misconcepts.keys():
                if isinstance(k, str) and k.strip():
                    keys.add(k.strip())
    return keys

def validate_taskform_canon_integrity(taskform_canon: Dict[str, Any], errors: List[str]) -> None:
    """Hard gate: all taskforms referenced in levels must exist in taskFormDefinitions."""
    defined = set((taskform_canon.get("taskFormDefinitions") or {}).keys())
    levels = taskform_canon.get("levels") or {}

    if not defined:
        errors.append("[CANON] taskFormDefinitions is empty or missing.")
        return

    if not isinstance(levels, dict):
        errors.append("[CANON] levels must be an object.")
        return

    for level_key, level in levels.items():
        if not isinstance(level, dict):
            errors.append(f"[CANON] levels.{level_key} must be an object.")
            continue

        for list_name in ["allowedTaskForms", "disallowedTaskForms"]:
            tfs = level.get(list_name, [])
            if tfs is None:
                continue
            if not isinstance(tfs, list):
                errors.append(f"[CANON] levels.{level_key}.{list_name} must be an array.")
                continue

            for tf in tfs:
                if not isinstance(tf, str) or not tf.strip():
                    errors.append(f"[CANON] levels.{level_key}.{list_name} contains invalid taskForm value: {tf!r}")
                    continue
                if tf not in defined:
                    errors.append(
                        f"[CANON] Level '{level_key}' references undefined taskForm '{tf}' in {list_name}"
                    )

def validate_canon_lock(errors: List[str], lock_path: Path) -> None:
    """
    Optional: if docs/canon-lock.json exists and locked=true,
    enforce versions match.
    """
    if not lock_path.exists():
        return

    lock = read_json(lock_path)
    if not lock.get("locked", False):
        return

    files = lock.get("files", {})
    if not isinstance(files, dict):
        errors.append("[CANON-LOCK] 'files' must be an object.")
        return

    for key, meta in files.items():
        if not isinstance(meta, dict):
            errors.append(f"[CANON-LOCK] files.{key} must be an object.")
            continue
        p = meta.get("path")
        v = meta.get("version")
        if not p or not v:
            errors.append(f"[CANON-LOCK] files.{key} must have 'path' and 'version'.")
            continue

        fp = Path(p)
        if not fp.exists():
            errors.append(f"[CANON-LOCK] Locked file missing: {fp}")
            continue

        data = read_json(fp)
        file_version = data.get("version")
        if file_version != v:
            errors.append(
                f"[CANON-LOCK] {key} version mismatch: lock={v} file={file_version}"
            )


# --------------------------
# Exercise validation
# --------------------------

def infer_taskform(ex: Dict[str, Any]) -> str | None:
    md = ex.get("metadata") or {}
    if isinstance(md, dict):
        tf = md.get("taskForm")
        if isinstance(tf, str):
            return tf
    return None

def get_level(ex: Dict[str, Any]) -> str | None:
    lvl = ex.get("level")
    return lvl if isinstance(lvl, str) else None

def validate_exercise_list(
    exercises: List[Dict[str, Any]],
    schema: Dict[str, Any],
    schema_validator: jsonschema.Validator,
    taskform_canon: Dict[str, Any],
    misconcept_keys_all: Set[str],
    topic_canon: Dict[str, Any] | None,
    file_path: Path
) -> List[str]:
    errors: List[str] = []

    levels_cfg = taskform_canon.get("levels") or {}
    defined_taskforms = set((taskform_canon.get("taskFormDefinitions") or {}).keys())

    # topic canon lookup (optional)
    allowed_topics: Set[str] = set()
    if topic_canon and isinstance(topic_canon, dict):
        # user’s topic canon format can vary; keep flexible:
        # recommended: topic_canon["topics"] = [{"domain":..., "grade":..., "level":..., "topic":...}, ...]
        topics = topic_canon.get("topics")
        if isinstance(topics, list):
            for t in topics:
                if isinstance(t, dict):
                    tp = t.get("topic")
                    if isinstance(tp, str) and tp.strip():
                        allowed_topics.add(tp.strip())

    def err(i: int, exid: str | None, msg: str) -> None:
        loc = f"{file_path}"
        prefix = f"[{loc}]"
        if exid:
            errors.append(f"{prefix} {exid}: {msg}")
        else:
            errors.append(f"{prefix} item[{i}]: {msg}")

    # A) Schema validation for entire file is already done in caller,
    # but validate each item too for better pinpointing.
    for i, ex in enumerate(exercises):
        exid = ex.get("id") if isinstance(ex.get("id"), str) else None

        try:
            schema_validator.validate(ex)
        except jsonschema.ValidationError as e:
            err(i, exid, f"Schema violation: {e.message}")
            continue

        # B) Taskform per level
        level = get_level(ex)
        tf = infer_taskform(ex)
        if not level:
            err(i, exid, "Missing or invalid 'level'")
            continue
        if level not in levels_cfg:
            err(i, exid, f"Unknown level '{level}' (not in taskvormen-canon)")
            continue

        if not tf:
            err(i, exid, "Missing metadata.taskForm")
            continue
        if tf not in defined_taskforms:
            err(i, exid, f"Unknown taskForm '{tf}' (not in taskFormDefinitions)")
            continue

        allowed = set(levels_cfg[level].get("allowedTaskForms", []) or [])
        disallowed = set(levels_cfg[level].get("disallowedTaskForms", []) or [])

        if allowed and tf not in allowed:
            err(i, exid, f"taskForm '{tf}' not allowed for level '{level}'")
        if disallowed and tf in disallowed:
            err(i, exid, f"taskForm '{tf}' is disallowed for level '{level}'")

        # B2) Enforce taskForm <-> interaction type consistency
        itype = (ex.get("interaction") or {}).get("type")
        if tf == "select_single" and itype != "mcq":
            err(i, exid, "taskForm 'select_single' requires interaction.type 'mcq'")
        if itype == "mcq" and tf != "select_single":
            err(i, exid, "interaction.type 'mcq' requires taskForm 'select_single'")

        # B3) Guardrail: prevent n2 MCQ from becoming error analysis by wording
        if level == "n2" and itype == "mcq":
            prompt = (ex.get("prompt") or "").lower()
            banned_phrases = [
                "wat gaat er mis",
                "welke fout",
                "waarom",
                "leg uit",
                "verklaar",
                "slimste aanpak",
                "beste strategie"
            ]
            for bp in banned_phrases:
                if bp in prompt:
                    err(i, exid, f"n2 mcq prompt contains banned wording: '{bp}'")
                    break

        # C) Misconcept key existence
        md = ex.get("metadata") or {}
        mkeys = md.get("misconceptKeys") if isinstance(md, dict) else None
        if not isinstance(mkeys, list) or len(mkeys) == 0:
            err(i, exid, "metadata.misconceptKeys must be a non-empty array")
        else:
            for mk in mkeys:
                if not isinstance(mk, str) or not mk.strip():
                    err(i, exid, f"Invalid misconceptKey value: {mk!r}")
                    continue
                if misconcept_keys_all and mk.strip() not in misconcept_keys_all:
                    err(i, exid, f"Unknown misconceptKey '{mk}' (not found in _shared/misconcepts)")

        # D) Interaction-specific validation
        if itype == "numeric":
            sol = ex.get("solution") or {}
            val = sol.get("value") if isinstance(sol, dict) else None
            if not is_numeric_value(val):
                err(i, exid, f"interaction.type 'numeric' requires numeric solution.value, got {val!r}")

        elif itype == "mcq":
            options = ex.get("options")
            sol = ex.get("solution") or {}
            idx = sol.get("index") if isinstance(sol, dict) else None

            if not isinstance(options, list) or len(options) < 2:
                err(i, exid, "mcq requires 'options' array with at least 2 items")
            else:
                for opt in options:
                    if not isinstance(opt, str) or not opt.strip():
                        err(i, exid, f"mcq options must be non-empty strings (found {opt!r})")

            if not isinstance(idx, int):
                err(i, exid, "mcq requires solution.index as integer")
            else:
                if idx < 0:
                    err(i, exid, "mcq solution.index must be >= 0")
                if isinstance(options, list) and len(options) > 0 and idx >= len(options):
                    err(i, exid, f"mcq solution.index {idx} out of range (options length {len(options)})")

        # E) Optional: topic canon membership (soft gate if topic_canon present)
        if allowed_topics:
            topic = ex.get("topic")
            if isinstance(topic, str) and topic.strip():
                if topic.strip() not in allowed_topics:
                    err(i, exid, f"topic '{topic}' not in topic-canon")
            else:
                err(i, exid, "Missing or invalid 'topic'")

    return errors


# --------------------------
# Main
# --------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--content-root", default="content", help="Root folder containing curriculum packs")
    ap.add_argument("--schema", default="docs/schemas/ExerciseSchema.json", help="Path to ExerciseSchema.json")
    ap.add_argument("--taskforms", default="docs/taskvormen-canon.json", help="Path to taskforms canon")
    ap.add_argument("--topics", default="docs/topic-canon.json", help="Path to topic canon (optional)")
    ap.add_argument("--canon-lock", default="docs/canon-lock.json", help="Path to canon lock (optional)")
    ap.add_argument("--misconcepts-root", default="content/nl-NL/_shared/misconcepts", help="Shared misconcepts root")
    ap.add_argument("--fail-fast", action="store_true", help="Stop on first file with errors")
    args = ap.parse_args()

    content_root = Path(args.content_root)
    schema_path = Path(args.schema)
    taskforms_path = Path(args.taskforms)
    topics_path = Path(args.topics)
    canon_lock_path = Path(args.canon_lock)
    misconcepts_root = Path(args.misconcepts_root)

    all_errors: List[str] = []

    # Load schema
    if not schema_path.exists():
        print(f"Schema file not found: {schema_path}", file=sys.stderr)
        return 2
    schema = read_json(schema_path)
    schema_validator = jsonschema.Draft202012Validator(schema)

    # Load canons
    taskform_canon = load_taskform_canon(taskforms_path)
    topic_canon = load_topic_canon(topics_path)

    # Canon integrity gates
    validate_taskform_canon_integrity(taskform_canon, all_errors)
    validate_canon_lock(all_errors, canon_lock_path)

    # Load misconcept keys
    misconcept_keys_all = load_misconcept_keys(misconcepts_root)

    if all_errors:
        for e in all_errors:
            print(e)
        print("❌ Canon validation failed.", file=sys.stderr)
        return 2

    # Find exercise files
    if not content_root.exists():
        print(f"content-root not found: {content_root}", file=sys.stderr)
        return 2

    ex_files = find_all_exercise_files(content_root)
    if not ex_files:
        print(f"No exercises.json files found under: {content_root}")
        return 0

    total_files = 0
    total_errors = 0

    for ex_path in ex_files:
        total_files += 1
        try:
            data = read_json(ex_path)
        except Exception as e:
            print(f"[{ex_path}] JSON parse error: {e}")
            total_errors += 1
            if args.fail_fast:
                return 2
            continue

        # Validate file shape: should be an array
        if not isinstance(data, list):
            print(f"[{ex_path}] File must be a JSON array (got {type(data).__name__})")
            total_errors += 1
            if args.fail_fast:
                return 2
            continue

        # Schema validate whole array
        try:
            schema_validator.validate(data)
        except jsonschema.ValidationError as e:
            print(f"[{ex_path}] Schema violation (file-level): {e.message}")
            total_errors += 1
            if args.fail_fast:
                return 2
            continue

        errs = validate_exercise_list(
            exercises=data,
            schema=schema,
            schema_validator=schema_validator,
            taskform_canon=taskform_canon,
            misconcept_keys_all=misconcept_keys_all,
            topic_canon=topic_canon,
            file_path=ex_path
        )

        if errs:
            for e in errs:
                print(e)
            total_errors += len(errs)
            if args.fail_fast:
                return 2

    if total_errors == 0:
        print(f"✅ OK — validated {total_files} exercises.json files.")
        return 0

    print(f"❌ FAIL — {total_errors} error(s) across {total_files} file(s).", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
