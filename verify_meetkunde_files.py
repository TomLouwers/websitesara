#!/usr/bin/env python3
"""Verify all meetkunde files have proper structure"""

import json
import os
import glob

def verify_file(filepath):
    """Verify a single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    file_id = os.path.basename(filepath).replace('.json', '')
    
    # Check structure
    checks = {
        'schema_version': 'schema_version' in data,
        'metadata': 'metadata' in data,
        'display': 'display' in data,
        'content': 'content' in data,
        'items': 'items' in data,
        'settings': 'settings' in data,
    }
    
    # Check metadata fields
    if 'metadata' in data:
        meta = data['metadata']
        checks['has_id'] = 'id' in meta
        checks['has_grade'] = 'grade' in meta
        checks['has_level'] = 'level' in meta
        checks['has_tussendoelen'] = 'slo_alignment' in meta and 'tussendoelen' in meta['slo_alignment']
    
    # Check items
    item_count = len(data.get('items', []))
    questions = [ex['question']['text'] for ex in data.get('items', [])]
    unique_count = len(set(questions))
    duplicates = item_count - unique_count
    
    # Get tussendoelen codes
    tussendoelen = []
    if 'metadata' in data and 'slo_alignment' in data['metadata']:
        tussendoelen = data['metadata']['slo_alignment'].get('tussendoelen', [])
    
    return {
        'file_id': file_id,
        'checks': checks,
        'item_count': item_count,
        'duplicates': duplicates,
        'tussendoelen': tussendoelen,
        'all_checks_pass': all(checks.values())
    }

# Verify all files
files = sorted(glob.glob('data-v2/exercises/mk/gb_groep*_meetkunde_*.json'))

print("=" * 100)
print("MEETKUNDE FILE VERIFICATION")
print("=" * 100)
print()

results = []
for filepath in files:
    result = verify_file(filepath)
    results.append(result)
    
    status = "✅" if result['all_checks_pass'] and result['duplicates'] == 0 else "⚠️ "
    tussendoelen_str = ', '.join(result['tussendoelen'])
    
    print(f"{status} {result['file_id']}")
    print(f"   Exercises: {result['item_count']}, Duplicates: {result['duplicates']}")
    print(f"   Tussendoelen: [{tussendoelen_str}]")
    print(f"   Structure: {' '.join([k for k, v in result['checks'].items() if v])}")
    print()

print("=" * 100)
print("SUMMARY")
print("=" * 100)
print()
print(f"Total files: {len(results)}")
print(f"All files valid: {'✅ YES' if all(r['all_checks_pass'] and r['duplicates'] == 0 for r in results) else '⚠️  NO'}")
print(f"Total exercises: {sum(r['item_count'] for r in results)}")
print(f"Total duplicates: {sum(r['duplicates'] for r in results)}")
