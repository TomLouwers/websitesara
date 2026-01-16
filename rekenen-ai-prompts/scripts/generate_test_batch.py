#!/usr/bin/env python3
"""
Script om een test batch van opdrachten te genereren.

Gebruik:
    python scripts/generate_test_batch.py --groep 3 --domein getalbegrip --count 10
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import PromptLibrary, OpgaveGenerator


def generate_test_batch(
    groep: int,
    domein: str,
    count: int,
    output_dir: Path = None
) -> None:
    """
    Genereer een test batch van opdrachten.

    Args:
        groep: Groep nummer (3-8).
        domein: Rekendomein.
        count: Aantal opdrachten om te genereren.
        output_dir: Directory om resultaten op te slaan.
    """
    print(f"Genereren van test batch...")
    print(f"  Groep: {groep}")
    print(f"  Domein: {domein}")
    print(f"  Aantal: {count}\n")

    # Setup
    library = PromptLibrary()
    library.load_prompts()
    generator = OpgaveGenerator(prompt_library=library)

    # Zoek geschikte prompts
    prompts = library.search_prompts(groep=groep, domein=domein)

    if not prompts:
        print(f"✗ Geen prompts gevonden voor groep {groep}, domein '{domein}'")
        sys.exit(1)

    print(f"✓ {len(prompts)} geschikte prompts gevonden")

    # Gebruik eerste prompt
    prompt = prompts[0]
    print(f"  Gebruiken van: {prompt.titel} ({prompt.id})\n")

    # Genereer opdrachten
    print(f"Genereren van {count} opdrachten...")
    try:
        opdrachten = generator.generate_batch(
            prompt_id=prompt.id,
            count=count
        )
        print(f"✓ {len(opdrachten)} opdrachten gegenereerd\n")
    except Exception as e:
        print(f"✗ Fout bij genereren: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Sla op naar bestand
    if output_dir is None:
        output_dir = Path("output")

    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_batch_{groep}_{domein}_{timestamp}.txt"
    output_file = output_dir / filename

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Test Batch - Groep {groep} - {domein}\n")
        f.write(f"Gegenereerd: {datetime.now()}\n")
        f.write(f"Prompt: {prompt.titel} ({prompt.id})\n")
        f.write("="*60 + "\n\n")

        for i, opgave in enumerate(opdrachten, 1):
            f.write(f"Opdracht {i}\n")
            f.write("-"*40 + "\n")
            f.write(f"ID: {opgave.id}\n")
            f.write(f"Moeilijkheidsgraad: {opgave.moeilijkheidsgraad}\n\n")
            f.write(f"Vraag:\n{opgave.vraag}\n\n")

            if opgave.antwoord:
                f.write(f"Antwoord:\n{opgave.antwoord}\n\n")

            if opgave.toelichting:
                f.write(f"Toelichting:\n{opgave.toelichting}\n\n")

            f.write("\n")

    print(f"✓ Resultaten opgeslagen in: {output_file}")


def main():
    """Main functie."""
    parser = argparse.ArgumentParser(
        description="Genereer een test batch van opdrachten"
    )
    parser.add_argument(
        "--groep",
        type=int,
        required=True,
        choices=range(3, 9),
        help="Groep nummer (3-8)"
    )
    parser.add_argument(
        "--domein",
        type=str,
        required=True,
        help="Rekendomein (bijv. 'getalbegrip', 'strategieën')"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Aantal opdrachten om te genereren (default: 10)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (default: output/)"
    )

    args = parser.parse_args()

    try:
        generate_test_batch(
            groep=args.groep,
            domein=args.domein,
            count=args.count,
            output_dir=args.output_dir
        )
    except Exception as e:
        print(f"✗ Fout: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
