#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_prompt_packs.py — 2-phase pipeline

Phase 1 (Validity Gate):
  - Generate JSON array
  - Clean/parse JSON
  - Enforce exact count
  - Validate schema + taskforms
  - Targeted repair using validator output until valid (bounded)
  - Write staging/.../exercises.raw.json
  - Promote to content/.../exercises.json

Phase 2 (Quality + Duplicate Gate):
  - Start from already-valid content/.../exercises.json (Phase 1 output)
  - Run quality_pack_checks.py (warnings-only) for the pack
  - Run hard_duplicate_gate.py (optional)
  - If warnings > limit or dup-gate fails -> targeted rewrite:
      * MUST preserve schema keys, count, meta fields
      * Only vary prompts/options/values/ids as needed
  - Re-validate after each rewrite (schema gate)
  - Re-check quality/dup gates (bounded)
  - Write staging/.../exercises.quality.json (optional)
  - Final write to content/.../exercises.json

Resumable:
  - State file tracks per-pack status per phase.
  - --resume continues; --force reruns.

Defaults:
  - Primary model:  gpt-4o-mini
  - Fallback model: gpt-4o

Requires:
  - OPENAI_API_KEY set
  - tools/new/validate_one_exercises_file.py
  - tools/new/quality_pack_checks.py (optional but recommended)
  - tools/new/hard_duplicate_gate.py (optional)
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import random
import re
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI

# ----------------------------
# Repo paths
# ----------------------------

PROMPTS_ROOT = os.path.join("prompts", "packs", "nl-NL")
CONTENT_ROOT = os.path.join("content", "nl-NL")

SCHEMA_PATH = os.path.join("content", "nl-NL", "_shared", "schemas", "ExerciseSchema.json")
TASKFORMS_PATH = os.path.join("docs", "new", "taskvormen-canon.json")

QUALITY_SCRIPT = os.path.join("tools", "new", "quality_pack_checks.py")

DUP_SCRIPT = os.path.join("tools", "new", "hard_duplicate_gate.py")
DUP_BASELINE = os.path.join("docs", "new", "duplicate_baseline.json")
DUP_OVERRIDES = os.path.join("docs", "new", "duplicate_gate_overrides.json")

STAGING_ROOT = os.path.join("staging", "nl-NL")
STATE_DIR = "state"
DEFAULT_STATE_PHASE1 = os.path.join(STATE_DIR, "phase1.state.json")
DEFAULT_STATE_PHASE2 = os.path.join(STATE_DIR, "phase2.state.json")

client = OpenAI()

# Robustly remove JSON fences
_JSON_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE | re.MULTILINE)


# ----------------------------
# File helpers
# ----------------------------

def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _atomic_write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def _atomic_write_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def _norm_slashes(p: str) -> str:
    return p.replace("\\", "/")


# ----------------------------
# Prompt pack discovery + meta
# ----------------------------

def find_prompt_packs() -> List[str]:
    paths: List[str] = []
    for root, _, files in os.walk(PROMPTS_ROOT):
        for fn in files:
            if fn.endswith(".txt"):
                paths.append(os.path.join(root, fn))
    return sorted(paths)


def extract_meta(prompt_text: str) -> Tuple[str, int, str, str]:
    """
    Extract domain/grade/level/topic from a prompt pack.

    Accepts:
      - domain: "verhoudingen"
      domain: "verhoudingen"
    """

    def grab(patterns: List[str], field: str) -> str:
        for pat in patterns:
            m = re.search(pat, prompt_text, flags=re.IGNORECASE)
            if m:
                return m.group(1).strip()
        raise ValueError(f"Missing field '{field}' in prompt pack")

    domain = grab([r'-\s*domain:\s*"([^"]+)"', r'\bdomain:\s*"([^"]+)"'], "domain")
    grade = int(grab([r'-\s*grade:\s*([0-9]+)', r'\bgrade:\s*([0-9]+)'], "grade"))
    level = grab([r'-\s*level:\s*"([^"]+)"', r'\blevel:\s*"([^"]+)"'], "level")
    topic = grab([r'-\s*topic:\s*"([^"]+)"', r'\btopic:\s*"([^"]+)"'], "topic")
    return domain, grade, level, topic


