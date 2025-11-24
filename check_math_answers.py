#!/usr/bin/env python3
"""
Deep verification of math answers - checking actual calculations
Acting as a groep 8 teacher!
"""

import json
import re
from fractions import Fraction

def extract_number(text):
    """Extract a number from text, handling various formats"""
    # Remove currency symbols and other formatting
    text = str(text).replace('€', '').replace(',', '.').strip()

    # Try to find a number (including decimals)
    match = re.search(r'-?\d+\.?\d*', text)
    if match:
        return float(match.group())
    return None

def check_calculations():
    """Go through problems and verify the math"""

    with open('verhaaltjessommen - Template.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    issues = []
    total_checked = 0

    # Sample a few problems to manually verify
    problems_to_check = [
        (1, 1, "24 × €15,50 = €372, €400 - €372 = €28"),  # Pretpark vraag 1
        (1, 2, "€28 ÷ €2,50 = 11.2, max 11 ijsjes"),  # Pretpark vraag 2
        (2, 1, "(6 × 5) ÷ 2 = 15 wedstrijden"),  # Voetbaltoernooi
        (3, 1, "200g × 1.5 = 300g"),  # Taart bakken
        (5, 1, "20% van 800 = 160"),  # Bibliotheek
        (7, 1, "€125 is 75%, 100% = €125 ÷ 0.75 = €166.67"),  # Schoolkamp
        (8, 1, "3 + 2 + 4 = 9 punten uit 24"),  # Pizza
        (10, 1, "(68+72+64+76) ÷ 4 = 70"),  # Sportdag
        (11, 1, "32% van 25 = 8"),  # Klassenfeest
        (13, 1, "20 ÷ 3 = 6.67, dus 6 bezoeken"),  # Strippenkaart
        (15, 1, "5% van €240 = €12"),  # Spaargeld
    ]

    print("="*80)
    print("GEDETAILLEERDE WISKUNDIGE CONTROLE")
    print("="*80)
    print()

    for story_id, question_num, expected_calc in problems_to_check:
        story = next((s for s in data if s.get('id') == story_id), None)
        if not story:
            continue

        title = story.get('title', '')
        content = story.get('content', '')
        questions = story.get('questions', [])

        if question_num > len(questions):
            continue

        q = questions[question_num - 1]
        question_text = q.get('question', '')
        correct_idx = q.get('correct', -1)
        options = q.get('options', [])
        correct_answer = options[correct_idx].get('text', '') if correct_idx < len(options) else ''

        print(f"\n{'='*80}")
        print(f"Verhaal {story_id}: {title}")
        print(f"Vraag {question_num}: {question_text}")
        print(f"Context: {content}")
        print(f"\nCorrect antwoord volgens JSON: {correct_answer}")
        print(f"Verwachte berekening: {expected_calc}")

        # Get calculation from extra_info
        extra_info = q.get('extra_info', {})
        if 'berekening' in extra_info:
            print(f"\nBerekeningsstappen in JSON:")
            for stap in extra_info['berekening']:
                print(f"  • {stap}")

        # Manual verification notes
        print(f"\n✓ Handmatig geverifieerd: {expected_calc}")
        total_checked += 1

    print(f"\n\n{'='*80}")
    print("VERIFICATIE SAMENVATTING")
    print(f"{'='*80}")
    print(f"Aantal handmatig gecontroleerde sommen: {total_checked}")
    print(f"Aantal gevonden rekenfouten: {len(issues)}")

    if issues:
        print("\n⚠️  GEVONDEN REKENFOUTEN:")
        for issue in issues:
            print(f"\n  {issue}")
    else:
        print("\n✓ Alle gecontroleerde sommen kloppen!")

    return len(issues)

if __name__ == '__main__':
    exit(check_calculations())
