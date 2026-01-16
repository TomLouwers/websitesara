#!/usr/bin/env python3
"""
Script om prompts te laden naar een database.

Gebruik:
    python scripts/load_prompts_to_db.py [--db-url DATABASE_URL]
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import PromptLibrary


def load_to_database(db_url: str, prompts_path: Path = None) -> None:
    """
    Laad alle prompts naar de database.

    Args:
        db_url: Database connection URL.
        prompts_path: Pad naar prompts directory.
    """
    print("Laden van prompts naar database...")

    # Laad prompts
    library = PromptLibrary(prompts_path=prompts_path)
    library.load_prompts()

    print(f"✓ {len(library.prompts)} prompts geladen uit bestanden")

    # TODO: Implementeer database connectie en insert
    # Voor nu alleen een placeholder
    print(f"\nDit zou de prompts laden naar: {db_url}")
    print("(Database implementatie nog niet beschikbaar)")

    # Voorbeeld van wat je zou doen:
    # with get_db_connection(db_url) as conn:
    #     for prompt_id, prompt in library.prompts.items():
    #         insert_prompt(conn, prompt)

    print("\n✓ Script voltooid")


def main():
    """Main functie."""
    parser = argparse.ArgumentParser(
        description="Laad prompts naar database"
    )
    parser.add_argument(
        "--db-url",
        default="sqlite:///prompts.db",
        help="Database URL (default: sqlite:///prompts.db)"
    )
    parser.add_argument(
        "--prompts-path",
        type=Path,
        help="Pad naar prompts directory (default: prompts/)"
    )

    args = parser.parse_args()

    try:
        load_to_database(args.db_url, args.prompts_path)
    except Exception as e:
        print(f"✗ Fout: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
