#!/usr/bin/env python3
import json
import random
from collections import Counter
import sys

def analyze_distribution(data):
    """Analyze the current distribution of correct answers."""
    correct_answers = []
    for item in data:
        if 'questions' in item:
            for question in item['questions']:
                if 'correct' in question:
                    correct_answers.append(question['correct'])
    return Counter(correct_answers)

def rebalance_answers(data, seed=42):
    """
    Rebalance the answer distribution by shuffling options.

    Strategy:
    - For each question, shuffle the options array
    - Update the 'correct' index to point to the new position
    - Ensure all option data (text, foutanalyse) moves with the option
    """
    random.seed(seed)

    # Count questions
    total_questions = sum(len(item.get('questions', [])) for item in data)
    target_per_position = total_questions // 4

    # Track how many times each position should be correct
    target_distribution = {0: target_per_position, 1: target_per_position,
                          2: target_per_position, 3: target_per_position}

    # Add remainder to first positions
    remainder = total_questions % 4
    for i in range(remainder):
        target_distribution[i] += 1

    print(f"\nTarget distribution for {total_questions} questions:")
    for pos, count in sorted(target_distribution.items()):
        print(f"  Position {pos+1}: {count} questions ({count/total_questions*100:.1f}%)")

    # Track actual distribution as we go
    actual_distribution = {0: 0, 1: 0, 2: 0, 3: 0}

    # Create a list of desired target positions
    desired_positions = []
    for position, count in target_distribution.items():
        desired_positions.extend([position] * count)

    # Shuffle to randomize which questions get which positions
    random.shuffle(desired_positions)

    # Apply the rebalancing
    question_index = 0
    for item in data:
        if 'questions' in item:
            for question in item['questions']:
                if 'correct' in question and 'options' in question:
                    current_correct = question['correct']
                    target_correct = desired_positions[question_index]

                    # If we need to move the correct answer to a different position
                    if current_correct != target_correct:
                        options = question['options']

                        # Swap the current correct answer with the target position
                        options[current_correct], options[target_correct] = \
                            options[target_correct], options[current_correct]

                        # Update the correct index
                        question['correct'] = target_correct

                    actual_distribution[question['correct']] += 1
                    question_index += 1

    print(f"\nActual distribution after rebalancing:")
    for pos, count in sorted(actual_distribution.items()):
        print(f"  Position {pos+1}: {count} questions ({count/total_questions*100:.1f}%)")

    return data

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 rebalance_answers.py <input_file> [output_file]")
        print("If output_file is not specified, will overwrite input_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file

    print(f"{'='*60}")
    print(f"Rebalancing: {input_file}")
    print(f"{'='*60}")

    # Load the data
    print(f"\nLoading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Show original distribution
    print(f"\nOriginal distribution:")
    original_dist = analyze_distribution(data)
    total = sum(original_dist.values())
    for pos in sorted(original_dist.keys()):
        count = original_dist[pos]
        print(f"  Position {pos+1}: {count} questions ({count/total*100:.1f}%)")

    # Rebalance
    print(f"\nRebalancing...")
    rebalanced_data = rebalance_answers(data)

    # Save the result
    print(f"\nSaving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rebalanced_data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Successfully rebalanced and saved to {output_file}")

    # Verify
    print(f"\nVerifying...")
    final_dist = analyze_distribution(rebalanced_data)
    print(f"Final distribution:")
    for pos in sorted(final_dist.keys()):
        count = final_dist[pos]
        print(f"  Position {pos+1}: {count} questions ({count/total*100:.1f}%)")

if __name__ == "__main__":
    main()
