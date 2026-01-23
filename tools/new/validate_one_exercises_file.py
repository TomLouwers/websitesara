#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from jsonschema import Draft202012Validator


# -----------------------------
# Helpers
# -----------------------------

@dataclass
class Issue:
    kind: str   # "ERROR" or "WARN"
    code: str   # e.g. "CONTENT-FAIL"
    message: str

def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _load_schema(schema_path: str) -> Draft202012Validator:
    schema = _read_json(schema_path)
    return Draft202012Validator(schema)

def _load_taskforms(taskforms_path: str) -> Dict[str, Any]:
    """
    Expected format like:
    {
      "levels": {
        "n2": {"allowedTaskForms":[...], "disallowedTaskForms":[...]},
        ...
      },
      "taskFormDefinitions": {...}
    }
    """
    return _read_json(taskforms_path)

def _format_schema_error(e) -> str:
    loc = "/".join([str(p) for p in e.absolute_path]) if e.absolute_path else "(root)"
    return f"{loc}: {e.message}"

def _is_explain_what_happens(taskform: str) -> bool:
    return taskform == "explain_what_happens"

def _normalize_text(s: str) -> str:
    return (s or "").lower()

def _path_guess_topic_and_level(file_path: str) -> Tuple[str, str]:
    """
    Best-effort: extract topic slug and level folder from content/... path.
    Example:
      content/nl-NL/verhoudingen/groep-5/n2/topics/breuken-vergelijken/exercises.json
    """
    parts = file_path.replace("\\", "/").split("/")
    topic = ""
    level = ""
    for i, p in enumerate(parts):
        if p in ("n1", "n2", "n3", "n4"):
            level = p
        if p == "topics" and i + 1 < len(parts):
            topic = parts[i + 1]
    return topic, level


# -----------------------------
# NEW: Content rules
# -----------------------------

FORBIDDEN_BY_LEVEL = {
    "n2": ["waarom", "leg uit", "verklaar", "beargumenteer", "onderbouw"],
}

FORBIDDEN_BY_TASKFORM_WARN = {
    # Warnings: stylistic guidance (not always fatal)
    "explain_what_happens": ["strategie", "handig", "handiger", "makkelijker"],
}

HINT_LEAK_FATAL_EXPLAIN = [
    # Fatal in explain_what_happens: it gives away the answer
    "afronden",
    "splitsen",
    "aanvullen",
    "compens",
]

def run_content_rules(ex: Dict[str, Any], file_path: str) -> List[Issue]:
    issues: List[Issue] = []

    level = ex.get("level") or ""
    topic = ex.get("topic") or ""
    taskform = (ex.get("metadata") or {}).get("taskForm") or ""
    prompt = _normalize_text(ex.get("prompt") or "")
    interaction_type = ((ex.get("interaction") or {}).get("type")) or ""
    solution = ex.get("solution") or {}

    # ---- Rule A: forbidden phrases in n2 prompts (FAIL)
    if level in FORBIDDEN_BY_LEVEL:
        for phrase in FORBIDDEN_BY_LEVEL[level]:
            if phrase in prompt:
                issues.append(Issue(
                    kind="ERROR",
                    code="CONTENT-FAIL",
                    message=f"Forbidden phrase '{phrase}' in n2 prompt."
                ))

    # ---- Rule B: explain_what_happens hint leakage (FAIL)
    if _is_explain_what_happens(taskform):
        for phrase in HINT_LEAK_FATAL_EXPLAIN:
            if phrase in prompt:
                issues.append(Issue(
                    kind="ERROR",
                    code="CONTENT-FAIL",
                    message=f"Hint leakage in explain_what_happens: prompt contains '{phrase}'."
                ))
        # Soft warnings too
        for phrase in FORBIDDEN_BY_TASKFORM_WARN.get(taskform, []):
            if phrase in prompt:
                issues.append(Issue(
                    kind="WARN",
                    code="CONTENT-WARN",
                    message=f"Discouraged word in explain_what_happens prompt: '{phrase}'."
                ))

    # ---- Rule C: numeric interaction must not have non-numeric string answers
    # (You previously had 'evenveel' with numeric. We'll enforce.)
    if interaction_type == "numeric":
        v = solution.get("value")
        if isinstance(v, str):
            # allow numeric strings like "7 rest 2" or "12" or "3,5"
            # - if it contains letters other than 'rest' => fail
            vv = v.strip().lower()
            if "rest" in vv:
                # ok (handled below for specific topics as well)
                pass
            else:
                # numeric string should be parseable-ish; if alpha present -> fail
                has_alpha = any(ch.isalpha() for ch in vv)
                if has_alpha:
                    issues.append(Issue(
                        kind="ERROR",
                        code="CONTENT-FAIL",
                        message=f"numeric interaction has non-numeric string solution.value: '{v}'."
                    ))

    # ---- Rule D: topic-specific: delen-met-rest format
    # Your n2 pack used solution.value string "q rest r". Enforce for this topic.
    if topic == "delen-met-rest":
        v = solution.get("value")
        if not isinstance(v, str):
            issues.append(Issue(
                kind="ERROR",
                code="CONTENT-FAIL",
                message="delen-met-rest requires solution.value as string 'q rest r'."
            ))
        else:
            vv = v.strip().lower()
            if " rest " not in vv:
                issues.append(Issue(
                    kind="ERROR",
                    code="CONTENT-FAIL",
                    message=f"delen-met-rest requires format '<q> rest <r>', got '{v}'."
                ))

    # ---- Rule E: percentages-herkennen-in-context should not be numeric
    if topic == "percentages-herkennen-in-context":
        if interaction_type == "numeric":
            issues.append(Issue(
                kind="ERROR",
                code="CONTENT-FAIL",
                message="percentages-herkennen-in-context must not use numeric interaction (use mcq/select_single)."
            ))

    return issues


