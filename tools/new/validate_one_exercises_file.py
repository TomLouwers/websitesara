#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_one_exercises_file.py

Validate a single exercises.json file:
- JSON Schema (Draft 2020-12) validation
- taskForm validation against taskvormen-canon.json (best-effort)
- Report ONE clear "diff-style" error per invalid item (instead of a wall of errors)

Usage:
  py -3.13 tools/new/validate_one_exercises_file.py path/to/exercises.json --schema path/to/ExerciseSchema.json --taskforms docs/new/taskvormen-canon.json

Exit codes:
  0 = OK
  1 = validation failed (one or more items invalid)
  2 = CLI / IO / parse error
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import best_match
except Exception as e:
    print("ERROR: jsonschema package missing or incompatible:", e)
    sys.exit(2)

# NEW (no deprecated resolver)
try:
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except Exception as e:
    print("ERROR: referencing package missing or incompatible:", e)
    print("Install/upgrade: pip install 'jsonschema[format]' referencing")
    sys.exit(2)


# ----------------------------
# IO helpers
# ----------------------------

def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_print(s: str) -> None:
    """
    Avoid UnicodeEncodeError on Windows consoles.
    """
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("utf-8", errors="replace").decode("utf-8"))


# ----------------------------
# JSON pointer helpers
# ----------------------------

def join_json_pointer(parts: List[str]) -> str:
    if not parts:
        return "/"
    esc = []
    for p in parts:
        p = str(p).replace("~", "~0").replace("/", "~1")
        esc.append(p)
    return "/" + "/".join(esc)


def get_at_path(obj: Any, path: List[Any]) -> Any:
    cur = obj
    for p in path:
        try:
            if isinstance(cur, list):
                cur = cur[int(p)]
            elif isinstance(cur, dict):
                cur = cur[p]
            else:
                return None
        except Exception:
            return None
    return cur


def format_value(v: Any, max_len: int = 180) -> str:
    try:
        s = json.dumps(v, ensure_ascii=False)
    except Exception:
        s = repr(v)
    if len(s) > max_len:
        return s[:max_len] + "...(truncated)"
    return s


# ----------------------------
# taskForm canon parsing (best effort)
# ----------------------------

def extract_taskforms_from_canon(canon: Any) -> Tuple[Optional[set], Optional[Dict[str, set]]]:
    all_taskforms: set = set()
    by_level: Dict[str, set] = {}

    if isinstance(canon, list):
        for it in canon:
            if isinstance(it, str):
                all_taskforms.add(it)
            elif isinstance(it, dict):
                tf = it.get("taskForm") or it.get("id") or it.get("name")
                if isinstance(tf, str):
                    all_taskforms.add(tf)
                lvl = it.get("level")
                if isinstance(lvl, str) and isinstance(tf, str):
                    by_level.setdefault(lvl, set()).add(tf)

    elif isinstance(canon, dict):
        if isinstance(canon.get("taskForms"), list):
            for it in canon["taskForms"]:
                if isinstance(it, str):
                    all_taskforms.add(it)
                elif isinstance(it, dict):
                    tf = it.get("taskForm") or it.get("id") or it.get("name")
                    if isinstance(tf, str):
                        all_taskforms.add(tf)
                    lvl = it.get("level")
                    if isinstance(lvl, str) and isinstance(tf, str):
                        by_level.setdefault(lvl, set()).add(tf)

        levels = canon.get("levels") or canon.get("byLevel") or canon.get("levelTaskForms")
        if isinstance(levels, dict):
            for lvl, arr in levels.items():
                if not isinstance(lvl, str) or not isinstance(arr, list):
                    continue
                for it in arr:
                    if isinstance(it, str):
                        all_taskforms.add(it)
                        by_level.setdefault(lvl, set()).add(it)
                    elif isinstance(it, dict):
                        tf = it.get("taskForm") or it.get("id") or it.get("name")
                        if isinstance(tf, str):
                            all_taskforms.add(tf)
                            by_level.setdefault(lvl, set()).add(tf)

        if isinstance(canon.get("items"), list):
            for it in canon["items"]:
                if not isinstance(it, dict):
                    continue
                tf = it.get("taskForm") or it.get("id") or it.get("name")
                if isinstance(tf, str):
                    all_taskforms.add(tf)
                lvl = it.get("level")
                if isinstance(lvl, str) and isinstance(tf, str):
                    by_level.setdefault(lvl, set()).add(tf)

    all_taskforms_out = all_taskforms if all_taskforms else None
    by_level_out = by_level if by_level else None
    return all_taskforms_out, by_level_out


