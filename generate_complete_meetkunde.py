#!/usr/bin/env python3
"""
Complete meetkunde exercise generator with proper JSON structure.
Generates all 24 files (12 core + 12 support) for Groep 3-8.
"""

import json
import csv
import random
import os

# Load CSV templates
def load_csv_templates():
    """Load all prompt templates from CSV"""
    templates = {}
    with open('docs/reference/rekenen-meten-meetkunde.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row['Code']
            templates[code] = {
                'groep': row['Groep'],
                'beschrijving': row['Beschrijving'],
                'level': row['Level'],
                'toelichting': row['Toelichting'],
                'prompt_template': row['Prompt_Template']
            }
    return templates

def create_exercise(question_text, correct_answer, wrong_answers, theme="meetkunde"):
    """Create a single exercise in the correct format"""
    options = [correct_answer] + wrong_answers
    random.shuffle(options)

    return {
        "id": f"ex_{random.randint(100000, 999999)}",
        "question": {"text": question_text},
        "options": options,
        "correct_answer": correct_answer,
        "theme": theme
    }

def create_file_structure(file_id, grade, level_code, tussendoelen):
    """Create complete JSON file structure with metadata"""
    # Determine level (M3, E3, M4, E4, etc.)
    level = f"{'M' if 'm' in level_code else 'E'}{grade}"

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
                "tussendoelen": tussendoelen,
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

# ============================================================================
# GROEP 3 GENERATORS
# ============================================================================

def generate_3MM1_exercises(count=17):
    """3MM1: Meten met liniaal (cm)"""
    exercises = []
    seen = set()
    objects = ["potlood", "lijn", "streep", "stokje", "strook papier", "lint", "touwtje",
               "pen", "stift", "gum", "paperclip", "blokje", "kaartje", "boek", "schrift"]

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        obj = random.choice(objects)
        length = random.randint(3, 25)

        templates = [
            f"Hoe lang is deze {obj} in centimeters? De liniaal laat {length} cm zien.",
            f"Meet dit {obj} met de liniaal. Het is {length} cm lang. Hoeveel cm is dat?",
            f"Deze {obj} meet {length} centimeter. Hoeveel cm is dat?",
            f"Begin bij 0 cm en meet deze {obj}. De liniaal toont {length} cm. Hoeveel cm?",
        ]

        q = random.choice(templates)
        if q in seen:
            continue
        seen.add(q)

        correct = f"{length} cm"
        wrong = [f"{length-1} cm", f"{length+1} cm", f"{length+2} cm"]
        exercises.append(create_exercise(q, correct, wrong, "meten_liniaal"))

    return exercises[:count]

def generate_3MM2_exercises(count=17):
    """3MM2: Tijd halve uren"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        hour = random.randint(1, 11)
        digital = f"{hour}:30"

        templates = [
            f"Hoe laat is het op de klok? De wijzers staan op half {hour+1}.",
            f"Welke klok toont half {hour+1}?",
            f"Half {hour+1} is hetzelfde als welke tijd?",
            f"De grote wijzer staat op de 6 en de kleine wijzer tussen {hour} en {hour+1}. Hoe laat is het?",
        ]

        q = random.choice(templates)
        if q in seen:
            continue
        seen.add(q)

        correct = digital
        wrong = [f"{hour}:00", f"{hour+1}:00", f"{hour}:15"]
        exercises.append(create_exercise(q, correct, wrong, "tijd_halve_uren"))

    return exercises[:count]

def generate_3MM3_exercises(count=16):
    """3MM3: Geld tot 20 euro"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        price = random.randint(3, 18)
        payment = random.choice([10, 20]) if price < 15 else 20
        change = payment - price

        items = ["speelgoedauto", "boek", "schrift", "snoep", "pen", "potlood",
                 "stickers", "kaart", "ballon", "gum", "lineaal", "kleurpotlood"]
        item = random.choice(items)

        templates = [
            f"Je koopt een {item} voor €{price} en betaalt met €{payment}. Hoeveel wisselgeld krijg je?",
            f"Een {item} kost €{price}. Je geeft €{payment}. Hoeveel krijg je terug?",
            f"Prijs: €{price}. Betaald: €{payment}. Hoeveel wisselgeld?",
        ]

        q = random.choice(templates)
        if q in seen:
            continue
        seen.add(q)

        correct = f"€{change}"
        wrong = [f"€{change-1}" if change > 1 else f"€{change+1}",
                 f"€{change+1}", f"€{change+2}"]
        exercises.append(create_exercise(q, correct, wrong, "geld_tot_20"))

    return exercises[:count]

def generate_3MM4_exercises(count=17):
    """3MM4: Meter en centimeter"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        choice = random.choice(['basic', 'to_cm', 'to_m'])

        if choice == 'basic':
            q = "Hoeveel centimeter is 1 meter?"
            correct = "100 cm"
            wrong = ["10 cm", "50 cm", "1000 cm"]
        elif choice == 'to_cm':
            meters = random.randint(1, 5)
            cm_part = random.choice([0, 10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90])
            total_cm = meters * 100 + cm_part
            if cm_part == 0:
                q = f"{meters} meter = hoeveel centimeter?"
            else:
                q = f"{meters} meter en {cm_part} cm = hoeveel centimeter in totaal?"
            correct = f"{total_cm} cm"
            wrong = [f"{total_cm-10} cm", f"{total_cm+10} cm", f"{total_cm-50} cm"]
        else:  # to_m
            total_cm = random.randint(110, 450)
            meters = total_cm // 100
            cm = total_cm % 100
            q = f"{total_cm} cm = hoeveel meter en centimeter?"
            correct = f"{meters} m en {cm} cm"
            wrong = [f"{meters+1} m en {cm} cm", f"{meters} m en {cm+10} cm" if cm < 90 else f"{meters} m en {cm-10} cm",
                    f"{meters-1} m en {cm} cm" if meters > 1 else f"{meters} m en {cm+20} cm"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "meter_centimeter"))

    return exercises[:count]

def generate_3MM5_exercises(count=17):
    """3MM5: Vlakke figuren"""
    exercises = []
    seen = set()

    questions_pool = [
        ("Hoeveel hoeken heeft een vierkant?", ["4 hoeken", "3 hoeken", "5 hoeken", "6 hoeken"], 0),
        ("Hoeveel hoeken heeft een rechthoek?", ["4 hoeken", "3 hoeken", "5 hoeken", "2 hoeken"], 0),
        ("Hoeveel hoeken heeft een driehoek?", ["3 hoeken", "4 hoeken", "2 hoeken", "5 hoeken"], 0),
        ("Hoeveel hoeken heeft een cirkel?", ["0 hoeken", "1 hoek", "2 hoeken", "4 hoeken"], 0),
        ("Hoeveel zijden heeft een vierkant?", ["4 zijden", "3 zijden", "5 zijden", "6 zijden"], 0),
        ("Hoeveel zijden heeft een driehoek?", ["3 zijden", "4 zijden", "2 zijden", "5 zijden"], 0),
        ("Welke figuur heeft geen hoeken?", ["cirkel", "vierkant", "driehoek", "rechthoek"], 0),
        ("Een vierkant heeft...", ["4 gelijke zijden", "3 gelijke zijden", "2 gelijke zijden", "geen gelijke zijden"], 0),
        ("Een rechthoek heeft...", ["4 rechte hoeken", "3 rechte hoeken", "2 rechte hoeken", "1 rechte hoek"], 0),
        ("Welke figuur heeft 3 hoeken?", ["driehoek", "vierkant", "cirkel", "rechthoek"], 0),
        ("Een cirkel is...", ["rond", "vierkant", "driehoekig", "rechthoekig"], 0),
        ("Hoeveel rechte hoeken heeft een vierkant?", ["4", "3", "2", "1"], 0),
        ("Welke figuur heeft 4 zijden?", ["vierkant", "driehoek", "cirkel", "ster"], 0),
        ("Een driehoek heeft hoeveel punten?", ["3 punten", "4 punten", "2 punten", "5 punten"], 0),
        ("Welke figuur kun je met een passer tekenen?", ["cirkel", "vierkant", "driehoek", "rechthoek"], 0),
        ("Hoeveel gelijke zijden heeft een vierkant?", ["4", "3", "2", "0"], 0),
        ("Een rechthoek heeft ook een andere naam. Welke?", ["vierhoek met rechte hoeken", "langwerpig vierkant", "ovaal", "driehoek"], 0),
    ]

    for i, (q, opts, correct_idx) in enumerate(questions_pool[:count]):
        if q in seen:
            continue
        seen.add(q)

        correct = opts[correct_idx]
        wrong = [opt for i, opt in enumerate(opts) if i != correct_idx]
        exercises.append(create_exercise(q, correct, wrong, "vlakke_figuren"))

    return exercises[:count]

def generate_3MM6_exercises(count=16):
    """3MM6: Tijd kwartieren"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        hour = random.randint(1, 11)
        time_type = random.choice(['kwart_over', 'kwart_voor', 'half'])

        if time_type == 'kwart_over':
            q_templates = [
                f"Hoe laat is het? De wijzers staan op kwart over {hour}.",
                f"Welke klok toont kwart over {hour}?",
                f"Kwart over {hour} is hetzelfde als welke digitale tijd?",
            ]
            q = random.choice(q_templates)
            correct = f"{hour}:15"
            wrong = [f"{hour}:30", f"{hour}:45", f"{hour+1}:00"]
        elif time_type == 'kwart_voor':
            q_templates = [
                f"Hoe laat is het? De wijzers staan op kwart voor {hour+1}.",
                f"Welke klok toont kwart voor {hour+1}?",
                f"Kwart voor {hour+1} is hetzelfde als welke tijd?",
            ]
            q = random.choice(q_templates)
            correct = f"{hour}:45"
            wrong = [f"{hour}:15", f"{hour}:30", f"{hour+1}:00"]
        else:  # half
            q_templates = [
                f"Hoe laat is het? De wijzers staan op half {hour+1}.",
                f"Welke klok toont half {hour+1}?",
            ]
            q = random.choice(q_templates)
            correct = f"{hour}:30"
            wrong = [f"{hour}:15", f"{hour}:45", f"{hour+1}:00"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "tijd_kwartieren"))

    return exercises[:count]

