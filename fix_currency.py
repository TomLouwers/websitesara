#!/usr/bin/env python3
"""
Fix currency formatting: €28,0 -> €28,00
"""

import json
import re

def fix_currency_format(text):
    """Fix currency that has only 1 decimal to have 2 decimals"""
    # Pattern: €number,single_digit followed by " or end of string
    pattern = r'€(\d+),(\d)(?=["\s]|$)'

    def replacer(match):
        integer_part = match.group(1)
        decimal_part = match.group(2)
        return f'€{integer_part},{decimal_part}0'

    return re.sub(pattern, replacer, text)

def main():
    filepath = '/home/user/websitesara/verhaaltjessommen - Template.json'

    print("Loading template file...")
    with open(filepath, 'r', encoding='utf-8') as f:
        problems = json.load(f)

    print(f"Fixing currency formatting in {len(problems)} problems...")

    # Process each problem
    for problem in problems:
        for question in problem.get('questions', []):
            # Fix options
            if 'options' in question:
                fixed_options = []
                for option in question['options']:
                    fixed = fix_currency_format(option)
                    fixed_options.append(fixed)
                question['options'] = fixed_options

    print("Saving fixed version...")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)

    print("✓ Currency formatting fixed!")

if __name__ == '__main__':
    main()
