#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import jsonschema


# --------------------------
# JSON helpers
# --------------------------

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def is_numeric_value(v: Any) -> bool:
    if isinstance(v, (int, float)):
        return True
    if isinstance(v, str):
        try:
            float(v.replace(",", "."))
            return True
        except ValueError:
            return False
    return False

def find_all_exercise_files(content_root: Path) -> List[Path]:
    return sorted(content_root.rglob("exercises.json"))


# --------------------------
# Path parsing for gate
# --------------------------

def parse_group_from_path(ex_path: Path) -> str | None:
    for part in ex_path.parts:
        if part.startswith("groep-"):
            return part
    return None

def parse_domain_from_path(ex_path: Path, content_root: Path) -> str | None:
    try:
        rel = ex_path.relative_to(content_root)
    except ValueError:
        return None
    # rel parts: nl-NL, domain, groep-x, ...
    if len(rel.parts) >= 2:
        return rel.parts[1]
    return None

def parse_topic_from_path(ex_path: Path) -> str | None:
    parts = list(ex_path.parts)
    if "topics" not in parts:
        return None
    i = parts.index("topics")
    if i + 1 < len(parts):
        return parts[i + 1]
    return None


# --------------------------
# Misconcept keys loader (supports dict OR list format)
# --------------------------

def load_misconcept_keys(shared_misconcepts_root: Path) -> Set[str]:
    keys: Set[str] = set()
    if not shared_misconcepts_root.exists():
        return keys

    for p in sorted(shared_misconcepts_root.glob("*.json")):
        try:
            data = read_json(p)
        except Exception:
            continue

        misconcepts = data.get("misconcepts")

        # Format A: dict/object
        if isinstance(misconcepts, dict):
            for k in misconcepts.keys():
                if isinstance(k, str) and k.strip():
                    keys.add(k.strip())
            continue

        # Format B: array/list
        if isinstance(misconcepts, list):
            for item in misconcepts:
                if isinstance(item, dict):
                    k = item.get("key")
                    if isinstance(k, str) and k.strip():
                        keys.add(k.strip())
            continue

    return keys


# --------------------------
# Taskform canon validation
# --------------------------

def validate_taskform_canon_integrity(taskform_canon: Dict[str, Any], errors: List[str]) -> None:
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
                    errors.append(f"[CANON] Level '{level_key}' references undefined taskForm '{tf}' in {list_name}")


# --------------------------
# Kerndoelen-per-groep + topic canon loaders (gate)
# --------------------------

def load_kerndoelen_per_groep(path: Path) -> dict[str, set[int]]:
    data = read_json(path)
    groups = data.get("groups", {})
    out: dict[str, set[int]] = {}

    if not isinstance(groups, dict):
        return out

    for g, payload in groups.items():
        if not isinstance(payload, dict):
            continue
        ks = payload.get("kerndoelen", [])
        if isinstance(ks, list):
            ints: set[int] = set()
            for k in ks:
                if isinstance(k, int):
                    ints.add(k)
            out[g] = ints
    return out

def load_topic_canon_for_domain(topic_canon_root: Path, domain: str) -> dict[str, set[int]]:
    """
    Returns mapping: topicSlug -> set(kerndoelen)
    Expects file: topic-canon.<domain>.json
    """
    candidates = [
        topic_canon_root / f"topic-canon.{domain}.json",
        topic_canon_root / f"topic-canon.{domain.replace('_','-')}.json",
        topic_canon_root / f"topic-canon.{domain.replace('-','_')}.json",
    ]
    canon_path = None
    for c in candidates:
        if c.exists():
            canon_path = c
            break
    if canon_path is None:
        return {}

    data = read_json(canon_path)
    topics = data.get("topics", [])
    out: dict[str, set[int]] = {}
    if not isinstance(topics, list):
        return out

    for t in topics:
        if not isinstance(t, dict):
            continue
        slug = t.get("topic")
        ks = t.get("kerndoelen", [])
        if isinstance(slug, str) and isinstance(ks, list):
            out[slug] = set(k for k in ks if isinstance(k, int))
    return out