# ============================================================================
# GROEP 4 GENERATORS
# ============================================================================

def generate_4MM1_exercises(count=13):
    """4MM1: mm, cm, dm, m"""
    exercises = []
    seen = set()

    conversions = [
        # mm to cm
        (lambda: (random.randint(10, 99), "mm", "cm", 10), "mm_to_cm"),
        # cm to dm
        (lambda: (random.randint(10, 99), "cm", "dm", 10), "cm_to_dm"),
        # dm to m
        (lambda: (random.randint(1, 20), "dm", "m", 10), "dm_to_m"),
        # cm to m
        (lambda: (random.randint(100, 500), "cm", "m", 100), "cm_to_m"),
    ]

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        conv_type, type_name = random.choice(conversions)
        value, from_unit, to_unit, divisor = conv_type()

        q = f"{value} {from_unit} = hoeveel {to_unit}?"
        if q in seen:
            continue
        seen.add(q)

        result = value / divisor
        correct = f"{result:.1f} {to_unit}" if result % 1 != 0 else f"{int(result)} {to_unit}"

        wrong = [
            f"{result+1:.1f} {to_unit}" if result % 1 != 0 else f"{int(result)+1} {to_unit}",
            f"{value} {to_unit}",
            f"{result-0.5:.1f} {to_unit}" if result % 1 != 0 else f"{int(result)-1} {to_unit}"
        ]

        exercises.append(create_exercise(q, correct, wrong, "lengte_eenheden"))

    return exercises[:count]

def generate_4MM2_exercises(count=12):
    """4MM2: gram en kilogram"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        choice = random.choice(['kg_to_g', 'g_to_kg', 'basic'])

        if choice == 'basic':
            q = "Hoeveel gram is 1 kilogram?"
            correct = "1000 gram"
            wrong = ["100 gram", "500 gram", "10000 gram"]
        elif choice == 'kg_to_g':
            kg = random.randint(1, 5)
            g = kg * 1000
            q = f"{kg} kg = hoeveel gram?"
            correct = f"{g} gram"
            wrong = [f"{g+100} gram", f"{g-100} gram", f"{kg*100} gram"]
        else:  # g_to_kg
            grams = random.randint(500, 5000)
            kg = grams / 1000
            q = f"{grams} gram = hoeveel kilogram?"
            correct = f"{kg:.1f} kg" if kg % 1 != 0 else f"{int(kg)} kg"
            wrong_val = kg + 0.5 if kg < 2 else kg - 0.5
            wrong = [
                f"{kg+0.5:.1f} kg",
                f"{grams/100:.1f} kg",
                f"{wrong_val:.1f} kg"
            ]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "gewicht"))

    return exercises[:count]

def generate_4MM3_exercises(count=12):
    """4MM3: Inhoud liter"""
    exercises = []
    seen = set()

    questions = [
        ("Een emmer bevat meestal hoeveel liter?", ["10 liter", "11 liter", "20 liter", "9.5 liter"], 0),
        ("Een kan bevat meestal hoeveel liter?", ["2 liter", "3 liter", "4 liter", "1.5 liter"], 0),
        ("Een beker bevat meestal hoeveel liter?", ["0.25 liter", "0.5 liter", "1 liter", "2 liter"], 0),
        ("Een pak melk bevat meestal hoeveel liter?", ["1 liter", "2 liter", "0.5 liter", "1.5 liter"], 0),
        ("Een fles water bevat meestal hoeveel liter?", ["1.5 liter", "1.0 liter", "2.5 liter", "3.0 liter"], 0),
        ("Een glas water bevat meestal hoeveel liter?", ["0.25 liter", "0.5 liter", "1 liter", "0.1 liter"], 0),
        ("Een badkuip bevat ongeveer hoeveel liter?", ["150 liter", "50 liter", "500 liter", "10 liter"], 0),
        ("Een zwembad bevat ongeveer hoeveel liter?", ["1000 liter of meer", "100 liter", "50 liter", "10 liter"], 0),
        ("2 pakken melk van 1 liter = hoeveel liter?", ["2 liter", "1 liter", "3 liter", "1.5 liter"], 0),
        ("Een halve liter is hetzelfde als...", ["0.5 liter", "0.25 liter", "1 liter", "2 liter"], 0),
        ("Een kwart liter is hetzelfde als...", ["0.25 liter", "0.5 liter", "1 liter", "0.75 liter"], 0),
        ("3 bekers van 0.25 liter = hoeveel liter?", ["0.75 liter", "1 liter", "0.5 liter", "1.5 liter"], 0),
    ]

    for i, (q, opts, correct_idx) in enumerate(questions[:count]):
        if q in seen:
            continue
        seen.add(q)

        correct = opts[correct_idx]
        wrong = [opt for j, opt in enumerate(opts) if j != correct_idx]
        exercises.append(create_exercise(q, correct, wrong, "inhoud_liter"))

    return exercises[:count]

def generate_4MM4_exercises(count=13):
    """4MM4: Tijd minuten"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        # Generate time intervals
        hour1 = random.randint(8, 14)
        min1 = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        duration = random.choice([5, 10, 15, 20, 25, 30])

        min2 = min1 + duration
        hour2 = hour1
        if min2 >= 60:
            min2 -= 60
            hour2 += 1

        q = f"Hoeveel minuten zitten er tussen {hour1}:{min1:02d} en {hour2}:{min2:02d}?"
        if q in seen:
            continue
        seen.add(q)

        correct = f"{duration} minuten"
        wrong = [
            f"{duration+5} minuten",
            f"{duration-5} minuten" if duration > 5 else f"{duration+10} minuten",
            f"{duration+10} minuten" if duration < 30 else f"{duration-10} minuten"
        ]

        exercises.append(create_exercise(q, correct, wrong, "tijd_minuten"))

    return exercises[:count]