def taskform_error(ex: Dict[str, Any], all_taskforms: Optional[set], by_level: Optional[Dict[str, set]]) -> Optional[Dict[str, Any]]:
    md = ex.get("metadata") if isinstance(ex.get("metadata"), dict) else {}
    tf = md.get("taskForm")
    lvl = ex.get("level")

    if not isinstance(tf, str) or not tf.strip():
        return {
            "path": "/metadata/taskForm",
            "message": "metadata.taskForm missing/empty",
            "expected": "non-empty string (must exist in taskvormen-canon.json)",
            "actual": format_value(tf),
        }

    # If canon unavailable, don't hard-fail here (schema likely enforces enum anyway)
    if all_taskforms is None and by_level is None:
        return None

    if isinstance(lvl, str) and by_level and lvl in by_level:
        allowed = by_level[lvl]
        if tf not in allowed:
            return {
                "path": "/metadata/taskForm",
                "message": f"taskForm not allowed for level {lvl}",
                "expected": f"one of: {sorted(list(allowed))[:40]}",
                "actual": format_value(tf),
            }

    if all_taskforms and tf not in all_taskforms:
        return {
            "path": "/metadata/taskForm",
            "message": "taskForm not found in canon",
            "expected": f"one of: {sorted(list(all_taskforms))[:60]}",
            "actual": format_value(tf),
        }

    return None


# ----------------------------
# Error formatting
# ----------------------------

def describe_expected(err) -> str:
    v = getattr(err, "validator", "")
    val = getattr(err, "validator_value", None)

    if v == "required":
        if isinstance(val, list):
            return f"required fields include: {val}"
        return "missing required field(s)"

    if v == "type":
        return f"type: {val}"

    if v == "enum":
        if isinstance(val, list):
            show = val[:40]
            return f"one of: {show}" + (" ...(truncated)" if len(val) > 40 else "")
        return "one of enum values"

    if v == "minItems":
        return f"minItems >= {val}"
    if v == "maxItems":
        return f"maxItems <= {val}"
    if v == "minLength":
        return f"minLength >= {val}"
    if v == "pattern":
        return f"pattern: {val}"
    if v == "additionalProperties":
        return "no additional properties allowed"

    if val is not None:
        return f"{v}: {val}"
    return str(v) if v else "schema requirement"


def schema_error_for_item(validator: Draft202012Validator, item: Any) -> Optional[Dict[str, Any]]:
    errors = list(validator.iter_errors(item))
    if not errors:
        return None

    bm = best_match(errors) or errors[0]

    path_list = list(getattr(bm, "absolute_path", []))
    schema_path_list = list(getattr(bm, "absolute_schema_path", []))

    instance_path = join_json_pointer([str(p) for p in path_list])
    actual = get_at_path(item, path_list)
    expected = describe_expected(bm)

    return {
        "path": instance_path,
        "schemaPath": join_json_pointer([str(p) for p in schema_path_list]),
        "message": bm.message,
        "expected": expected,
        "actual": format_value(actual),
    }


# ----------------------------
# Registry-based schema setup (no deprecated resolver)
# ----------------------------

def _file_uri(path: str) -> str:
    # Minimal file:// URI that works on Windows + *nix
    ap = os.path.abspath(path)
    ap = ap.replace("\\", "/")
    if not ap.startswith("/"):
        # Windows drive letter "C:/..."
        return "file:///" + ap
    return "file://" + ap


