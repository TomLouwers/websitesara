#!/usr/bin/env python3
"""
Script to fix the distribution of correct answers in begrijpend lezen exercises.
Redistributes correct answers evenly across options A, B, C, D.
"""

import json
import os
import random
from collections import Counter

def fix_answer_distribution(file_path):
    """Fix the correct answer distribution in a single file."""

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # First pass: collect all questions
    all_questions = []
    for story in data:
        if 'questions' not in story:
            continue
        for question in story['questions']:
            if 'options' not in question or len(question['options']) != 4:
                continue
            all_questions.append(question)

    total_questions = len(all_questions)

    # Create a balanced list of target indices
    # For perfect distribution, we want exactly 25% for each option
    target_per_option = total_questions // 4
    remainder = total_questions % 4

    # Create balanced distribution
    target_indices = []
    for i in range(4):
        count = target_per_option + (1 if i < remainder else 0)
        target_indices.extend([i] * count)

    # Shuffle the target indices to randomize
    # Use filename-based seed for different patterns per file but reproducibility
    random.seed(hash(file_path))
    random.shuffle(target_indices)

    # Apply the new distribution
    for idx, question in enumerate(all_questions):
        # Find the current correct answer
        current_correct_idx = None
        for opt_idx, opt in enumerate(question['options']):
            if opt.get('is_correct', False):
                current_correct_idx = opt_idx
                break

        if current_correct_idx is None:
            print(f"Warning: No correct answer found in question {question.get('item_id', '?')}")
            continue

        target_idx = target_indices[idx]

        # If we need to change the correct answer
        if current_correct_idx != target_idx:
            # Swap the is_correct flags
            question['options'][current_correct_idx]['is_correct'] = False
            question['options'][target_idx]['is_correct'] = True

    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return total_questions


def analyze_distribution(file_path):
    """Analyze the correct answer distribution in a file."""

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    correct_answers = []
    for story in data:
        if 'questions' in story:
            for q in story['questions']:
                if 'options' in q:
                    for opt in q['options']:
                        if opt.get('is_correct', False):
                            correct_answers.append(opt['label'])

    return Counter(correct_answers), len(correct_answers)


def main():
    """Main function to fix all bl_ files."""

    bl_dir = 'exercises/bl'
    files = sorted([f for f in os.listdir(bl_dir) if f.startswith('bl_') and f.endswith('.json')])

    print("=" * 60)
    print("BEFORE FIX:")
    print("=" * 60)

    for file in files:
        file_path = os.path.join(bl_dir, file)
        dist, total = analyze_distribution(file_path)
        print(f"\n{file}:")
        print(f"Total questions: {total}")
        for label in ['A', 'B', 'C', 'D']:
            count = dist.get(label, 0)
            pct = (count/total*100) if total > 0 else 0
            print(f"  {label}: {count:3d} ({pct:5.1f}%)")

    print("\n" + "=" * 60)
    print("FIXING FILES...")
    print("=" * 60)

    for file in files:
        file_path = os.path.join(bl_dir, file)
        questions = fix_answer_distribution(file_path)
        print(f"Fixed {file} ({questions} questions)")

    print("\n" + "=" * 60)
    print("AFTER FIX:")
    print("=" * 60)

    for file in files:
        file_path = os.path.join(bl_dir, file)
        dist, total = analyze_distribution(file_path)
        print(f"\n{file}:")
        print(f"Total questions: {total}")
        for label in ['A', 'B', 'C', 'D']:
            count = dist.get(label, 0)
            pct = (count/total*100) if total > 0 else 0
            print(f"  {label}: {count:3d} ({pct:5.1f}%)")


if __name__ == '__main__':
    main()