def generate_4MM5_exercises(count=17):
    """4MM5: Omtrek vierkant en rechthoek"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        shape = random.choice(['vierkant', 'rechthoek'])

        if shape == 'vierkant':
            zijde = random.randint(3, 15)
            omtrek = 4 * zijde
            q = f"Een vierkant heeft zijde {zijde} cm. Wat is de omtrek?"
            correct = f"{omtrek} cm"
            wrong = [f"{omtrek+4} cm", f"{omtrek-4} cm", f"{zijde*2} cm"]
        else:
            lengte = random.randint(5, 20)
            breedte = random.randint(3, lengte-1)
            omtrek = 2 * (lengte + breedte)
            q = f"Een rechthoek heeft lengte {lengte} cm en breedte {breedte} cm. Wat is de omtrek?"
            correct = f"{omtrek} cm"
            wrong = [f"{omtrek+2} cm", f"{omtrek-2} cm", f"{lengte+breedte} cm"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "omtrek"))

    return exercises[:count]

def generate_4MM6_exercises(count=17):
    """4MM6: Ruimtelijke figuren"""
    exercises = []
    seen = set()

    questions = [
        ("Hoeveel vlakken heeft een kubus?", ["6 vlakken", "4 vlakken", "8 vlakken", "5 vlakken"], 0),
        ("Hoeveel hoekpunten heeft een kubus?", ["8 hoekpunten", "6 hoekpunten", "12 hoekpunten", "4 hoekpunten"], 0),
        ("Hoeveel ribben heeft een kubus?", ["12 ribben", "8 ribben", "6 ribben", "10 ribben"], 0),
        ("Een dobbelsteen heeft de vorm van een...", ["kubus", "balk", "bol", "cilinder"], 0),
        ("Een voetbal heeft de vorm van een...", ["bol", "kubus", "cilinder", "piramide"], 0),
        ("Een blikje heeft de vorm van een...", ["cilinder", "kubus", "bol", "balk"], 0),
        ("Een schoenendoos heeft de vorm van een...", ["balk", "kubus", "cilinder", "bol"], 0),
        ("Welke ruimtelijke figuur heeft geen hoeken?", ["bol", "kubus", "balk", "piramide"], 0),
        ("Hoeveel vlakken heeft een balk?", ["6 vlakken", "4 vlakken", "8 vlakken", "5 vlakken"], 0),
        ("Een piramide heeft aan de bovenkant een...", ["punt", "vlak", "cirkel", "vierkant"], 0),
        ("Welke figuur kun je rollen?", ["cilinder", "kubus", "piramide", "balk"], 0),
        ("Een kubus heeft allemaal...", ["vierkante vlakken", "rechthoekige vlakken", "driehoekige vlakken", "ronde vlakken"], 0),
        ("Hoeveel gelijke ribben heeft een kubus?", ["12", "6", "8", "4"], 0),
        ("Een cilinder heeft hoeveel platte vlakken?", ["2", "1", "3", "0"], 0),
        ("Welke figuur heeft 1 punt bovenaan?", ["piramide", "kubus", "balk", "cilinder"], 0),
        ("Een balk heeft...", ["6 rechthoekige vlakken", "6 vierkante vlakken", "4 vlakken", "8 vlakken"], 0),
        ("Een bol heeft hoeveel vlakken?", ["0 vlakken", "1 vlak", "2 vlakken", "oneindig veel"], 0),
    ]

    for i, (q, opts, correct_idx) in enumerate(questions[:count]):
        if q in seen:
            continue
        seen.add(q)

        correct = opts[correct_idx]
        wrong = [opt for j, opt in enumerate(opts) if j != correct_idx]
        exercises.append(create_exercise(q, correct, wrong, "ruimtelijke_figuren"))

    return exercises[:count]

def generate_4MM7_exercises(count=16):
    """4MM7: Geld tot 100 euro"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        price = round(random.uniform(5, 85), 2)
        if price < 50:
            payment = 50
        else:
            payment = 100
        change = round(payment - price, 2)

        items = ["speelgoed", "boek", "trui", "schoenen", "jas", "tas", "spel",
                 "puzzel", "bal", "racket", "rugzak"]
        item = random.choice(items)

        q = f"Je koopt {item} voor €{price:.2f} en betaalt met €{payment}. Hoeveel wisselgeld?"
        if q in seen:
            continue
        seen.add(q)

        correct = f"€{change:.2f}"
        wrong = [
            f"€{change+1:.2f}",
            f"€{change-1:.2f}" if change > 1 else f"€{change+2:.2f}",
            f"€{change+0.50:.2f}"
        ]

        exercises.append(create_exercise(q, correct, wrong, "geld_100"))

    return exercises[:count]

# ============================================================================
# GROEP 5 GENERATORS
# ============================================================================

def generate_5MM1_exercises(count=12):
    """5MM1: Kilometer"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        choice = random.choice(['km_to_m', 'm_to_km', 'basic'])

        if choice == 'basic':
            q = "Hoeveel meter is 1 kilometer?"
            correct = "1000 meter"
            wrong = ["100 meter", "500 meter", "10000 meter"]
        elif choice == 'km_to_m':
            km = random.randint(1, 10)
            m = km * 1000
            q = f"{km} km = hoeveel meter?"
            correct = f"{m} meter"
            wrong = [f"{m+100} meter", f"{m-100} meter", f"{km*100} meter"]
        else:  # m_to_km
            meters = random.choice([500, 1000, 1500, 2000, 2500, 3000, 4000, 5000])
            km = meters / 1000
            q = f"{meters} meter = hoeveel kilometer?"
            correct = f"{km:.1f} km" if km % 1 != 0 else f"{int(km)} km"
            wrong = [
                f"{km+0.5:.1f} km",
                f"{meters/100:.1f} km",
                f"{km-0.5:.1f} km" if km > 1 else f"{km+1:.1f} km"
            ]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "kilometer"))

    return exercises[:count]

def generate_5MM2_exercises(count=13):
    """5MM2: Ton"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        choice = random.choice(['ton_to_kg', 'kg_to_ton', 'basic'])

        if choice == 'basic':
            q = "Hoeveel kilogram is 1 ton?"
            correct = "1000 kg"
            wrong = ["100 kg", "500 kg", "10000 kg"]
        elif choice == 'ton_to_kg':
            ton = random.randint(1, 5)
            kg = ton * 1000
            q = f"{ton} ton = hoeveel kilogram?"
            correct = f"{kg} kg"
            wrong = [f"{kg+100} kg", f"{kg-100} kg", f"{ton*100} kg"]
        else:  # kg_to_ton
            kg = random.choice([500, 1000, 1500, 2000, 2500, 3000, 4000, 5000])
            ton = kg / 1000
            q = f"{kg} kg = hoeveel ton?"
            correct = f"{ton:.1f} ton" if ton % 1 != 0 else f"{int(ton)} ton"
            wrong = [
                f"{ton+0.5:.1f} ton",
                f"{kg/100:.1f} ton",
                f"{ton-0.5:.1f} ton" if ton > 1 else f"{ton+1:.1f} ton"
            ]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "ton"))

    return exercises[:count]

def generate_5MM3_exercises(count=12):
    """5MM3: ml, cl, dl, l"""
    exercises = []
    seen = set()

    conversions_data = [
        (250, "ml", "cl", 10, 25),
        (500, "ml", "l", 1000, 0.5),
        (100, "cl", "l", 100, 1),
        (50, "cl", "dl", 10, 5),
        (5, "dl", "l", 10, 0.5),
        (750, "ml", "l", 1000, 0.75),
    ]

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        value, from_unit, to_unit, divisor, result = random.choice(conversions_data)
        # Randomize value a bit
        value = value + random.randint(-50, 50)
        result = value / divisor

        q = f"{value} {from_unit} = hoeveel {to_unit}?"
        if q in seen:
            continue
        seen.add(q)

        correct = f"{result:.2f} {to_unit}" if result % 1 != 0 else f"{int(result)} {to_unit}"
        wrong_val1 = result + (divisor/100 if divisor > 10 else 1)
        wrong_val2 = result - (divisor/100 if divisor > 10 else 1) if result > 1 else result + 2
        wrong = [
            f"{wrong_val1:.2f} {to_unit}" if wrong_val1 % 1 != 0 else f"{int(wrong_val1)} {to_unit}",
            f"{value} {to_unit}",
            f"{wrong_val2:.2f} {to_unit}" if wrong_val2 % 1 != 0 else f"{int(wrong_val2)} {to_unit}"
        ]

        exercises.append(create_exercise(q, correct, wrong, "inhoud_eenheden"))

    return exercises[:count]