def validate_topic_kerndoelen_gate(
    ex_path: Path,
    content_root: Path,
    kerndoelen_per_groep: dict[str, set[int]],
    topic_kerndoelen_map: dict[str, set[int]],
    *,
    strict_topic_canon: bool,
    warn_unknown_topics: bool
) -> Tuple[List[str], List[str]]:
    """
    Gate:
      - If strict_topic_canon: unknown topic => ERROR
      - Else: unknown topic => WARNING (if warn_unknown_topics) or ignore
      - If known topic: topic kerndoelen must be subset of group kerndoelen
    """
    errs: list[str] = []
    warns: list[str] = []

    group = parse_group_from_path(ex_path)
    domain = parse_domain_from_path(ex_path, content_root)
    topic = parse_topic_from_path(ex_path)

    if group is None or domain is None or topic is None:
        return errs, warns  # ignore non-standard paths

    if group not in kerndoelen_per_groep:
        errs.append(f"[{ex_path}] [KERND-GATE] Group '{group}' not found in kerndoelen-per-groep.json")
        return errs, warns

    if topic not in topic_kerndoelen_map:
        msg = f"[{ex_path}] [KERND-GATE] Topic '{topic}' not found in topic-canon for domain '{domain}'"
        if strict_topic_canon:
            errs.append(msg)
        else:
            if warn_unknown_topics:
                warns.append(msg.replace("[KERND-GATE]", "[KERND-WARN]"))
        return errs, warns

    topic_k = topic_kerndoelen_map[topic]
    group_k = kerndoelen_per_groep[group]

    missing = sorted(list(topic_k - group_k))
    if missing:
        errs.append(
            f"[{ex_path}] [KERND-GATE] Topic '{topic}' has kerndoelen {sorted(list(topic_k))} "
            f"but group '{group}' allows {sorted(list(group_k))}. Missing in group: {missing}"
        )
    return errs, warns


# --------------------------
# Exercise validation
# --------------------------

def infer_taskform(ex: Dict[str, Any]) -> str | None:
    md = ex.get("metadata") or {}
    if isinstance(md, dict):
        tf = md.get("taskForm")
        return tf if isinstance(tf, str) else None
    return None

def get_level(ex: Dict[str, Any]) -> str | None:
    lvl = ex.get("level")
    return lvl if isinstance(lvl, str) else None

def validate_exercise_list(
    exercises: List[Dict[str, Any]],
    item_validator: jsonschema.Validator,
    taskform_canon: Dict[str, Any],
    misconcept_keys_all: Set[str],
    file_path: Path
) -> List[str]:
    errors: List[str] = []

    levels_cfg = taskform_canon.get("levels") or {}
    defined_taskforms = set((taskform_canon.get("taskFormDefinitions") or {}).keys())

    def err(i: int, exid: str | None, msg: str) -> None:
        prefix = f"[{file_path}]"
        errors.append(f"{prefix} {exid}: {msg}" if exid else f"{prefix} item[{i}]: {msg}")

    for i, ex in enumerate(exercises):
        exid = ex.get("id") if isinstance(ex.get("id"), str) else None

        # Validate ONE exercise against #/$defs/Exercise
        try:
            item_validator.validate(ex)
        except jsonschema.ValidationError as e:
            err(i, exid, f"Schema violation: {e.message}")
            continue

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

        itype = (ex.get("interaction") or {}).get("type")

        # select_single <-> mcq consistency
        if tf == "select_single" and itype != "mcq":
            err(i, exid, "taskForm 'select_single' requires interaction.type 'mcq'")
        if itype == "mcq" and tf != "select_single":
            err(i, exid, "interaction.type 'mcq' requires taskForm 'select_single'")

        # n2 MCQ wording guardrail
        if level == "n2" and itype == "mcq":
            prompt = (ex.get("prompt") or "").lower()
            banned_phrases = [
                "wat gaat er mis", "welke fout", "waarom", "leg uit", "verklaar",
                "slimste aanpak", "beste strategie"
            ]
            for bp in banned_phrases:
                if bp in prompt:
                    err(i, exid, f"n2 mcq prompt contains banned wording: '{bp}'")
                    break

        # misconcept keys existence (if shared packs exist)
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

        # numeric => numeric solution.value
        if itype == "numeric":
            sol = ex.get("solution") or {}
            val = sol.get("value") if isinstance(sol, dict) else None
            if not is_numeric_value(val):
                err(i, exid, f"interaction.type 'numeric' requires numeric solution.value, got {val!r}")

        # mcq bounds check
        if itype == "mcq":
            options = ex.get("options")
            sol = ex.get("solution") or {}
            idx = sol.get("index") if isinstance(sol, dict) else None
            if isinstance(options, list) and isinstance(idx, int) and idx >= len(options):
                err(i, exid, f"mcq solution.index {idx} out of range (options length {len(options)})")

    return errors


