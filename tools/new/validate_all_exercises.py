import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple
#python tools/validate_all_exercises.py \
#  --topic-canon docs/topic-canon.json \
#  --taskforms docs/taskvormen-canon.json \
#  --misconcepts content/nl-NL/_shared/misconcepts/getal-en-bewerkingen.json \
#  --feedback content/nl-NL/_shared/feedback/getal-en-bewerkingen.json \
#  --content-root content/nl-NL

def load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canon_key(domain: str, grade: int, topic: str) -> Tuple[str, int, str]:
    return (domain, grade, topic)


def normalize_domain_for_canon(domain_value: str) -> str:
    """
    Exercises currently use snake_case (e.g. getal_en_bewerkingen)
    while canon uses kebab-case (e.g. getal-en-bewerkingen).
    Normalize snake_case -> kebab-case so matching works.
    """
    if not isinstance(domain_value, str):
        return domain_value
    return domain_value.replace("_", "-")


def infer_task_form(ex: Dict[str, Any]) -> str:
    """
    Prefer explicit metadata.taskForm.
    Fallback is only a last resort; explicit is strongly recommended.
    """
    md = ex.get("metadata", {})
    if isinstance(md, dict) and md.get("taskForm"):
        return md["taskForm"]

    itype = ex.get("interaction", {}).get("type")
    if itype == "numeric":
        return "numeric_simple"
    if itype == "mcq":
        return "select_single"
    if itype == "fill_blanks":
        return "fill_single_step"
    return "unknown"


def validate_exercise_list(
    exercises: List[Dict[str, Any]],
    topic_canon: List[Dict[str, Any]],
    taskforms: Dict[str, Any],
    misconcepts: Dict[str, Any],
    feedback: Dict[str, Any],
) -> List[str]:
    errors: List[str] = []

    # Build topic canon lookup
    canon_lookup: Dict[Tuple[str, int, str], Dict[str, Any]] = {}
    for item in topic_canon:
        k = canon_key(item["domain"], int(item["grade"]), item["topic"])
        canon_lookup[k] = item

    # Misconcept keys set
    mc_keys = set(m["key"] for m in misconcepts.get("misconcepts", []))

    # Feedback keys set
    fb = feedback.get("misconceptFeedback", {})
    fb_keys = set(fb.keys())

    levels = taskforms.get("levels", {})
    task_def = taskforms.get("taskFormDefinitions", {})

    def err(i: int, exid: str, msg: str) -> None:
        errors.append(f"[{i}] {exid}: {msg}")

    for i, ex in enumerate(exercises):
        exid = ex.get("id", "<no-id>")

        # Required fields (hard)
        for field in [
            "schemaVersion",
            "id",
            "domain",
            "grade",
            "level",
            "topic",
            "interaction",
            "prompt",
            "solution",
        ]:
            if field not in ex:
                err(i, exid, f"Missing required field '{field}'")

        domain_raw = ex.get("domain")
        domain = normalize_domain_for_canon(domain_raw)
        grade = int(ex.get("grade", -1))
        level = ex.get("level")
        topic = ex.get("topic")

        # A. Topic & level check (hard)
        ck = canon_key(domain, grade, topic)
        if ck not in canon_lookup:
            err(
                i,
                exid,
                f"Topic not in topic-canon: (domain={ck[0]}, grade={ck[1]}, topic={ck[2]})",
            )
        else:
            allowed = canon_lookup[ck].get("allowedLevels", [])
            if level not in allowed:
                err(i, exid, f"Level '{level}' not allowed for this topic (allowed={allowed})")

        # B. Taskform check (hard)
        tf = infer_task_form(ex)
        if tf == "unknown":
            err(i, exid, "Cannot infer taskForm (add metadata.taskForm)")
        else:
            if level not in levels:
                err(i, exid, f"Level '{level}' not found in taskforms canon")
            else:
                allowed_tf = set(levels[level].get("allowedTaskForms", []))
                disallowed_tf = set(levels[level].get("disallowedTaskForms", []))

                # If not explicitly defined anywhere, flag it
                if tf not in allowed_tf and tf not in disallowed_tf and tf not in task_def:
                    err(i, exid, f"taskForm '{tf}' not recognized in taskforms canon")

                if tf in disallowed_tf:
                    err(i, exid, f"taskForm '{tf}' is DISALLOWED for level {level}")
                elif tf not in allowed_tf:
                    err(
                        i,
                        exid,
                        f"taskForm '{tf}' is not allowed for level {level} (allowed={sorted(allowed_tf)})",
                    )

        # C. Misconcept keys check (hard)
        md = ex.get("metadata", {})
        keys = []
        if isinstance(md, dict):
            keys = md.get("misconceptKeys", []) or []
        if not isinstance(keys, list):
            err(i, exid, "metadata.misconceptKeys must be a list")
            keys = []

        for k in keys:
            if k not in mc_keys:
                err(i, exid, f"Misconcept key '{k}' not found in misconcepts canon")
            if k not in fb_keys:
                err(i, exid, f"Misconcept key '{k}' has no feedback entry in feedback pack")

        # D. MCQ structure validation
        itype = ex.get("interaction", {}).get("type")
        if itype == "mcq":
            options = ex.get("options")
            sol = ex.get("solution", {})
            idx = sol.get("index")
            if not isinstance(options, list) or len(options) < 2:
                err(i, exid, "MCQ must have 'options' as a list with at least 2 items")
            if not isinstance(idx, int):
                err(i, exid, "MCQ solution.index must be an integer")
            elif isinstance(options, list) and not (0 <= idx < len(options)):
                err(i, exid, f"MCQ solution.index out of range (index={idx}, options={len(options)})")

    return errors


def find_exercise_files(root: Path) -> List[Path]:
    """
    Find all exercises.json under the given root.
    """
    return sorted(root.rglob("exercises.json"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic-canon", required=True)
    ap.add_argument("--taskforms", required=True)
    ap.add_argument("--misconcepts", required=True)
    ap.add_argument("--feedback", required=True)
    ap.add_argument("--content-root", default="content/nl-NL", help="Root folder to scan for exercises.json")
    args = ap.parse_args()

    topic_canon = load_json(args.topic_canon)
    taskforms = load_json(args.taskforms)
    misconcepts = load_json(args.misconcepts)
    feedback = load_json(args.feedback)

    content_root = Path(args.content_root)
    if not content_root.exists():
        print(f"ERROR: content root does not exist: {content_root}", file=sys.stderr)
        sys.exit(2)

    files = find_exercise_files(content_root)
    if not files:
        print(f"No exercises.json files found under {content_root}")
        sys.exit(0)

    total_files = 0
    total_errors = 0

    for f in files:
        total_files += 1
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            total_errors += 1
            print(f"\nFILE: {f}")
            print(f" - ERROR: cannot parse JSON: {e}")
            continue

        if not isinstance(data, list):
            total_errors += 1
            print(f"\nFILE: {f}")
            print(" - ERROR: exercises.json must be a JSON array of exercise objects")
            continue

        errs = validate_exercise_list(data, topic_canon, taskforms, misconcepts, feedback)

        if errs:
            total_errors += len(errs)
            print(f"\nFILE: {f}  -> FAILED ({len(errs)} issues)")
            for e in errs:
                print(" - " + e)
        else:
            print(f"\nFILE: {f}  -> OK")

    print("\n" + "=" * 60)
    print(f"Scanned files : {total_files}")
    print(f"Total issues  : {total_errors}")
    print("=" * 60)

    if total_errors > 0:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
