#!/usr/bin/env python3
import json
from collections import Counter

def analyze_file(filename):
    print(f"\n{'='*60}")
    print(f"Analyzing: {filename}")
    print(f"{'='*60}")

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    correct_answers = []

    # Extract correct answers from all questions
    for item in data:
        if 'questions' in item:
            for question in item['questions']:
                if 'correct' in question:
                    # Convert 0-based index to 1-based (0->1, 1->2, 2->3, 3->4)
                    correct_answers.append(question['correct'] + 1)

    # Count occurrences
    answer_counts = Counter(correct_answers)
    total = len(correct_answers)

    print(f"\nTotal questions: {total}")
    print(f"\nCorrect Answer Distribution:")
    print(f"{'-'*40}")

    # Sort by answer option (1, 2, 3, 4 or A, B, C, D)
    for answer in sorted(answer_counts.keys()):
        count = answer_counts[answer]
        percentage = (count / total * 100) if total > 0 else 0
        bar = '█' * int(percentage / 2)
        print(f"{answer}: {count:4d} ({percentage:5.1f}%) {bar}")

    # Check for problematic distribution
    if total > 0:
        max_percentage = max(answer_counts.values()) / total * 100
        if max_percentage > 40:
            print(f"\n⚠️  WARNING: Answer '{max(answer_counts, key=answer_counts.get)}' appears {max_percentage:.1f}% of the time!")
            print("   This is significantly higher than expected (should be ~25% for 4 options)")

# Analyze both files
analyze_file('verhaaltjessommen - Template.json')
analyze_file('verhaaltjessommen_Template8_CITO_reworked.json')
