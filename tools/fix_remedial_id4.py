#!/usr/bin/env python3
"""
Fill in remedial_basis_id for time conversion errors in ID 4.
Link conversiefout to ID 11 (Tijd omrekenen: uren naar minuten) from basisvaardigheden.
"""

import json

def fix_remedial_id4(data):
    """Add remedial_basis_id to conversion errors in ID 4."""

    fixes_count = 0

    for item in data:
        if item.get('id') != 4:
            continue

        print(f"ID 4: {item.get('title')}")

        if 'questions' not in item:
            continue

        for q_idx, question in enumerate(item['questions'], start=1):
            if 'options' not in question:
                continue

            for opt_idx, option in enumerate(question['options']):
                error_type = option.get('error_type', '')

                # Check if this is a conversion error without remedial link
                if error_type == 'conversiefout':
                    current_remedial = option.get('remedial_basis_id')

                    if current_remedial is None:
                        # Link to ID 11: Tijd omrekenen (uren naar minuten)
                        option['remedial_basis_id'] = 11
                        fixes_count += 1

                        print(f"  ✅ Vraag {q_idx}, Optie {opt_idx}: remedial_basis_id = 11")
                        print(f"     '{option['text']}'")

    return fixes_count


def main():
    # Read JSON
    with open('verhaaltjessommen - Template.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Fix remedial links
    fixes = fix_remedial_id4(data)

    # Write back
    with open('verhaaltjessommen - Template.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Report
    print(f"\n✅ Remedial loop ingevuld!")
    print(f"   {fixes} conversiefout opties gekoppeld aan ID 11 (Tijd omrekenen)")


if __name__ == '__main__':
    main()