def generate_5MM4_exercises(count=13):
    """5MM4: Oppervlakte begrip (tellen cm²)"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        # Simple rectangle on grid
        lengte = random.randint(3, 8)
        breedte = random.randint(2, 6)
        oppervlakte = lengte * breedte

        q = f"Een rechthoek op roosterpapier is {lengte} hokjes lang en {breedte} hokjes breed. Hoeveel cm² bedekt deze figuur?"
        if q in seen:
            continue
        seen.add(q)

        correct = f"{oppervlakte} cm²"
        wrong = [
            f"{oppervlakte+2} cm²",
            f"{oppervlakte-2} cm²" if oppervlakte > 5 else f"{oppervlakte+4} cm²",
            f"{lengte+breedte} cm²"
        ]

        exercises.append(create_exercise(q, correct, wrong, "oppervlakte_tellen"))

    return exercises[:count]

def generate_5MM5_exercises(count=14):
    """5MM5: Tijd digitale en analoge klok"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        # Time calculations
        hour1 = random.randint(8, 16)
        min1 = random.randint(0, 59)
        duration_min = random.choice([30, 45, 60, 75, 90, 120])

        total_min = hour1 * 60 + min1 + duration_min
        hour2 = (total_min // 60) % 24
        min2 = total_min % 60

        q = f"Van {hour1}:{min1:02d} tot {hour2}:{min2:02d} is hoeveel tijd?"
        if q in seen:
            continue
        seen.add(q)

        hours = duration_min // 60
        minutes = duration_min % 60

        if hours > 0 and minutes > 0:
            correct = f"{hours} uur en {minutes} minuten"
        elif hours > 0:
            correct = f"{hours} uur"
        else:
            correct = f"{minutes} minuten"

        wrong = [
            f"{duration_min+30} minuten",
            f"{duration_min-15} minuten" if duration_min > 15 else f"{duration_min+15} minuten",
            f"{hours+1} uur" if hours > 0 else f"{minutes+30} minuten"
        ]

        exercises.append(create_exercise(q, correct, wrong, "tijd_berekenen"))

    return exercises[:count]

def generate_5MM6_exercises(count=12):
    """5MM6: Oppervlakte vierkant/rechthoek met formule"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        shape = random.choice(['vierkant', 'rechthoek'])

        if shape == 'vierkant':
            zijde = random.randint(4, 12)
            opp = zijde * zijde
            q = f"Een vierkant heeft zijde {zijde} cm. Wat is de oppervlakte?"
            correct = f"{opp} cm²"
            wrong = [f"{opp+5} cm²", f"{opp-5} cm²" if opp > 10 else f"{opp+10} cm²", f"{zijde*4} cm²"]
        else:
            lengte = random.randint(5, 15)
            breedte = random.randint(3, 10)
            opp = lengte * breedte
            q = f"Een rechthoek heeft lengte {lengte} cm en breedte {breedte} cm. Wat is de oppervlakte?"
            correct = f"{opp} cm²"
            wrong = [f"{opp+5} cm²", f"{opp-5} cm²", f"{(lengte+breedte)*2} cm²"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "oppervlakte_formule"))

    return exercises[:count]

def generate_5MM7_exercises(count=14):
    """5MM7: Symmetrie"""
    exercises = []
    seen = set()

    questions = [
        ("Is een vierkant symmetrisch?", ["Ja", "Nee", "Soms", "Alleen diagonaal"], 0),
        ("Hoeveel symmetrie-assen heeft een vierkant?", ["4", "2", "1", "8"], 0),
        ("Hoeveel symmetrie-assen heeft een rechthoek?", ["2", "1", "4", "0"], 0),
        ("Hoeveel symmetrie-assen heeft een cirkel?", ["Oneindig veel", "1", "2", "4"], 0),
        ("Welke letter is symmetrisch?", ["A", "B", "F", "R"], 0),
        ("Is de letter B symmetrisch?", ["Nee", "Ja", "Alleen horizontaal", "Alleen verticaal"], 0),
        ("Een vlinder is meestal...", ["symmetrisch", "asymmetrisch", "rond", "vierkant"], 0),
        ("Hoeveel symmetrie-assen heeft een gelijkzijdige driehoek?", ["3", "1", "2", "4"], 0),
        ("Een hart is symmetrisch. Hoeveel assen?", ["1", "2", "0", "4"], 0),
        ("De letter M heeft hoeveel symmetrie-assen?", ["1", "2", "0", "4"], 0),
        ("Een ster (vijfpuntig) heeft hoeveel symmetrie-assen?", ["5", "1", "2", "10"], 0),
        ("Is een vierkant verticaal symmetrisch?", ["Ja", "Nee", "Soms", "Nooit"], 0),
        ("Welke figuur heeft de meeste symmetrie-assen?", ["cirkel", "vierkant", "driehoek", "rechthoek"], 0),
        ("Een symmetrie-as deelt een figuur in...", ["twee gelijke delen", "twee ongelijke delen", "drie delen", "vier delen"], 0),
    ]

    for i, (q, opts, correct_idx) in enumerate(questions[:count]):
        if q in seen:
            continue
        seen.add(q)

        correct = opts[correct_idx]
        wrong = [opt for j, opt in enumerate(opts) if j != correct_idx]
        exercises.append(create_exercise(q, correct, wrong, "symmetrie"))

    return exercises[:count]

# ============================================================================
# GROEP 6 GENERATORS
# ============================================================================

def generate_6MM1_exercises(count=13):
    """6MM1: Oppervlakte driehoek"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        basis = random.randint(4, 20)
        hoogte = random.randint(3, 15)
        opp = (basis * hoogte) / 2

        q = f"Een driehoek heeft basis {basis} cm en hoogte {hoogte} cm. Wat is de oppervlakte?"
        if q in seen:
            continue
        seen.add(q)

        correct = f"{opp:.1f} cm²" if opp % 1 != 0 else f"{int(opp)} cm²"
        wrong_val = basis * hoogte  # Common mistake: forgetting to divide by 2
        wrong = [
            f"{wrong_val} cm²",
            f"{opp+5:.1f} cm²" if opp % 1 != 0 else f"{int(opp)+5} cm²",
            f"{opp-5:.1f} cm²" if opp > 10 else f"{opp+10:.1f} cm²"
        ]

        exercises.append(create_exercise(q, correct, wrong, "oppervlakte_driehoek"))

    return exercises[:count]

def generate_6MM2_exercises(count=12):
    """6MM2: Omtrek cirkel"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        choice = random.choice(['diameter', 'straal'])

        if choice == 'diameter':
            diameter = random.randint(5, 20)
            omtrek = round(3.14 * diameter, 2)
            q = f"Een cirkel heeft diameter {diameter} cm. Wat is de omtrek? (gebruik π = 3,14)"
            correct = f"{omtrek:.2f} cm"
        else:  # straal
            straal = random.randint(3, 15)
            omtrek = round(2 * 3.14 * straal, 2)
            q = f"Een cirkel heeft straal {straal} cm. Wat is de omtrek? (gebruik π = 3,14)"
            correct = f"{omtrek:.2f} cm"

        if q in seen:
            continue
        seen.add(q)

        wrong = [
            f"{omtrek+5:.2f} cm",
            f"{omtrek-5:.2f} cm" if omtrek > 10 else f"{omtrek+10:.2f} cm",
            f"{omtrek*2:.2f} cm"
        ]

        exercises.append(create_exercise(q, correct, wrong, "omtrek_cirkel"))

    return exercises[:count]

def generate_6MM3_exercises(count=12):
    """6MM3: Coördinaten"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        x = random.randint(1, 10)
        y = random.randint(1, 10)

        templates = [
            f"Punt A ligt op ({x}, {y}). Wat is de x-coördinaat?",
            f"Punt B ligt op ({x}, {y}). Wat is de y-coördinaat?",
            f"Welke coördinaten heeft punt C als het op x={x} en y={y} ligt?",
        ]

        q = random.choice(templates)
        if q in seen:
            continue
        seen.add(q)

        if "x-coördinaat" in q:
            correct = str(x)
            wrong = [str(y), str(x+1), str(x-1) if x > 1 else str(x+2)]
        elif "y-coördinaat" in q:
            correct = str(y)
            wrong = [str(x), str(y+1), str(y-1) if y > 1 else str(y+2)]
        else:
            correct = f"({x}, {y})"
            wrong = [f"({y}, {x})", f"({x+1}, {y})", f"({x}, {y+1})"]

        exercises.append(create_exercise(q, correct, wrong, "coordinaten"))

    return exercises[:count]

def generate_6MM4_exercises(count=13):
    """6MM4: Hoeken meten"""
    exercises = []
    seen = set()

    questions = [
        ("Een rechte hoek is hoeveel graden?", ["90°", "45°", "180°", "60°"], 0),
        ("Een halve cirkel is hoeveel graden?", ["180°", "90°", "360°", "270°"], 0),
        ("Een hele cirkel is hoeveel graden?", ["360°", "180°", "270°", "90°"], 0),
        ("Een kwart cirkel is hoeveel graden?", ["90°", "45°", "60°", "180°"], 0),
        ("Welke hoek is 45°?", ["halve rechte hoek", "rechte hoek", "stompe hoek", "halve cirkel"], 0),
        ("Een driehoek heeft hoeveel graden in totaal?", ["180°", "90°", "360°", "270°"], 0),
        ("60° is een...", ["scherpe hoek", "rechte hoek", "stompe hoek", "gestrekte hoek"], 0),
        ("120° is een...", ["stompe hoek", "scherpe hoek", "rechte hoek", "gestrekte hoek"], 0),
        ("Een gestrekte hoek is...", ["180°", "90°", "360°", "270°"], 0),
        ("30° + 60° = ?", ["90°", "80°", "100°", "120°"], 0),
        ("180° - 90° = ?", ["90°", "80°", "100°", "180°"], 0),
        ("Een vierkant heeft in elke hoek...", ["90°", "45°", "60°", "180°"], 0),
        ("Twee rechte hoeken samen zijn...", ["180°", "90°", "360°", "270°"], 0),
    ]

    for i, (q, opts, correct_idx) in enumerate(questions[:count]):
        if q in seen:
            continue
        seen.add(q)

        correct = opts[correct_idx]
        wrong = [opt for j, opt in enumerate(opts) if j != correct_idx]
        exercises.append(create_exercise(q, correct, wrong, "hoeken_meten"))

    return exercises[:count]

def generate_6MM5_exercises(count=14):
    """6MM5: Volume kubus/balk"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        shape = random.choice(['kubus', 'balk'])

        if shape == 'kubus':
            ribbe = random.randint(3, 10)
            volume = ribbe ** 3
            q = f"Een kubus heeft ribbe {ribbe} cm. Wat is het volume?"
            correct = f"{volume} cm³"
            wrong = [f"{volume+10} cm³", f"{volume-10} cm³" if volume > 20 else f"{volume+20} cm³", f"{ribbe*6} cm³"]
        else:
            lengte = random.randint(4, 12)
            breedte = random.randint(3, 10)
            hoogte = random.randint(2, 8)
            volume = lengte * breedte * hoogte
            q = f"Een balk heeft afmetingen {lengte} × {breedte} × {hoogte} cm. Wat is het volume?"
            correct = f"{volume} cm³"
            wrong = [f"{volume+10} cm³", f"{volume-10} cm³", f"{lengte*breedte} cm³"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "volume"))

    return exercises[:count]

def generate_6MM6_exercises(count=14):
    """6MM6: Perspectief tekenen"""
    exercises = []
    seen = set()

    questions = [
        ("Hoeveel blokjes zie je in deze stapel: 2 lagen van 3×2 blokjes?", ["12 blokjes", "6 blokjes", "8 blokjes", "10 blokjes"], 0),
        ("Een kubus heeft hoeveel zichtbare vlakken als je van voren kijkt?", ["3 vlakken", "1 vlak", "2 vlakken", "6 vlakken"], 0),
        ("Van bovenaf zie je 4×3 blokjes. Hoeveel blokjes zijn dat?", ["12 blokjes", "7 blokjes", "16 blokjes", "10 blokjes"], 0),
        ("Een stapel van 2 hoog en 3×3 breed heeft hoeveel blokjes?", ["18 blokjes", "9 blokjes", "12 blokjes", "27 blokjes"], 0),
        ("Bovenaanzicht toont 6 blokjes. Hoeveel blokjes zijn er minimaal?", ["6 blokjes", "1 blokje", "12 blokjes", "3 blokjes"], 0),
        ("Een toren van 5 blokjes hoog - hoeveel blokjes?", ["5 blokjes", "10 blokjes", "15 blokjes", "20 blokjes"], 0),
        ("2 lagen van elk 2×2 blokjes = hoeveel blokjes totaal?", ["8 blokjes", "4 blokjes", "6 blokjes", "12 blokjes"], 0),
        ("Van voren zie je 4 blokjes, van opzij 3. Minimaal aantal?", ["4 blokjes", "7 blokjes", "12 blokjes", "3 blokjes"], 0),
        ("Een L-vorm van 5 blokjes, 2 lagen hoog = hoeveel blokjes?", ["10 blokjes", "5 blokjes", "15 blokjes", "20 blokjes"], 0),
        ("3 blokjes naast elkaar, 3 lagen hoog = ?", ["9 blokjes", "6 blokjes", "12 blokjes", "3 blokjes"], 0),
        ("Een trap van 1, 2, 3 blokjes heeft hoeveel blokjes totaal?", ["6 blokjes", "3 blokjes", "9 blokjes", "12 blokjes"], 0),
        ("Een vierkant van 4×4 blokjes is hoeveel blokjes?", ["16 blokjes", "8 blokjes", "12 blokjes", "20 blokjes"], 0),
        ("2×3 blokjes, 4 lagen hoog = ?", ["24 blokjes", "6 blokjes", "12 blokjes", "18 blokjes"], 0),
        ("Een rij van 6 blokjes, 2 hoog = ?", ["12 blokjes", "6 blokjes", "8 blokjes", "18 blokjes"], 0),
    ]

    for i, (q, opts, correct_idx) in enumerate(questions[:count]):
        if q in seen:
            continue
        seen.add(q)

        correct = opts[correct_idx]
        wrong = [opt for j, opt in enumerate(opts) if j != correct_idx]
        exercises.append(create_exercise(q, correct, wrong, "perspectief"))

    return exercises[:count]

def generate_6MM7_exercises(count=11):
    """6MM7: Schaal op kaarten"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        schalen = [100000, 50000, 25000]
        schaal = random.choice(schalen)
        cm_op_kaart = random.randint(2, 10)

        # Calculate real distance in meters, then convert to km
        real_m = cm_op_kaart * schaal / 100  # cm to m
        real_km = real_m / 1000

        q = f"Op de kaart is de afstand {cm_op_kaart} cm. Schaal 1:{schaal}. Wat is de echte afstand in km?"
        if q in seen:
            continue
        seen.add(q)

        correct = f"{real_km:.1f} km" if real_km % 1 != 0 else f"{int(real_km)} km"
        wrong = [
            f"{real_km+0.5:.1f} km",
            f"{real_km-0.5:.1f} km" if real_km > 1 else f"{real_km+1:.1f} km",
            f"{cm_op_kaart} km"
        ]

        exercises.append(create_exercise(q, correct, wrong, "schaal_kaarten"))

    return exercises[:count]

# ============================================================================
# GROEP 7 GENERATORS
# ============================================================================

def generate_7MM1_exercises(count=17):
    """7MM1: Oppervlakte cirkel"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        straal = random.randint(3, 15)
        opp = round(3.14 * straal * straal, 2)

        q = f"Een cirkel heeft straal {straal} cm. Wat is de oppervlakte? (gebruik π = 3,14)"
        if q in seen:
            continue
        seen.add(q)

        correct = f"{opp:.2f} cm²"
        wrong = [
            f"{opp+10:.2f} cm²",
            f"{opp-10:.2f} cm²" if opp > 20 else f"{opp+20:.2f} cm²",
            f"{round(2*3.14*straal, 2):.2f} cm²"  # Common mistake: using circumference formula
        ]

        exercises.append(create_exercise(q, correct, wrong, "oppervlakte_cirkel"))

    return exercises[:count]

def generate_7MM2_exercises(count=17):
    """7MM2: Diagonalen meten (praktisch, geen Pythagoras)"""
    exercises = []
    seen = set()

    questions = [
        ("Een vierkant met zijde 10 cm. Schat de diagonaal.", ["ongeveer 14 cm", "10 cm", "20 cm", "5 cm"], 0),
        ("Hoeveel diagonalen heeft een rechthoek?", ["2", "1", "4", "0"], 0),
        ("De diagonalen in een rechthoek zijn...", ["even lang", "verschillend lang", "loodrecht", "geen van allen"], 0),
        ("Een vierkant met zijde 5 cm. Diagonaal is ongeveer...", ["7 cm", "5 cm", "10 cm", "3 cm"], 0),
        ("Meet de diagonaal van een rechthoek 6×8 cm. Ongeveer...", ["10 cm", "6 cm", "8 cm", "14 cm"], 0),
        ("Een vierkant met zijde 8 cm heeft diagonaal van ongeveer...", ["11 cm", "8 cm", "16 cm", "4 cm"], 0),
        ("Diagonalen in een vierkant zijn...", ["even lang", "verschillend", "kort", "lang"], 0),
        ("Een rechthoek 3×4 cm. Diagonaal ongeveer...", ["5 cm", "3 cm", "4 cm", "7 cm"], 0),
        ("Hoeveel diagonalen heeft een vierkant?", ["2", "1", "4", "8"], 0),
        ("De diagonaal van een vierkant is... dan de zijde", ["langer", "korter", "even lang", "half"], 0),
        ("Een rechthoek 5×12 cm. Diagonaal ongeveer...", ["13 cm", "5 cm", "12 cm", "17 cm"], 0),
        ("Vierkant zijde 12 cm. Diagonaal ongeveer...", ["17 cm", "12 cm", "24 cm", "6 cm"], 0),
        ("Een vierkant zijde 6 cm. Diagonaal is ongeveer...", ["8 cm", "6 cm", "12 cm", "3 cm"], 0),
        ("Rechthoek 8×15 cm. Diagonaal ongeveer...", ["17 cm", "8 cm", "15 cm", "23 cm"], 0),
        ("Diagonaal van vierkant zijde 20 cm is ongeveer...", ["28 cm", "20 cm", "40 cm", "10 cm"], 0),
        ("Een rechthoek 9×12 cm. Diagonaal ongeveer...", ["15 cm", "9 cm", "12 cm", "21 cm"], 0),
        ("Vierkant zijde 15 cm. Diagonaal ongeveer...", ["21 cm", "15 cm", "30 cm", "7 cm"], 0),
    ]

    for i, (q, opts, correct_idx) in enumerate(questions[:count]):
        if q in seen:
            continue
        seen.add(q)

        correct = opts[correct_idx]
        wrong = [opt for j, opt in enumerate(opts) if j != correct_idx]
        exercises.append(create_exercise(q, correct, wrong, "diagonalen"))

    return exercises[:count]

def generate_7MM3_exercises(count=16):
    """7MM3: Hoeken soorten"""
    exercises = []
    seen = set()

    questions = [
        ("Een hoek van 45° is...", ["scherp", "recht", "stomp", "gestrekt"], 0),
        ("Een hoek van 90° is...", ["recht", "scherp", "stomp", "gestrekt"], 0),
        ("Een hoek van 120° is...", ["stomp", "scherp", "recht", "gestrekt"], 0),
        ("Een hoek van 180° is...", ["gestrekt", "recht", "stomp", "scherp"], 0),
        ("Welke hoek is scherp?", ["60°", "90°", "120°", "180°"], 0),
        ("Welke hoek is stomp?", ["135°", "90°", "60°", "45°"], 0),
        ("Een scherpe hoek is...", ["< 90°", "= 90°", "> 90°", "= 180°"], 0),
        ("Een stompe hoek is...", ["> 90° en < 180°", "< 90°", "= 90°", "= 180°"], 0),
        ("30° is een...", ["scherpe hoek", "rechte hoek", "stompe hoek", "gestrekte hoek"], 0),
        ("150° is een...", ["stompe hoek", "scherpe hoek", "rechte hoek", "gestrekte hoek"], 0),
        ("75° is een...", ["scherpe hoek", "rechte hoek", "stompe hoek", "gestrekte hoek"], 0),
        ("Een driehoek met hoeken 60°, 60°, 60° heeft...", ["alleen scherpe hoeken", "een rechte hoek", "een stompe hoek", "een gestrekte hoek"], 0),
        ("Een driehoek met hoeken 90°, 45°, 45° heeft...", ["een rechte hoek", "alleen scherpe hoeken", "een stompe hoek", "geen rechte hoek"], 0),
        ("110° is een...", ["stompe hoek", "scherpe hoek", "rechte hoek", "gestrekte hoek"], 0),
        ("25° is een...", ["scherpe hoek", "rechte hoek", "stompe hoek", "gestrekte hoek"], 0),
        ("Een hoek van 170° is...", ["stompe hoek", "scherpe hoek", "rechte hoek", "gestrekte hoek"], 0),
    ]

    for i, (q, opts, correct_idx) in enumerate(questions[:count]):
        if q in seen:
            continue
        seen.add(q)

        correct = opts[correct_idx]
        wrong = [opt for j, opt in enumerate(opts) if j != correct_idx]
        exercises.append(create_exercise(q, correct, wrong, "hoeksoorten"))

    return exercises[:count]

def generate_7MM4_exercises(count=17):
    """7MM4: Coördinatenstelsel met 4 kwadranten"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        x = random.randint(-10, 10)
        y = random.randint(-10, 10)

        # Determine kwadrant
        if x > 0 and y > 0:
            kwadrant = "I (eerste)"
        elif x < 0 and y > 0:
            kwadrant = "II (tweede)"
        elif x < 0 and y < 0:
            kwadrant = "III (derde)"
        elif x > 0 and y < 0:
            kwadrant = "IV (vierde)"
        else:
            kwadrant = "op een as"

        templates = [
            f"In welk kwadrant ligt punt ({x}, {y})?",
            f"Punt A ligt op ({x}, {y}). Wat is de x-coördinaat?",
            f"Punt B ligt op ({x}, {y}). Wat is de y-coördinaat?",
        ]

        q = random.choice(templates)
        if q in seen or kwadrant == "op een as":
            continue
        seen.add(q)

        if "kwadrant" in q:
            correct = kwadrant
            all_kw = ["I (eerste)", "II (tweede)", "III (derde)", "IV (vierde)"]
            wrong = [kw for kw in all_kw if kw != kwadrant][:3]
        elif "x-coördinaat" in q:
            correct = str(x)
            wrong = [str(y), str(x+1), str(-x)]
        else:  # y-coördinaat
            correct = str(y)
            wrong = [str(x), str(y+1), str(-y)]

        exercises.append(create_exercise(q, correct, wrong, "coordinatenstelsel"))

    return exercises[:count]

def generate_7MM5_exercises(count=17):
    """7MM5: Volume cilinder"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        straal = random.randint(3, 10)
        hoogte = random.randint(5, 20)

        # Volume = π × r² × h
        volume = round(3.14 * straal * straal * hoogte, 2)

        q = f"Een cilinder heeft straal {straal} cm en hoogte {hoogte} cm. Wat is het volume? (π = 3,14)"
        if q in seen:
            continue
        seen.add(q)

        correct = f"{volume:.2f} cm³"
        wrong = [
            f"{volume+50:.2f} cm³",
            f"{volume-50:.2f} cm³" if volume > 100 else f"{volume+100:.2f} cm³",
            f"{round(3.14*straal*hoogte, 2):.2f} cm³"  # Mistake: forgot r²
        ]

        exercises.append(create_exercise(q, correct, wrong, "volume_cilinder"))

    return exercises[:count]

def generate_7MM6_exercises(count=16):
    """7MM6: Spiegeling en rotatie"""
    exercises = []
    seen = set()

    questions = [
        ("Punt (3, 4) gespiegeld in x-as wordt...", ["(3, -4)", "(-3, 4)", "(-3, -4)", "(4, 3)"], 0),
        ("Punt (5, 2) gespiegeld in y-as wordt...", ["(-5, 2)", "(5, -2)", "(-5, -2)", "(2, 5)"], 0),
        ("Punt (-2, 3) gespiegeld in x-as wordt...", ["(-2, -3)", "(2, 3)", "(2, -3)", "(3, -2)"], 0),
        ("Punt (4, -1) gespiegeld in y-as wordt...", ["(-4, -1)", "(4, 1)", "(-4, 1)", "(-1, 4)"], 0),
        ("Punt (6, 0) gespiegeld in x-as wordt...", ["(6, 0)", "(-6, 0)", "(0, 6)", "(0, -6)"], 0),
        ("Punt (0, 5) gespiegeld in y-as wordt...", ["(0, 5)", "(0, -5)", "(5, 0)", "(-5, 0)"], 0),
        ("Spiegelen in x-as verandert...", ["de y-coördinaat", "de x-coördinaat", "beide", "geen"], 0),
        ("Spiegelen in y-as verandert...", ["de x-coördinaat", "de y-coördinaat", "beide", "geen"], 0),
        ("Punt (3, 3) 90° draaien tegen de klok in om oorsprong wordt...", ["(-3, 3)", "(3, -3)", "(-3, -3)", "(3, 3)"], 0),
        ("Punt (4, 0) 180° draaien om oorsprong wordt...", ["(-4, 0)", "(4, 0)", "(0, 4)", "(0, -4)"], 0),
        ("Punt (2, 5) 180° draaien om oorsprong wordt...", ["(-2, -5)", "(2, -5)", "(-2, 5)", "(5, 2)"], 0),
        ("Een figuur spiegelen in de x-as: y wordt...", ["-y", "x", "-x", "y"], 0),
        ("Een figuur spiegelen in de y-as: x wordt...", ["-x", "y", "-y", "x"], 0),
        ("Punt (-3, -2) gespiegeld in x-as wordt...", ["(-3, 2)", "(3, -2)", "(3, 2)", "(-2, -3)"], 0),
        ("Punt (7, -3) gespiegeld in y-as wordt...", ["(-7, -3)", "(7, 3)", "(-7, 3)", "(-3, 7)"], 0),
        ("180° rotatie verandert (x, y) in...", ["(-x, -y)", "(y, x)", "(-y, -x)", "(x, -y)"], 0),
    ]

    for i, (q, opts, correct_idx) in enumerate(questions[:count]):
        if q in seen:
            continue
        seen.add(q)

        correct = opts[correct_idx]
        wrong = [opt for j, opt in enumerate(opts) if j != correct_idx]
        exercises.append(create_exercise(q, correct, wrong, "transformaties"))

    return exercises[:count]

# ============================================================================
# GROEP 8 GENERATORS
# ============================================================================

def generate_8MM1_exercises(count=17):
    """8MM1: Complexe oppervlaktes (samengestelde figuren)"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        # L-vorm: two rectangles
        r1_l = random.randint(5, 12)
        r1_b = random.randint(3, 8)
        r2_l = random.randint(3, 8)
        r2_b = random.randint(2, 6)

        opp_total = r1_l * r1_b + r2_l * r2_b

        q = f"Een L-vorm bestaat uit twee rechthoeken: {r1_l}×{r1_b} cm en {r2_l}×{r2_b} cm. Totale oppervlakte?"
        if q in seen:
            continue
        seen.add(q)

        correct = f"{opp_total} cm²"
        wrong = [
            f"{opp_total+10} cm²",
            f"{opp_total-10} cm²" if opp_total > 20 else f"{opp_total+20} cm²",
            f"{(r1_l+r2_l)*(r1_b+r2_b)} cm²"
        ]

        exercises.append(create_exercise(q, correct, wrong, "complexe_oppervlakte"))

    return exercises[:count]

def generate_8MM2_exercises(count=17):
    """8MM2: Eigenschappen meetkundige figuren"""
    exercises = []
    seen = set()

    questions = [
        ("Hoeveel ribben heeft een kubus?", ["12", "8", "6", "10"], 0),
        ("Wat is de som van hoeken in een driehoek?", ["180°", "90°", "360°", "270°"], 0),
        ("Hoeveel vlakken heeft een cilinder?", ["3 (2 cirkels + 1 gebogen)", "2", "1", "4"], 0),
        ("Een rechthoek heeft...", ["4 rechte hoeken en 2 paar evenwijdige zijden", "3 hoeken", "geen evenwijdige zijden", "alleen scherpe hoeken"], 0),
        ("Een kubus en een balk: overeenkomst?", ["Beide hebben 6 vlakken", "Beide zijn rond", "Beide hebben 4 vlakken", "Geen overeenkomst"], 0),
        ("Een vijfhoek heeft hoeveel hoeken?", ["5", "4", "6", "3"], 0),
        ("Hoeveel symmetrie-assen heeft een vierkant?", ["4", "2", "1", "8"], 0),
        ("Welke ruimtelijke figuur heeft geen hoekpunten?", ["bol", "kubus", "piramide", "balk"], 0),
        ("Een rechthoek heeft hoeveel symmetrie-assen?", ["2", "1", "4", "0"], 0),
        ("Hoeveel hoekpunten heeft een piramide met vierkant grondvlak?", ["5", "4", "6", "8"], 0),
        ("Een parallellogram heeft...", ["2 paar evenwijdige zijden", "geen evenwijdige zijden", "1 paar evenwijdige zijden", "4 rechte hoeken"], 0),
        ("Een ruit heeft...", ["4 gelijke zijden", "4 verschillende zijden", "3 gelijke zijden", "geen gelijke zijden"], 0),
        ("Een trapezium heeft...", ["minstens 1 paar evenwijdige zijden", "geen evenwijdige zijden", "4 rechte hoeken", "4 gelijke zijden"], 0),
        ("Hoeveel diagonalen heeft een vijfhoek?", ["5", "2", "3", "10"], 0),
        ("Een regelmatige zeshoek heeft hoeveel symmetrie-assen?", ["6", "3", "2", "12"], 0),
        ("Een cilinder heeft hoeveel ribben?", ["2 (randen van de cirkels)", "0", "1", "4"], 0),
        ("Een kegel heeft hoeveel vlakken?", ["2 (1 cirkel + 1 gebogen)", "1", "3", "0"], 0),
    ]

    for i, (q, opts, correct_idx) in enumerate(questions[:count]):
        if q in seen:
            continue
        seen.add(q)

        correct = opts[correct_idx]
        wrong = [opt for j, opt in enumerate(opts) if j != correct_idx]
        exercises.append(create_exercise(q, correct, wrong, "eigenschappen_figuren"))

    return exercises[:count]

def generate_8MM3_exercises(count=16):
    """8MM3: Schaalmodellen maken"""
    exercises = []
    seen = set()

    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        schalen = [50, 100, 200]
        schaal = random.choice(schalen)

        choice = random.choice(['model_to_real', 'real_to_model'])

        if choice == 'model_to_real':
            model_cm = random.randint(5, 30)
            real_cm = model_cm * schaal
            real_m = real_cm / 100
            q = f"Een schaalmodel op schaal 1:{schaal}. Het model is {model_cm} cm. Echte afmeting in meters?"
            correct = f"{real_m:.2f} m" if real_m % 1 != 0 else f"{int(real_m)} m"
            wrong = [
                f"{real_m+0.5:.2f} m",
                f"{real_m-0.5:.2f} m" if real_m > 1 else f"{real_m+1:.2f} m",
                f"{model_cm} m"
            ]
        else:  # real_to_model
            real_m = random.randint(2, 15)
            real_cm = real_m * 100
            model_cm = real_cm / schaal
            q = f"Een kamer is {real_m} meter. Op schaal 1:{schaal}, hoeveel cm op tekening?"
            correct = f"{model_cm:.1f} cm" if model_cm % 1 != 0 else f"{int(model_cm)} cm"
            wrong = [
                f"{model_cm+2:.1f} cm" if model_cm % 1 != 0 else f"{int(model_cm)+2} cm",
                f"{model_cm-2:.1f} cm" if model_cm > 5 else f"{model_cm+4:.1f} cm",
                f"{real_m} cm"
            ]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "schaalmodellen"))

    return exercises[:count]

