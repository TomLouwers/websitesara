#!/usr/bin/env python3
"""
Batch-run prompt packs under prompts/packs/nl-NL and write the generated
exercise JSON arrays into the matching content/nl-NL/.../exercises.json files.

Relies on OPENAI_API_KEY being set. Uses gpt-4o-mini by default; falls back to
gpt-4o when parsing or validation fails.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI


PROMPTS_ROOT = os.path.join("prompts", "packs", "nl-NL")
CONTENT_ROOT = os.path.join("content", "nl-NL")
SCHEMA_PATH = os.path.join("content", "nl-NL", "_shared", "schemas", "ExerciseSchema.json")
TASKFORMS_PATH = os.path.join("docs", "new", "taskvormen-canon.json")

client = OpenAI()


def find_prompts() -> List[str]:
    paths: List[str] = []
    for root, _, files in os.walk(PROMPTS_ROOT):
        for fn in files:
            if fn.endswith(".txt"):
                paths.append(os.path.join(root, fn))
    return sorted(paths)


def extract_meta(text: str) -> Tuple[str, int, str, str]:
    """
    Extract domain/grade/level/topic from a prompt pack.

    Accepts lines with or without leading dash/bullet, e.g.:
      - domain: "verhoudingen"
      domain: "verhoudingen"
    """

    def _grab(patterns: List[str], field: str) -> str:
        for pat in patterns:
            m = re.search(pat, text, flags=re.IGNORECASE)
            if m:
                return m.group(1).strip()
        raise ValueError(f"Missing field '{field}' (patterns tried: {patterns})")

    domain = _grab(
        [r'-\s*domain:\s*"([^"]+)"', r'\bdomain:\s*"([^"]+)"'],
        "domain",
    )
    grade = int(
        _grab([r'-\s*grade:\s*([0-9]+)', r'\bgrade:\s*([0-9]+)'], "grade")
    )
    level = _grab(
        [r'-\s*level:\s*"([^"]+)"', r'\blevel:\s*"([^"]+)"'],
        "level",
    )
    topic = _grab(
        [r'-\s*topic:\s*"([^"]+)"', r'\btopic:\s*"([^"]+)"'],
        "topic",
    )
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


def clean_json(raw: str) -> List[Any]:
    s = raw.strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?", "", s, flags=re.IGNORECASE).strip()
        s = re.sub(r"```$", "", s).strip()
    start = s.find("[")
    end = s.rfind("]")
    if start != -1 and end != -1 and end > start:
        s = s[start : end + 1]
    return json.loads(s)


def write_json(path: str, data: List[Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def call_model(prompt_text: str, model: str, max_tokens: int) -> Tuple[str, Optional[str]]:
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a strict exercise generator. Return only the JSON array the user asks for. No markdown.",
            },
            {"role": "user", "content": prompt_text},
        ],
        max_tokens=max_tokens,
        temperature=0.25,
    )
    choice = resp.choices[0]
    return choice.message.content or "", getattr(choice, "finish_reason", None)


def validate_file(path: str) -> Tuple[bool, str]:
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
    ok = proc.returncode == 0
    output = (proc.stdout or "") + (proc.stderr or "")
    return ok, output


def generate_for_prompt(
    prompt_path: str,
    model_primary: str,
    model_fallback: str,
    max_tokens: int,
    required_count: int = 50,
) -> Tuple[List[Any], str]:
    prompt_text = open(prompt_path, "r", encoding="utf-8").read()
    models = [model_primary, model_fallback]
    errors: List[str] = []
    for model in models:
        for attempt in range(3):
            try:
                raw, finish = call_model(prompt_text, model=model, max_tokens=max_tokens)
                data = clean_json(raw)
                if not isinstance(data, list):
                    raise ValueError(f"Model {model} returned non-list payload")
                if len(data) != required_count:
                    raise ValueError(
                        f"Model {model} returned {len(data)} items (expected {required_count})"
                    )
                return data, model
            except Exception as e:
                errors.append(f"{model} attempt {attempt+1}: {e}")
    raise RuntimeError("Both models failed: " + "; ".join(errors))


def run(selected: Optional[List[str]], model_primary: str, model_fallback: str, max_tokens: int, skip_validate: bool) -> None:
    prompts = selected if selected else find_prompts()
    print(f"Found {len(prompts)} prompt(s). Generating...")

    failures: List[str] = []
    for idx, p in enumerate(prompts, 1):
        rel = os.path.relpath(p)
        print(f"[{idx}/{len(prompts)}] {rel}")
        text = open(p, "r", encoding="utf-8").read()

        try:
            domain, grade, level, topic = extract_meta(text)
            out_file = output_path(domain, grade, level, topic)
        except Exception as e:
            print(f"  -> ERROR (meta): {e}")
            failures.append(f"{rel} (meta)")
            continue

        try:
            data, used_model = generate_for_prompt(
                p,
                model_primary,
                model_fallback,
                max_tokens,
                required_count=50,
            )
            write_json(out_file, data)
            print(f"  -> wrote {len(data)} items to {out_file} (model: {used_model})")
            if not skip_validate:
                ok, msg = validate_file(out_file)
                if ok:
                    print("  -> validate: OK")
                else:
                    print("  -> validate: FAIL")
                    print(msg.strip())
                    failures.append(out_file)
        except Exception as e:
            print(f"  -> ERROR: {e}")
            failures.append(out_file)
        # small pause to avoid rate limits
        time.sleep(0.3)

    if failures:
        print("\nFailed files:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--prompt",
        action="append",
        help="Specific prompt file(s) to run (default: all under prompts/packs/nl-NL).",
    )
    ap.add_argument("--model", default="gpt-4o", help="Primary model (default: gpt-4o).")
    ap.add_argument("--fallback", default="gpt-4o-mini", help="Fallback model.")
    ap.add_argument("--max-tokens", type=int, default=14000, help="max_tokens for completion.")
    ap.add_argument("--skip-validate", action="store_true", help="Skip validation step.")
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.prompt, args.model, args.fallback, args.max_tokens, args.skip_validate)