def output_path(domain: str, grade: int, level: str, topic: str) -> str:
    return os.path.join(
        CONTENT_ROOT,
        domain,
        f"groep-{grade}",
        level,
        "topics",
        topic,
        "exercises.json",
    )


def staging_raw_path(domain: str, grade: int, level: str, topic: str) -> str:
    return os.path.join(
        STAGING_ROOT,
        domain,
        f"groep-{grade}",
        level,
        "topics",
        topic,
        "exercises.raw.json",
    )


def staging_quality_path(domain: str, grade: int, level: str, topic: str) -> str:
    return os.path.join(
        STAGING_ROOT,
        domain,
        f"groep-{grade}",
        level,
        "topics",
        topic,
        "exercises.quality.json",
    )


def find_prompt_for_meta(domain: str, grade: int, level: str, topic: str) -> Optional[str]:
    """
    Useful in Phase 2 when user runs it without Phase 1 state.
    """
    for p in find_prompt_packs():
        try:
            txt = _read_text(p)
            d, g, l, t = extract_meta(txt)
            if (d, g, l, t) == (domain, grade, level, topic):
                return p
        except Exception:
            continue
    return None


# ----------------------------
# Model + JSON parsing
# ----------------------------

def clean_json_array(raw: str) -> List[Any]:
    s = raw.strip()
    s = _JSON_FENCE_RE.sub("", s).strip()

    # If model added chatter, try to extract the outermost JSON array
    start = s.find("[")
    end = s.rfind("]")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON array brackets found in model output")

    payload = s[start : end + 1]
    data = json.loads(payload)
    if not isinstance(data, list):
        raise ValueError("Parsed JSON is not an array")
    return data


def call_model(prompt_text: str, model: str, max_tokens: int, temperature: float) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict exercise generator.\n"
                    "Return ONLY the JSON array the user asks for.\n"
                    "No markdown. No explanations. No extra wrapper keys.\n"
                    "All required fields must be present and correctly placed.\n"
                ),
            },
            {"role": "user", "content": prompt_text},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content or ""


# ----------------------------
# Validation + external checks
# ----------------------------