def generate_8MM4_exercises(count=17):
    """8MM4: Alle meeteenheden"""
    exercises = []
    seen = set()

    conversions_data = [
        ("2.5 ton = hoeveel kg?", "2500 kg", ["2000 kg", "250 kg", "25000 kg"]),
        ("375 cl = hoeveel liter?", "3.75 liter", ["37.5 liter", "0.375 liter", "375 liter"]),
        ("90 minuten = hoeveel uur?", "1.5 uur", ["1 uur", "9 uur", "0.9 uur"]),
        ("5.5 km = hoeveel meter?", "5500 meter", ["550 meter", "55 meter", "55000 meter"]),
        ("250 ml = hoeveel liter?", "0.25 liter", ["2.5 liter", "25 liter", "0.025 liter"]),
        ("3500 gram = hoeveel kg?", "3.5 kg", ["35 kg", "0.35 kg", "350 kg"]),
        ("15 dm = hoeveel meter?", "1.5 m", ["15 m", "0.15 m", "150 m"]),
        ("120 minuten = hoeveel uur?", "2 uur", ["1 uur", "12 uur", "1.2 uur"]),
        ("4.2 km = hoeveel meter?", "4200 meter", ["420 meter", "42 meter", "42000 meter"]),
        ("800 gram = hoeveel kg?", "0.8 kg", ["8 kg", "0.08 kg", "80 kg"]),
        ("50 cl = hoeveel ml?", "500 ml", ["50 ml", "5 ml", "5000 ml"]),
        ("2.5 kg = hoeveel gram?", "2500 gram", ["250 gram", "25 gram", "25000 gram"]),
        ("75 cm = hoeveel meter?", "0.75 m", ["7.5 m", "75 m", "0.075 m"]),
        ("1.5 ton = hoeveel kg?", "1500 kg", ["150 kg", "15 kg", "15000 kg"]),
        ("200 cl = hoeveel liter?", "2 liter", ["20 liter", "0.2 liter", "200 liter"]),
        ("45 minuten = hoeveel uur?", "0.75 uur", ["4.5 uur", "0.45 uur", "7.5 uur"]),
        ("3.8 km = hoeveel meter?", "3800 meter", ["380 meter", "38 meter", "38000 meter"]),
    ]

    for i, (q, correct, wrong) in enumerate(conversions_data[:count]):
        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "alle_eenheden"))

    return exercises[:count]

