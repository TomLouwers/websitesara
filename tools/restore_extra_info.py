#!/usr/bin/env python3
"""
Restore extra_info sections from the original template while keeping other improvements
"""

import json

def main():
    print("Loading original template (with extra_info)...")
    with open('/tmp/original_template.json', 'r', encoding='utf-8') as f:
        original = json.load(f)

    print("Loading improved template (without extra_info)...")
    with open('/home/user/websitesara/verhaaltjessommen - Template.json', 'r', encoding='utf-8') as f:
        improved = json.load(f)

    print(f"Original has {len(original)} problems")
    print(f"Improved has {len(improved)} problems")

    # Create a mapping of original problems by ID
    original_by_id = {p['id']: p for p in original}

    # Restore extra_info for matching problems
    restored_count = 0
    for problem in improved:
        problem_id = problem.get('id')

        # Only restore for problems that existed in original
        if problem_id in original_by_id:
            original_problem = original_by_id[problem_id]

            # Match questions and restore extra_info
            for i, question in enumerate(problem.get('questions', [])):
                if i < len(original_problem.get('questions', [])):
                    original_question = original_problem['questions'][i]

                    # Restore extra_info if it exists in original
                    if 'extra_info' in original_question:
                        question['extra_info'] = original_question['extra_info']
                        restored_count += 1

    print(f"Restored extra_info for {restored_count} questions")

    # Save the restored version
    print("Saving restored version...")
    with open('/home/user/websitesara/verhaaltjessommen - Template.json', 'w', encoding='utf-8') as f:
        json.dump(improved, f, ensure_ascii=False, indent=2)

    print("✓ Extra info restored successfully!")
    print(f"  New problems (without extra_info): {len(improved) - len(original)}")

if __name__ == '__main__':
    main()
