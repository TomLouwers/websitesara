#!/usr/bin/env python3
"""Create summary table of all meetkunde files"""

import json
import glob

files = sorted(glob.glob('data-v2/exercises/mk/gb_groep*_meetkunde_*.json'))

print("\n" + "=" * 120)
print(f"{'FILE':<40} {'GRADE':<8} {'LEVEL':<8} {'TUSSENDOELEN':<30} {'EXERCISES':<12} {'STATUS':<10}")
print("=" * 120)

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    file_id = filepath.split('/')[-1].replace('.json', '')
    grade = data['metadata']['grade']
    level = data['metadata']['level']
    tussendoelen = ', '.join(data['metadata']['slo_alignment']['tussendoelen'])
    count = len(data['items'])
    
    # Check for duplicates
    questions = [ex['question']['text'] for ex in data['items']]
    duplicates = len(questions) - len(set(questions))
    status = "✅ OK" if duplicates == 0 else f"⚠️  {duplicates} dups"
    
    print(f"{file_id:<40} {grade:<8} {level:<8} {tussendoelen:<30} {count:<12} {status:<10}")

print("=" * 120)
print()