def generate_8MM5_exercises(count=17):
    """8MM5: Alle figuren (omtrek, oppervlakte, volume)"""
    exercises = []
    seen = set()

    # Mix of all formulas
    for _ in range(count * 10):
        if len(exercises) >= count:
            break

        choice = random.choice(['omtrek_rechthoek', 'opp_rechthoek', 'opp_driehoek',
                               'opp_cirkel', 'omtrek_cirkel', 'volume_kubus', 'volume_balk'])

        if choice == 'omtrek_rechthoek':
            l = random.randint(5, 15)
            b = random.randint(3, 10)
            result = 2 * (l + b)
            q = f"Rechthoek {l}×{b} cm. Omtrek?"
            correct = f"{result} cm"
            wrong = [f"{result+2} cm", f"{result-2} cm", f"{l*b} cm"]

        elif choice == 'opp_rechthoek':
            l = random.randint(5, 15)
            b = random.randint(3, 10)
            result = l * b
            q = f"Rechthoek {l}×{b} cm. Oppervlakte?"
            correct = f"{result} cm²"
            wrong = [f"{result+5} cm²", f"{result-5} cm²", f"{2*(l+b)} cm²"]

        elif choice == 'opp_driehoek':
            basis = random.randint(4, 12)
            hoogte = random.randint(3, 10)
            result = (basis * hoogte) / 2
            q = f"Driehoek basis {basis} cm, hoogte {hoogte} cm. Oppervlakte?"
            correct = f"{result:.1f} cm²" if result % 1 != 0 else f"{int(result)} cm²"
            wrong = [f"{basis*hoogte} cm²", f"{result+5:.1f} cm²", f"{result-5:.1f} cm²" if result > 10 else f"{result+10:.1f} cm²"]

        elif choice == 'opp_cirkel':
            r = random.randint(3, 10)
            result = round(3.14 * r * r, 2)
            q = f"Cirkel straal {r} cm. Oppervlakte? (π=3,14)"
            correct = f"{result:.2f} cm²"
            wrong = [f"{result+10:.2f} cm²", f"{result-10:.2f} cm²", f"{round(2*3.14*r, 2):.2f} cm²"]

        elif choice == 'omtrek_cirkel':
            d = random.randint(5, 15)
            result = round(3.14 * d, 2)
            q = f"Cirkel diameter {d} cm. Omtrek? (π=3,14)"
            correct = f"{result:.2f} cm"
            wrong = [f"{result+5:.2f} cm", f"{result-5:.2f} cm", f"{round(3.14*d*d, 2):.2f} cm"]

        elif choice == 'volume_kubus':
            r = random.randint(3, 8)
            result = r ** 3
            q = f"Kubus ribbe {r} cm. Volume?"
            correct = f"{result} cm³"
            wrong = [f"{result+10} cm³", f"{result-10} cm³", f"{r*6} cm³"]

        else:  # volume_balk
            l = random.randint(4, 10)
            b = random.randint(3, 8)
            h = random.randint(2, 7)
            result = l * b * h
            q = f"Balk {l}×{b}×{h} cm. Volume?"
            correct = f"{result} cm³"
            wrong = [f"{result+15} cm³", f"{result-15} cm³", f"{l*b} cm³"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "alle_figuren"))

    return exercises[:count]

