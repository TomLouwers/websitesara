#!/usr/bin/env python3
"""
Properly generate all meetkunde exercises using SLO prompt templates
from docs/reference/rekenen-meten-meetkunde.csv
"""
import json
import csv
import random

# Load templates
templates = {}
with open('docs/reference/rekenen-meten-meetkunde.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        templates[row['Code']] = row

def create_base_file(file_id, grade, level):
    """Create base JSON structure"""
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
                "tussendoelen": [f"{grade}MM_meetkunde_{level.lower()}"],
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

# Exercise generators based on prompt templates
def generate_3MM1_exercises(count=17):
    """3MM1: Meten met liniaal (cm)"""
    exercises = []
    objects = ["potlood", "lijn", "stokje", "krijtje", "schrift", "gum", "lint", "boek",
               "kleurpotlood", "pen", "paperclip", "staaf", "touw", "wortel", "peen"]
    lengths = list(range(7, 29))

    used = set()
    for i in range(count):
        while True:
            length = random.choice(lengths)
            obj = random.choice(objects)
            key = f"{obj}_{length}"
            if key not in used:
                used.add(key)
                break

        exercises.append({
            "id": len(exercises) + 1,
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

    return exercises

def generate_3MM2_exercises(count=17):
    """3MM2: Tijd halve uren"""
    exercises = []
    times = [
        (1, 30, "half twee"), (2, 30, "half drie"), (3, 30, "half vier"),
        (4, 30, "half vijf"), (5, 30, "half zes"), (6, 30, "half zeven"),
        (7, 30, "half acht"), (8, 30, "half negen"), (9, 30, "half tien"),
        (10, 30, "half elf"), (11, 30, "half twaalf"), (12, 30, "half één"),
        (1, 0, "één uur"), (2, 0, "twee uur"), (3, 0, "drie uur"),
        (4, 0, "vier uur"), (5, 0, "vijf uur")
    ]

    for i, (h, m, text) in enumerate(times[:count]):
        if m == 30:
            q = f"De klok wijst {text} aan. Hoe laat is het?"
        else:
            q = f"Het is {text}. Hoe schrijf je dat met cijfers?"

        exercises.append({
            "id": len(exercises) + 1,
            "type": "multiple_choice",
            "theme": "tijd_halve_uren",
            "question": {"text": q},
            "options": [
                {"text": f"{h}:{m:02d}"},
                {"text": f"{h+1}:00" if h < 12 else "1:00"},
                {"text": f"{h}:00" if m == 30 else f"{h}:30"},
                {"text": f"{h-1 if h > 1 else 12}:{m:02d}"}
            ],
            "answer": {"type": "single", "correct_index": 0},
            "hint": f"{text.capitalize()} betekent {h}:{m:02d}"
        })

    return exercises

def generate_3MM3_exercises(count=16):
    """3MM3: Geld rekenen tot 20 euro"""
    exercises = []

    # Wisselgeld vragen
    transactions = [
        (3, 5), (4, 10), (6, 10), (7, 12), (8, 10), (9, 15),
        (11, 20), (5, 8), (12, 15), (14, 20), (13, 18), (16, 20)
    ]

    for price, paid in transactions[:count//2]:
        change = paid - price
        exercises.append({
            "id": len(exercises) + 1,
            "type": "multiple_choice",
            "theme": "geld_wisselgeld",
            "question": {"text": f"Je koopt iets voor €{price}. Je betaalt met €{paid}. Hoeveel wisselgeld krijg je?"},
            "options": [
                {"text": f"€{change}"},
                {"text": f"€{change+1}"},
                {"text": f"€{change-1}" if change > 1 else "€10"},
                {"text": f"€{paid+price}"}
            ],
            "answer": {"type": "single", "correct_index": 0},
            "hint": f"Trek af: €{paid} - €{price} = €{change}"
        })

    # Optellen vragen
    items = [(2, 3), (4, 5), (3, 6), (5, 7), (6, 8), (4, 9), (7, 8), (5, 6)]
    for item1, item2 in items[:count-len(exercises)]:
        total = item1 + item2
        exercises.append({
            "id": len(exercises) + 1,
            "type": "multiple_choice",
            "theme": "geld_optellen",
            "question": {"text": f"Een schrift kost €{item1}. Een pen kost €{item2}. Hoeveel betaal je samen?"},
            "options": [
                {"text": f"€{total}"},
                {"text": f"€{total+2}"},
                {"text": f"€{total-2}"},
                {"text": f"€{item1}"}
            ],
            "answer": {"type": "single", "correct_index": 0},
            "hint": f"Tel op: €{item1} + €{item2} = €{total}"
        })

    return exercises

def generate_3MM4_exercises(count=17):
    """3MM4: Meter en centimeter"""
    exercises = []

    # meter naar cm
    for m in [1, 2, 3, 4, 5]:
        cm = m * 100
        exercises.append({
            "id": len(exercises) + 1,
            "type": "multiple_choice",
            "theme": "lengte_omrekenen",
            "question": {"text": f"{m} meter is hoeveel centimeter?"},
            "options": [
                {"text": f"{cm} cm"},
                {"text": f"{cm+10} cm"},
                {"text": f"{cm-10} cm"},
                {"text": f"{m*10} cm"}
            ],
            "answer": {"type": "single", "correct_index": 0},
            "hint": f"1 meter = 100 cm, dus {m} × 100 = {cm} cm"
        })

    # cm naar m en cm
    conversions = [(150, 1, 50), (230, 2, 30), (175, 1, 75), (280, 2, 80),
                   (310, 3, 10), (265, 2, 65), (145, 1, 45), (190, 1, 90),
                   (320, 3, 20), (255, 2, 55), (185, 1, 85), (295, 2, 95)]

    for cm_total, m, cm_rest in conversions[:count-len(exercises)]:
        exercises.append({
            "id": len(exercises) + 1,
            "type": "multiple_choice",
            "theme": "lengte_omrekenen",
            "question": {"text": f"{cm_total} cm is hoeveel meter en centimeter?"},
            "options": [
                {"text": f"{m} m en {cm_rest} cm"},
                {"text": f"{m+1} m en {cm_rest} cm"},
                {"text": f"{m} m en {cm_rest+10} cm"},
                {"text": f"{cm_total} m"}
            ],
            "answer": {"type": "single", "correct_index": 0},
            "hint": f"100 cm = 1 m, dus {cm_total} cm = {m} m en {cm_rest} cm"
        })

    return exercises

def generate_3MM5_exercises(count=17):
    """3MM5: Vlakke figuren"""
    exercises = []

    questions = [
        ("Hoeveel hoeken heeft een vierkant?", ["4", "3", "5", "6"], 0, "Een vierkant heeft 4 hoeken"),
        ("Hoeveel hoeken heeft een rechthoek?", ["4", "3", "5", "2"], 0, "Een rechthoek heeft 4 hoeken"),
        ("Hoeveel hoeken heeft een driehoek?", ["3", "4", "2", "5"], 0, "Een driehoek heeft 3 hoeken"),
        ("Hoeveel hoeken heeft een cirkel?", ["0", "1", "2", "4"], 0, "Een cirkel heeft geen hoeken"),
        ("Hoeveel zijden heeft een vierkant?", ["4", "3", "5", "6"], 0, "Een vierkant heeft 4 zijden"),
        ("Hoeveel zijden heeft een driehoek?", ["3", "4", "2", "5"], 0, "Een driehoek heeft 3 zijden"),
        ("Welke figuur heeft geen hoeken?", ["cirkel", "vierkant", "driehoek", "rechthoek"], 0, "Een cirkel is rond"),
        ("Een vierkant heeft...", ["4 gelijke zijden", "3 gelijke zijden", "2 gelijke zijden", "geen gelijke zijden"], 0, "Alle zijden zijn even lang"),
        ("Een rechthoek heeft...", ["4 rechte hoeken", "3 rechte hoeken", "2 rechte hoeken", "geen rechte hoeken"], 0, "Alle hoeken zijn 90°"),
        ("Welke figuur heeft 3 hoeken?", ["driehoek", "vierkant", "cirkel", "rechthoek"], 0, "Drie-hoek = 3 hoeken"),
        ("Een cirkel is...", ["rond", "vierkant", "driehoekig", "rechthoekig"], 0, "Een cirkel heeft geen hoeken"),
        ("Hoeveel rechte hoeken heeft een vierkant?", ["4", "3", "2", "1"], 0, "Alle hoeken zijn recht"),
        ("Welke figuur heeft 4 zijden?", ["vierkant", "driehoek", "cirkel", "geen"], 0, "Vier-kant = 4 zijden"),
        ("Een driehoek heeft hoeveel punten?", ["3", "4", "2", "5"], 0, "3 hoekpunten"),
        ("Welke figuur kun je met een passer tekenen?", ["cirkel", "vierkant", "driehoek", "rechthoek"], 0, "Een passer maakt ronde vormen"),
        ("Hoeveel gelijke zijden heeft een vierkant?", ["4", "3", "2", "geen"], 0, "Alle 4 zijden zijn gelijk"),
        ("Welke figuur heeft evenwijdige zijden?", ["rechthoek", "driehoek", "cirkel", "geen"], 0, "Rechthoek heeft 2 paar evenwijdige zijden")
    ]

    for i, (q, opts, correct, hint) in enumerate(questions[:count]):
        exercises.append({
            "id": i + 1,
            "type": "multiple_choice",
            "theme": "vlakke_figuren",
            "question": {"text": q},
            "options": [{"text": opt} for opt in opts],
            "answer": {"type": "single", "correct_index": correct},
            "hint": hint
        })

    return exercises

def generate_3MM6_exercises(count=16):
    """3MM6: Tijd kwartieren"""
    exercises = []

    times = [
        ("kwart over 3", "3:15"), ("kwart voor 8", "7:45"), ("half 4", "3:30"),
        ("kwart over 7", "7:15"), ("kwart voor 5", "4:45"), ("kwart over 9", "9:15"),
        ("kwart voor 11", "10:45"), ("kwart over 2", "2:15"), ("kwart voor 3", "2:45"),
        ("half 9", "8:30"), ("kwart over 5", "5:15"), ("kwart voor 6", "5:45"),
        ("half 7", "6:30"), ("kwart over 10", "10:15"), ("kwart voor 12", "11:45"),
        ("half 2", "1:30")
    ]

    for i, (text, digital) in enumerate(times[:count]):
        h_str, m_str = digital.split(':')
        h = int(h_str)

        exercises.append({
            "id": i + 1,
            "type": "multiple_choice",
            "theme": "tijd_kwartieren",
            "question": {"text": f"Hoe laat is {text}? Schrijf met cijfers."},
            "options": [
                {"text": digital},
                {"text": f"{h}:00"},
                {"text": f"{h+1 if h < 12 else 1}:00"},
                {"text": f"{h}:30" if ":15" in digital or ":45" in digital else f"{h}:15"}
            ],
            "answer": {"type": "single", "correct_index": 0},
            "hint": f"{text.capitalize()} = {digital}"
        })

    return exercises

# Generator function mapping
generators = {
    "3MM1": generate_3MM1_exercises,
    "3MM2": generate_3MM2_exercises,
    "3MM3": generate_3MM3_exercises,
    "3MM4": generate_3MM4_exercises,
    "3MM5": generate_3MM5_exercises,
    "3MM6": generate_3MM6_exercises,
}

# File mapping
file_codes = {
    "gb_groep3_meetkunde_m3": ["3MM1", "3MM2", "3MM3"],
    "gb_groep3_meetkunde_e3": ["3MM4", "3MM5", "3MM6"],
}

print("Generating Groep 3 exercises...\n")

for base_name, codes in file_codes.items():
    for file_type in ["core", "support"]:
        file_id = f"{base_name}_{file_type}"
        filepath = f"data-v2/exercises/mk/{file_id}.json"

        # Generate exercises
        all_exercises = []
        for code in codes:
            if code in generators:
                exercises = generators[code](17 if len(codes) == 3 else 25)
                all_exercises.extend(exercises)

        # Renumber
        for i, ex in enumerate(all_exercises, 1):
            ex['id'] = i

        # Create file
        grade = 3
        level = "M3" if "_m3_" in file_id else "E3"
        data = create_base_file(file_id, grade, level)
        data['items'] = all_exercises[:50]

        # Save
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Verify
        questions = [ex['question']['text'] for ex in data['items']]
        unique = len(set(questions))

        if unique == len(questions):
            print(f"✅ {file_id}: {len(questions)} unique exercises")
        else:
            print(f"⚠️  {file_id}: {len(questions)} exercises, {len(questions)-unique} duplicates")

print("\nGroep 3 complete!")
