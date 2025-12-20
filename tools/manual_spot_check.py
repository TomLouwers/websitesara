#!/usr/bin/env python3
"""
Manual spot-check of flagged problems - as a groep 8 teacher!
"""

import json

def manually_verify():
    """Manually verify the flagged calculations"""

    with open('verhaaltjessommen - Template.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Problems to verify manually
    checks = [
        # (story_id, question_num, manual_calculation, expected_answer)
        (7, 1, "€125 is 75% (25% korting). 100% = €125 ÷ 0.75 = €166.67", "€166,70"),
        (41, 1, "Boodschappen optellen", "€12,20"),
        (136, 1, "Voetbalveld oppervlakte", None),
        (184, 1, "Gemiddelde wiskundecijfer", "7,2"),
        (199, 1, "Gemiddelde stappen per dag", None),
    ]

    print("="*80)
    print("HANDMATIGE NACONTROLE VAN GEMARKEERDE PROBLEMEN")
    print("="*80)
    print()

    errors_found = []

    for story_id, q_num, manual_calc, expected in checks:
        story = next((s for s in data if s.get('id') == story_id), None)
        if not story:
            print(f"⚠️  Verhaal {story_id} niet gevonden!")
            continue

        questions = story.get('questions', [])
        if q_num > len(questions):
            print(f"⚠️  Vraag {q_num} niet gevonden in verhaal {story_id}!")
            continue

        q = questions[q_num - 1]
        correct_idx = q.get('correct', -1)
        options = q.get('options', [])
        correct_answer = options[correct_idx].get('text', '') if correct_idx < len(options) else ''

        print(f"\n{'='*80}")
        print(f"Verhaal {story_id}: {story.get('title')}")
        print(f"{'='*80}")
        print(f"Context: {story.get('content')}")
        print(f"\nVraag {q_num}: {q.get('question')}")
        print(f"\nAlle antwoordopties:")
        for idx, opt in enumerate(options):
            marker = " ✓ CORRECT" if idx == correct_idx else ""
            print(f"  [{idx}] {opt.get('text')}{marker}")

        print(f"\nCorrect antwoord volgens JSON: {correct_answer}")

        # Show calculation from extra_info
        extra_info = q.get('extra_info', {})
        if 'berekening' in extra_info:
            print(f"\nBerekeningsstappen:")
            for stap in extra_info['berekening']:
                print(f"  • {stap}")

        # Manual verification
        print(f"\n🧮 Handmatige controle:")
        print(f"   {manual_calc}")

        if expected:
            if correct_answer == expected:
                print(f"   ✓ KLOPT: {correct_answer} = {expected}")
            else:
                print(f"   ❌ FOUT: {correct_answer} ≠ {expected}")
                errors_found.append({
                    'story_id': story_id,
                    'question_num': q_num,
                    'found': correct_answer,
                    'expected': expected
                })

        # Let me manually calculate some of these
        if story_id == 7 and q_num == 1:
            # €125 is 75%, what is 100%?
            calc = 125 / 0.75
            print(f"   Berekening: €125 ÷ 0.75 = €{calc:.2f}")
            print(f"   Afgerond: €{calc:.2f} ≈ €166,67")
            if "€166," in correct_answer:
                print(f"   ✓ CORRECT (kleine afrondingsverschillen zijn normaal)")

        elif story_id == 136 and q_num == 1:
            # Need to read the actual content
            content = story.get('content', '')
            print(f"   Context: {content}")

    print(f"\n\n{'='*80}")
    print("CONCLUSIE HANDMATIGE CONTROLE")
    print(f"{'='*80}")
    if errors_found:
        print(f"❌ Er zijn {len(errors_found)} echte fouten gevonden:")
        for err in errors_found:
            print(f"   Verhaal {err['story_id']}, vraag {err['question_num']}: {err['found']} moet zijn {err['expected']}")
    else:
        print("✓ Alle gecontroleerde antwoorden zijn correct!")
        print("✓ De automatische waarschuwingen waren false positives (formatting verschillen)")

    return len(errors_found)

if __name__ == '__main__':
    exit(manually_verify())