def generate_8MM6_exercises(count=16):
    """8MM6: CITO-niveau meetkunde"""
    exercises = []
    seen = set()

    # Complex CITO-style questions
    questions_pool = [
        ("Een plattegrond heeft schaal 1:200. Een kamer is op de tekening 6 cm. Echte lengte?",
         ["12 meter", "6 meter", "120 meter", "1.2 meter"], 0),

        ("Een rechthoekige tuin is 15×8 m. Hoeveel meter hek rondom?",
         ["46 meter", "120 m²", "23 meter", "30 meter"], 0),

        ("Volume van een balk 10×5×4 cm?",
         ["200 cm³", "50 cm³", "100 cm³", "40 cm³"], 0),

        ("Een cirkel heeft diameter 20 cm. Omtrek? (π≈3,14)",
         ["62,8 cm", "31,4 cm", "125,6 cm", "40 cm"], 0),

        ("L-vorm: rechthoek 8×6 m + rechthoek 4×3 m. Totale oppervlakte?",
         ["60 m²", "48 m²", "72 m²", "36 m²"], 0),

        ("Een kubus heeft ribbe 5 cm. Volume?",
         ["125 cm³", "25 cm³", "75 cm³", "100 cm³"], 0),

        ("Driehoek basis 12 cm, hoogte 8 cm. Oppervlakte?",
         ["48 cm²", "96 cm²", "20 cm²", "24 cm²"], 0),

        ("3,5 km hardlopen = hoeveel meter?",
         ["3500 meter", "350 meter", "35 meter", "35000 meter"], 0),

        ("Een cilinder: straal 4 cm, hoogte 10 cm. Volume? (π≈3,14)",
         ["502,4 cm³", "125,6 cm³", "251,2 cm³", "40 cm³"], 0),

        ("Vierkant zijde 9 cm. Diagonaal ongeveer?",
         ["13 cm", "9 cm", "18 cm", "4,5 cm"], 0),

        ("Rechthoek 6×8 cm. Diagonaal ongeveer?",
         ["10 cm", "6 cm", "8 cm", "14 cm"], 0),

        ("Punt (4, -3) in kwadrant?",
         ["IV", "I", "II", "III"], 0),

        ("Een hoek van 125° is...",
         ["stomp", "scherp", "recht", "gestrekt"], 0),

        ("Kubus: hoeveel ribben?",
         ["12", "6", "8", "10"], 0),

        ("Som van hoeken in driehoek?",
         ["180°", "90°", "360°", "270°"], 0),

        ("4,5 ton = hoeveel kg?",
         ["4500 kg", "450 kg", "45 kg", "45000 kg"], 0),
    ]

    for i, (q, opts, correct_idx) in enumerate(questions_pool[:count]):
        if q in seen:
            continue
        seen.add(q)

        correct = opts[correct_idx]
        wrong = [opt for j, opt in enumerate(opts) if j != correct_idx]
        exercises.append(create_exercise(q, correct, wrong, "cito_niveau"))

    return exercises[:count]