# --------------------------
# Main
# --------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--content-root", default="content")
    ap.add_argument("--schema", default="docs/new/schemas/ExerciseSchema.json")
    ap.add_argument("--taskforms", default="docs/new/taskvormen-canon.json")
    ap.add_argument("--misconcepts-root", default="content/nl-NL/_shared/misconcepts")
    ap.add_argument("--kerndoelen", default="docs/new/kerndoelen-per-groep.json")
    ap.add_argument("--topic-canon-root", default="docs/new")

    ap.add_argument("--fail-fast", action="store_true")
    ap.add_argument(
        "--strict-topic-canon",
        action="store_true",
        help="If set: unknown topic slugs (not found in topic-canon.<domain>.json) are errors. "
             "If not set: unknown topics are warnings or ignored (migration mode)."
    )
    ap.add_argument(
        "--warn-unknown-topics",
        action="store_true",
        default=True,
        help="In migration mode (no --strict-topic-canon): print warnings for unknown topics. "
             "Use --no-warn-unknown-topics to silence."
    )
    ap.add_argument(
        "--no-warn-unknown-topics",
        action="store_false",
        dest="warn_unknown_topics",
        help="Silence warnings for unknown topics in migration mode."
    )

    args = ap.parse_args()

    content_root = Path(args.content_root)
    schema_path = Path(args.schema)
    taskforms_path = Path(args.taskforms)
    misconcepts_root = Path(args.misconcepts_root)
    kerndoelen_path = Path(args.kerndoelen)
    topic_canon_root = Path(args.topic_canon_root)

    if not schema_path.exists():
        print(f"Schema file not found: {schema_path}", file=sys.stderr)
        return 2
    if not taskforms_path.exists():
        print(f"Taskforms canon not found: {taskforms_path}", file=sys.stderr)
        return 2
    if not kerndoelen_path.exists():
        print(f"Kerndoelen-per-groep file not found: {kerndoelen_path}", file=sys.stderr)
        return 2

    schema = read_json(schema_path)
    taskform_canon = read_json(taskforms_path)

    # Two validators:
    # - file_validator validates the whole exercises.json file (array root)
    # - item_validator validates ONE exercise object against #/$defs/Exercise
    file_validator = jsonschema.Draft202012Validator(schema)
    item_validator = file_validator.evolve(schema={"$ref": "#/$defs/Exercise"})

    canon_errors: List[str] = []
    validate_taskform_canon_integrity(taskform_canon, canon_errors)
    if canon_errors:
        for e in canon_errors:
            print(e)
        print("❌ Taskforms canon invalid.", file=sys.stderr)
        return 2

    kerndoelen_per_groep = load_kerndoelen_per_groep(kerndoelen_path)
    misconcept_keys_all = load_misconcept_keys(misconcepts_root)

    ex_files = find_all_exercise_files(content_root)
    if not ex_files:
        print(f"No exercises.json files found under: {content_root}")
        return 0

    topic_canon_cache: dict[str, dict[str, set[int]]] = {}

    total_files = 0
    total_errors = 0
    total_warnings = 0

    for ex_path in ex_files:
        total_files += 1

        # ---- Gate: kerndoelen per topic/group ----
        domain = parse_domain_from_path(ex_path, content_root)
        if domain:
            if domain not in topic_canon_cache:
                topic_canon_cache[domain] = load_topic_canon_for_domain(topic_canon_root, domain)

            gate_errs, gate_warns = validate_topic_kerndoelen_gate(
                ex_path=ex_path,
                content_root=content_root,
                kerndoelen_per_groep=kerndoelen_per_groep,
                topic_kerndoelen_map=topic_canon_cache[domain],
                strict_topic_canon=args.strict_topic_canon,
                warn_unknown_topics=args.warn_unknown_topics
            )

            if gate_warns:
                for w in gate_warns:
                    print(w)
                total_warnings += len(gate_warns)

            if gate_errs:
                for e in gate_errs:
                    print(e)
                total_errors += len(gate_errs)
                if args.fail_fast:
                    return 2

        # ---- Read + parse JSON (treat empty file as []) ----
        try:
            text = ex_path.read_text(encoding="utf-8")
            if text.strip() == "":
                data = []
            else:
                data = json.loads(text)
        except Exception as e:
            print(f"[{ex_path}] JSON parse error: {e}")
            total_errors += 1
            if args.fail_fast:
                return 2
            continue

        # ---- file-level schema validate (array root) ----
        try:
            file_validator.validate(data)
        except jsonschema.ValidationError as e:
            print(f"[{ex_path}] Schema violation (file-level): {e.message}")
            total_errors += 1
            if args.fail_fast:
                return 2
            continue

        if not isinstance(data, list):
            print(f"[{ex_path}] File must be a JSON array (got {type(data).__name__})")
            total_errors += 1
            if args.fail_fast:
                return 2
            continue

        # ---- item-level checks ----
        errs = validate_exercise_list(
            exercises=data,
            item_validator=item_validator,
            taskform_canon=taskform_canon,
            misconcept_keys_all=misconcept_keys_all,
            file_path=ex_path
        )

        if errs:
            for e in errs:
                print(e)
            total_errors += len(errs)
            if args.fail_fast:
                return 2

    if total_errors == 0:
        msg = f"✅ OK — validated {total_files} exercises.json files."
        if total_warnings > 0:
            msg += f" ({total_warnings} warning(s))"
        print(msg)
        return 0

    msg = f"❌ FAIL — {total_errors} error(s) across {total_files} file(s)."
    if total_warnings > 0:
        msg += f" ({total_warnings} warning(s))"
    print(msg, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
