#!/usr/bin/env python3
"""
Script om alle prompts te valideren.

Gebruik:
    python scripts/validate_all_prompts.py
"""

import sys
from pathlib import Path
from typing import Dict, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import PromptLibrary
from src.validators import PromptValidator


def validate_all_prompts(prompts_path: Path = None) -> Dict[str, List[str]]:
    """
    Valideer alle prompts.

    Args:
        prompts_path: Pad naar prompts directory.

    Returns:
        Dictionary met errors en warnings per prompt.
    """
    print("Valideren van alle prompts...")
    print("="*60)

    # Laad prompts
    library = PromptLibrary(prompts_path=prompts_path)

    try:
        library.load_prompts()
        print(f"✓ {len(library.prompts)} prompts geladen\n")
    except Exception as e:
        print(f"✗ Fout bij laden: {e}")
        return {}

    # Valideer elke prompt
    total_errors = 0
    total_warnings = 0
    results = {}

    for prompt_id, prompt in library.prompts.items():
        result = PromptValidator.validate_prompt(prompt)

        if not result.is_valid or result.warnings:
            results[prompt_id] = {
                'errors': result.errors,
                'warnings': result.warnings
            }

        total_errors += len(result.errors)
        total_warnings += len(result.warnings)

    # Print resultaten
    print("\nVALIDATIE RESULTATEN")
    print("="*60)

    if not results:
        print("✓ Alle prompts zijn valide!")
    else:
        for prompt_id, result_data in results.items():
            print(f"\n{prompt_id}:")

            if result_data['errors']:
                print("  Errors:")
                for error in result_data['errors']:
                    print(f"    ✗ {error}")

            if result_data['warnings']:
                print("  Warnings:")
                for warning in result_data['warnings']:
                    print(f"    ⚠ {warning}")

    # Samenvatting
    print("\n" + "="*60)
    print("SAMENVATTING")
    print("="*60)
    print(f"Totaal prompts: {len(library.prompts)}")
    print(f"Met errors: {len([r for r in results.values() if r['errors']])}")
    print(f"Met warnings: {len([r for r in results.values() if r['warnings']])}")
    print(f"Totaal errors: {total_errors}")
    print(f"Totaal warnings: {total_warnings}")

    return results


def main():
    """Main functie."""
    try:
        results = validate_all_prompts()

        # Exit met error code als er errors zijn
        has_errors = any(r['errors'] for r in results.values())
        sys.exit(1 if has_errors else 0)

    except Exception as e:
        print(f"✗ Fout: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