# ============================================================================
# GENERATOR MAPPING
# ============================================================================

generators = {
    "3MM1": generate_3MM1_exercises,
    "3MM2": generate_3MM2_exercises,
    "3MM3": generate_3MM3_exercises,
    "3MM4": generate_3MM4_exercises,
    "3MM5": generate_3MM5_exercises,
    "3MM6": generate_3MM6_exercises,
    "4MM1": generate_4MM1_exercises,
    "4MM2": generate_4MM2_exercises,
    "4MM3": generate_4MM3_exercises,
    "4MM4": generate_4MM4_exercises,
    "4MM5": generate_4MM5_exercises,
    "4MM6": generate_4MM6_exercises,
    "4MM7": generate_4MM7_exercises,
    "5MM1": generate_5MM1_exercises,
    "5MM2": generate_5MM2_exercises,
    "5MM3": generate_5MM3_exercises,
    "5MM4": generate_5MM4_exercises,
    "5MM5": generate_5MM5_exercises,
    "5MM6": generate_5MM6_exercises,
    "5MM7": generate_5MM7_exercises,
    "6MM1": generate_6MM1_exercises,
    "6MM2": generate_6MM2_exercises,
    "6MM3": generate_6MM3_exercises,
    "6MM4": generate_6MM4_exercises,
    "6MM5": generate_6MM5_exercises,
    "6MM6": generate_6MM6_exercises,
    "6MM7": generate_6MM7_exercises,
    "7MM1": generate_7MM1_exercises,
    "7MM2": generate_7MM2_exercises,
    "7MM3": generate_7MM3_exercises,
    "7MM4": generate_7MM4_exercises,
    "7MM5": generate_7MM5_exercises,
    "7MM6": generate_7MM6_exercises,
    "8MM1": generate_8MM1_exercises,
    "8MM2": generate_8MM2_exercises,
    "8MM3": generate_8MM3_exercises,
    "8MM4": generate_8MM4_exercises,
    "8MM5": generate_8MM5_exercises,
    "8MM6": generate_8MM6_exercises,
}

# File mappings with tussendoelen codes
file_mappings = {
    'gb_groep3_meetkunde_m3': {
        'codes': ['3MM1', '3MM2', '3MM3'],
        'grade': 3,
        'level_code': 'm3'
    },
    'gb_groep3_meetkunde_e3': {
        'codes': ['3MM4', '3MM5', '3MM6'],
        'grade': 3,
        'level_code': 'e3'
    },
    'gb_groep4_meetkunde_m4': {
        'codes': ['4MM1', '4MM2', '4MM3', '4MM4'],
        'grade': 4,
        'level_code': 'm4'
    },
    'gb_groep4_meetkunde_e4': {
        'codes': ['4MM5', '4MM6', '4MM7'],
        'grade': 4,
        'level_code': 'e4'
    },
    'gb_groep5_meetkunde_m5': {
        'codes': ['5MM1', '5MM2', '5MM3', '5MM4'],
        'grade': 5,
        'level_code': 'm5'
    },
    'gb_groep5_meetkunde_e5': {
        'codes': ['5MM5', '5MM6', '5MM7'],
        'grade': 5,
        'level_code': 'e5'
    },
    'gb_groep6_meetkunde_m6': {
        'codes': ['6MM1', '6MM2', '6MM3', '6MM4'],
        'grade': 6,
        'level_code': 'm6'
    },
    'gb_groep6_meetkunde_e6': {
        'codes': ['6MM5', '6MM6', '6MM7'],
        'grade': 6,
        'level_code': 'e6'
    },
    'gb_groep7_meetkunde_m7': {
        'codes': ['7MM1', '7MM2', '7MM3'],
        'grade': 7,
        'level_code': 'm7'
    },
    'gb_groep7_meetkunde_e7': {
        'codes': ['7MM4', '7MM5', '7MM6'],
        'grade': 7,
        'level_code': 'e7'
    },
    'gb_groep8_meetkunde_m8': {
        'codes': ['8MM1', '8MM2', '8MM3'],
        'grade': 8,
        'level_code': 'm8'
    },
    'gb_groep8_meetkunde_e8': {
        'codes': ['8MM4', '8MM5', '8MM6'],
        'grade': 8,
        'level_code': 'e8'
    },
}

def generate_file(base_name, config, file_type='core'):
    """Generate a complete file with proper JSON structure"""
    file_id = f"{base_name}_{file_type}"
    codes = config['codes']
    grade = config['grade']
    level_code = config['level_code']

    # Create base structure
    data = create_file_structure(file_id, grade, level_code, codes)

    # Generate exercises
    all_exercises = []
    exercises_per_code = 50 // len(codes)
    remainder = 50 % len(codes)

    for i, code in enumerate(codes):
        count = exercises_per_code + (1 if i < remainder else 0)
        if code in generators:
            exercises = generators[code](count)
            all_exercises.extend(exercises)
        else:
            print(f"  ⚠️  WARNING: No generator for {code}")

    # Ensure exactly 50 exercises
    all_exercises = all_exercises[:50]

    # Renumber exercises
    for i, ex in enumerate(all_exercises, 1):
        ex['id'] = f"ex_{i:06d}"

    # Add to structure
    data['items'] = all_exercises

    return data

def check_duplicates(exercises):
    """Check for duplicate questions"""
    questions = [ex['question']['text'] for ex in exercises]
    unique = len(set(questions))
    return len(exercises) - unique

def main():
    print("=" * 80)
    print("COMPLETE MEETKUNDE GENERATOR - ALL 24 FILES")
    print("=" * 80)
    print()

    results = []

    for base_name, config in file_mappings.items():
        # Generate both core and support files
        for file_type in ['core', 'support']:
            file_id = f"{base_name}_{file_type}"
            file_path = f"data-v2/exercises/mk/{file_id}.json"

            print(f"Generating {file_id}...")

            # Generate file with complete structure
            data = generate_file(base_name, config, file_type)

            # Check duplicates
            dup_count = check_duplicates(data['items'])

            # Save file
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # Report
            status = "✅" if dup_count == 0 else "⚠️ "
            print(f"  {status} {file_id}: {len(data['items'])} exercises, {dup_count} duplicates")

            results.append({
                'file': file_id,
                'codes': config['codes'],
                'count': len(data['items']),
                'duplicates': dup_count,
                'has_structure': 'schema_version' in data
            })

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    all_ok = True
    for r in results:
        status = "✅" if r['duplicates'] == 0 and r['has_structure'] else "⚠️ "
        struct = "✓ Complete JSON" if r['has_structure'] else "✗ Missing structure"
        print(f"{status} {r['file']}: {r['count']} exercises, {r['duplicates']} duplicates, {struct}")
        all_ok = all_ok and (r['duplicates'] == 0 and r['has_structure'])

    print()
    print(f"Total files generated: {len(results)}")
    print(f"All files OK: {'✅ YES' if all_ok else '⚠️  NO'}")
    print()

if __name__ == "__main__":
    main()
