"""
Basis voorbeeld voor het gebruik van de prompt library.

Dit voorbeeld laat zien hoe je:
- De prompt library initialiseert
- Prompts laadt
- Een specifieke prompt ophaalt
- Statistieken bekijkt
- Zoekt naar prompts
"""

from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.prompt_library import PromptLibrary


def main():
    """Demonstreer basis gebruik van de library."""

    print("=" * 60)
    print("REKENEN AI PROMPTS - BASIS VOORBEELD")
    print("=" * 60)
    print()

    # Initialiseer de prompt library
    print("📚 Initialiseren van prompt library...")
    library = PromptLibrary()

    # Laad alle prompts
    print("\n📖 Laden van prompts...")
    try:
        library.load_prompts()
    except FileNotFoundError as e:
        print(f"❌ Fout bij laden: {e}")
        print("\n💡 Tip: Zorg dat je de prompts directory hebt aangemaakt")
        print("    met ten minste één YAML bestand.")
        return

    # Toon statistieken
    print("\n📊 STATISTIEKEN")
    print("=" * 60)
    stats = library.get_statistics()
    print(f"Totaal aantal prompts: {stats['totaal']}")

    if stats['per_groep']:
        print("\nPer groep:")
        for groep in sorted(stats['per_groep'].keys()):
            print(f"  Groep {groep}: {stats['per_groep'][groep]} prompts")

    if stats['per_niveau']:
        print("\nPer niveau:")
        for niveau in sorted(stats['per_niveau'].keys()):
            print(f"  {niveau}: {stats['per_niveau'][niveau]} prompts")

    if stats['per_inhoudslijn']:
        print("\nPer inhoudslijn:")
        for lijn in sorted(stats['per_inhoudslijn'].keys()):
            print(f"  {lijn}: {stats['per_inhoudslijn'][lijn]} prompts")

    # Toon beschikbare inhoudslijnen
    print("\n📋 BESCHIKBARE INHOUDSLIJNEN")
    print("=" * 60)
    for groep in range(3, 9):
        lijnen = library.list_inhoudslijnen(groep=groep)
        if lijnen:
            print(f"Groep {groep}: {', '.join(lijnen)}")

    # Voorbeeld: Zoek prompts voor groep 5
    print("\n🔍 ZOEKEN NAAR PROMPTS")
    print("=" * 60)
    print("Zoeken naar: Groep 5, Getalbegrip, Niveau N2")

    prompts = library.search_prompts(
        groep=5,
        inhoudslijn="Getalbegrip",
        niveau="N2"
    )

    print(f"Gevonden: {len(prompts)} prompt(s)")

    if prompts:
        # Toon details van eerste prompt
        prompt = prompts[0]
        print(f"\n📄 VOORBEELD PROMPT: {prompt['PROMPT_ID']}")
        print("-" * 60)

        metadata = prompt.get('METADATA', {})
        print(f"Groep:        {metadata.get('groep')}")
        print(f"Inhoudslijn:  {metadata.get('inhoudslijn')}")
        print(f"Niveau:       {metadata.get('niveau')}")
        print(f"Referentie:   {metadata.get('referentie')}")

        if 'OPDRACHT' in prompt:
            print(f"\nOpdracht:")
            opdracht_preview = prompt['OPDRACHT'].strip()[:150]
            print(f"  {opdracht_preview}...")

        if 'SPECIFICATIES' in prompt:
            specs = prompt['SPECIFICATIES']
            if 'getallenreeks' in specs:
                print(f"\nGetallenreeks: {specs['getallenreeks']}")

    # Voorbeeld: Haal specifieke prompt op
    print("\n\n🎯 SPECIFIEKE PROMPT OPHALEN")
    print("=" * 60)

    # Probeer eerste prompt uit library
    if library.prompts:
        first_id = list(library.prompts.keys())[0]
        print(f"Ophalen van prompt: {first_id}")

        try:
            specific_prompt = library.get_prompt(first_id)
            print("✅ Prompt succesvol opgehaald")

            # Toon structuur
            print("\nPrompt bevat de volgende secties:")
            for key in specific_prompt.keys():
                print(f"  - {key}")

        except KeyError as e:
            print(f"❌ Prompt niet gevonden: {e}")
    else:
        print("⚠️  Geen prompts beschikbaar om op te halen")

    print("\n" + "=" * 60)
    print("✨ Klaar! Bekijk de andere voorbeelden voor meer functionaliteit.")
    print("=" * 60)


if __name__ == "__main__":
    main()
