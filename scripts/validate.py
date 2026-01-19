import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def pick_first_existing(*relative_paths: str) -> str:
    """Return the first existing path (as string) from the given relative candidates."""
    for rel in relative_paths:
        candidate = ROOT / rel
        if candidate.exists():
            return str(candidate)
    raise FileNotFoundError(f"None of the candidate paths exist: {relative_paths}")


cmd = [
    sys.executable,
    str(ROOT / "tools/new/validate_all_exercises_multidomain.py"),
    "--topic-canon",
    pick_first_existing("docs/topic-canon.json", "docs/new/topic-canon.json"),
    "--taskforms",
    pick_first_existing("docs/taskvormen-canon.json", "docs/new/taskvormen-canon.json"),
    "--content-root",
    str(ROOT / "content/nl-NL"),
    "--shared-root",
    str(ROOT / "content/nl-NL/_shared"),
]

raise SystemExit(subprocess.call(cmd))
