#!/usr/bin/env python3
"""
Find REAL calculation errors - comparing numeric values only
"""

import json
import re

def extract_number(text):
    """Extract the primary numeric value from text"""
    if not text:
        return None

    # Remove currency symbols and spaces
    text = str(text).replace('€', '').replace('.', '').replace(',', '.').strip()

    # Extract first number (including decimals)
    match = re.search(r'(\d+(?:\.\d+)?)', text)
    if match:
        try:
            return float(match.group(1))
        except:
            return None
    return None

def extract_fraction(text):
    """Extract fraction like 9/24"""
    match = re.search(r'(\d+)/(\d+)', text)
    if match:
        return (int(match.group(1)), int(match.group(2)))
    return None

def fractions_equal(frac1_text, frac2_text):
    """Check if two fractions are equivalent"""
    f1 = extract_fraction(frac1_text)
    f2 = extract_fraction(frac2_text)

    if f1 and f2:
        # Check if equivalent: cross multiply
        return f1[0] * f2[1] == f1[1] * f2[0]
    return False

def numbers_close(n1, n2, tolerance=0.05):
    """Check if two numbers are close (within tolerance)"""
    if n1 is None or n2 is None:
        return False
    return abs(n1 - n2) <= tolerance

def main():
    with open('verhaaltjessommen - Template.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    real_errors = []
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

            # Extract the final calculation result
            last_step = berekening[-1]

            # Check for fractions first
            if '/' in last_step and '/' in correct_answer:
                if not fractions_equal(last_step, correct_answer):
                    # Might be equivalent fractions
                    continue

            # Extract numeric values
            calc_num = extract_number(last_step)
            answer_num = extract_number(correct_answer)

            if calc_num and answer_num and not numbers_close(calc_num, answer_num, tolerance=0.1):
                # Real error found!
                real_errors.append({
                    'story_id': story_id,
                    'story_title': story_title,
                    'question_num': q_idx,
                    'question': question.get('question'),
                    'context': story.get('content'),
                    'correct_answer': correct_answer,
                    'last_calc_step': last_step,
                    'berekening': berekening,
                    'calc_value': calc_num,
                    'answer_value': answer_num,
                    'difference': abs(calc_num - answer_num),
                    'all_options': [(i, opt.get('text')) for i, opt in enumerate(options)],
                    'correct_idx': correct_idx
                })

    print("="*80)
    print("🔍 ZOEKEN NAAR ECHTE REKENFOUTEN")
    print("="*80)
    print()
    print(f"Totaal aantal verhalen: {len(data)}")
    print(f"Totaal aantal vragen met berekeningen: {checked}")
    print(f"Aantal ECHTE rekenfouten gevonden: {len(real_errors)}")
    print()

    if real_errors:
        print("="*80)
        print("❌ GEVONDEN REKENFOUTEN:")
        print("="*80)

        for idx, err in enumerate(real_errors, 1):
            print(f"\n{'='*80}")
            print(f"{idx}. FOUT in Verhaal {err['story_id']}: {err['story_title']}")
            print(f"{'='*80}")
            print(f"Vraag {err['question_num']}: {err['question']}")
            print(f"\nContext: {err['context']}")
            print()
            print(f"Alle antwoordopties:")
            for i, opt_text in err['all_options']:
                marker = " ✓ GEMARKEERD ALS CORRECT" if i == err['correct_idx'] else ""
                print(f"   [{i}] {opt_text}{marker}")
            print()
            print(f"Berekening volgens JSON:")
            for stap in err['berekening']:
                print(f"   • {stap}")
            print()
            print(f"❌ PROBLEEM:")
            print(f"   Berekend: {err['calc_value']} (uit: {err['last_calc_step']})")
            print(f"   Gemarkeerd als correct: {err['answer_value']} (uit: {err['correct_answer']})")
            print(f"   Verschil: {err['difference']:.2f}")
            print()

    else:
        print("✅ GEEN REKENFOUTEN GEVONDEN!")
        print("Alle numerieke waarden komen overeen met de berekeningen!")

    return len(real_errors)

if __name__ == '__main__':
    exit(main())
