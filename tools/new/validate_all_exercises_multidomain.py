#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_all_exercises_multidomain.py

Validate all exercises.json files under a content root:
- JSON Schema validation (Draft 2020-12)
- taskForm validation against taskvormen-canon.json (best-effort)
- Print ONE diff-style error per invalid item (not a wall)
- Summaries per pack + overall

Exit codes:
  0 = OK
  1 = one or more packs invalid
  2 = CLI/IO/parse error
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import best_match
except Exception as e:
    print("ERROR: jsonschema package missing or incompatible:", e)
    sys.exit(2)


# ----------------------------
# Console-safe printing
# ----------------------------

def safe_print(s: str = "") -> None:
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("utf-8", errors="replace").decode("utf-8"))


# ----------------------------
# IO helpers
# ----------------------------

def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def norm_slashes(p: str) -> str:
    return p.replace("\\", "/")


def rel_to(root: str, path: str) -> str:
    try:
        return norm_slashes(os.path.relpath(path, root))
    except Exception:
        return norm_slashes(path)


# ----------------------------
# JSON pointer helpers
# ----------------------------

def join_json_pointer(parts: List[str]) -> str:
    if not parts:
        return "/"
    esc: List[str] = []
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

    all_out = all_taskforms if all_taskforms else None
    by_level_out = by_level if by_level else None
    return all_out, by_level_out


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
# Schema error selection
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


def schema_error_for_item(item_validator: Draft202012Validator, item: Any) -> Optional[Dict[str, Any]]:
    errors = list(item_validator.iter_errors(item))
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
# Pack validation
# ----------------------------

def validate_pack(
    pack_path: str,
    content_root: str,
    item_validator: Draft202012Validator,
    all_taskforms: Optional[set],
    by_level: Optional[Dict[str, set]],
    max_items: int,
) -> Tuple[bool, int, List[Dict[str, Any]], Counter]:
    """
    Returns:
      ok: bool
      total_items: int
      item_errors: list of {index, id?, ...diff...} (max 1 per invalid item)
      causes: Counter of message keys (for summary)
    """
    try:
        data = read_json(pack_path)
    except Exception as e:
        err = {
            "index": None,
            "id": None,
            "path": "/",
            "message": f"parse error: {e}",
            "expected": "valid JSON",
            "actual": "unparseable",
        }
        c = Counter()
        c["parse error"] += 1
        return False, 0, [err], c

    if not isinstance(data, list):
        err = {
            "index": None,
            "id": None,
            "path": "/",
            "message": "root must be a JSON array",
            "expected": "array",
            "actual": type(data).__name__,
        }
        c = Counter()
        c["root not array"] += 1
        return False, 0, [err], c

    total = len(data)
    item_errors: List[Dict[str, Any]] = []
    causes = Counter()

    scan_n = min(total, max_items)

    for idx in range(scan_n):
        ex = data[idx]
        ex_id = ex.get("id") if isinstance(ex, dict) else None

        schema_err = schema_error_for_item(item_validator, ex)

        tf_err = None
        if isinstance(ex, dict):
            tf_err = taskform_error(ex, all_taskforms, by_level)

        chosen = schema_err or tf_err
        if chosen:
            causes[chosen.get("message", "unknown")] += 1
            item_errors.append(
                {
                    "index": idx,
                    "id": ex_id,
                    **chosen,
                }
            )

    ok = len(item_errors) == 0
    return ok, total, item_errors, causes


# ----------------------------
# File discovery
# ----------------------------

def find_exercises_json_files(content_root: str) -> List[str]:
    out: List[str] = []
    for root, _, files in os.walk(content_root):
        if "exercises.json" in files:
            out.append(os.path.join(root, "exercises.json"))
    return sorted(out)


