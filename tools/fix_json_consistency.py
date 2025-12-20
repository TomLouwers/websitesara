#!/usr/bin/env python3
"""
Fix JSON consistency issues:
1. Remove redundant 'correct' field from all questions
2. Remove 'correct' field from all options (use 'is_correct' instead)
3. Convert complex 'verhoudingstabel' objects to simple Markdown 'berekening_tabel'
"""

import json

def verhoudingstabel_to_markdown(verhoudingstabel):
    """Convert complex verhoudingstabel object to Markdown table array."""

    if not isinstance(verhoudingstabel, dict):
        return None

    # Build Markdown table
    table = []
    table.append("| Stap | Bewerking | Uitkomst |")
    table.append("|------|-----------|----------|")

    kolommen = verhoudingstabel.get('kolommen', [])

    # Extract steps from columns
    for idx, col in enumerate(kolommen, start=1):
        label = col.get('label', f'Stap {idx}')
        waarde = col.get('waarde', '')
        eenheid = col.get('eenheid', '')
        berekening = col.get('berekening', '')

        # Build bewerking cell
        if berekening:
            bewerking = berekening
        else:
            bewerking = label

        # Build uitkomst cell
        uitkomst = f"{waarde} {eenheid}".strip()

        # Mark final answer with star
        if label.lower() in ['antwoord', 'totaal', 'resultaat']:
            uitkomst = f"**{uitkomst}** ⭐"

        table.append(f"| {idx}. {label.capitalize()} | {bewerking} | {uitkomst} |")

    return table if len(table) > 2 else None


def fix_consistency(data):
    """Fix all consistency issues in the data."""

    fixes_count = {
        'correct_field_removed_questions': 0,
        'correct_field_removed_options': 0,
        'verhoudingstabel_converted': 0,
        'verhoudingstabel_removed': 0
    }

    for item in data:
        if 'questions' not in item:
            continue

        for question in item['questions']:
            # Fix 1: Remove 'correct' field from question level
            if 'correct' in question:
                del question['correct']
                fixes_count['correct_field_removed_questions'] += 1

            # Fix 2: Remove 'correct' field from options (keep 'is_correct')
            if 'options' in question:
                for option in question['options']:
                    if 'correct' in option:
                        del option['correct']
                        fixes_count['correct_field_removed_options'] += 1

            # Fix 3: Handle verhoudingstabel
            if 'extra_info' in question:
                extra_info = question['extra_info']

                has_verhoudingstabel = 'verhoudingstabel' in extra_info
                has_berekening_tabel = 'berekening_tabel' in extra_info

                if has_verhoudingstabel:
                    if has_berekening_tabel:
                        # Both exist: remove verhoudingstabel
                        del extra_info['verhoudingstabel']
                        fixes_count['verhoudingstabel_removed'] += 1
                    else:
                        # Only verhoudingstabel: convert to berekening_tabel
                        markdown_table = verhoudingstabel_to_markdown(extra_info['verhoudingstabel'])
                        if markdown_table:
                            extra_info['berekening_tabel'] = markdown_table
                            del extra_info['verhoudingstabel']
                            fixes_count['verhoudingstabel_converted'] += 1

    return fixes_count


def main():
    # Read JSON
    with open('verhaaltjessommen - Template.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Fix consistency issues
    fixes = fix_consistency(data)

    # Write back
    with open('verhaaltjessommen - Template.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Report
    print("✅ JSON consistentie gefixed!")
    print(f"\n📊 Overzicht:")
    print(f"   • 'correct' veld verwijderd uit {fixes['correct_field_removed_questions']} vragen")
    print(f"   • 'correct' veld verwijderd uit {fixes['correct_field_removed_options']} opties")
    print(f"   • {fixes['verhoudingstabel_converted']} verhoudingstabel objecten geconverteerd naar Markdown")
    print(f"   • {fixes['verhoudingstabel_removed']} redundante verhoudingstabel velden verwijderd")


if __name__ == '__main__':
    main()
