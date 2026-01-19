#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

import jsonschema

from validate_all_exercises_multidomain import (
    read_json,
    load_taskform_canon,
    load_topic_canon,
    load_misconcept_keys,
    validate_taskform_canon_integrity,
    validate_canon_lock,
    validate_exercise_list
)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="Path to an exercises.json file")
    ap.add_argument("--schema", default="docs/schemas/ExerciseSchema.json")
    ap.add_argument("--taskforms", default="docs/taskvormen-canon.json")
    ap.add_argument("--topics", default="docs/topic-canon.json")
    ap.add_argument("--canon-lock", default="docs/canon-lock.json")
    ap.add_argument("--misconcepts-root", default="content/nl-NL/_shared/misconcepts")
    args = ap.parse_args()

    ex_path = Path(args.file)
    if not ex_path.exists():
        print(f"File not found: {ex_path}", file=sys.stderr)
        return 2

    schema = read_json(Path(args.schema))
    schema_validator = jsonschema.Draft202012Validator(schema)

    taskform_canon = load_taskform_canon(Path(args.taskforms))
    topic_canon = load_topic_canon(Path(args.topics))

    errors: List[str] = []
    validate_taskform_canon_integrity(taskform_canon, errors)
    validate_canon_lock(errors, Path(args.canon_lock))
    if errors:
        for e in errors:
            print(e)
        print("❌ Canon validation failed.", file=sys.stderr)
        return 2

    misconcept_keys_all: Set[str] = load_misconcept_keys(Path(args.misconcepts_root))

    data = read_json(ex_path)
    if not isinstance(data, list):
        print(f"[{ex_path}] File must be a JSON array.", file=sys.stderr)
        return 2

    # file-level schema
    try:
        schema_validator.validate(data)
    except jsonschema.ValidationError as e:
        print(f"[{ex_path}] Schema violation (file-level): {e.message}", file=sys.stderr)
        return 2

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
        print(f"❌ FAIL — {len(errs)} error(s).", file=sys.stderr)
        return 2

    print("✅ OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
