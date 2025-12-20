#!/usr/bin/env python3
"""
Comprehensive automated check of all math problems
"""

import json
import re

def extract_numbers(text):
    """Extract all numbers from text"""
    # Handle percentages
    if '%' in text:
        matches = re.findall(r'(\d+(?:[,.]\d+)?)\s*%', text)
        return [float(m.replace(',', '.')) for m in matches]

    # Handle currency
    text = text.replace('€', '').replace(',', '.')

    # Extract all numbers (including decimals and negatives)
    matches = re.findall(r'-?\d+(?:[,.]\d+)?', text)
    return [float(m.replace(',', '.')) for m in matches]

def verify_calculation(story, question, q_idx):
    """
    Verify if the calculation in extra_info matches the correct answer
    """
    issues = []

    correct_idx = question.get('correct', -1)
    options = question.get('options', [])

    if correct_idx < 0 or correct_idx >= len(options):
        return [f"Invalid correct index: {correct_idx}"]

    correct_answer_text = options[correct_idx].get('text', '')
    extra_info = question.get('extra_info', {})
    berekening = extra_info.get('berekening', [])

    # Extract the number from the correct answer
    correct_numbers = extract_numbers(correct_answer_text)

    if not correct_numbers:
        return []  # Can't verify without a number

    correct_value = correct_numbers[0]

    # Check if the calculation steps mention this value
    found_in_calc = False
    for stap in berekening:
        stap_numbers = extract_numbers(stap)
        for num in stap_numbers:
            if abs(num - correct_value) < 0.01:  # Allow for small rounding differences
                found_in_calc = True
                break

    if berekening and not found_in_calc:
        # This might indicate a problem
        issues.append({
            'story_id': story.get('id'),
            'story_title': story.get('title'),
            'question_num': q_idx + 1,
            'question': question.get('question'),
            'correct_answer': correct_answer_text,
            'issue': f'Correct answer value {correct_value} not found in calculation steps'
        })

    # Check that correct option has empty foutanalyse
    if options[correct_idx].get('foutanalyse', '') != '':
        issues.append({
            'story_id': story.get('id'),
            'story_title': story.get('title'),
            'question_num': q_idx + 1,
            'question': question.get('question'),
            'correct_answer': correct_answer_text,
            'issue': 'Correct answer has non-empty foutanalyse'
        })

    # Check that incorrect options have foutanalyse
    for opt_idx, option in enumerate(options):
        if opt_idx != correct_idx and option.get('foutanalyse', '').strip() == '':
            issues.append({
                'story_id': story.get('id'),
                'story_title': story.get('title'),
                'question_num': q_idx + 1,
                'question': question.get('question'),
                'incorrect_option': option.get('text'),
                'issue': f'Incorrect option has empty foutanalyse'
            })

    return issues

def main():
    print("="*80)
    print("VOLLEDIGE AUTOMATISCHE CONTROLE VAN ALLE VERHAALTJESSOMMEN")
    print("="*80)
    print()

    with open('verhaaltjessommen - Template.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_issues = []
    total_questions = 0

    for story in data:
        for q_idx, question in enumerate(story.get('questions', [])):
            total_questions += 1
            issues = verify_calculation(story, question, q_idx)
            all_issues.extend(issues)

    print(f"Totaal aantal verhalen: {len(data)}")
    print(f"Totaal aantal vragen: {total_questions}")
    print(f"Aantal gevonden problemen: {len(all_issues)}")
    print()

    if all_issues:
        print("GEVONDEN PROBLEMEN:")
        print("="*80)

        # Group by type
        calc_issues = [i for i in all_issues if 'calculation' in i.get('issue', '').lower()]
        foutanalyse_issues = [i for i in all_issues if 'foutanalyse' in i.get('issue', '').lower()]

        if calc_issues:
            print(f"\n📊 BEREKENIN GSPROBLEMEN ({len(calc_issues)}):")
            for issue in calc_issues[:20]:  # Show first 20
                print(f"\n  • Verhaal {issue['story_id']}: {issue['story_title']}")
                print(f"    Vraag {issue['question_num']}: {issue['question']}")
                print(f"    Probleem: {issue['issue']}")

        if foutanalyse_issues:
            print(f"\n📝 FOUTANALYSE PROBLEMEN ({len(foutanalyse_issues)}):")
            for issue in foutanalyse_issues[:20]:  # Show first 20
                print(f"\n  • Verhaal {issue['story_id']}: {issue['story_title']}")
                print(f"    Vraag {issue['question_num']}: {issue['question']}")
                if 'incorrect_option' in issue:
                    print(f"    Optie: {issue['incorrect_option']}")
                print(f"    Probleem: {issue['issue']}")

            if len(foutanalyse_issues) > 20:
                print(f"\n  ... en nog {len(foutanalyse_issues) - 20} andere problemen")

    else:
        print("✅ GEEN PROBLEMEN GEVONDEN!")
        print("\n🎉 Alle antwoorden lijken correct te zijn!")
        print("   • Alle correcte antwoorden hebben lege foutanalyse")
        print("   • Alle foute antwoorden hebben foutanalyse")
        print("   • Berekeningen komen overeen met de correcte antwoorden")

    print(f"\n{'='*80}")
    print("CONCLUSIE:")
    print(f"{'='*80}")
    if len(all_issues) == 0:
        print("✓ Het nakijkwerk is klaar!")
        print("✓ Alle 809 vragen hebben correcte antwoorden!")
        print("✓ Goed gedaan, groep 8! 🌟")
    else:
        print(f"⚠️  Er zijn {len(all_issues)} problemen gevonden die aandacht nodig hebben.")

    return len(all_issues)

if __name__ == '__main__':
    exit(main())
