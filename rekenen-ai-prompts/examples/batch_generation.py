"""
Voorbeeld voor het genereren van meerdere opdrachten in één keer.

Dit voorbeeld laat zien hoe je:
- Meerdere opdrachten in een batch genereert
- Parameters varieert over de batch
- Resultaten opslaat
"""

from pathlib import Path
from src import PromptLibrary, OpgaveGenerator


def main():
    """Demonstreer batch generatie van opdrachten."""

    # Setup
    library = PromptLibrary()
    library.load_prompts()
    generator = OpgaveGenerator(prompt_library=library)

    # Zoek een geschikte prompt
    prompts = library.search_prompts(groep=3, domein="getalbegrip", niveau=1)

    if not prompts:
        print("Geen geschikte prompts gevonden")
        return

    prompt = prompts[0]
    print(f"Gebruiken van prompt: {prompt.titel} ({prompt.id})")

    # Genereer een batch van 5 opdrachten
    print(f"\nGenereren van 5 opdrachten...")
    batch_size = 5

    try:
        opdrachten = generator.generate_batch(
            prompt_id=prompt.id,
            count=batch_size,
            aantal=3,
            moeilijkheid="makkelijk"
        )

        print(f"✓ {len(opdrachten)} opdrachten gegenereerd\n")

        # Toon alle gegenereerde opdrachten
        for i, opgave in enumerate(opdrachten, 1):
            print(f"Opdracht {i}:")
            print(f"  ID: {opgave.id}")
            print(f"  Vraag: {opgave.vraag}")
            if opgave.antwoord:
                print(f"  Antwoord: {opgave.antwoord}")
            print()

        # Optioneel: sla resultaten op
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / f"batch_{prompt.id}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, opgave in enumerate(opdrachten, 1):
                f.write(f"Opdracht {i}\n")
                f.write(f"Vraag: {opgave.vraag}\n")
                if opgave.antwoord:
                    f.write(f"Antwoord: {opgave.antwoord}\n")
                f.write("\n" + "-"*50 + "\n\n")

        print(f"✓ Resultaten opgeslagen in {output_file}")

    except Exception as e:
        print(f"✗ Fout bij genereren: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
