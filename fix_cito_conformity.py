#!/usr/bin/env python3
"""
Fix CITO-conformity issues:
1. id 12: Remove duplicate €35,80
2. id 14: Fix €1,7,00 typo -> €864,00
3. id 24: Fix "1,0 views" format -> proper numbers
4. id 29: Fix 73 vs 74 hour calculation
5. id 32: Fix tips with wrong scores
"""

import json

def fix_problem_12(problem):
    """Fix duplicate €35,80 option"""
    if problem.get('id') == 12:
        # Change options to be unique
        question = problem['questions'][0]
        question['options'] = [
            "€26,85",
            "€35,80",
            "€39,20",
            "€44,75"
        ]
        # Correct answer is still index 1 (€35,80)
        print("  ✓ Fixed id 12: Removed duplicate €35,80")
    return problem

def fix_problem_14(problem):
    """Fix €1,7,00 typo -> €864,00"""
    if problem.get('id') == 14:
        question = problem['questions'][2]
        # 192 tegels × €4,50 = €864,00
        question['options'] = [
            "€216,00",
            "€432,00",
            "€864,00",
            "€1.728,00"
        ]
        # Correct answer is still index 2 (€864,00)
        print("  ✓ Fixed id 14: Changed €1,7,00 to €1.728,00")
    return problem

def fix_problem_24(problem):
    """Fix "1,0 views" format to proper CITO numbers"""
    if problem.get('id') == 24:
        question = problem['questions'][0]
        # Total is 240 + 180 + 320 + 200 + 260 = 1200 views
        question['options'] = [
            "900",
            "1.000",
            "1.200",
            "1.300"
        ]
        # Correct answer is still index 2 (1.200)

        # Update tips to match
        question['extra_info']['tips'] = [
            "Tel alle views bij elkaar op",
            "240 + 180 + 320 + 200 + 260 = 1.200"
        ]
        print("  ✓ Fixed id 24: Changed '1,0 views' format to proper numbers")
    return problem

def fix_problem_29(problem):
    """Fix 73 vs 74 hour issue - correct answer should be 73"""
    if problem.get('id') == 29:
        question = problem['questions'][2]
        # Calculation: 3×2 + 5×3 + 8×4 + 4×5 = 6 + 15 + 32 + 20 = 73
        question['options'] = [
            "68 uur",
            "73 uur",
            "80 uur",
            "86 uur"
        ]
        # Correct answer changes to index 1 (73 uur)
        question['correct'] = 1

        # Fix tips to show correct calculation
        question['extra_info']['tips'] = [
            "Bereken per groep het totaal aantal uren:",
            "3 leerlingen × 2 uur = 6 uur",
            "5 leerlingen × 3 uur = 15 uur",
            "8 leerlingen × 4 uur = 32 uur",
            "4 leerlingen × 5 uur = 20 uur",
            "Totaal: 6 + 15 + 32 + 20 = 73 uur"
        ]
        print("  ✓ Fixed id 29: Corrected 74→73 uur and tips calculation")
    return problem

def fix_problem_32(problem):
    """Fix tips with incorrect score list"""
    if problem.get('id') == 32:
        question = problem['questions'][0]
        # Fix tips to match the actual table data
        question['extra_info']['tips'] = [
            "Zoek de hoogste waarde in de tabel",
            "De scores zijn: 6 punten (3×), 7 punten (2×), 8 punten (3×), 9 punten (2×), 10 punten (2×)",
            "De hoogste score is 10 punten"
        ]

        # Fix second question tips too
        question2 = problem['questions'][1]
        question2['extra_info']['tips'] = [
            "Tel het aantal keer op uit de tabel",
            "3 + 2 + 3 + 2 + 2 = 12 kinderen",
            "Er hebben 12 kinderen geschoten"
        ]
        print("  ✓ Fixed id 32: Corrected tips to match table data")
    return problem

def find_all_duplicates(problems):
    """Find all problems with duplicate answer options"""
    print("\nScanning for duplicate answer options:")
    found_duplicates = False

    for problem in problems:
        problem_id = problem.get('id')
        title = problem.get('title')

        for q_idx, question in enumerate(problem.get('questions', [])):
            options = question.get('options', [])
            unique_options = set(options)

            if len(unique_options) < len(options):
                print(f"  ⚠ ID {problem_id} ({title}), Question {q_idx + 1}: Has duplicate options")
                print(f"    Options: {options}")
                found_duplicates = True

    if not found_duplicates:
        print("  ✓ No duplicates found")

    return found_duplicates

def find_notation_issues(problems):
    """Find inconsistent notation issues"""
    print("\nScanning for notation issues:")
    issues = []

    for problem in problems:
        problem_id = problem.get('id')
        title = problem.get('title')

        for q_idx, question in enumerate(problem.get('questions', [])):
            options = question.get('options', [])

            for opt in options:
                # Check for weird patterns like "1,0 views" or "1,1 bezoekers"
                if any(pattern in opt for pattern in ["1,0 ", "1,1 ", "0,5 bezoekers", "0,8 leerlingen"]):
                    issues.append(f"  ⚠ ID {problem_id} ({title}), Q{q_idx + 1}: '{opt}'")

    if issues:
        for issue in issues[:10]:  # Show first 10
            print(issue)
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more issues")
    else:
        print("  ✓ No obvious notation issues found")

def main():
    print("Loading template file...")
    filepath = '/home/user/websitesara/verhaaltjessommen - Template.json'

    with open(filepath, 'r', encoding='utf-8') as f:
        problems = json.load(f)

    print(f"Found {len(problems)} problems\n")

    # Find all issues first
    find_all_duplicates(problems)
    find_notation_issues(problems)

    print("\n" + "="*60)
    print("Applying fixes:")
    print("="*60 + "\n")

    # Apply all fixes
    fixed_problems = []
    for problem in problems:
        problem = fix_problem_12(problem)
        problem = fix_problem_14(problem)
        problem = fix_problem_24(problem)
        problem = fix_problem_29(problem)
        problem = fix_problem_32(problem)
        fixed_problems.append(problem)

    print("\n" + "="*60)
    print("Saving fixed version...")
    print("="*60 + "\n")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(fixed_problems, f, ensure_ascii=False, indent=2)

    print("✓ All CITO-conformity fixes applied!")
    print("\nSummary of fixes:")
    print("  • ID 12: Removed duplicate €35,80 option")
    print("  • ID 14: Fixed €1,7,00 → €1.728,00")
    print("  • ID 24: Fixed '1,0 views' → '1.200' (CITO format)")
    print("  • ID 29: Corrected 74→73 uur with proper calculation")
    print("  • ID 32: Fixed tips to match actual table data")

if __name__ == '__main__':
    main()
