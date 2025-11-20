#!/usr/bin/env python3
"""
Check which questions are missing extra_info
"""

import json

def main():
    filepath = '/home/user/websitesara/verhaaltjessommen - Template.json'

    with open(filepath, 'r', encoding='utf-8') as f:
        problems = json.load(f)

    print("Problems without complete extra_info:\n")

    for problem in problems:
        problem_id = problem.get('id')
        title = problem.get('title')

        missing_questions = []
        for question_idx, question in enumerate(problem.get('questions', [])):
            if 'extra_info' not in question:
                missing_questions.append(question_idx)

        if missing_questions:
            print(f"ID {problem_id}: {title}")
            print(f"  Missing tips for question(s): {missing_questions}")
            for idx in missing_questions:
                print(f"    Q{idx}: {problem['questions'][idx]['question']}")
            print()

if __name__ == '__main__':
    main()