def build_item_validator(schema: Dict[str, Any], schema_path: str) -> Draft202012Validator:
    """
    Build an item-level validator that can still resolve $ref to the root schema.
    Uses referencing.Registry (jsonschema>=4.18+ recommended approach).
    """
    item_schema = schema.get("items")
    if not isinstance(item_schema, dict):
        raise ValueError("Schema has no top-level 'items' object to validate array elements.")

    schema_id = schema.get("$id")
    if not isinstance(schema_id, str) or not schema_id.strip():
        schema_id = _file_uri(schema_path)
        schema["$id"] = schema_id

    registry = Registry().with_resource(
        schema_id,
        Resource.from_contents(schema, default_specification=DRAFT202012),
    )

    # CRITICAL FIX:
    # If items is a fragment-only $ref (e.g. "#/$defs/Exercise"),
    # make it absolute against the root schema id so it resolves in the full schema.
    if isinstance(item_schema.get("$ref"), str) and item_schema["$ref"].startswith("#"):
        item_schema = {"$ref": f"{schema_id}{item_schema['$ref']}"}

    # Safety: embed $defs locally so $ref fragments resolve even if registry lookup fails
    if "$defs" in schema and "$defs" not in item_schema:
        # copy to avoid mutating the original schema dict
        item_schema = dict(item_schema)
        item_schema["$defs"] = schema["$defs"]

    return Draft202012Validator(item_schema, registry=registry)

# ----------------------------
# Main
# ----------------------------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="Path to exercises.json")
    ap.add_argument("--schema", required=True, help="Path to ExerciseSchema.json")
    ap.add_argument("--taskforms", required=True, help="Path to taskvormen-canon.json")
    ap.add_argument("--max-errors", type=int, default=50, help="Max items to report (default 50)")
    return ap.parse_args()


def main() -> int:
    args = parse_args()

    if not os.path.exists(args.file):
        safe_print(f"ERROR: file not found: {args.file}")
        return 2
    if not os.path.exists(args.schema):
        safe_print(f"ERROR: schema not found: {args.schema}")
        return 2
    if not os.path.exists(args.taskforms):
        safe_print(f"ERROR: taskforms file not found: {args.taskforms}")
        return 2

    try:
        data = read_json(args.file)
    except Exception as e:
        safe_print(f"ERROR: cannot parse JSON file: {args.file}\n  {e}")
        return 2

    if not isinstance(data, list):
        safe_print(f"FAIL: root must be a JSON array, got {type(data).__name__}")
        return 1

    try:
        schema = read_json(args.schema)
    except Exception as e:
        safe_print(f"ERROR: cannot parse schema JSON: {args.schema}\n  {e}")
        return 2

    try:
        item_validator = build_item_validator(schema, args.schema)
    except Exception as e:
        safe_print(f"ERROR: cannot build validator:\n  {e}")
        return 2

    # Load canon (best-effort)
    try:
        canon = read_json(args.taskforms)
        all_taskforms, by_level = extract_taskforms_from_canon(canon)
    except Exception:
        all_taskforms, by_level = None, None

    invalid_count = 0
    reported = 0

    for idx, ex in enumerate(data):
        if reported >= args.max_errors:
            break

        ex_id = ex.get("id") if isinstance(ex, dict) else None

        schema_err = schema_error_for_item(item_validator, ex)
        tf_err = None
        if isinstance(ex, dict):
            tf_err = taskform_error(ex, all_taskforms, by_level)

        chosen = schema_err or tf_err
        if chosen:
            invalid_count += 1
            reported += 1

            header = f"[ITEM {idx}] id={ex_id!r}" if ex_id is not None else f"[ITEM {idx}]"
            safe_print(header)
            safe_print(f"  path:     {chosen.get('path')}")
            if chosen.get("schemaPath"):
                safe_print(f"  schema:   {chosen.get('schemaPath')}")
            safe_print(f"  message:  {chosen.get('message')}")
            safe_print(f"  expected: {chosen.get('expected')}")
            safe_print(f"  actual:   {chosen.get('actual')}")
            safe_print("")

    if invalid_count == 0:
        safe_print(f"OK: validated {args.file} ({len(data)} item(s))")
        return 0

    safe_print(f"FAIL: {invalid_count} item(s) invalid in {args.file} (showing up to {args.max_errors})")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
