"""
Voorbeeld voor het gebruik van het adaptieve systeem.

Dit voorbeeld laat zien hoe je:
- Leerling voortgang bijhoudt
- Het systeem de moeilijkheidsgraad laat aanpassen
- Statistieken ophaalt
"""

import random
from src import PromptLibrary, OpgaveGenerator, AdaptiveSystem


def simulate_student_answer(correct_rate: float = 0.7) -> bool:
    """
    Simuleer een leerling antwoord.

    Args:
        correct_rate: Kans dat het antwoord correct is (0-1).

    Returns:
        True als correct, False als incorrect.
    """
    return random.random() < correct_rate


def main():
    """Demonstreer adaptief systeem."""

    # Setup
    library = PromptLibrary()
    library.load_prompts()
    generator = OpgaveGenerator(prompt_library=library)
    adaptive = AdaptiveSystem()

    # Simuleer een leerling
    student_id = "student_001"
    domein = "getalbegrip"

    print(f"Simulatie voor leerling: {student_id}")
    print(f"Domein: {domein}\n")

    # Simuleer 15 opdrachten
    num_rounds = 15

    for round_num in range(1, num_rounds + 1):
        print(f"Ronde {round_num}:")

        # Vraag adaptief systeem om volgende prompt
        try:
            prompt_id = adaptive.get_next_prompt(student_id, domein, library)

            if not prompt_id:
                print("  Geen geschikte prompt gevonden")
                continue

            prompt = library.get_prompt(prompt_id)
            print(f"  Prompt: {prompt.titel} (niveau {prompt.niveau})")

            # Genereer opdracht
            opgave = generator.generate(prompt_id)

            # Simuleer antwoord (later in de ronde meer correct)
            # Dit simuleert een leerling die beter wordt
            correct_rate = min(0.3 + (round_num * 0.04), 0.95)
            correct = simulate_student_answer(correct_rate)

            # Registreer resultaat
            adaptive.record_result(student_id, prompt_id, correct)

            result_str = "✓ Correct" if correct else "✗ Incorrect"
            print(f"  Resultaat: {result_str}")

        except Exception as e:
            print(f"  ✗ Fout: {e}")

        print()

    # Toon statistieken
    print("="*50)
    print("STATISTIEKEN")
    print("="*50)

    stats = adaptive.get_student_statistics(student_id)

    print(f"\nLeerling: {stats['student_id']}")
    print(f"Groep: {stats['groep']}")
    print(f"Totaal opdrachten: {stats['totaal_opgaven']}")
    print(f"Correct: {stats['totaal_correct']}")
    print(f"Success rate: {stats['success_rate']:.1%}")

    print(f"\nHuidige niveaus per domein:")
    for domein, niveau in stats['huidige_niveaus'].items():
        print(f"  {domein}: niveau {niveau}")

    print("\n✓ Simulatie voltooid")


if __name__ == "__main__":
    # Seed voor reproduceerbare resultaten
    random.seed(42)
    main()
