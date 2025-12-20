#!/usr/bin/env python3
"""
Script to verify all answers in verhaaltjessommen - Template.json
Acts as a groep 8 teacher checking math problems!
"""

import json
import re

def verify_math(content, question, correct_option):
    """
    Verify if the marked correct answer is actually correct.
    Returns (is_correct, explanation, calculated_answer)
    """
    # This is a basic checker - we'll manually review the results
    # since the problems are word problems that need human interpretation
    return True, "Needs manual verification", None

def main():
    print("=" * 80)
    print("NAKIJKWERK VERHAALTJESSOMMEN - GROEP 8")
    print("=" * 80)
    print()

    with open('verhaaltjessommen - Template.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Aantal verhalen gevonden: {len(data)}")
    print()

    errors = []
    total_questions = 0

    for story_idx, story in enumerate(data, 1):
        story_id = story.get('id', story_idx)
        title = story.get('title', 'Geen titel')
        content = story.get('content', '')

        print(f"\n{'='*80}")
        print(f"VERHAAL {story_id}: {title}")
        print(f"{'='*80}")
        print(f"Context: {content}")
        print()

        for q_idx, q in enumerate(story.get('questions', []), 1):
            total_questions += 1
            question_text = q.get('question', '')
            correct_idx = q.get('correct', -1)
            options = q.get('options', [])

            print(f"\nVraag {q_idx}: {question_text}")
            print(f"Aantal antwoordopties: {len(options)}")

            if correct_idx < 0 or correct_idx >= len(options):
                error_msg = f"FOUT: Correct index {correct_idx} is ongeldig (moet tussen 0 en {len(options)-1})"
                print(f"   ❌ {error_msg}")
                errors.append({
                    'story_id': story_id,
                    'story_title': title,
                    'question_num': q_idx,
                    'question': question_text,
                    'error': error_msg
                })
                continue

            correct_answer = options[correct_idx].get('text', '')
            print(f"   Correct antwoord (index {correct_idx}): {correct_answer}")

            # Show all options for manual verification
            print(f"\n   Alle antwoordopties:")
            for opt_idx, opt in enumerate(options):
                marker = "✓ CORRECT" if opt_idx == correct_idx else ""
                print(f"      [{opt_idx}] {opt.get('text', 'Geen tekst')} {marker}")

            # Check if the correct answer has empty foutanalyse (which it should)
            if options[correct_idx].get('foutanalyse', '') != '':
                error_msg = f"WAARSCHUWING: Het correcte antwoord heeft een foutanalyse (zou leeg moeten zijn)"
                print(f"   ⚠️  {error_msg}")

            # Extract calculation info if available
            extra_info = q.get('extra_info', {})
            if 'berekening' in extra_info:
                print(f"\n   Berekeningsstappen:")
                for stap in extra_info['berekening']:
                    print(f"      • {stap}")

    print(f"\n\n{'='*80}")
    print("SAMENVATTING")
    print(f"{'='*80}")
    print(f"Totaal aantal verhalen: {len(data)}")
    print(f"Totaal aantal vragen: {total_questions}")
    print(f"Aantal fouten gevonden: {len(errors)}")
    print()

    if errors:
        print("GEVONDEN FOUTEN:")
        for err in errors:
            print(f"\n• Verhaal {err['story_id']}: {err['story_title']}")
            print(f"  Vraag {err['question_num']}: {err['question']}")
            print(f"  Fout: {err['error']}")
    else:
        print("✓ Alle antwoorden hebben geldige indexen!")
        print("\nOPMERKING: Dit script controleert alleen of de indexen kloppen.")
        print("De wiskundige berekeningen moeten handmatig geverifieerd worden.")

    return len(errors)

if __name__ == '__main__':
    exit(main())