# ----------------------------
# CLI / main
# ----------------------------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--content-root", required=True, help="Root folder that contains nl-NL/.../exercises.json")
    ap.add_argument("--schema", required=True, help="Path to ExerciseSchema.json")
    ap.add_argument("--taskforms", required=True, help="Path to taskvormen-canon.json")

    ap.add_argument("--max-items-per-pack", type=int, default=100000, help="Max items to scan per pack (default all)")
    ap.add_argument("--max-errors-total", type=int, default=500, help="Stop printing after this many item errors total")
    ap.add_argument("--max-packs", type=int, default=0, help="0=all packs, else limit number of packs scanned")
    ap.add_argument("--fail-fast", action="store_true", help="Stop on first invalid pack")

    ap.add_argument("--quiet", action="store_true", help="Only print summaries (no per-item diffs)")
    return ap.parse_args()


def main() -> int:
    args = parse_args()

    if not os.path.exists(args.content_root):
        safe_print(f"ERROR: content-root not found: {args.content_root}")
        return 2
    if not os.path.exists(args.schema):
        safe_print(f"ERROR: schema not found: {args.schema}")
        return 2
    if not os.path.exists(args.taskforms):
        safe_print(f"ERROR: taskforms not found: {args.taskforms}")
        return 2

    try:
        schema = read_json(args.schema)
    except Exception as e:
        safe_print(f"ERROR: cannot parse schema: {args.schema}\n  {e}")
        return 2

    item_schema = schema.get("items")
    if not isinstance(item_schema, dict):
        safe_print("ERROR: schema.items missing or not an object")
        return 2

    try:
        item_validator = Draft202012Validator(item_schema, schema=schema)
    except Exception:
        item_validator = Draft202012Validator(schema)

    # Load canon (best-effort)
    try:
        canon = read_json(args.taskforms)
        all_taskforms, by_level = extract_taskforms_from_canon(canon)
    except Exception:
        all_taskforms, by_level = None, None

    packs = find_exercises_json_files(args.content_root)
    if args.max_packs and args.max_packs > 0:
        packs = packs[: args.max_packs]

    safe_print(f"Scanning {len(packs)} pack(s) under {args.content_root} ...")

    total_packs = 0
    ok_packs = 0
    bad_packs = 0
    total_items = 0
    total_item_errors = 0

    global_causes = Counter()

    for pack_path in packs:
        total_packs += 1
        rel_pack = rel_to(args.content_root, pack_path)

        ok, n_items, item_errors, causes = validate_pack(
            pack_path=pack_path,
            content_root=args.content_root,
            item_validator=item_validator,
            all_taskforms=all_taskforms,
            by_level=by_level,
            max_items=args.max_items_per_pack,
        )

        total_items += n_items
        global_causes.update(causes)

        if ok:
            ok_packs += 1
            safe_print(f"Result: ✅ OK — validated {n_items} items. {rel_pack}")
            continue

        bad_packs += 1
        safe_print(f"Result: ❌ FAIL — {len(item_errors)}/{min(n_items, args.max_items_per_pack)} item(s) invalid. {rel_pack}")

        if not args.quiet:
            for err in item_errors:
                if total_item_errors >= args.max_errors_total:
                    safe_print(f"... stopped printing after --max-errors-total={args.max_errors_total}")
                    break

                idx = err.get("index")
                ex_id = err.get("id")
                safe_print(f"  [ITEM {idx}] id={ex_id!r}" if idx is not None else "  [ITEM ?]")
                safe_print(f"    path:     {err.get('path')}")
                if err.get("schemaPath"):
                    safe_print(f"    schema:   {err.get('schemaPath')}")
                safe_print(f"    message:  {err.get('message')}")
                safe_print(f"    expected: {err.get('expected')}")
                safe_print(f"    actual:   {err.get('actual')}")
                safe_print("")
                total_item_errors += 1

        if args.fail_fast:
            safe_print("Fail-fast enabled: stopping on first invalid pack.")
            break

    safe_print("")

    safe_print("=== VALIDATION SUMMARY ===")
    safe_print(f"Packs: {total_packs} total — {ok_packs} OK, {bad_packs} FAIL")
    safe_print(f"Items: {total_items} total")
    if bad_packs > 0:
        safe_print("Top causes (by message):")
        for msg, cnt in global_causes.most_common(10):
            safe_print(f"- {cnt}× {msg}")

    return 0 if bad_packs == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
