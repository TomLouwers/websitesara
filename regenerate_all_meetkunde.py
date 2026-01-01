#!/usr/bin/env python3
"""
Regenerate all meetkunde exercises with high-quality, unique content
based on SLO prompt templates from rekenen-meten-meetkunde.csv
"""
import json
import csv
import random
import os

# Load CSV templates
with open('docs/reference/rekenen-meten-meetkunde.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    templates = {row['Code']: row for row in reader}

def create_base_file(file_id, grade, level):
    """Create base structure for a meetkunde file"""
    return {
        "schema_version": "2.0.0",
        "metadata": {
            "id": file_id,
            "type": "multiple_choice",
            "category": "gb",
            "grade": grade,
            "level": level,
            "language": "nl-NL",
            "domain": "meetkunde",
            "slo_alignment": {
                "kerndoelen": ["K32", "K33"],
                "rekendomeinen": ["meetkunde", "meten"],
                "tussendoelen": [f"{grade}MM{i}_{level.lower()}" for i in range(1, 4)],
                "referentieniveau": "1S" if grade == 8 else "1F",
                "cognitive_level": "toepassen"
            }
        },
        "display": {
            "title": f"Meetkunde Groep {grade}"
        },
        "content": {
            "instruction": "Kies het goede antwoord:"
        },
        "items": [],
        "settings": {
            "allow_review": True
        }
    }

def generate_groep3_m3(file_type):
    """Groep 3 M3: liniaal (cm), halve uren, geld tot €20"""
    exercises = []
    ex_id = 1

    # Liniaal exercises
    scenarios = [
        (14, "potlood"), (18, "stokje"), (7, "lijn"), (21, "schrift"),
        (8, "krijtje"), (25, "tekening"), (12, "paperclip"), (16, "lint"),
        (10, "gum"), (19, "kleurpotlood"), (23, "sleutelbos"), (11, "lijntje"),
        (15, "pen"), (20, "touw"), (9, "blokje"), (22, "boek"), (27, "staaf")
    ]
    for length, obj in scenarios:
        exercises.append({
            "id": ex_id,
            "type": "multiple_choice",
            "theme": "meten_liniaal",
            "question": {"text": f"Een {obj} is {length} cm lang. Hoeveel centimeter meet je met de liniaal?"},
            "options": [
                {"text": f"{length} cm"},
                {"text": f"{length-2} cm"},
                {"text": f"{length+2} cm"},
                {"text": f"{length+5} cm"}
            ],
            "answer": {"type": "single", "correct_index": 0},
            "hint": "Begin bij 0 op de liniaal en tel de streepjes"
        })
        ex_id += 1

    # Tijd halve uren
    times = [(2, 30, "half drie"), (8, 30, "half negen"), (10, 30, "half elf"),
             (12, 30, "half één"), (1, 30, "half twee"), (5, 30, "half zes"),
             (7, 30, "half acht"), (3, 30, "half vier"), (4, 30, "half vijf"),
             (6, 30, "half zeven"), (9, 30, "half tien"), (11, 30, "half twaalf"),
             (2, 0, "twee uur"), (3, 0, "drie uur"), (5, 0, "vijf uur"), (8, 0, "acht uur"),
             (10, 0, "tien uur")]

    for h, m, text in times[:17]:
        if m == 30:
            q = f"De klok wijst {text} aan. Hoe laat is het?"
        else:
            q = f"Het is {text}. Hoe schrijf je dat met cijfers?"
        exercises.append({
            "id": ex_id,
            "type": "multiple_choice",
            "theme": "tijd_halve_uren",
            "question": {"text": q},
            "options": [
                {"text": f"{h}:{m:02d}"},
                {"text": f"{h+1}:00"},
                {"text": f"{h}:00" if m == 30 else f"{h}:30"},
                {"text": f"{h-1}:{m:02d}" if h > 1 else f"{12}:{m:02d}"}
            ],
            "answer": {"type": "single", "correct_index": 0},
            "hint": f"{text.capitalize()} = {h}:{m:02d}"
        })
        ex_id += 1

    # Geld tot 20 euro
    transactions = [(3, 5, 2), (4, 10, 6), (7, 10, 3), (9, 10, 1), (6, 8, 2),
                    (5, 10, 5), (8, 12, 4), (11, 15, 4), (12, 5, -7), (14, 20, 6),
                    (6, 10, 4), (13, 18, 5), (7, 12, 5), (15, 8, -7), (10, 7, -3), (16, 4, -12)]

    for price, paid, change in transactions[:16]:
        if change > 0:
            q = f"Je koopt iets voor €{price}. Je betaalt met €{paid}. Hoeveel wisselgeld?"
            actual_change = paid - price
            exercises.append({
                "id": ex_id,
                "type": "multiple_choice",
                "theme": "geld_tot_20",
                "question": {"text": q},
                "options": [
                    {"text": f"€{actual_change}"},
                    {"text": f"€{actual_change+1}"},
                    {"text": f"€{actual_change-1}" if actual_change > 1 else "€10"},
                    {"text": f"€{paid+price}"}
                ],
                "answer": {"type": "single", "correct_index": 0},
                "hint": f"€{paid} - €{price} = €{actual_change}"
            })
        else:
            # Different type: addition
            item1, item2 = price, paid
            total = item1 + item2
            q = f"Een schrift kost €{item1}. Een pen kost €{item2}. Hoeveel kost het samen?"
            exercises.append({
                "id": ex_id,
                "type": "multiple_choice",
                "theme": "geld_tot_20",
                "question": {"text": q},
                "options": [
                    {"text": f"€{total}"},
                    {"text": f"€{total+2}"},
                    {"text": f"€{total-2}"},
                    {"text": f"€{item1}"}
                ],
                "answer": {"type": "single", "correct_index": 0},
                "hint": f"€{item1} + €{item2} = €{total}"
            })
        ex_id += 1

    return exercises[:50]

print("Regenerating all meetkunde files...")
print("=" * 60)

# Regenerate all files
files = {
    "gb_groep3_meetkunde_m3_core": (3, "M3", generate_groep3_m3),
    "gb_groep3_meetkunde_m3_support": (3, "M3", generate_groep3_m3),
}

for file_id, (grade, level, gen_func) in files.items():
    filepath = f"data-v2/exercises/mk/{file_id}.json"

    # Generate exercises
    file_type = "core" if "core" in file_id else "support"
    exercises = gen_func(file_type)

    # Create file
    data = create_base_file(file_id, grade, level)
    data['items'] = exercises

    # Save
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Verify
    questions = [ex['question']['text'] for ex in exercises]
    unique = len(set(questions))

    if unique == len(questions):
        print(f"✅ {file_id}: {len(exercises)} unique exercises")
    else:
        print(f"⚠️  {file_id}: {len(exercises)} exercises, {len(questions)-unique} duplicates")

print("\nDone!")
