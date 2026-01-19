import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional
#python tools/validate_all_exercises_multidomain.py \
#  --topic-canon docs/topic-canon.json \
#  --taskforms docs/taskvormen-canon.json \
#  --content-root content/nl-NL \
#  --shared-root content/nl-NL/_shared

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_domain_to_kebab(domain_value: str) -> str:
    """
    Exercises: snake_case (getal_en_bewerkingen)
    Canon/packs: kebab-case (getal-en-bewerkingen)
    """
    if not isinstance(domain_value, str):
        return domain_value
    return domain_value.replace("_", "-")


def canon_key(domain_kebab: str, grade: int, topic: str) -> Tuple[str, int, str]:
    return (domain_kebab, grade, topic)


def infer_task_form(ex: Dict[str, Any]) -> str:
    """
    Prefer explicit metadata.taskForm.
    Fallback heuristic exists but explicit is strongly recommended.
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


class DomainPacks:
    def __init__(self, misconcepts: Dict[str, Any], feedback: Dict[str, Any]) -> None:
        self.misconcept_keys = set(m["key"] for m in misconcepts.get("misconcepts", []))
        self.feedback_map = feedback.get("misconceptFeedback", {})
        self.feedback_keys = set(self.feedback_map.keys())


def validate_exercise_list(
    exercises: List[Dict[str, Any]],
    topic_canon_lookup: Dict[Tuple[str, int, str], Dict[str, Any]],
    taskforms: Dict[str, Any],
    packs_by_domain: Dict[str, DomainPacks],
    file_path: Path,
) -> List[str]:
    errors: List[str] = []

    levels = taskforms.get("levels", {})
    task_def = taskforms.get("taskFormDefinitions", {})

    def err(i: int, exid: str, msg: str) -> None:
        errors.append(f"[{i}] {exid}: {msg}")

    for i, ex in enumerate(exercises):
        exid = ex.get("id", "<no-id>")

        # Required fields
        for field in [
            "schemaVersion", "id", "domain", "grade", "level", "topic",
            "interaction", "prompt", "solution"
        ]:
            if field not in ex:
                err(i, exid, f"Missing required field '{field}'")

        domain_raw = ex.get("domain")
        if not isinstance(domain_raw, str):
            err(i, exid, "domain must be a string")
            continue

        domain_kebab = normalize_domain_to_kebab(domain_raw)
        grade = int(ex.get("grade", -1))
        level = ex.get("level")
        topic = ex.get("topic")

        # A) Topic + allowedLevels check against topic-canon
        ck = canon_key(domain_kebab, grade, topic)
        if ck not in topic_canon_lookup:
            err(i, exid, f"Topic not in topic-canon: (domain={ck[0]}, grade={ck[1]}, topic={ck[2]})")
        else:
            allowed_levels = topic_canon_lookup[ck].get("allowedLevels", [])
            if level not in allowed_levels:
                err(i, exid, f"Level '{level}' not allowed for this topic (allowed={allowed_levels})")

        # B) Taskform check
        tf = infer_task_form(ex)
        if tf == "unknown":
            err(i, exid, "Cannot infer taskForm (add metadata.taskForm)")
        else:
            if level not in levels:
                err(i, exid, f"Level '{level}' not found in taskforms canon")
            else:
                allowed_tf = set(levels[level].get("allowedTaskForms", []))
                disallowed_tf = set(levels[level].get("disallowedTaskForms", []))

                if tf not in allowed_tf and tf not in disallowed_tf and tf not in task_def:
                    err(i, exid, f"taskForm '{tf}' not recognized in taskforms canon")

                if tf in disallowed_tf:
                    err(i, exid, f"taskForm '{tf}' is DISALLOWED for level {level}")
                elif tf not in allowed_tf:
                    err(i, exid, f"taskForm '{tf}' is not allowed for level {level} (allowed={sorted(allowed_tf)})")

        # C) Misconcept keys + feedback (domain-aware)
        if domain_kebab not in packs_by_domain:
            err(
                i,
                exid,
                f"Missing domain packs for '{domain_kebab}'. Expected files:\n"
                f"  content/nl-NL/_shared/misconcepts/{domain_kebab}.json\n"
                f"  content/nl-NL/_shared/feedback/{domain_kebab}.json"
            )
            continue

        packs = packs_by_domain[domain_kebab]

        md = ex.get("metadata", {})
        keys = []
        if isinstance(md, dict):
            keys = md.get("misconceptKeys", []) or []
        if not isinstance(keys, list):
            err(i, exid, "metadata.misconceptKeys must be a list")
            keys = []

        for k in keys:
            if k not in packs.misconcept_keys:
                err(i, exid, f"Misconcept key '{k}' not found in misconcepts canon for domain '{domain_kebab}'")
            if k not in packs.feedback_keys:
                err(i, exid, f"Misconcept key '{k}' has no feedback entry in feedback pack for domain '{domain_kebab}'")

        # D) MCQ structure validation
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

        # E) Numeric interaction must have numeric solution
        if itype == "numeric":
            sol = ex.get("solution", {})
            val = sol.get("value")

            def is_numeric(v):
                if isinstance(v, (int, float)):
                    return True
                if isinstance(v, str):
                    try:
                        float(v)
                        return True
                    except ValueError:
                        return False
                return False

            if not is_numeric(val):
                err(
                    i,
                    exid,
                    f"interaction.type 'numeric' requires numeric solution.value, got '{val}' ({type(val).__name__})"
                )

    return errors


def find_exercise_files(root: Path) -> List[Path]:
    return sorted(root.rglob("exercises.json"))


def load_domain_packs(shared_root: Path) -> Dict[str, DomainPacks]:
    """
    Load all packs that exist under:
      _shared/misconcepts/*.json
      _shared/feedback/*.json
    Only domains that have BOTH files are considered ready.
    """
    misconcepts_dir = shared_root / "misconcepts"
    feedback_dir = shared_root / "feedback"

    packs_by_domain: Dict[str, DomainPacks] = {}

    if not misconcepts_dir.exists() or not feedback_dir.exists():
        return packs_by_domain

    for mfile in misconcepts_dir.glob("*.json"):
        domain_kebab = mfile.stem  # e.g. "getal-en-bewerkingen"
        ffile = feedback_dir / f"{domain_kebab}.json"
        if not ffile.exists():
            continue

        try:
            misconcepts = load_json(mfile)
            feedback = load_json(ffile)
            packs_by_domain[domain_kebab] = DomainPacks(misconcepts, feedback)
        except Exception as e:
            # If pack cannot be parsed, mark as unusable by skipping, but print warning.
            print(f"WARNING: Could not load packs for domain '{domain_kebab}': {e}", file=sys.stderr)

    return packs_by_domain


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic-canon", required=True, help="Path to docs/topic-canon.json")
    ap.add_argument("--taskforms", required=True, help="Path to docs/taskvormen-canon.json")
    ap.add_argument("--content-root", default="content/nl-NL", help="Root folder to scan for exercises.json")
    ap.add_argument(
        "--shared-root",
        default="content/nl-NL/_shared",
        help="Root folder containing misconcepts/ and feedback/ packs"
    )
    args = ap.parse_args()

    topic_canon_path = Path(args.topic_canon)
    taskforms_path = Path(args.taskforms)
    content_root = Path(args.content_root)
    shared_root = Path(args.shared_root)

    if not content_root.exists():
        print(f"ERROR: content root does not exist: {content_root}", file=sys.stderr)
        sys.exit(2)

    try:
        topic_canon = load_json(topic_canon_path)
    except Exception as e:
        print(f"ERROR: cannot read topic-canon: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        taskforms = load_json(taskforms_path)
    except Exception as e:
        print(f"ERROR: cannot read taskforms canon: {e}", file=sys.stderr)
        sys.exit(2)

    # Build topic canon lookup
    topic_canon_lookup: Dict[Tuple[str, int, str], Dict[str, Any]] = {}
    if not isinstance(topic_canon, list):
        print("ERROR: topic-canon.json must be a JSON array", file=sys.stderr)
        sys.exit(2)

    for item in topic_canon:
        try:
            k = canon_key(item["domain"], int(item["grade"]), item["topic"])
            topic_canon_lookup[k] = item
        except Exception:
            print(f"ERROR: invalid entry in topic-canon: {item}", file=sys.stderr)
            sys.exit(2)

    # Load all domain packs available
    packs_by_domain = load_domain_packs(shared_root)

    files = find_exercise_files(content_root)
    if not files:
        print(f"No exercises.json files found under {content_root}")
        sys.exit(0)

    total_files = 0
    total_issues = 0

    for f in files:
        total_files += 1
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            total_issues += 1
            print(f"\nFILE: {f}")
            print(f" - ERROR: cannot parse JSON: {e}")
            continue

        if not isinstance(data, list):
            total_issues += 1
            print(f"\nFILE: {f}")
            print(" - ERROR: exercises.json must be a JSON array of exercise objects")
            continue

        errs = validate_exercise_list(
            exercises=data,
            topic_canon_lookup=topic_canon_lookup,
            taskforms=taskforms,
            packs_by_domain=packs_by_domain,
            file_path=f,
        )

        if errs:
            total_issues += len(errs)
            print(f"\nFILE: {f}  -> FAILED ({len(errs)} issues)")
            for e in errs:
                print(" - " + e)
        else:
            print(f"\nFILE: {f}  -> OK")

    print("\n" + "=" * 60)
    print(f"Scanned files : {total_files}")
    print(f"Total issues  : {total_issues}")
    print("=" * 60)

    sys.exit(1 if total_issues > 0 else 0)


if __name__ == "__main__":
    main()
