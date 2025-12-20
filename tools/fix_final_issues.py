#!/usr/bin/env python3
"""
Fix final CITO-conformity issues:
1. ID 32: Fix modus problem (both 6 and 8 appear 3 times)
2. ID 12: Fix rounding (€30,40 → €30,43)
3. Standardize thousand separators (1200 → 1.200)
"""

import json
import re

def fix_problem_32(problem):
    """Fix modus problem: make 8 points clearly the most frequent"""
    if problem.get('id') == 32:
        # Change table so 8 points appears 4 times instead of 3
        problem['visual']['rows'] = [
            ["6 punten", 3],
            ["7 punten", 2],
            ["8 punten", 4],  # Changed from 3 to 4
            ["9 punten", 2],
            ["10 punten", 2]
        ]

        # Update question 2 - total children is now 13 instead of 12
        problem['questions'][1]['options'] = [
            "11 kinderen",
            "12 kinderen",
            "13 kinderen",
            "15 kinderen"
        ]
        problem['questions'][1]['correct'] = 2  # Now 13 kinderen
        problem['questions'][1]['extra_info']['tips'] = [
            "Tel het aantal keer op uit de tabel",
            "3 + 2 + 4 + 2 + 2 = 13 kinderen",
            "Er hebben 13 kinderen geschoten"
        ]

        # Update question 1 tips
        problem['questions'][0]['extra_info']['tips'] = [
            "Zoek de hoogste waarde in de tabel",
            "De scores zijn: 6 punten (3×), 7 punten (2×), 8 punten (4×), 9 punten (2×), 10 punten (2×)",
            "De hoogste score is 10 punten"
        ]

        # Update question 3 tips - now 8 is clearly the mode
        problem['questions'][2]['extra_info']['tips'] = [
            "Tel hoe vaak elke score voorkomt:",
            "6 punten: 3×, 7 punten: 2×, 8 punten: 4×, 9 punten: 2×, 10 punten: 2×",
            "8 punten komt het vaakst voor (4 keer), dit is de modus"
        ]

        print("  ✓ Fixed id 32: Made 8 points clearly the mode (4×)")
    return problem

def fix_problem_12(problem):
    """Fix rounding: use exact amount €30,43 instead of €30,40"""
    if problem.get('id') == 12:
        # Change answer options to include exact amount
        problem['questions'][1]['options'] = [
            "€30,43",
            "€30,60",
            "€32,30",
            "€35,80"
        ]
        # Correct answer stays at index 0 (now €30,43)

        # Tips already show €30,43, which is correct
        print("  ✓ Fixed id 12: Changed €30,40 to exact amount €30,43")
    return problem

def standardize_thousands(problems):
    """Standardize thousand separators to 1.200 format"""
    fixes = 0

    for problem in problems:
        # Check content
        if 'content' in problem:
            original = problem['content']
            # Replace standalone numbers like 1200, 2500 with 1.200, 2.500
            problem['content'] = re.sub(r'\b(\d)(\d{3})\b', r'\1.\2', problem['content'])
            if original != problem['content']:
                fixes += 1

        # Check table data
        if 'visual' in problem and 'rows' in problem['visual']:
            for row in problem['visual']['rows']:
                for i, cell in enumerate(row):
                    if isinstance(cell, int) and cell >= 1000:
                        # Format with thousand separator
                        row[i] = f"{cell:,}".replace(',', '.')

        # Check questions and options
        for question in problem.get('questions', []):
            # Check question text
            if 'question' in question:
                original = question['question']
                question['question'] = re.sub(r'\b(\d)(\d{3})\b', r'\1.\2', question['question'])
                if original != question['question']:
                    fixes += 1

            # Check options
            if 'options' in question:
                for i, option in enumerate(question['options']):
                    original = option
                    # Match patterns like "1200" or "1200 views" but not currency or decimals
                    if isinstance(option, str):
                        # Only fix plain numbers, not currency (€) or percentages (%)
                        if '€' not in option and '%' not in option:
                            option = re.sub(r'\b(\d)(\d{3})(?=\s|$)', r'\1.\2', option)
                            if original != option:
                                question['options'][i] = option
                                fixes += 1

    if fixes > 0:
        print(f"  ✓ Standardized {fixes} thousand separators to CITO format (1.200)")
    else:
        print("  ✓ Thousand separators already consistent")

    return problems

def find_inconsistent_thousands(problems):
    """Find numbers >= 1000 without proper separator"""
    print("\nScanning for inconsistent thousand separators:")
    issues = []

    for problem in problems:
        problem_id = problem.get('id')
        title = problem.get('title')

        # Check content
        if 'content' in problem:
            matches = re.findall(r'\b\d{4,}\b', problem['content'])
            if matches:
                for match in matches:
                    if '.' not in match:
                        issues.append(f"  ID {problem_id} ({title}): content has '{match}'")

        # Check questions
        for q_idx, question in enumerate(problem.get('questions', [])):
            for option in question.get('options', []):
                if isinstance(option, str):
                    # Find 4+ digit numbers without separator
                    matches = re.findall(r'\b\d{4,}\b', option)
                    for match in matches:
                        if '€' not in option and '.' not in match:
                            issues.append(f"  ID {problem_id} ({title}) Q{q_idx+1}: '{option}'")
                            break

    if issues:
        for issue in issues[:10]:
            print(issue)
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
    else:
        print("  ✓ All consistent")

    return len(issues)

def main():
    print("Loading template file...")
    filepath = '/home/user/websitesara/verhaaltjessommen - Template.json'

    with open(filepath, 'r', encoding='utf-8') as f:
        problems = json.load(f)

    print(f"Found {len(problems)} problems\n")

    # Find issues first
    find_inconsistent_thousands(problems)

    print("\n" + "="*60)
    print("Applying fixes:")
    print("="*60 + "\n")

    # Apply all fixes
    fixed_problems = []
    for problem in problems:
        problem = fix_problem_32(problem)
        problem = fix_problem_12(problem)
        fixed_problems.append(problem)

    # Standardize thousands across all problems
    fixed_problems = standardize_thousands(fixed_problems)

    print("\n" + "="*60)
    print("Saving fixed version...")
    print("="*60 + "\n")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(fixed_problems, f, ensure_ascii=False, indent=2)

    print("✓ All final fixes applied!")
    print("\nSummary:")
    print("  • ID 32: Fixed modus (8 points now appears 4× instead of 3×)")
    print("  • ID 12: Changed €30,40 to exact €30,43")
    print("  • Standardized thousand separators throughout")

if __name__ == '__main__':
    main()
