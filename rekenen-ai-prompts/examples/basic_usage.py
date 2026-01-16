"""
Basis voorbeeld voor het gebruik van de prompt library.

Dit voorbeeld laat zien hoe je:
- De prompt library initialiseert
- Prompts laadt
- Een specifieke prompt ophaalt
- Een opdracht genereert
"""

from pathlib import Path
from src import PromptLibrary, OpgaveGenerator


def main():
    """Demonstreer basis gebruik van de library."""

    # Initialiseer de prompt library
    print("Initialiseren van prompt library...")
    library = PromptLibrary()

    # Laad alle prompts
    print("Laden van prompts...")
    try:
        library.load_prompts()
        print(f"✓ {len(library.prompts)} prompts geladen")
    except FileNotFoundError as e:
        print(f"✗ Fout bij laden: {e}")
        return

    # Toon beschikbare domeinen
    print("\nBeschikbare domeinen:")
    for groep in range(3, 9):
        domains = library.list_domains(groep=groep)
        if domains:
            print(f"  Groep {groep}: {', '.join(domains)}")

    # Zoek prompts voor groep 3
    print("\nZoeken naar prompts voor groep 3, domein 'getalbegrip'...")
    prompts = library.search_prompts(groep=3, domein="getalbegrip")
    print(f"✓ {len(prompts)} prompts gevonden")

    if prompts:
        # Toon details van eerste prompt
        prompt = prompts[0]
        print(f"\nEerste prompt:")
        print(f"  ID: {prompt.id}")
        print(f"  Titel: {prompt.titel}")
        print(f"  Niveau: {prompt.niveau}")
        print(f"  Parameters: {[p.name for p in prompt.parameters]}")

        # Genereer een opdracht
        print("\nGenereren van opdracht...")
        generator = OpgaveGenerator(prompt_library=library)

        try:
            opgave = generator.generate(
                prompt_id=prompt.id,
                aantal=3,
                moeilijkheid="makkelijk"
            )
            print("✓ Opdracht gegenereerd:")
            print(f"  ID: {opgave.id}")
            print(f"  Vraag: {opgave.vraag}")
            print(f"  Moeilijkheidsgraad: {opgave.moeilijkheidsgraad}")
        except Exception as e:
            print(f"✗ Fout bij genereren: {e}")


if __name__ == "__main__":
    main()
