#!/usr/bin/env python3
"""
Find exercises with quality scores below threshold.
"""

import json
import sys
from pathlib import Path

def get_quality_from_validation():
    """Parse all exercises and estimate quality."""
    exercises_dir = Path('data-v2/exercises')
    low_quality = []

    for exercise_file in exercises_dir.rglob('*_core.json'):
        try:
            with open(exercise_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            metadata = data.get('metadata', {})
            items = data.get('items', [])

            # Count items with support
            has_hints = 0
            has_feedback = 0

            for item in items:
                support = item.get('support', {})
                if support.get('hints'):
                    has_hints += 1
                if support.get('option_feedback'):
                    has_feedback += 1

            total = len(items)
            if total == 0:
                continue

            # Estimate quality
            hints_pct = (has_hints / total) * 100
            feedback_pct = (has_feedback / total) * 100
            quality_estimate = (hints_pct + feedback_pct) / 2

            exercise_id = metadata.get('id', exercise_file.stem)

            if quality_estimate < 60:
                low_quality.append({
                    'file': str(exercise_file),
                    'id': exercise_id,
                    'quality': quality_estimate,
                    'total_items': total,
                    'with_hints': has_hints,
                    'with_feedback': has_feedback
                })

        except Exception as e:
            print(f"Error reading {exercise_file}: {e}", file=sys.stderr)

    # Sort by quality (lowest first)
    low_quality.sort(key=lambda x: x['quality'])

    return low_quality

if __name__ == '__main__':
    exercises = get_quality_from_validation()

    print(f"\n📊 Found {len(exercises)} exercises with quality < 60%\n")
    print("=" * 80)
    print(f"{'Exercise ID':<30} {'Quality':<10} {'Items':<8} {'Hints':<8} {'Feedback':<10}")
    print("=" * 80)

    for ex in exercises:
        print(f"{ex['id']:<30} {ex['quality']:>6.1f}%  {ex['total_items']:>6}  {ex['with_hints']:>6}  {ex['with_feedback']:>8}")

    print("=" * 80)
    print(f"\nTotal: {len(exercises)} exercises need enrichment")

    # Show summary
    if exercises:
        avg_quality = sum(e['quality'] for e in exercises) / len(exercises)
        print(f"Average quality of low-scoring exercises: {avg_quality:.1f}%")
        print(f"\nWorst 5 exercises:")
        for ex in exercises[:5]:
            print(f"  - {ex['id']} ({ex['quality']:.1f}%): {ex['file']}")
