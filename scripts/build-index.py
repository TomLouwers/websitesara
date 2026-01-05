#!/usr/bin/env python3
"""
Build Exercise Index
====================

Rebuilds index.json for all exercises in production directory.

Usage:
    # Build index for default directory
    python3 scripts/build-index.py

    # Build index for specific directory
    python3 scripts/build-index.py --directory data-v2/exercises

    # Output to different location
    python3 scripts/build-index.py --output custom-index.json

Features:
- Scans all _core.json files recursively
- Extracts metadata (id, category, grade, level, etc.)
- Generates sortable, searchable index
- Validates JSON syntax before indexing
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import argparse


def build_index(exercises_dir: str, output_path: str = None) -> Dict:
    """
    Build exercise index from directory

    Args:
        exercises_dir: Directory containing exercises
        output_path: Optional custom output path

    Returns:
        Index data dictionary
    """
    exercises_path = Path(exercises_dir)

    if not exercises_path.exists():
        print(f"❌ Directory not found: {exercises_dir}")
        return None

    if output_path is None:
        output_path = exercises_path / "index.json"
    else:
        output_path = Path(output_path)

    print(f"📁 Scanning: {exercises_dir}")
    print(f"📄 Output: {output_path}")
    print()

    # Find all core files
    core_files = sorted(exercises_path.glob("**/*_core.json"))
    print(f"Found {len(core_files)} exercise files\n")

    exercises = []
    errors = []

    for idx, core_file in enumerate(core_files, 1):
        try:
            # Read and parse core file
            with open(core_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            metadata = data.get('metadata', {})

            # Determine paths relative to exercises directory
            rel_path = core_file.relative_to(exercises_path)
            category = rel_path.parts[0] if len(rel_path.parts) > 1 else 'unknown'

            # Check if support file exists
            support_file = core_file.parent / core_file.name.replace('_core.json', '_support.json')
            has_support = support_file.exists()

            # Extract item count
            items = data.get('items', [])
            if not items:
                # Try BL structure
                exercises_data = data.get('exercises', [])
                items = []
                for ex in exercises_data:
                    items.extend(ex.get('items', []))

            # Create index entry
            exercise_entry = {
                'id': metadata.get('id', core_file.stem.replace('_core', '')),
                'category': metadata.get('category', category),
                'type': metadata.get('type', 'multiple_choice'),
                'title': data.get('display', {}).get('title', ''),
                'grade': metadata.get('grade'),
                'level': metadata.get('level', ''),
                'difficulty': metadata.get('difficulty', 'medium'),
                'item_count': len(items),
                'has_support': has_support,
                'language': metadata.get('language', 'nl-NL'),
                'paths': {
                    'core': str(rel_path),
                    'support': str(rel_path).replace('_core.json', '_support.json') if has_support else None
                }
            }

            # Add SLO alignment if present
            if 'slo_alignment' in metadata:
                exercise_entry['slo_alignment'] = metadata['slo_alignment']

            exercises.append(exercise_entry)

            # Progress indicator
            if idx % 10 == 0:
                print(f"  Processed {idx}/{len(core_files)} files...")

        except json.JSONDecodeError as e:
            error_msg = f"{core_file.name}: Invalid JSON - {e}"
            errors.append(error_msg)
            print(f"  ⚠️  {error_msg}")
        except Exception as e:
            error_msg = f"{core_file.name}: {str(e)}"
            errors.append(error_msg)
            print(f"  ⚠️  {error_msg}")

    # Sort exercises by category, grade, id
    exercises.sort(key=lambda x: (
        x['category'],
        x['grade'] or 0,
        x['level'],
        x['id']
    ))

    # Create index structure
    index_data = {
        'schema_version': '2.0.0',
        'generated_at': datetime.now().isoformat(),
        'total_exercises': len(exercises),
        'categories': list(set(ex['category'] for ex in exercises)),
        'exercises': exercises
    }

    # Add statistics
    stats = {
        'by_category': {},
        'by_grade': {},
        'with_support': sum(1 for ex in exercises if ex['has_support']),
        'total_items': sum(ex['item_count'] for ex in exercises)
    }

    # Count by category
    for ex in exercises:
        cat = ex['category']
        stats['by_category'][cat] = stats['by_category'].get(cat, 0) + 1

        grade = ex['grade']
        if grade:
            stats['by_grade'][grade] = stats['by_grade'].get(grade, 0) + 1

    index_data['statistics'] = stats

    # Write index
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    # Print summary
    print(f"\n{'='*80}")
    print("INDEX BUILT SUCCESSFULLY")
    print(f"{'='*80}")
    print(f"Total exercises:    {len(exercises)}")
    print(f"Total items:        {stats['total_items']}")
    print(f"With support files: {stats['with_support']}")
    print(f"\nBy category:")
    for cat, count in sorted(stats['by_category'].items()):
        print(f"  {cat}: {count}")
    print(f"\nBy grade:")
    for grade, count in sorted(stats['by_grade'].items()):
        print(f"  Groep {grade}: {count}")

    if errors:
        print(f"\n⚠️  Errors encountered: {len(errors)}")
        for error in errors[:5]:  # Show first 5
            print(f"  - {error}")
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more")

    print(f"\n📄 Index saved to: {output_path}")
    print(f"{'='*80}")

    return index_data


def main():
    parser = argparse.ArgumentParser(description='Build exercise index from directory')
    parser.add_argument('--directory', '-d', default='data-v2/exercises',
                       help='Directory containing exercises (default: data-v2/exercises)')
    parser.add_argument('--output', '-o',
                       help='Output path for index.json (default: <directory>/index.json)')

    args = parser.parse_args()

    result = build_index(args.directory, args.output)

    return 0 if result else 1


if __name__ == '__main__':
    sys.exit(main())
