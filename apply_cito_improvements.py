#!/usr/bin/env python3
"""
Apply CITO template improvements to the main Template.json file.

Improvements applied:
1. Fill empty foutanalyse fields with "Dit is het juiste antwoord."
2. Remove "Dit is een meeteenheid probleem:" labels
3. Replace generic feedback with specific hints from CITO
4. Integrate rounding notation
"""

import json
import re
from typing import Dict, Any, List

def load_json(filepath: str) -> Dict[str, Any]:
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath: str, data: Dict[str, Any]) -> None:
    """Save JSON file with proper formatting."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fill_empty_foutanalyse(story_problems: List[Dict]) -> int:
    """Fill empty foutanalyse fields for correct answers."""
    count = 0
    for story in story_problems:
        for question in story.get('questions', []):
            if 'options' in question:
                correct_idx = question.get('correct', 0)
                for idx, option in enumerate(question['options']):
                    if idx == correct_idx:
                        if not option.get('foutanalyse') or option.get('foutanalyse').strip() == '':
                            option['foutanalyse'] = 'Dit is het juiste antwoord.'
                            count += 1
    return count

def remove_meeteenheid_labels(story_problems: List[Dict]) -> int:
    """Remove 'Dit is een meeteenheid probleem:' labels and improve text."""
    count = 0
    pattern = r'^Dit is een meeteenheid probleem:\s*'

    for story in story_problems:
        for question in story.get('questions', []):
            # Check extra_info concept
            if 'extra_info' in question and 'concept' in question['extra_info']:
                concept = question['extra_info']['concept']
                if 'Dit is een meeteenheid probleem:' in concept:
                    # Remove the label
                    new_concept = re.sub(pattern, '', concept)

                    # Improve the instruction
                    if 'let goed op de eenheden' in new_concept.lower():
                        new_concept = new_concept.replace(
                            'let goed op de eenheden (gram, liter, meter) en reken ze om waar nodig',
                            'Let goed op de eenheden (bijvoorbeeld meter, centimeter, liter) en reken alles eerst naar dezelfde eenheid voordat je gaat rekenen'
                        )

                    question['extra_info']['concept'] = new_concept
                    count += 1

    return count

def improve_generic_feedback(template_stories: List[Dict], cito_stories: List[Dict]) -> int:
    """Replace generic feedback with specific hints from CITO file."""
    count = 0

    # Create a mapping of CITO stories by ID for quick lookup
    cito_map = {s.get('id'): s for s in cito_stories if 'id' in s}

    for template_story in template_stories:
        story_id = template_story.get('id')
        if not story_id or story_id not in cito_map:
            continue

        cito_story = cito_map[story_id]
        template_questions = template_story.get('questions', [])
        cito_questions = cito_story.get('questions', [])

        # Compare questions within the same story
        for q_idx, template_q in enumerate(template_questions):
            if q_idx >= len(cito_questions):
                continue

            cito_q = cito_questions[q_idx]
            template_options = template_q.get('options', [])
            cito_options = cito_q.get('options', [])

            # Compare and update foutanalyse for each option
            for o_idx, template_opt in enumerate(template_options):
                if o_idx >= len(cito_options):
                    continue

                cito_opt = cito_options[o_idx]
                template_feedback = template_opt.get('foutanalyse', '').strip()
                cito_feedback = cito_opt.get('foutanalyse', '').strip()

                # Only replace if template has generic feedback and CITO has better feedback
                generic_phrases = [
                    'Controleer je berekening',
                    'Je hebt verkeerd gerekend',
                    'Dit is niet correct',
                    'Probeer het opnieuw'
                ]

                is_generic = any(phrase in template_feedback for phrase in generic_phrases)
                cito_is_better = (
                    cito_feedback and
                    len(cito_feedback) > len(template_feedback) and
                    not any(phrase in cito_feedback for phrase in generic_phrases)
                )

                if is_generic and cito_is_better:
                    template_opt['foutanalyse'] = cito_feedback
                    count += 1

    return count

def integrate_rounding_notation(template_stories: List[Dict], cito_stories: List[Dict]) -> int:
    """Integrate rounding notation from CITO file."""
    count = 0

    cito_map = {s.get('id'): s for s in cito_stories if 'id' in s}

    for template_story in template_stories:
        story_id = template_story.get('id')
        if not story_id or story_id not in cito_map:
            continue

        cito_story = cito_map[story_id]
        template_questions = template_story.get('questions', [])
        cito_questions = cito_story.get('questions', [])

        for q_idx, template_q in enumerate(template_questions):
            if q_idx >= len(cito_questions):
                continue

            cito_q = cito_questions[q_idx]

            # Check berekening field in extra_info
            if ('extra_info' in template_q and 'berekening' in template_q['extra_info'] and
                'extra_info' in cito_q and 'berekening' in cito_q['extra_info']):

                template_berekening = template_q['extra_info']['berekening']
                cito_berekening = cito_q['extra_info']['berekening']

                # Look for rounding improvements in CITO
                for i, line in enumerate(cito_berekening):
                    if '≈' in line and 'na afronden' in line:
                        # Check if template has a similar line that can be improved
                        if i < len(template_berekening):
                            template_line = template_berekening[i]
                            if '≈' not in template_line and 'na afronden' not in template_line:
                                # Replace with CITO version
                                template_q['extra_info']['berekening'][i] = line
                                count += 1

                # Also check for separate "Afgerond:" lines that should be integrated
                if len(template_berekening) > len(cito_berekening):
                    # CITO might have integrated rounding into fewer lines
                    template_q['extra_info']['berekening'] = cito_berekening.copy()
                    count += 1

    return count

def improve_rounding_feedback(template_stories: List[Dict], cito_stories: List[Dict]) -> int:
    """Improve context-specific rounding feedback to be more principle-based."""
    count = 0

    cito_map = {s.get('id'): s for s in cito_stories if 'id' in s}

    for template_story in template_stories:
        story_id = template_story.get('id')
        if not story_id or story_id not in cito_map:
            continue

        cito_story = cito_map[story_id]
        template_questions = template_story.get('questions', [])
        cito_questions = cito_story.get('questions', [])

        for q_idx, template_q in enumerate(template_questions):
            if q_idx >= len(cito_questions):
                continue

            cito_q = cito_questions[q_idx]
            template_options = template_q.get('options', [])
            cito_options = cito_q.get('options', [])

            for o_idx, template_opt in enumerate(template_options):
                if o_idx >= len(cito_options):
                    continue

                cito_opt = cito_options[o_idx]
                template_feedback = template_opt.get('foutanalyse', '')
                cito_feedback = cito_opt.get('foutanalyse', '')

                # Check for context-specific rounding feedback
                if ('hele stuks' in template_feedback or 'hele ijsjes' in template_feedback) and \
                   'Controleer of afronden hier wel mag' in cito_feedback:
                    template_opt['foutanalyse'] = cito_feedback
                    count += 1

    return count

def main():
    """Main function to apply all improvements."""
    print("Loading JSON files...")
    template_stories = load_json('/home/user/websitesara/verhaaltjessommen - Template.json')
    cito_stories = load_json('/home/user/websitesara/verhaaltjessommen_Template8_CITO_reworked.json')

    print(f"Template has {len(template_stories)} stories")
    print(f"CITO has {len(cito_stories)} stories")
    print()

    # Apply improvements
    print("1. Filling empty foutanalyse fields...")
    count1 = fill_empty_foutanalyse(template_stories)
    print(f"   ✓ Filled {count1} empty fields")

    print("2. Removing 'meeteenheid probleem' labels...")
    count2 = remove_meeteenheid_labels(template_stories)
    print(f"   ✓ Removed {count2} labels")

    print("3. Improving generic feedback...")
    count3 = improve_generic_feedback(template_stories, cito_stories)
    print(f"   ✓ Improved {count3} feedback messages")

    print("4. Integrating rounding notation...")
    count4 = integrate_rounding_notation(template_stories, cito_stories)
    print(f"   ✓ Integrated {count4} rounding notations")

    print("5. Improving rounding feedback...")
    count5 = improve_rounding_feedback(template_stories, cito_stories)
    print(f"   ✓ Improved {count5} rounding feedback messages")

    # Save improved template
    print()
    print("Saving improved template...")
    backup_path = '/home/user/websitesara/verhaaltjessommen - Template.json.backup'
    save_json(backup_path, template_stories)
    print(f"✓ Backup saved to: {backup_path}")

    save_json('/home/user/websitesara/verhaaltjessommen - Template.json', template_stories)
    print(f"✓ Improved template saved")

    print()
    print("=" * 60)
    print("SUMMARY OF IMPROVEMENTS APPLIED")
    print("=" * 60)
    print(f"Empty foutanalyse fields filled:     {count1}")
    print(f"'Meeteenheid probleem' labels removed: {count2}")
    print(f"Generic feedback improved:            {count3}")
    print(f"Rounding notations integrated:        {count4}")
    print(f"Rounding feedback improved:           {count5}")
    print(f"TOTAL CHANGES:                        {count1 + count2 + count3 + count4 + count5}")
    print("=" * 60)

if __name__ == '__main__':
    main()