def validate_exercises_file(path: str) -> Tuple[bool, str]:
    cmd = [
        "py",
        "-3.13",
        "tools/new/validate_one_exercises_file.py",
        path,
        "--schema",
        SCHEMA_PATH,
        "--taskforms",
        TASKFORMS_PATH,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    ok = (proc.returncode == 0)
    out = (proc.stdout or "") + (proc.stderr or "")
    return ok, out.strip()


def run_quality_checks_for_pack(content_root: str, out_file: str) -> Tuple[bool, List[str]]:
    """
    Runs quality_pack_checks.py (warnings-only).
    Returns warnings relevant to out_file (filtered).
    ok=True means script executed; warnings may exist.
    """
    if not os.path.exists(QUALITY_SCRIPT):
        return True, []

    cmd = ["py", "-3.13", QUALITY_SCRIPT, "--content-root", content_root]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")

    target = _norm_slashes(out_file)
    rel: List[str] = []
    for line in out.splitlines():
        if "WARN" not in line:
            continue
        if target in _norm_slashes(line):
            rel.append(line.strip())

    return True, rel


def run_duplicate_gate_for_pack(content_root: str, out_file: str) -> Tuple[bool, List[str]]:
    """
    Runs hard_duplicate_gate.py and returns relevant lines.
    Returncode != 0 means gate failed for at least one pack; we filter to our pack.
    """
    if not os.path.exists(DUP_SCRIPT):
        return True, []

    cmd = [
        "py",
        "-3.13",
        DUP_SCRIPT,
        "--content-root",
        content_root,
        "--baseline",
        DUP_BASELINE,
        "--overrides",
        DUP_OVERRIDES,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")

    rel: List[str] = []
    target_norm = _norm_slashes(out_file)
    for line in out.splitlines():
        if target_norm in _norm_slashes(line):
            rel.append(line.strip())

    # If the whole gate failed but pack didn't show lines (rare), add summary line
    summary = ""
    for line in out.splitlines()[::-1]:
        if "HARD DUPLICATE GATE" in line:
            summary = line.strip()
            break
    if summary and (not rel):
        rel.append(summary)

    ok = (proc.returncode == 0)
    return ok, rel


# ----------------------------
# Targeted prompts
# ----------------------------

def build_phase1_repair_prompt(original_prompt: str, issues: str, last_output_snippet: str, required_count: int) -> str:
    snippet = (last_output_snippet or "").strip()
    if len(snippet) > 2500:
        snippet = snippet[:2500] + "\n...<truncated>..."

    return f"""
You previously generated an INVALID exercise JSON array.

ORIGINAL PROMPT PACK (do not change requirements):
----------------
{original_prompt}
----------------

VALIDATION ISSUES (must be fixed):
----------------
{issues}
----------------

SNIPPET OF LAST OUTPUT (for debugging; do not copy blindly):
----------------
{snippet}
----------------

YOUR TASK:
- Regenerate the FULL output as ONE JSON ARRAY with EXACTLY {required_count} exercises.
- Every item MUST include ALL required fields in the correct place.
- Follow ALL requirements from the original prompt pack.
- Output MUST start with [ and end with ] and contain ONLY JSON. No markdown.

GENERATE NOW.
""".strip()


def build_phase2_rewrite_prompt(
    original_prompt: str,
    current_json: List[Any],
    issues: str,
    required_count: int,
) -> str:
    # keep small snippet of the current JSON to anchor structure without bloating tokens
    snippet_obj = current_json[:2] if isinstance(current_json, list) else []
    snippet = json.dumps(snippet_obj, ensure_ascii=False, indent=2)
    if len(snippet) > 2500:
        snippet = snippet[:2500] + "\n...<truncated>..."

    return f"""
You are improving an already-VALID exercises.json pack.

ORIGINAL PROMPT PACK (requirements are binding):
----------------
{original_prompt}
----------------

CURRENT PROBLEMS TO FIX (quality/duplicates):
----------------
{issues}
----------------

STRUCTURE ANCHOR (example items; keep this structure):
----------------
{snippet}
----------------

HARD RULES (do not violate):
- Output MUST be a single JSON ARRAY of EXACTLY {required_count} exercises.
- Each exercise MUST remain schema-valid and include ALL required fields in correct places.
- Keep domain/grade/level/topic aligned to the prompt pack for EVERY item.
- Do NOT remove metadata/feedback/interaction/solution fields.
- You MAY change: prompt text, options, solution values/index, ids, and metadata.strategy/misconceptKeys to reduce duplicates/warnings
  (but keep metadata.taskForm correct).
- Ensure options sets are not repeated and prompts are varied.
- Output MUST start with [ and end with ] and contain ONLY JSON. No markdown.

REWRITE NOW.
""".strip()


# ----------------------------
# Core generation + write
# ----------------------------

def try_generate_and_write_json(prompt_text: str, out_path: str, model: str, max_tokens: int, temperature: float, required_count: int) -> Tuple[List[Any], str]:
    raw = call_model(prompt_text, model=model, max_tokens=max_tokens, temperature=temperature)
    data = clean_json_array(raw)

    if len(data) != required_count:
        raise ValueError(f"Wrong item count: got {len(data)}, expected {required_count}")

    _atomic_write_json(out_path, data)
    return data, raw


# ----------------------------
# Phase 1: validity gate
# ----------------------------

def run_phase1_for_pack(
    prompt_path: str,
    prompt_text: str,
    domain: str,
    grade: int,
    level: str,
    topic: str,
    required_count: int,
    model_primary: str,
    model_fallback: str,
    max_tokens: int,
    temperature: float,
    max_repairs: int,
) -> Tuple[bool, str]:
    out_content = output_path(domain, grade, level, topic)
    out_staging = staging_raw_path(domain, grade, level, topic)

    models = [model_primary, model_fallback]
    last_issue = ""
    last_raw = ""

    for model in models:
        # 1) initial attempt
        try:
            data, raw = try_generate_and_write_json(
                prompt_text=prompt_text,
                out_path=out_staging,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                required_count=required_count,
            )
            last_raw = raw

            ok, msg = validate_exercises_file(out_staging)
            if ok:
                # promote to content
                _atomic_write_json(out_content, data)
                return True, f"PHASE1 OK (model={model}) -> promoted to {out_content}"
            last_issue = "VALIDATION FAIL:\n" + msg

        except Exception as e:
            last_issue = f"GENERATION/PARSE FAIL: {e}"
            last_raw = ""

        # 2) targeted repairs
        issues = last_issue or "Unknown issue"
        snippet = last_raw or ""

        for r in range(max_repairs):
            repair_prompt = build_phase1_repair_prompt(
                original_prompt=prompt_text,
                issues=issues,
                last_output_snippet=snippet,
                required_count=required_count,
            )
            try:
                data, raw = try_generate_and_write_json(
                    prompt_text=repair_prompt,
                    out_path=out_staging,
                    model=model,
                    max_tokens=max_tokens,
                    temperature=max(0.0, temperature - 0.05),
                    required_count=required_count,
                )
                snippet = raw

                ok, msg = validate_exercises_file(out_staging)
                if ok:
                    _atomic_write_json(out_content, data)
                    return True, f"PHASE1 OK after repair {r+1} (model={model}) -> promoted to {out_content}"

                issues = "VALIDATION FAIL:\n" + msg

            except Exception as e:
                issues = f"REPAIR FAIL: {e}"
                snippet = ""

    return False, last_issue or "Phase 1 failed across models/repairs"


# ----------------------------
# Phase 2: quality + duplicates gate
# ----------------------------

def run_phase2_for_pack(
    prompt_text: str,
    domain: str,
    grade: int,
    level: str,
    topic: str,
    required_count: int,
    model_primary: str,
    model_fallback: str,
    max_tokens: int,
    temperature: float,
    max_repairs: int,
    check_quality: bool,
    quality_warn_limit: int,
    check_duplicates: bool,
    write_quality_staging: bool,
) -> Tuple[bool, str]:
    out_content = output_path(domain, grade, level, topic)
    out_quality = staging_quality_path(domain, grade, level, topic)

    if not os.path.exists(out_content):
        return False, f"PHASE2 cannot run: missing valid Phase1 output {out_content}"

    # Load current valid JSON
    try:
        current = json.loads(_read_text(out_content))
        if not isinstance(current, list):
            return False, "PHASE2: content exercises.json is not an array"
        if len(current) != required_count:
            return False, f"PHASE2: content has {len(current)} items, expected {required_count}"
    except Exception as e:
        return False, f"PHASE2: failed to read/parse content JSON: {e}"

    def check_gates() -> Tuple[bool, str]:
        issues_parts: List[str] = []

        if check_duplicates:
            d_ok, d_lines = run_duplicate_gate_for_pack(CONTENT_ROOT, out_content)
            if not d_ok:
                issues_parts.append("DUPLICATE GATE FAIL:\n" + ("\n".join(d_lines) if d_lines else "<no relevant lines>"))

        if check_quality:
            _, q_lines = run_quality_checks_for_pack(CONTENT_ROOT, out_content)
            if len(q_lines) > quality_warn_limit:
                issues_parts.append(
                    f"QUALITY WARNINGS too many: {len(q_lines)} > {quality_warn_limit}\n" +
                    "\n".join(q_lines[:50])
                )

        if issues_parts:
            return False, "\n\n".join(issues_parts)

        return True, "PHASE2 gates OK"

    # First check on current content
    ok, gate_msg = check_gates()
    if ok:
        return True, f"PHASE2 OK (no rewrite needed) ({gate_msg})"

    last_issue = gate_msg

    # Rewrite loop (bounded), switching models if needed
    for model in [model_primary, model_fallback]:
        for r in range(max_repairs):
            # reload content each time (because previous loop may have updated it)
            try:
                current = json.loads(_read_text(out_content))
                if not isinstance(current, list) or len(current) != required_count:
                    return False, "PHASE2: content changed into invalid shape before rewrite"
            except Exception as e:
                return False, f"PHASE2: cannot reload content: {e}"

            rewrite_prompt = build_phase2_rewrite_prompt(
                original_prompt=prompt_text,
                current_json=current,
                issues=last_issue,
                required_count=required_count,
            )

            try:
                new_data, _ = try_generate_and_write_json(
                    prompt_text=rewrite_prompt,
                    out_path=out_quality if write_quality_staging else out_content,
                    model=model,
                    max_tokens=max_tokens,
                    temperature=max(0.0, temperature - 0.05),
                    required_count=required_count,
                )
            except Exception as e:
                last_issue = f"PHASE2 rewrite generation failed: {e}"
                continue

            # Validate rewrite output before promoting to content
            check_path = out_quality if write_quality_staging else out_content
            v_ok, v_msg = validate_exercises_file(check_path)
            if not v_ok:
                last_issue = "PHASE2 rewrite validation failed:\n" + v_msg
                continue

            # Promote rewritten pack to content if it was staged
            if write_quality_staging:
                _atomic_write_json(out_content, new_data)

            # Re-check gates
            ok2, gate_msg2 = check_gates()
            if ok2:
                return True, f"PHASE2 OK after rewrite {r+1} (model={model})"
            last_issue = gate_msg2

    return False, f"PHASE2 failed after rewrites. Last issues:\n{last_issue}"


# ----------------------------
# Resumable state
# ----------------------------

@dataclasses.dataclass
class PackState:
    prompt_path: str
    phase: int
    status: str = "pending"  # pending|ok|fail
    out_file: str = ""
    staging_file: str = ""
    attempts: int = 0
    model_info: str = ""
    last_error: str = ""
    updated_at: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PackState":
        return PackState(**d)


def load_state(state_path: str) -> Dict[str, PackState]:
    if not os.path.exists(state_path):
        return {}
    try:
        raw = json.loads(_read_text(state_path))
        if not isinstance(raw, dict):
            return {}
        out: Dict[str, PackState] = {}
        for k, v in raw.items():
            if isinstance(v, dict):
                out[k] = PackState.from_dict(v)
        return out
    except Exception:
        return {}


def save_state(state_path: str, state: Dict[str, PackState]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(state_path)) or ".", exist_ok=True)
    payload = {k: v.to_dict() for k, v in state.items()}
    _atomic_write_json(state_path, payload)


# ----------------------------
# Main runner
# ----------------------------

def run(
    phase: int,
    selected_prompts: Optional[List[str]],
    model_primary: str,
    model_fallback: str,
    max_tokens: int,
    temperature: float,
    required_count: int,
    max_repairs: int,
    resume: bool,
    force: bool,
    state_path: str,
    check_duplicates: bool,
    check_quality: bool,
    quality_warn_limit: int,
    sleep_s: float,
    shuffle: bool,
    write_quality_staging: bool,
) -> None:
    prompts = selected_prompts if selected_prompts else find_prompt_packs()
    prompts = [os.path.normpath(p) for p in prompts]
    if shuffle:
        random.shuffle(prompts)

    state = load_state(state_path) if resume else {}
    if resume:
        print(f"[resume] Loaded {len(state)} pack(s) from {state_path}")

    print(f"PHASE {phase} — Found {len(prompts)} prompt pack(s).")
    failures: List[str] = []

    for i, p in enumerate(prompts, 1):
        rel = os.path.relpath(p)
        prompt_text = _read_text(p)

        try:
            domain, grade, level, topic = extract_meta(prompt_text)
        except Exception as e:
            print(f"[{i}/{len(prompts)}] {rel}")
            print(f"  -> ERROR(meta): {e}")
            failures.append(f"{rel} (meta)")
            continue

        out_content = output_path(domain, grade, level, topic)
        out_staging = staging_raw_path(domain, grade, level, topic)

        key = os.path.abspath(p) + f"::phase{phase}"
        ps = state.get(key) or PackState(prompt_path=os.path.abspath(p), phase=phase)
        ps.out_file = out_content
        ps.staging_file = out_staging
        ps.updated_at = time.time()

        if not force and ps.status == "ok":
            print(f"[{i}/{len(prompts)}] {rel}")
            print(f"  -> SKIP (already ok in state) -> {out_content}")
            continue

        print(f"[{i}/{len(prompts)}] {rel}")
        ps.status = "pending"
        save_state(state_path, {**state, key: ps})

        try:
            if phase == 1:
                ok, msg = run_phase1_for_pack(
                    prompt_path=p,
                    prompt_text=prompt_text,
                    domain=domain,
                    grade=grade,
                    level=level,
                    topic=topic,
                    required_count=required_count,
                    model_primary=model_primary,
                    model_fallback=model_fallback,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    max_repairs=max_repairs,
                )
            else:
                # Phase 2: ensure we still have the exact prompt text requirements
                ok, msg = run_phase2_for_pack(
                    prompt_text=prompt_text,
                    domain=domain,
                    grade=grade,
                    level=level,
                    topic=topic,
                    required_count=required_count,
                    model_primary=model_primary,
                    model_fallback=model_fallback,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    max_repairs=max_repairs,
                    check_quality=check_quality,
                    quality_warn_limit=quality_warn_limit,
                    check_duplicates=check_duplicates,
                    write_quality_staging=write_quality_staging,
                )

            ps.attempts += 1
            ps.updated_at = time.time()

            if ok:
                ps.status = "ok"
                ps.last_error = ""
                ps.model_info = msg
                print(f"  -> OK: {msg}")
            else:
                ps.status = "fail"
                ps.last_error = msg
                failures.append(out_content)
                print(f"  -> FAIL: {msg}")

        except Exception as e:
            ps.attempts += 1
            ps.status = "fail"
            ps.last_error = str(e)
            ps.updated_at = time.time()
            failures.append(out_content)
            print(f"  -> ERROR: {e}")

        state[key] = ps
        save_state(state_path, state)

        if sleep_s > 0:
            time.sleep(sleep_s)

    if failures:
        print("\nFailed packs:")
        for f in failures:
            print(f"- {f}")
        print(f"\nState saved to: {state_path}")
        sys.exit(1)

    print(f"\nAll done. State saved to: {state_path}")
    sys.exit(0)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()

    ap.add_argument("--phase", type=int, choices=[1, 2], default=1, help="Pipeline phase: 1=validity, 2=quality+duplicates")

    ap.add_argument(
        "--prompt",
        action="append",
        help="Specific prompt file(s) to run. Can be repeated. Default: all under prompts/packs/nl-NL.",
    )

    ap.add_argument("--model", default="gpt-4o-mini", help="Primary model (default: gpt-4o-mini).")
    ap.add_argument("--fallback", default="gpt-4o", help="Fallback model (default: gpt-4o).")

    ap.add_argument("--max-tokens", type=int, default=14000, help="max_tokens for completion.")
    ap.add_argument("--temperature", type=float, default=0.25, help="Sampling temperature.")
    ap.add_argument("--count", type=int, default=50, help="Required number of exercises per pack.")
    ap.add_argument("--max-repairs", type=int, default=3, help="Max targeted repair loops per model.")

    ap.add_argument("--resume", action="store_true", help="Resume using the state file.")
    ap.add_argument("--force", action="store_true", help="Force rerun even if already OK in state.")
    ap.add_argument("--shuffle", action="store_true", help="Shuffle processing order.")
    ap.add_argument("--sleep", type=float, default=0.35, help="Sleep seconds between packs (rate-limit buffer).")

    ap.add_argument(
        "--state",
        default=None,
        help="State file path. Default depends on --phase (state/phase1.state.json or state/phase2.state.json).",
    )

    # Phase 2 gates (can be enabled in Phase 1 too, but recommended only in Phase 2)
    ap.add_argument("--check-duplicates", action="store_true", help="Run hard_duplicate_gate.py and enforce pass in phase 2.")
    ap.add_argument("--check-quality", action="store_true", help="Run quality_pack_checks.py and enforce warn limit in phase 2.")
    ap.add_argument("--quality-warn-limit", type=int, default=0, help="Max allowed warnings for this pack (default 0).")

    ap.add_argument(
        "--write-quality-staging",
        action="store_true",
        help="If set, phase 2 writes rewrite output to staging/.../exercises.quality.json first, then promotes to content.",
    )

    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # default state per phase if not provided
    if args.state:
        state_path = args.state
    else:
        state_path = DEFAULT_STATE_PHASE1 if args.phase == 1 else DEFAULT_STATE_PHASE2

    run(
        phase=args.phase,
        selected_prompts=args.prompt,
        model_primary=args.model,
        model_fallback=args.fallback,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        required_count=args.count,
        max_repairs=args.max_repairs,
        resume=args.resume,
        force=args.force,
        state_path=state_path,
        check_duplicates=args.check_duplicates,
        check_quality=args.check_quality,
        quality_warn_limit=args.quality_warn_limit,
        sleep_s=args.sleep,
        shuffle=args.shuffle,
        write_quality_staging=args.write_quality_staging,
    )
