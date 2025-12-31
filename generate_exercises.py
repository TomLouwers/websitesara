#!/usr/bin/env python3
import json

# Helper function to create exercises
def create_groep5_m5_support_exercises(start_id=21, count=35):
    """Create exercises for Groep 5 M5 Support - similar topics as M5 Core"""
    exercises = []
    themes = [
        ("kilometer", [
            ("Een parcours is 14 km lang. Hoeveel meter is dat?", ["140 meter", "1400 meter", "14000 meter", "140000 meter"], 2, "14 × 1000 = 14000 meter"),
            ("Je fietst 9500 meter. Hoeveel kilometer is dat?", ["0,95 km", "9,5 km", "95 km", "950 km"], 1, "Deel 9500 door 1000"),
            ("Een wandeltocht is 25 km en 750 meter. Hoeveel meter totaal?", ["2575 meter", "25750 meter", "257500 meter", "2575000 meter"], 1, "25 km = 25000 meter. Plus 750 = 25750"),
        ]),
        ("ton", [
            ("Een bestelwagen weegt 2800 kg. Hoeveel ton is dat?", ["0,28 ton", "2,8 ton", "28 ton", "280 ton"], 1, "Deel 2800 door 1000"),
            ("Een container weegt 6 ton. Hoeveel kilogram is dat?", ["60 kg", "600 kg", "6000 kg", "60000 kg"], 2, "6 × 1000 = 6000 kg"),
            ("Een olifant weegt 5500 kg. Hoeveel ton is dat?", ["0,55 ton", "5,5 ton", "55 ton", "550 ton"], 1, "Deel 5500 door 1000"),
        ]),
        ("inhoud", [
            ("Een fles drinken bevat 750 ml. Hoeveel liter is dat?", ["0,075 liter", "0,75 liter", "7,5 liter", "75 liter"], 1, "Deel 750 door 1000"),
            ("Een emmer bevat 12 liter. Hoeveel deciliter is dat?", ["12 dl", "120 dl", "1200 dl", "12000 dl"], 1, "12 × 10 = 120 dl"),
            ("Een pipet bevat 5 ml. Hoeveel cl is dat?", ["0,05 cl", "0,5 cl", "5 cl", "50 cl"], 1, "5 ml = 0,5 cl"),
        ]),
        ("oppervlakte_begrip", [
            ("Een rechthoek is 11 hokjes lang en 6 hokjes breed. Hoeveel cm²?", ["17 cm²", "34 cm²", "66 cm²", "72 cm²"], 2, "11 × 6 = 66 cm²"),
            ("Een T-vorm heeft 15 hokjes. Hoeveel cm²?", ["12 cm²", "15 cm²", "18 cm²", "20 cm²"], 1, "Tel de hokjes: 15 cm²"),
            ("Een vierkant is 8 hokjes lang. Wat is de oppervlakte?", ["16 cm²", "32 cm²", "64 cm²", "128 cm²"], 2, "8 × 8 = 64 cm²"),
        ]),
    ]

    id_counter = start_id
    for theme, questions in themes:
        for q in questions:
            text, options, correct_idx, hint = q
            exercises.append({
                "id": id_counter,
                "type": "multiple_choice",
                "theme": theme,
                "question": {"text": text},
                "options": [{"text": opt} for opt in options],
                "answer": {"type": "single", "correct_index": correct_idx},
                "hint": hint
            })
            id_counter += 1
            if id_counter >= start_id + count:
                return exercises

    # Fill remaining with more variations
    while id_counter < start_id + count:
        remaining = [
            (f"Een route is {5 + id_counter} km. Hoeveel meter?", "kilometer",
             [f"{(5+id_counter)*10} meter", f"{(5+id_counter)*100} meter", f"{(5+id_counter)*1000} meter", f"{(5+id_counter)*10000} meter"],
             2, f"{5+id_counter} × 1000 meter"),
            (f"Een tank weegt {id_counter-20} ton. Hoeveel kg?", "ton",
             [f"{(id_counter-20)*10} kg", f"{(id_counter-20)*100} kg", f"{(id_counter-20)*1000} kg", f"{(id_counter-20)*10000} kg"],
             2, f"{id_counter-20} × 1000 kg"),
        ]
        for r in remaining:
            if id_counter >= start_id + count:
                break
            text, theme, options, idx, hint = r
            exercises.append({
                "id": id_counter,
                "type": "multiple_choice",
                "theme": theme,
                "question": {"text": text},
                "options": [{"text": opt} for opt in options],
                "answer": {"type": "single", "correct_index": idx},
                "hint": hint
            })
            id_counter += 1

    return exercises

print("Script ready to generate exercises")
