#!/usr/bin/env python3
"""
Fix geometry exercises to use schema 2.0 answer format.

Converts:
    "correct_answer": "17 cm"

To:
    "answer": {
        "type": "single",
        "correct_index": 2
    }
"""

import json
import sys
from pathlib import Path


def find_correct_index(options, correct_answer):
    """Find the index of the correct answer in the options list."""
    # Handle both string and object formats for options
    for i, opt in enumerate(options):
        opt_text = opt if isinstance(opt, str) else opt.get('text', '')
        if opt_text == correct_answer:
            return i

    # If not found, raise error
    raise ValueError(f"Correct answer '{correct_answer}' not found in options: {options}")


def fix_exercise_file(file_path):
    """Fix a single exercise file."""
    print(f"\n📄 Processing: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items_fixed = 0
    errors = []

    for item in data.get('items', []):
        # Check if this item uses the old format
        if 'correct_answer' in item and 'answer' not in item:
            correct_answer = item['correct_answer']
            options = item.get('options', [])

            try:
                # Find the correct index
                correct_index = find_correct_index(options, correct_answer)

                # Add new format answer
                item['answer'] = {
                    'type': 'single',
                    'correct_index': correct_index
                }

                # Remove old format
                del item['correct_answer']

                items_fixed += 1
                print(f"   ✓ Fixed item {item.get('id', 'unknown')}: '{correct_answer}' → index {correct_index}")

            except ValueError as e:
                errors.append(f"Item {item.get('id', 'unknown')}: {e}")

    if errors:
        print(f"\n   ❌ Errors:")
        for error in errors:
            print(f"      {error}")
        return False, items_fixed, errors

    if items_fixed > 0:
        # Write back the fixed file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"   ✅ Fixed {items_fixed} items in {file_path.name}")
        return True, items_fixed, []
    else:
        print(f"   ℹ️  No items to fix in {file_path.name}")
        return True, 0, []


def main():
    """Fix all geometry exercise files."""
    # Find all geometry core files
    mk_dir = Path('data-v2/exercises/mk')

    if not mk_dir.exists():
        print(f"❌ Error: Directory {mk_dir} not found")
        sys.exit(1)

    core_files = sorted(mk_dir.glob('*_core.json'))

    if not core_files:
        print(f"❌ Error: No *_core.json files found in {mk_dir}")
        sys.exit(1)

    print(f"🔧 Found {len(core_files)} geometry exercise files to check\n")
    print("=" * 60)

    total_fixed = 0
    total_files_fixed = 0
    all_errors = []

    for file_path in core_files:
        success, items_fixed, errors = fix_exercise_file(file_path)

        if success and items_fixed > 0:
            total_files_fixed += 1
            total_fixed += items_fixed

        if errors:
            all_errors.extend(errors)

    print("\n" + "=" * 60)
    print("\n📊 SUMMARY:")
    print(f"   Files processed: {len(core_files)}")
    print(f"   Files fixed: {total_files_fixed}")
    print(f"   Items fixed: {total_fixed}")

    if all_errors:
        print(f"\n   ⚠️  Errors encountered: {len(all_errors)}")
        for error in all_errors:
            print(f"      {error}")
        sys.exit(1)
    else:
        print(f"\n   ✅ All files processed successfully!")
        sys.exit(0)


if __name__ == '__main__':
    main()
