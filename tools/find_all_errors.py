#!/usr/bin/env python3
"""
Find all actual calculation errors where the berekening result doesn't match the correct answer
"""

import json
import re

def extract_final_answer(berekening_steps):
    """Extract the final calculated answer from the berekening steps"""
    if not berekening_steps:
        return None

    # Look at the last step
    last_step = berekening_steps[-1]

    # Common patterns for final answers
    patterns = [
        r'= ([€]?[\d.,]+[^\s]*)',  # "= €12,24" or "= 15 wedstrijden"
        r'([€]?[\d.,]+[^\s]*)\s*$',  # End of line number
        r'≈\s*([€]?[\d.,]+[^\s]*)',  # "≈ €166,67"
    ]

    for pattern in patterns:
        match = re.search(pattern, last_step)
        if match:
            return match.group(1).strip()

    return None

def normalize_answer(text):
    """Normalize answer text for comparison"""
    # Remove extra spaces
    text = ' '.join(text.split())
    # Standardize decimal separators
    return text

def main():
    with open('verhaaltjessommen - Template.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    errors = []
    checked = 0

    for story in data:
        story_id = story.get('id')
        story_title = story.get('title')

        for q_idx, question in enumerate(story.get('questions', []), 1):
            correct_idx = question.get('correct', -1)
            options = question.get('options', [])

            if correct_idx < 0 or correct_idx >= len(options):
                continue

            correct_answer = options[correct_idx].get('text', '')
            extra_info = question.get('extra_info', {})
            berekening = extra_info.get('berekening', [])

            if not berekening:
                continue

            checked += 1

            # Extract what the calculation says the answer should be
            calculated_answer = extract_final_answer(berekening)

            if calculated_answer and normalize_answer(calculated_answer) != normalize_answer(correct_answer):
                # Potential mismatch - let's verify it's a real error
                errors.append({
                    'story_id': story_id,
                    'story_title': story_title,
                    'question_num': q_idx,
                    'question': question.get('question'),
                    'context': story.get('content'),
                    'correct_answer': correct_answer,
                    'calculated_answer': calculated_answer,
                    'berekening': berekening,
                    'all_options': [opt.get('text') for opt in options],
                    'correct_idx': correct_idx
                })

    print("="*80)
    print("VOLLEDIGE FOUTANALYSE - GROEP 8 NAKIJKWERK")
    print("="*80)
    print()
    print(f"Totaal aantal verhalen: {len(data)}")
    print(f"Totaal aantal vragen gecontroleerd: {checked}")
    print(f"Aantal potentiële fouten gevonden: {len(errors)}")
    print()

    if errors:
        print("="*80)
        print("GEVONDEN FOUTEN:")
        print("="*80)

        for idx, err in enumerate(errors, 1):
            print(f"\n{idx}. Verhaal {err['story_id']}: {err['story_title']}")
            print(f"   Vraag {err['question_num']}: {err['question']}")
            print(f"   Context: {err['context'][:100]}...")
            print()
            print(f"   Alle antwoordopties:")
            for i, opt in enumerate(err['all_options']):
                marker = " ✓ GEMARKEERD ALS CORRECT" if i == err['correct_idx'] else ""
                print(f"      [{i}] {opt}{marker}")
            print()
            print(f"   Berekening volgens JSON:")
            for stap in err['berekening']:
                print(f"      • {stap}")
            print()
            print(f"   ❌ PROBLEEM:")
            print(f"      Berekend antwoord: {err['calculated_answer']}")
            print(f"      Gemarkeerd als correct: {err['correct_answer']}")
            print()

    else:
        print("✅ GEEN FOUTEN GEVONDEN!")
        print("Alle antwoorden komen overeen met de berekeningen!")

    return len(errors)

if __name__ == '__main__':
    exit(main())
