#!/usr/bin/env python3
"""
Generate high-quality meetkunde exercises for all remaining files
"""
import json
import random
import os

# Template for exercise structure
def create_exercise(id_num, theme, question, options, correct_idx, hint):
    return {
        "id": id_num,
        "type": "multiple_choice",
        "theme": theme,
        "question": {"text": question},
        "options": [{"text": opt} for opt in options],
        "answer": {"type": "single", "correct_index": correct_idx},
        "hint": hint
    }

# Groep 5 Exercise Generators
def generate_groep5_e5_tijd_exercises(start_id):
    """Time calculation exercises for Groep 5 E5"""
    exercises = []
    contexts = [
        ("De trein vertrekt om 13:25 en de reis duurt 1 uur en 15 minuten. Hoe laat komt de trein aan?",
         ["14:30", "14:40", "14:50", "15:00"], 1, "Tel 1 uur en 15 minuten bij 13:25 op"),
        ("Van 10:15 tot 12:30 is hoeveel tijd?",
         ["2 uur", "2 uur en 15 minuten", "2 uur en 30 minuten", "3 uur"], 1, "Reken: 12:30 - 10:15 = ?"),
        ("De bus vertrekt om 8:40 en rijdt 55 minuten. Hoe laat is de bus er?",
         ["9:25", "9:35", "9:45", "10:00"], 1, "Tel 55 minuten bij 8:40 op"),
    ]

    for i, (q, opts, correct, hint) in enumerate(contexts):
        exercises.append(create_exercise(start_id + i, "tijd_berekenen", q, opts, correct, hint))

    return exercises

def generate_groep5_e5_oppervlakte_exercises(start_id):
    """Area calculation exercises for Groep 5 E5"""
    exercises = []

    # Rectangle area calculations
    dimensions = [(6, 4, 24), (8, 3, 24), (5, 7, 35), (9, 4, 36), (7, 6, 42)]
    for i, (l, b, area) in enumerate(dimensions):
        q = f"Een rechthoek is {l} cm lang en {b} cm breed. Wat is de oppervlakte?"
        opts = [f"{area} cm²", f"{area+5} cm²", f"{area-5} cm²", f"{l+b} cm"]
        exercises.append(create_exercise(start_id + i, "oppervlakte_rechthoek", q, opts, 0,
                                        f"Oppervlakte = lengte × breedte: {l} × {b} = ?"))

    return exercises

def generate_groep5_e5_symmetrie_exercises(start_id):
    """Symmetry exercises for Groep 5 E5"""
    exercises = []
    contexts = [
        ("Hoeveel symmetrie-assen heeft een vierkant?", ["1", "2", "4", "8"], 2,
         "Een vierkant heeft 4 symmetrie-assen: 2 door de middens en 2 diagonaal"),
        ("Welke letter is symmetrisch?", ["A", "B", "C", "E"], 0,
         "De letter A kun je verticaal spiegelen"),
        ("Een rechthoek heeft hoeveel symmetrie-assen?", ["0", "1", "2", "4"], 2,
         "Een rechthoek heeft 2 symmetrie-assen door de middens"),
    ]

    for i, (q, opts, correct, hint) in enumerate(contexts):
        exercises.append(create_exercise(start_id + i, "symmetrie", q, opts, correct, hint))

    return exercises

# Main generation function
def generate_exercises_for_file(groep, level, file_type, current_count, target_count=50):
    """Generate exercises to bring a file up to target count"""
    needed = target_count - current_count
    exercises = []
    id_start = current_count + 1

    # Groep 5 E5 exercises
    if groep == 5 and level == 'e5':
        tijd_ex = generate_groep5_e5_tijd_exercises(id_start)
        opp_ex = generate_groep5_e5_oppervlakte_exercises(id_start + len(tijd_ex))
        sym_ex = generate_groep5_e5_symmetrie_exercises(id_start + len(tijd_ex) + len(opp_ex))
        exercises = tijd_ex + opp_ex + sym_ex

    return exercises[:needed]

# Test with one file
if __name__ == "__main__":
    # Load existing file
    file_path = "data-v2/exercises/mk/gb_groep5_meetkunde_e5_core.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    current_count = len(data['items'])
    print(f"Current exercises: {current_count}")

    new_exercises = generate_exercises_for_file(5, 'e5', 'core', current_count, 50)
    print(f"Generated {len(new_exercises)} new exercises")

    # Add to existing
    for ex in new_exercises:
        data['items'].append(ex)

    print(f"Total exercises: {len(data['items'])}")
