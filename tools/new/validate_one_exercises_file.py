#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Set

import jsonschema

from validate_all_exercises_multidomain import (
    read_json,
    load_misconcept_keys,
    validate_taskform_canon_integrity,
    validate_exercise_list,
    load_kerndoelen_per_groep,
    load_topic_canon_for_domain,
    validate_topic_kerndoelen_gate,
    parse_domain_from_path
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="Path to an exercises.json file")
    ap.add_argument("--schema", default="docs/new/schemas/ExerciseSchema.json")
    ap.add_argument("--taskforms", default="docs/new/taskvormen-canon.json")
    ap.add_argument("--misconcepts-root", default="content/nl-NL/_shared/misconcepts")
    ap.add_argument("--kerndoelen", default="docs/new/kerndoelen-per-groep.json")
    ap.add_argument("--topic-canon-root", default="docs/new")
    ap.add_argument("--strict-topic-canon", action="store_true", help="Treat unknown topics as errors")
    ap.add_argument(
        "--no-warn-unknown-topics",
        action="store_true",
        help="Silence warnings for topics not in canon when not strict"
    )
    args = ap.parse_args()

    ex_path = Path(args.file)
    if not ex_path.exists():
        print(f"File not found: {ex_path}", file=sys.stderr)
        return 2

    schema_path = Path(args.schema)
    taskforms_path = Path(args.taskforms)
    kerndoelen_path = Path(args.kerndoelen)

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

    file_validator = jsonschema.Draft202012Validator(schema)
    item_validator = file_validator.evolve(schema={"$ref": "#/$defs/Exercise"})

    canon_errors: List[str] = []
    validate_taskform_canon_integrity(taskform_canon, canon_errors)
    if canon_errors:
        for e in canon_errors:
            print(e)
        print("❌ Taskforms canon invalid.", file=sys.stderr)
        return 2

    misconcept_keys_all: Set[str] = load_misconcept_keys(Path(args.misconcepts_root))
    kerndoelen_per_groep = load_kerndoelen_per_groep(kerndoelen_path)

    # ---- Gate: kerndoelen per topic/group ----
    content_root = Path("content")
    domain = parse_domain_from_path(ex_path, content_root)
    topic_map = {}
    if domain:
        topic_map = load_topic_canon_for_domain(Path(args.topic_canon_root), domain)

    gate_errs, gate_warns = validate_topic_kerndoelen_gate(
        ex_path=ex_path,
        content_root=content_root,
        kerndoelen_per_groep=kerndoelen_per_groep,
        topic_kerndoelen_map=topic_map,
        strict_topic_canon=args.strict_topic_canon,
        warn_unknown_topics=not args.no_warn_unknown_topics
    )
    for w in gate_warns:
        print(w)
    if gate_errs:
        for e in gate_errs:
            print(e)
        return 2

    # ---- Read + parse JSON (treat empty file as []) ----
    try:
        text = ex_path.read_text(encoding="utf-8")
        if text.strip() == "":
            data = []
        else:
            data = json.loads(text)
    except Exception as e:
        print(f"[{ex_path}] JSON parse error: {e}", file=sys.stderr)
        return 2

    # ---- file-level schema validate ----
    try:
        file_validator.validate(data)
    except jsonschema.ValidationError as e:
        print(f"[{ex_path}] Schema violation (file-level): {e.message}", file=sys.stderr)
        return 2

    if not isinstance(data, list):
        print(f"[{ex_path}] File must be a JSON array.", file=sys.stderr)
        return 2

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
        print(f"❌ FAIL — {len(errs)} error(s).", file=sys.stderr)
        return 2

    print("✅ OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