# -----------------------------
# Taskform canon checks
# -----------------------------

def validate_taskform_allowed(ex: Dict[str, Any], taskforms_canon: Dict[str, Any]) -> List[Issue]:
    issues: List[Issue] = []
    level = ex.get("level")
    taskform = (ex.get("metadata") or {}).get("taskForm")

    levels = (taskforms_canon or {}).get("levels") or {}
    if level not in levels:
        issues.append(Issue("ERROR", "TASKFORM-FAIL", f"Unknown level '{level}' in taskforms canon."))
        return issues

    allowed = set(levels[level].get("allowedTaskForms") or [])
    disallowed = set(levels[level].get("disallowedTaskForms") or [])

    if taskform in disallowed:
        issues.append(Issue("ERROR", "TASKFORM-FAIL", f"taskForm '{taskform}' is disallowed for level '{level}'."))

    if allowed and taskform not in allowed:
        issues.append(Issue("ERROR", "TASKFORM-FAIL", f"taskForm '{taskform}' not in allowedTaskForms for level '{level}'."))

    return issues


# -----------------------------
# Main validation
# -----------------------------

def validate_one_file(exercises_path: str, schema_path: str, taskforms_path: str) -> Tuple[bool, List[Issue]]:
    issues: List[Issue] = []

    # parse JSON file
    try:
        data = _read_json(exercises_path)
    except Exception as e:
        issues.append(Issue("ERROR", "PARSE-FAIL", f"JSON parse error: {e}"))
        return False, issues

    # schema validation (file expected to be an array)
    validator = _load_schema(schema_path)
    schema_errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    for e in schema_errors:
        issues.append(Issue("ERROR", "SCHEMA-FAIL", _format_schema_error(e)))

    if any(i.kind == "ERROR" and i.code == "SCHEMA-FAIL" for i in issues):
        return False, issues

    taskforms_canon = _load_taskforms(taskforms_path)

    # per-exercise checks
    if not isinstance(data, list):
        issues.append(Issue("ERROR", "SCHEMA-FAIL", "Top-level JSON must be an array of exercises."))
        return False, issues

    for idx, ex in enumerate(data):
        if not isinstance(ex, dict):
            issues.append(Issue("ERROR", "SCHEMA-FAIL", f"Item[{idx}] is not an object."))
            continue

        # taskForm canon gate
        issues.extend(validate_taskform_allowed(ex, taskforms_canon))

        # NEW: content rules
        issues.extend(run_content_rules(ex, exercises_path))

    ok = not any(i.kind == "ERROR" for i in issues)
    return ok, issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exercises_json", help="Path to exercises.json")
    ap.add_argument("--schema", required=True, help="Path to ExerciseSchema.json")
    ap.add_argument("--taskforms", required=True, help="Path to taskvormen-canon.json")
    args = ap.parse_args()

    ok, issues = validate_one_file(args.exercises_json, args.schema, args.taskforms)

    if ok:
        print("Result: ✅ OK.")
        # still print warnings (if any)
        warns = [i for i in issues if i.kind == "WARN"]
        if warns:
            for w in warns:
                print(f"[{args.exercises_json}] [{w.code}] {w.message}")
        sys.exit(0)

    # Print all issues
    for i in issues:
        print(f"[{args.exercises_json}] [{i.code}] {i.message}")

    # Summary
    err_count = sum(1 for i in issues if i.kind == "ERROR")
    warn_count = sum(1 for i in issues if i.kind == "WARN")
    print(f"Result: ❌ FAIL — {err_count} error(s), {warn_count} warning(s).")
    sys.exit(1)


if __name__ == "__main__":
    main()
