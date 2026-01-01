#!/usr/bin/env python3
"""
Comprehensive meetkunde exercise generator using CSV prompt templates.
This script reads the CSV and generates exercises that precisely follow the Prompt_Template guidance.
"""

import json
import random
import csv
from typing import List, Dict, Set

# Read CSV templates
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

# Helper function to create exercise
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

# ============================================================================
# GROEP 3 GENERATORS
# ============================================================================

def generate_3MM1_exercises(count=17):
    """3MM1: Meten met liniaal (cm)
    CSV Template says: Hoe lang is deze lijn in centimeters?, Meet dit potlood met de liniaal,
    Hoeveel cm is deze streep?, Begin bij 0 en meet tot....
    """
    exercises = []
    seen = set()
    objects = ["potlood", "lijn", "streep", "stokje", "strook papier", "lint", "touwtje",
               "pen", "stift", "gum", "paperclip", "blokje", "kaartje"]

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        obj = random.choice(objects)
        length = random.randint(3, 25)

        templates = [
            f"Hoe lang is deze {obj} in centimeters? De liniaal laat {length} cm zien.",
            f"Meet dit {obj} met de liniaal. Het is {length} cm lang. Hoeveel cm is dat?",
            f"Deze {obj} meet {length} centimeter. Hoeveel cm is dat?",
            f"Begin bij 0 cm en meet tot het einde van de {obj}. De liniaal toont {length}. Hoeveel cm?",
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
    """3MM2: Tijd halve uren
    CSV Template: Hoe laat is het? (half vier), Teken de wijzers op half acht,
    Welke klok toont half 6?, Half drie is hetzelfde als...? (2:30 of 14:30)
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        hour = random.randint(1, 11)
        half_hour = hour  # "half vier" = 3:30
        digital = f"{hour}:30"

        templates = [
            f"Hoe laat is het op de klok? De wijzers staan op half {half_hour + 1}.",
            f"Welke klok toont half {half_hour + 1}?",
            f"Half {half_hour + 1} is hetzelfde als welke tijd?",
            f"De grote wijzer staat op de 6 en de kleine wijzer tussen {half_hour} en {half_hour + 1}. Hoe laat is het?",
        ]

        q = random.choice(templates)
        if q in seen:
            continue
        seen.add(q)

        correct = f"half {half_hour + 1}"
        wrong_options = [f"{hour}:00", f"{hour + 1}:00", f"{hour}:15"]

        exercises.append(create_exercise(q, correct, wrong_options, "tijd_halve_uren"))

    return exercises[:count]

def generate_3MM3_exercises(count=16):
    """3MM3: Geld tot 20 euro
    CSV Template: Je koopt iets voor €8 en betaalt met €10, hoeveel wisselgeld?,
    Tel deze munten bij elkaar, Betaal €15 met zo min mogelijk biljetten
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        price = random.randint(3, 18)
        payment = random.choice([10, 20]) if price < 15 else 20
        change = payment - price

        items = ["speelgoedauto", "boek", "schrift", "snoep", "pen", "potlood",
                 "stickers", "kaart", "ballon", "gum"]
        item = random.choice(items)

        templates = [
            f"Je koopt een {item} voor €{price} en betaalt met €{payment}. Hoeveel wisselgeld krijg je?",
            f"Een {item} kost €{price}. Je geeft €{payment}. Hoeveel krijg je terug?",
            f"Prijs: €{price}. Betaald: €{payment}. Wisselgeld?",
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
    """3MM4: Meter en centimeter
    CSV Template: Hoeveel cm is 1 meter?, Meet de tafel in meters en centimeters,
    150 cm = ? m en ? cm, 2 meter en 30 cm = ? cm
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        templates_type = random.choice(['basic', 'convert_to_cm', 'convert_to_m'])

        if templates_type == 'basic':
            q = "Hoeveel centimeter is 1 meter?"
            correct = "100 cm"
            wrong = ["10 cm", "50 cm", "1000 cm"]
        elif templates_type == 'convert_to_cm':
            meters = random.randint(1, 5)
            cm_part = random.randint(0, 90)
            total_cm = meters * 100 + cm_part
            if cm_part == 0:
                q = f"{meters} meter = hoeveel centimeter?"
            else:
                q = f"{meters} meter en {cm_part} cm = hoeveel centimeter in totaal?"
            correct = f"{total_cm} cm"
            wrong = [f"{total_cm-10} cm", f"{total_cm+10} cm", f"{total_cm-50} cm"]
        else:  # convert_to_m
            total_cm = random.randint(110, 350)
            meters = total_cm // 100
            cm = total_cm % 100
            q = f"{total_cm} cm = hoeveel meter en centimeter?"
            correct = f"{meters} m en {cm} cm"
            wrong = [f"{meters+1} m en {cm} cm", f"{meters} m en {cm+10} cm", f"{meters-1} m en {cm} cm"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "meter_centimeter"))

    return exercises[:count]

def generate_3MM5_exercises(count=17):
    """3MM5: Vlakke figuren
    CSV Template: Teken een vierkant met zijde 4 hokjes, Welke figuur is dit?,
    Hoeveel hoeken heeft een rechthoek?, Welke figuur heeft geen hoeken?
    """
    exercises = []
    seen = set()

    properties = [
        ("vierkant", "4 hoeken", "4 gelijke zijden", "4", "ja"),
        ("rechthoek", "4 hoeken", "4 zijden (2 lang, 2 kort)", "4", "ja"),
        ("driehoek", "3 hoeken", "3 zijden", "3", "ja"),
        ("cirkel", "0 hoeken", "rond", "0", "nee"),
    ]

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        shape, corners, sides, corner_count, has_corners = random.choice(properties)

        templates = [
            f"Hoeveel hoeken heeft een {shape}?",
            f"Welke figuur heeft geen hoeken?",
            f"Een {shape} heeft ... hoeken.",
            f"Deze figuur is rond en heeft geen hoeken. Wat is het?",
        ]

        if shape == "cirkel":
            q = random.choice([
                "Welke figuur heeft geen hoeken?",
                "Een cirkel heeft hoeveel hoeken?",
                "Deze figuur is rond. Wat is het?",
            ])
            if "heeft geen" in q or "rond" in q:
                correct = "cirkel"
                wrong = ["vierkant", "driehoek", "rechthoek"]
            else:
                correct = "0 hoeken"
                wrong = ["1 hoek", "3 hoeken", "4 hoeken"]
        else:
            q = f"Hoeveel hoeken heeft een {shape}?"
            correct = f"{corner_count} hoeken"
            wrong = [f"{int(corner_count)-1} hoeken" if int(corner_count) > 1 else "5 hoeken",
                     f"{int(corner_count)+1} hoeken", "0 hoeken"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "vlakke_figuren"))

    return exercises[:count]

def generate_3MM6_exercises(count=16):
    """3MM6: Tijd kwartieren
    CSV Template: Hoe laat is het? (kwart over 3), Teken de wijzers op kwart voor 8,
    Kwart over 7 = 7:15 of 7:45?, Welke klok toont half 4?
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
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
    """4MM1: mm, cm, dm, m
    CSV Template: 3 dm = ? cm, 250 cm = ? m, 45 mm = ? cm,
    Welke eenheid gebruik je voor de dikte van een boek?
    """
    exercises = []
    seen = set()

    conversions = [
        ("mm", "cm", 10),
        ("cm", "dm", 10),
        ("dm", "m", 10),
        ("cm", "m", 100),
    ]

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        from_unit, to_unit, factor = random.choice(conversions)

        if from_unit == "mm" and to_unit == "cm":
            value = random.randint(10, 90)
            result = value / 10
            q = f"{value} {from_unit} = hoeveel {to_unit}?"
            correct = f"{result} {to_unit}"
            wrong = [f"{result-1} {to_unit}", f"{result+1} {to_unit}", f"{value} {to_unit}"]
        elif from_unit == "cm" and to_unit == "dm":
            value = random.randint(20, 90)
            result = value / 10
            q = f"{value} {from_unit} = hoeveel {to_unit}?"
            correct = f"{result} {to_unit}"
            wrong = [f"{result-1} {to_unit}", f"{result+1} {to_unit}", f"{value} {to_unit}"]
        elif from_unit == "dm" and to_unit == "m":
            value = random.randint(5, 25)
            result = value / 10
            q = f"{value} {from_unit} = hoeveel {to_unit}?"
            correct = f"{result} {to_unit}"
            wrong = [f"{result-1} {to_unit}", f"{result+1} {to_unit}", f"{value} {to_unit}"]
        else:  # cm to m
            value = random.randint(150, 450)
            result = value / 100
            q = f"{value} {from_unit} = hoeveel {to_unit}?"
            correct = f"{result} {to_unit}"
            wrong = [f"{result-0.5} {to_unit}", f"{result+0.5} {to_unit}", f"{value/10} {to_unit}"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "lengte_eenheden"))

    return exercises[:count]

def generate_4MM2_exercises(count=12):
    """4MM2: gram en kilogram
    CSV Template: Hoeveel weegt dit product?, 1 kg = ? gram, 1500 gram = ? kg
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        conversion_type = random.choice(['kg_to_g', 'g_to_kg', 'basic'])

        if conversion_type == 'basic':
            q = "Hoeveel gram is 1 kilogram?"
            correct = "1000 gram"
            wrong = ["100 gram", "500 gram", "10000 gram"]
        elif conversion_type == 'kg_to_g':
            kg = random.uniform(0.5, 5)
            grams = int(kg * 1000)
            q = f"{kg} kg = hoeveel gram?"
            correct = f"{grams} gram"
            wrong = [f"{grams-100} gram", f"{grams+100} gram", f"{int(kg*100)} gram"]
        else:  # g_to_kg
            grams = random.randint(500, 5000)
            kg = grams / 1000
            q = f"{grams} gram = hoeveel kilogram?"
            correct = f"{kg} kg"
            wrong = [f"{kg-0.5} kg", f"{kg+0.5} kg", f"{grams/100} kg"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "gewicht"))

    return exercises[:count]

def generate_4MM3_exercises(count=12):
    """4MM3: Inhoud liter
    CSV Template: Hoeveel liter past in deze emmer?, Een pak melk bevat meestal hoeveel liter?
    """
    exercises = []
    seen = set()

    containers = [
        ("fles water", 1.5),
        ("pak melk", 1),
        ("emmer", 10),
        ("beker", 0.25),
        ("kan", 2),
    ]

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        container, typical_volume = random.choice(containers)

        q = f"Een {container} bevat meestal hoeveel liter?"
        correct = f"{typical_volume} liter"

        if typical_volume < 1:
            wrong = ["1 liter", "0.5 liter", "2 liter"]
        else:
            wrong = [f"{typical_volume-0.5} liter", f"{typical_volume+1} liter", f"{typical_volume*2} liter"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "inhoud_liter"))

    return exercises[:count]

def generate_4MM4_exercises(count=13):
    """4MM4: Tijd minuten
    CSV Template: Hoe laat is het? (op 5 minuten nauwkeurig), Hoeveel minuten tussen 3:15 en 3:45?
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        hour_start = random.randint(8, 15)
        minute_start = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        duration = random.choice([5, 10, 15, 20, 25, 30])

        minute_end = minute_start + duration
        hour_end = hour_start
        if minute_end >= 60:
            minute_end -= 60
            hour_end += 1

        q = f"Hoeveel minuten zitten er tussen {hour_start}:{minute_start:02d} en {hour_end}:{minute_end:02d}?"
        correct = f"{duration} minuten"
        wrong = [f"{duration-5} minuten", f"{duration+5} minuten", f"{duration+10} minuten"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "tijd_minuten"))

    return exercises[:count]

def generate_4MM5_exercises(count=17):
    """4MM5: Omtrek berekenen
    CSV Template: Bereken omtrek van vierkant met zijde 4 cm, Rechthoek met lengte 5 cm en breedte 3 cm
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        shape_type = random.choice(['vierkant', 'rechthoek'])

        if shape_type == 'vierkant':
            side = random.randint(3, 12)
            perimeter = 4 * side
            q_templates = [
                f"Bereken de omtrek van een vierkant met zijde {side} cm.",
                f"Een vierkant heeft zijden van {side} cm. Wat is de omtrek?",
                f"Omtrek vierkant: zijde = {side} cm. Bereken.",
            ]
            q = random.choice(q_templates)
            correct = f"{perimeter} cm"
            wrong = [f"{perimeter-4} cm", f"{perimeter+4} cm", f"{side*2} cm"]
        else:  # rechthoek
            length = random.randint(5, 15)
            width = random.randint(3, 10)
            if length == width:
                width += 1
            perimeter = 2 * (length + width)
            q_templates = [
                f"Bereken de omtrek van een rechthoek met lengte {length} cm en breedte {width} cm.",
                f"Een rechthoek is {length} cm lang en {width} cm breed. Wat is de omtrek?",
                f"Omtrek rechthoek: lengte = {length} cm, breedte = {width} cm.",
            ]
            q = random.choice(q_templates)
            correct = f"{perimeter} cm"
            wrong = [f"{perimeter-2} cm", f"{perimeter+2} cm", f"{length+width} cm"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "omtrek"))

    return exercises[:count]

def generate_4MM6_exercises(count=17):
    """4MM6: Ruimtelijke figuren
    CSV Template: Welke ruimtelijke figuur is dit?, Hoeveel vlakken heeft een kubus?
    """
    exercises = []
    seen = set()

    shapes = [
        ("kubus", "6 vlakken", "8 hoekpunten", "12 ribben"),
        ("balk", "6 vlakken", "8 hoekpunten", "12 ribben"),
        ("bol", "0 vlakken", "0 hoekpunten", "0 ribben"),
        ("cilinder", "3 vlakken", "0 hoekpunten", "2 ribben"),
        ("piramide", "5 vlakken", "5 hoekpunten", "8 ribben"),
    ]

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        shape, vlakken, hoekpunten, ribben = random.choice(shapes)
        question_type = random.choice(['vlakken', 'hoekpunten', 'ribben', 'identify'])

        if question_type == 'vlakken':
            q = f"Hoeveel vlakken heeft een {shape}?"
            correct = vlakken
            num = int(vlakken.split()[0])
            wrong = [f"{num-1} vlakken" if num > 1 else "1 vlak",
                     f"{num+1} vlakken", f"{num+2} vlakken"]
        elif question_type == 'hoekpunten':
            q = f"Hoeveel hoekpunten heeft een {shape}?"
            correct = hoekpunten
            num = int(hoekpunten.split()[0])
            wrong = [f"{num+1} hoekpunten" if num > 0 else "1 hoekpunt",
                     f"{num+2} hoekpunten" if num > 0 else "4 hoekpunten",
                     "6 hoekpunten"]
        elif question_type == 'ribben':
            q = f"Hoeveel ribben heeft een {shape}?"
            correct = ribben
            num = int(ribben.split()[0])
            wrong = [f"{num+1} ribben" if num > 0 else "4 ribben",
                     f"{num+2} ribben" if num > 0 else "6 ribben",
                     "10 ribben"]
        else:  # identify
            objects = {
                "kubus": "dobbelsteen",
                "balk": "schoenendoos",
                "bol": "voetbal",
                "cilinder": "blik",
                "piramide": "puntzak"
            }
            obj = objects.get(shape, shape)
            q = f"Een {obj} heeft de vorm van een..."
            correct = shape
            other_shapes = [s for s, _, _, _ in shapes if s != shape]
            wrong = random.sample(other_shapes, 3)

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "ruimtelijke_figuren"))

    return exercises[:count]

def generate_4MM7_exercises(count=16):
    """4MM7: Geld tot 100 euro
    CSV Template: Je koopt voor €47,50 en betaalt met €50, Reken uit: 3 artikelen van €15,25
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        question_type = random.choice(['wisselgeld', 'totaal', 'rest'])

        if question_type == 'wisselgeld':
            price = round(random.uniform(15.50, 89.99), 2)
            payment = 50 if price < 50 else 100
            change = round(payment - price, 2)

            items = ["speelgoed", "trui", "boek", "tas", "schoenen", "jas"]
            item = random.choice(items)

            q = f"Je koopt {item} voor €{price:.2f} en betaalt met €{payment}. Hoeveel wisselgeld?"
            correct = f"€{change:.2f}"
            wrong = [f"€{change-1:.2f}", f"€{change+1:.2f}", f"€{change+0.50:.2f}"]
        elif question_type == 'totaal':
            count_items = random.randint(2, 4)
            price_per = round(random.uniform(8.25, 25.75), 2)
            total = round(count_items * price_per, 2)

            q = f"Je koopt {count_items} artikelen van €{price_per:.2f} per stuk. Wat is het totaal?"
            correct = f"€{total:.2f}"
            wrong = [f"€{total-price_per:.2f}", f"€{total+price_per:.2f}", f"€{total+1:.2f}"]
        else:  # rest
            start = round(random.uniform(80, 100), 2)
            spent = round(random.uniform(40, start-10), 2)
            remaining = round(start - spent, 2)

            q = f"Je hebt €{start:.2f} en geeft €{spent:.2f} uit. Hoeveel houd je over?"
            correct = f"€{remaining:.2f}"
            wrong = [f"€{remaining-5:.2f}", f"€{remaining+5:.2f}", f"€{start+spent:.2f}"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "geld_100"))

    return exercises[:count]

# ============================================================================
# GROEP 5 GENERATORS
# ============================================================================

def generate_5MM1_exercises(count=12):
    """5MM1: Kilometer
    CSV Template: 3 km = ? meter, De afstand van Amsterdam naar Utrecht is 45 km
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        conversion_type = random.choice(['km_to_m', 'm_to_km', 'basic'])

        if conversion_type == 'basic':
            q = "Hoeveel meter is 1 kilometer?"
            correct = "1000 meter"
            wrong = ["100 meter", "500 meter", "10000 meter"]
        elif conversion_type == 'km_to_m':
            km = random.randint(2, 10)
            meters = km * 1000
            q = f"{km} km = hoeveel meter?"
            correct = f"{meters} meter"
            wrong = [f"{meters-100} meter", f"{meters+100} meter", f"{km*100} meter"]
        else:  # m_to_km
            meters = random.choice([2000, 2500, 3000, 4500, 5000, 7500])
            km = meters / 1000
            q = f"{meters} meter = hoeveel kilometer?"
            correct = f"{km} km"
            wrong = [f"{km-0.5} km", f"{km+0.5} km", f"{meters/100} km"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "kilometer"))

    return exercises[:count]

def generate_5MM2_exercises(count=13):
    """5MM2: Ton
    CSV Template: 1 ton = ? kilogram, Een auto weegt ongeveer hoeveel ton?
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        conversion_type = random.choice(['basic', 'ton_to_kg', 'kg_to_ton', 'estimate'])

        if conversion_type == 'basic':
            q = "Hoeveel kilogram is 1 ton?"
            correct = "1000 kg"
            wrong = ["100 kg", "500 kg", "10000 kg"]
        elif conversion_type == 'ton_to_kg':
            ton = random.choice([2, 3, 5, 10])
            kg = ton * 1000
            q = f"{ton} ton = hoeveel kilogram?"
            correct = f"{kg} kg"
            wrong = [f"{kg-100} kg", f"{kg+100} kg", f"{ton*100} kg"]
        elif conversion_type == 'kg_to_ton':
            kg = random.choice([2000, 2500, 3000, 4500, 5000])
            ton = kg / 1000
            q = f"{kg} kg = hoeveel ton?"
            correct = f"{ton} ton"
            wrong = [f"{ton-0.5} ton", f"{ton+0.5} ton", f"{kg/100} ton"]
        else:  # estimate
            items = [("auto", "1.5"), ("olifant", "5"), ("vrachtwagen", "10"), ("fiets", "0.02")]
            item, weight = random.choice(items)
            q = f"Een {item} weegt ongeveer hoeveel ton?"
            correct = f"{weight} ton"
            if item == "fiets":
                wrong = ["1 ton", "0.5 ton", "2 ton"]
            else:
                w = float(weight)
                wrong = [f"{w-1} ton", f"{w+1} ton", f"{w*2} ton"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "ton"))

    return exercises[:count]

def generate_5MM3_exercises(count=12):
    """5MM3: ml, cl, dl, l
    CSV Template: 250 ml = ? cl, 1 liter = ? ml, 50 cl = ? dl
    """
    exercises = []
    seen = set()

    conversions = [
        ("ml", "cl", 10),
        ("cl", "dl", 10),
        ("dl", "l", 10),
        ("ml", "l", 1000),
    ]

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        from_unit, to_unit, factor = random.choice(conversions)

        if from_unit == "ml" and to_unit == "cl":
            value = random.choice([100, 150, 200, 250, 300, 500])
            result = value / 10
            q = f"{value} {from_unit} = hoeveel {to_unit}?"
            correct = f"{result} {to_unit}"
            wrong = [f"{result-5} {to_unit}", f"{result+5} {to_unit}", f"{value} {to_unit}"]
        elif from_unit == "cl" and to_unit == "dl":
            value = random.choice([20, 30, 40, 50, 60, 80])
            result = value / 10
            q = f"{value} {from_unit} = hoeveel {to_unit}?"
            correct = f"{result} {to_unit}"
            wrong = [f"{result-1} {to_unit}", f"{result+1} {to_unit}", f"{value} {to_unit}"]
        elif from_unit == "dl" and to_unit == "l":
            value = random.choice([5, 10, 15, 20, 25])
            result = value / 10
            q = f"{value} {from_unit} = hoeveel {to_unit}?"
            correct = f"{result} {to_unit}"
            wrong = [f"{result-0.5} {to_unit}", f"{result+0.5} {to_unit}", f"{value} {to_unit}"]
        else:  # ml to l
            value = random.choice([250, 500, 750, 1000, 1500])
            result = value / 1000
            q = f"{value} {from_unit} = hoeveel {to_unit}?"
            correct = f"{result} {to_unit}"
            wrong = [f"{result-0.25} {to_unit}", f"{result+0.25} {to_unit}", f"{value/100} {to_unit}"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "inhoudsmaten"))

    return exercises[:count]

def generate_5MM4_exercises(count=13):
    """5MM4: Oppervlakte begrip
    CSV Template: Hoeveel cm² bedekt deze figuur? (tel de hokjes)
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        # Simple rectangular areas
        width = random.randint(3, 8)
        height = random.randint(3, 8)
        area = width * height

        q_templates = [
            f"Hoeveel cm² bedekt een rechthoek van {width} hokjes breed en {height} hokjes hoog? (Tel de hokjes)",
            f"Een figuur op roosterpapier is {width}×{height} hokjes groot. Hoeveel cm² is de oppervlakte?",
            f"Tel de hokjes: {width} breed en {height} hoog. Oppervlakte in cm²?",
        ]

        q = random.choice(q_templates)
        if q in seen:
            continue
        seen.add(q)

        correct = f"{area} cm²"
        wrong = [f"{area-2} cm²", f"{area+2} cm²", f"{width+height} cm²"]

        exercises.append(create_exercise(q, correct, wrong, "oppervlakte_tellen"))

    return exercises[:count]

def generate_5MM5_exercises(count=14):
    """5MM5: Tijd digitale en analoge klok
    CSV Template: Van 13:45 tot 15:20 is hoeveel tijd?, De trein vertrekt om 14:23
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        hour_start = random.randint(9, 16)
        minute_start = random.randint(0, 45)

        duration_minutes = random.choice([35, 45, 55, 65, 75, 85, 95, 97])

        total_minutes = hour_start * 60 + minute_start + duration_minutes
        hour_end = total_minutes // 60
        minute_end = total_minutes % 60

        hours = duration_minutes // 60
        minutes = duration_minutes % 60

        q = f"Van {hour_start}:{minute_start:02d} tot {hour_end}:{minute_end:02d} is hoeveel tijd?"

        if hours > 0:
            correct = f"{hours} uur en {minutes} minuten"
            wrong = [f"{hours} uur en {minutes+5} minuten",
                     f"{hours+1} uur en {minutes} minuten",
                     f"{duration_minutes} minuten"]
        else:
            correct = f"{minutes} minuten"
            wrong = [f"{minutes+5} minuten", f"{minutes-5} minuten", f"{minutes+10} minuten"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "tijdsduur"))

    return exercises[:count]

def generate_5MM6_exercises(count=12):
    """5MM6: Oppervlakte vierkant/rechthoek
    CSV Template: Oppervlakte rechthoek met lengte 5 cm en breedte 3 cm
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        shape_type = random.choice(['vierkant', 'rechthoek'])

        if shape_type == 'vierkant':
            side = random.randint(4, 12)
            area = side * side

            q_templates = [
                f"Bereken de oppervlakte van een vierkant met zijde {side} cm.",
                f"Een vierkant heeft zijden van {side} cm. Wat is de oppervlakte in cm²?",
                f"Oppervlakte vierkant: zijde = {side} cm.",
            ]
            q = random.choice(q_templates)
            correct = f"{area} cm²"
            wrong = [f"{area-side} cm²", f"{area+side} cm²", f"{side*4} cm²"]
        else:
            length = random.randint(5, 15)
            width = random.randint(3, 10)
            if length == width:
                width += 1
            area = length * width

            q_templates = [
                f"Bereken de oppervlakte van een rechthoek met lengte {length} cm en breedte {width} cm.",
                f"Een rechthoek is {length} cm lang en {width} cm breed. Oppervlakte?",
                f"Oppervlakte rechthoek: {length} × {width} cm.",
            ]
            q = random.choice(q_templates)
            correct = f"{area} cm²"
            wrong = [f"{area-width} cm²", f"{area+length} cm²", f"{2*(length+width)} cm²"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "oppervlakte_formule"))

    return exercises[:count]

def generate_5MM7_exercises(count=14):
    """5MM7: Symmetrie
    CSV Template: Is deze figuur symmetrisch?, Hoeveel symmetrie-assen heeft deze figuur?
    """
    exercises = []
    seen = set()

    shapes_symmetry = [
        ("vierkant", 4),
        ("rechthoek", 2),
        ("gelijkzijdige driehoek", 3),
        ("cirkel", "oneindig veel"),
        ("willekeurige driehoek", 0),
        ("letter A", 1),
        ("letter B", 1),
        ("letter O", 2),
    ]

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        shape, axes = random.choice(shapes_symmetry)

        question_type = random.choice(['count', 'identify'])

        if question_type == 'count' and axes != "oneindig veel":
            q = f"Hoeveel symmetrie-assen heeft een {shape}?"
            correct = f"{axes} symmetrie-as" if axes == 1 else f"{axes} symmetrie-assen"
            if axes == 0:
                wrong = ["1 symmetrie-as", "2 symmetrie-assen", "3 symmetrie-assen"]
            else:
                wrong = [f"{axes-1} symmetrie-assen" if axes > 1 else "0 symmetrie-assen",
                         f"{axes+1} symmetrie-assen",
                         f"{axes+2} symmetrie-assen"]
        else:
            if axes == 0 or (isinstance(axes, int) and axes == 0):
                q = f"Is een {shape} symmetrisch?"
                correct = "Nee"
                wrong = ["Ja", "Alleen horizontaal", "Alleen verticaal"]
            else:
                q = f"Is een {shape} symmetrisch?"
                correct = "Ja"
                wrong = ["Nee", "Alleen als je hem draait", "Soms"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "symmetrie"))

    return exercises[:count]

# ============================================================================
# GROEP 6 GENERATORS
# ============================================================================

def generate_6MM1_exercises(count=12):
    """6MM1: Oppervlakte driehoek
    CSV Template: Driehoek met basis 6 cm en hoogte 4 cm - oppervlakte?
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        basis = random.randint(4, 14)
        hoogte = random.randint(3, 12)
        area = (basis * hoogte) / 2

        q_templates = [
            f"Bereken de oppervlakte van een driehoek met basis {basis} cm en hoogte {hoogte} cm.",
            f"Driehoek: basis = {basis} cm, hoogte = {hoogte} cm. Oppervlakte?",
            f"Oppervlakte driehoek met basis {basis} cm en hoogte {hoogte} cm?",
        ]

        q = random.choice(q_templates)
        if q in seen:
            continue
        seen.add(q)

        correct = f"{area} cm²"
        wrong = [f"{area-2} cm²", f"{area+2} cm²", f"{basis*hoogte} cm²"]

        exercises.append(create_exercise(q, correct, wrong, "oppervlakte_driehoek"))

    return exercises[:count]

def generate_6MM2_exercises(count=13):
    """6MM2: Omtrek cirkel
    CSV Template: Cirkel met diameter 10 cm - omtrek?, gebruik π = 3,14
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        measure_type = random.choice(['diameter', 'straal'])

        if measure_type == 'diameter':
            diameter = random.choice([6, 8, 10, 12, 14])
            circumference = round(3.14 * diameter, 2)

            q = f"Bereken de omtrek van een cirkel met diameter {diameter} cm. Gebruik π = 3,14."
            correct = f"{circumference} cm"
            wrong = [f"{circumference-3} cm", f"{circumference+3} cm", f"{diameter*3} cm"]
        else:  # straal
            straal = random.choice([3, 4, 5, 6, 7])
            circumference = round(2 * 3.14 * straal, 2)

            q = f"Bereken de omtrek van een cirkel met straal {straal} cm. Gebruik π = 3,14."
            correct = f"{circumference} cm"
            wrong = [f"{circumference-3} cm", f"{circumference+3} cm", f"{straal*6} cm"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "omtrek_cirkel"))

    return exercises[:count]

def generate_6MM3_exercises(count=12):
    """6MM3: Coördinaten
    CSV Template: Wat staat op coördinaat (3, 5)?, Geef de coördinaten van punt A
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        x = random.randint(1, 10)
        y = random.randint(1, 10)

        points = ["A", "B", "C", "D", "P", "Q"]
        point = random.choice(points)

        q_templates = [
            f"Punt {point} ligt op coördinaat ({x}, {y}). Wat is de x-coördinaat?",
            f"Een punt heeft coördinaten ({x}, {y}). Wat is de y-coördinaat?",
            f"Welk punt ligt op ({x}, {y})?",
        ]

        q_type = random.choice(['x', 'y', 'both'])

        if q_type == 'x':
            q = f"Punt {point} ligt op ({x}, {y}). Wat is de x-coördinaat?"
            correct = f"{x}"
            wrong = [f"{x-1}", f"{x+1}", f"{y}"]
        elif q_type == 'y':
            q = f"Punt {point} ligt op ({x}, {y}). Wat is de y-coördinaat?"
            correct = f"{y}"
            wrong = [f"{y-1}", f"{y+1}", f"{x}"]
        else:
            q = f"Waar ligt punt {point} als x={x} en y={y}?"
            correct = f"({x}, {y})"
            wrong = [f"({y}, {x})", f"({x+1}, {y})", f"({x}, {y+1})"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "coordinaten"))

    return exercises[:count]

def generate_6MM4_exercises(count=13):
    """6MM4: Hoeken meten
    CSV Template: Meet deze hoek met de gradenboog, Een rechte hoek is...graden?
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        question_type = random.choice(['basic', 'measure', 'estimate'])

        if question_type == 'basic':
            basics = [
                ("Een rechte hoek is hoeveel graden?", "90°", ["45°", "180°", "60°"]),
                ("Een halve draai is hoeveel graden?", "180°", ["90°", "360°", "270°"]),
                ("Een hele draai is hoeveel graden?", "360°", ["180°", "270°", "90°"]),
            ]
            q, correct, wrong = random.choice(basics)
        else:
            angle = random.choice([30, 45, 60, 75, 90, 120, 135, 150])
            q = f"Meet deze hoek met de gradenboog. De hoek is {angle}°. Hoeveel graden?"
            correct = f"{angle}°"
            wrong = [f"{angle-15}°", f"{angle+15}°", f"{180-angle}°"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "hoeken_meten"))

    return exercises[:count]

def generate_6MM5_exercises(count=12):
    """6MM5: Volume kubus/balk
    CSV Template: Balk met afmetingen 5×3×4 cm - volume?, Kubus met ribbe 6 cm
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        shape_type = random.choice(['kubus', 'balk'])

        if shape_type == 'kubus':
            side = random.randint(3, 10)
            volume = side ** 3

            q_templates = [
                f"Bereken het volume van een kubus met ribbe {side} cm.",
                f"Een kubus heeft ribben van {side} cm. Volume?",
                f"Volume kubus: ribbe = {side} cm.",
            ]
            q = random.choice(q_templates)
            correct = f"{volume} cm³"
            wrong = [f"{volume-side} cm³", f"{volume+side} cm³", f"{side*side} cm³"]
        else:  # balk
            length = random.randint(4, 10)
            width = random.randint(3, 8)
            height = random.randint(2, 7)
            volume = length * width * height

            q_templates = [
                f"Bereken het volume van een balk met afmetingen {length}×{width}×{height} cm.",
                f"Balk: lengte {length} cm, breedte {width} cm, hoogte {height} cm. Volume?",
                f"Volume balk: {length} × {width} × {height} cm.",
            ]
            q = random.choice(q_templates)
            correct = f"{volume} cm³"
            wrong = [f"{volume-10} cm³", f"{volume+10} cm³", f"{length*width} cm³"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "volume"))

    return exercises[:count]

def generate_6MM6_exercises(count=13):
    """6MM6: Perspectief tekenen
    CSV Template: Hoeveel blokjes zie je in deze stapel (ook verborgen)?
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        # Simple 3D block configurations
        visible = random.randint(5, 12)
        hidden = random.randint(2, 6)
        total = visible + hidden

        q_templates = [
            f"Je ziet {visible} blokjes in een stapel. Er zijn {hidden} blokjes verborgen. Hoeveel in totaal?",
            f"Een 3D-stapel heeft {total} blokjes. Je ziet er {visible}. Hoeveel zijn verborgen?",
            f"Bovenaanzicht toont een stapel van 3×3 blokjes, allemaal 1 laag hoog. Hoeveel blokjes?",
        ]

        q_type = random.choice(['total', 'hidden', 'simple'])

        if q_type == 'total':
            q = f"Je ziet {visible} blokjes. Er zijn {hidden} verborgen blokjes. Totaal?"
            correct = f"{total} blokjes"
            wrong = [f"{total-1} blokjes", f"{total+1} blokjes", f"{visible} blokjes"]
        elif q_type == 'hidden':
            q = f"Een stapel heeft {total} blokjes totaal. Je ziet {visible} blokjes. Hoeveel verborgen?"
            correct = f"{hidden} blokjes"
            wrong = [f"{hidden-1} blokjes", f"{hidden+1} blokjes", f"{visible} blokjes"]
        else:
            size = random.randint(2, 4)
            total_simple = size * size
            q = f"Een stapel van {size}×{size} blokjes, allemaal 1 laag hoog. Hoeveel blokjes?"
            correct = f"{total_simple} blokjes"
            wrong = [f"{total_simple-1} blokjes", f"{total_simple+1} blokjes", f"{size*4} blokjes"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "perspectief"))

    return exercises[:count]

def generate_6MM7_exercises(count=12):
    """6MM7: Schaal op kaarten
    CSV Template: Op de kaart is de afstand 5 cm, schaal 1:100.000 - echte afstand in km?
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        map_cm = random.choice([3, 4, 5, 6, 8, 10])
        scale = random.choice([100000, 50000, 25000])

        real_cm = map_cm * scale
        real_km = real_cm / 100000  # cm to km

        q = f"Op de kaart is de afstand {map_cm} cm. Schaal is 1:{scale}. Echte afstand in km?"
        correct = f"{real_km} km"
        wrong = [f"{real_km-0.5} km", f"{real_km+0.5} km", f"{map_cm} km"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "schaal_kaarten"))

    return exercises[:count]

# ============================================================================
# GROEP 7 GENERATORS
# ============================================================================

def generate_7MM1_exercises(count=17):
    """7MM1: Oppervlakte cirkel
    CSV Template: Cirkel met straal 5 cm - bereken oppervlakte, gebruik π = 3,14
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        measure_type = random.choice(['straal', 'diameter'])

        if measure_type == 'straal':
            straal = random.choice([3, 4, 5, 6, 7, 8])
            area = round(3.14 * straal * straal, 2)

            q = f"Bereken de oppervlakte van een cirkel met straal {straal} cm. Gebruik π = 3,14."
            correct = f"{area} cm²"
            wrong = [f"{area-5} cm²", f"{area+5} cm²", f"{straal*6} cm²"]
        else:  # diameter given, need to find straal first
            diameter = random.choice([6, 8, 10, 12, 14])
            straal = diameter / 2
            area = round(3.14 * straal * straal, 2)

            q = f"Cirkel met diameter {diameter} cm. Bereken eerst de straal, dan de oppervlakte. π = 3,14."
            correct = f"{area} cm²"
            wrong = [f"{area-5} cm²", f"{area+5} cm²", f"{diameter*3} cm²"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "oppervlakte_cirkel"))

    return exercises[:count]

def generate_7MM2_exercises(count=17):
    """7MM2: Diagonalen meten en schatten
    CSV Template: Meet de diagonaal van deze rechthoek, Schat de diagonaal van een voetbalveld
    IMPORTANT: NO FORMULAS, only measuring and estimating!
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        question_type = random.choice(['measure', 'estimate', 'compare', 'count'])

        if question_type == 'measure':
            length = random.randint(6, 15)
            width = random.randint(4, 10)
            # Approximate diagonal (not using formula, but realistic measurement)
            diagonal_approx = random.choice([length + 2, length + 3, width + 5])

            q = f"Meet de diagonaal van een rechthoek van {length}×{width} cm met een liniaal. De diagonaal is ongeveer..."
            correct = f"{diagonal_approx} cm"
            wrong = [f"{diagonal_approx-1} cm", f"{diagonal_approx+1} cm", f"{length+width} cm"]
        elif question_type == 'estimate':
            contexts = [
                ("voetbalveld van 100×60 meter", "120", ["100", "160", "200"]),
                ("klaslokaal van 8×6 meter", "10", ["8", "14", "16"]),
                ("rechthoekige tuin van 12×8 meter", "15", ["12", "20", "24"]),
            ]
            context, correct, wrong = random.choice(contexts)
            q = f"Schat de diagonaal van een {context}."
            correct = f"ongeveer {correct} meter"
        elif question_type == 'count':
            q = "Hoeveel diagonalen heeft een rechthoek?"
            correct = "2 diagonalen"
            wrong = ["1 diagonaal", "4 diagonalen", "0 diagonalen"]
        else:  # compare
            q = "Een vierkant met zijde 10 cm heeft een diagonaal. Schat de lengte."
            correct = "ongeveer 14 cm"
            wrong = ["10 cm", "20 cm", "ongeveer 12 cm"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "diagonalen"))

    return exercises[:count]

def generate_7MM3_exercises(count=16):
    """7MM3: Hoeken: soorten
    CSV Template: Is deze hoek scherp, recht of stomp?, Welke hoek is 45° (scherp)
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        question_type = random.choice(['identify', 'classify', 'example'])

        if question_type == 'identify':
            angle = random.choice([30, 45, 60, 90, 120, 135, 150])
            if angle < 90:
                angle_type = "scherpe hoek"
            elif angle == 90:
                angle_type = "rechte hoek"
            else:
                angle_type = "stompe hoek"

            q = f"Een hoek van {angle}° is een..."
            correct = angle_type
            wrong = ["scherpe hoek", "rechte hoek", "stompe hoek"]
            wrong = [w for w in wrong if w != correct][:3]
        elif question_type == 'classify':
            types = [
                ("scherpe hoek", "kleiner dan 90°"),
                ("rechte hoek", "precies 90°"),
                ("stompe hoek", "tussen 90° en 180°"),
            ]
            angle_name, description = random.choice(types)
            q = f"Een {angle_name} is..."
            correct = description
            all_desc = [d for _, d in types]
            wrong = [d for d in all_desc if d != correct]
        else:  # example
            q = "Geef een voorbeeld van een rechte hoek in de klas."
            correct = "hoek van de deur"
            wrong = ["de klok om 2 uur", "een schuin dak", "een open boek"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "hoeksoorten"))

    return exercises[:count]

def generate_7MM4_exercises(count=17):
    """7MM4: Coördinatenstelsel
    CSV Template: Teken punt op (-3, 5), In welk kwadrant ligt punt (-2, -4)?
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        x = random.randint(-8, 8)
        y = random.randint(-8, 8)

        # Determine quadrant
        if x > 0 and y > 0:
            quadrant = "I (eerste kwadrant)"
        elif x < 0 and y > 0:
            quadrant = "II (tweede kwadrant)"
        elif x < 0 and y < 0:
            quadrant = "III (derde kwadrant)"
        elif x > 0 and y < 0:
            quadrant = "IV (vierde kwadrant)"
        else:
            quadrant = "op een as"

        question_type = random.choice(['quadrant', 'coordinate', 'identify'])

        if question_type == 'quadrant' and quadrant != "op een as":
            q = f"In welk kwadrant ligt punt ({x}, {y})?"
            correct = quadrant
            wrong = ["I (eerste kwadrant)", "II (tweede kwadrant)", "III (derde kwadrant)", "IV (vierde kwadrant)"]
            wrong = [w for w in wrong if w != correct][:3]
        elif question_type == 'coordinate':
            q = f"Punt P ligt op ({x}, {y}). Wat is de x-coördinaat?"
            correct = f"{x}"
            wrong = [f"{x-1}", f"{x+1}", f"{y}"]
        else:
            q = f"Een punt heeft x-coördinaat {x} en y-coördinaat {y}. Notatie?"
            correct = f"({x}, {y})"
            wrong = [f"({y}, {x})", f"[{x}, {y}]", f"{x}, {y}"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "coordinatenstelsel"))

    return exercises[:count]

def generate_7MM5_exercises(count=17):
    """7MM5: Volume cilinder
    CSV Template: Cilinder met straal 4 cm en hoogte 10 cm, gebruik π = 3,14
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        straal = random.choice([3, 4, 5, 6])
        hoogte = random.randint(8, 15)

        # Volume = π × r² × h
        volume = round(3.14 * straal * straal * hoogte, 2)

        q_templates = [
            f"Bereken het volume van een cilinder met straal {straal} cm en hoogte {hoogte} cm. π = 3,14.",
            f"Cilinder: straal = {straal} cm, hoogte = {hoogte} cm. Volume? (π = 3,14)",
            f"Volume cilinder: r = {straal} cm, h = {hoogte} cm. Gebruik π = 3,14.",
        ]

        q = random.choice(q_templates)
        if q in seen:
            continue
        seen.add(q)

        correct = f"{volume} cm³"
        wrong = [f"{volume-20} cm³", f"{volume+20} cm³", f"{straal*hoogte} cm³"]

        exercises.append(create_exercise(q, correct, wrong, "volume_cilinder"))

    return exercises[:count]

def generate_7MM6_exercises(count=16):
    """7MM6: Spiegeling en rotatie
    CSV Template: Spiegel deze figuur in de x-as, Roteer 90° met de klok mee
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        transformation_type = random.choice(['spiegeling', 'rotatie', 'identify'])

        if transformation_type == 'spiegeling':
            axis = random.choice(['x-as', 'y-as'])
            x = random.randint(1, 5)
            y = random.randint(1, 5)

            if axis == 'x-as':
                new_coords = f"({x}, -{y})"
            else:  # y-as
                new_coords = f"(-{x}, {y})"

            q = f"Spiegel punt ({x}, {y}) in de {axis}. Nieuwe coördinaten?"
            correct = new_coords
            wrong = [f"({-x}, {-y})", f"({y}, {x})", f"({-x}, {y})"]
            wrong = [w for w in wrong if w != correct][:3]
        elif transformation_type == 'rotatie':
            rotation = random.choice(['90°', '180°', '270°'])
            q = f"Roteer een punt 90° met de klok mee om de oorsprong. Een punt op (2, 0) gaat naar..."
            correct = "(0, -2)"
            wrong = ["(-2, 0)", "(0, 2)", "(2, 0)"]
        else:  # identify
            q = "Welke transformatie verandert (3, 4) naar (-3, 4)?"
            correct = "Spiegeling in de y-as"
            wrong = ["Spiegeling in de x-as", "Rotatie 90°", "Rotatie 180°"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "transformaties"))

    return exercises[:count]

# ============================================================================
# GROEP 8 GENERATORS
# ============================================================================

def generate_8MM1_exercises(count=17):
    """8MM1: Complexe oppervlaktes
    CSV Template: L-vormige tuin, Rechthoek met halve cirkel, Figuur met driehoekige uitsparing
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        shape_type = random.choice(['L-vorm', 'rechthoek_plus_driehoek', 'rechthoek_minus_vierkant'])

        if shape_type == 'L-vorm':
            # L-shape: two rectangles
            rect1_l = random.randint(8, 12)
            rect1_w = random.randint(3, 5)
            rect2_l = random.randint(4, 6)
            rect2_w = random.randint(3, 5)

            area = rect1_l * rect1_w + rect2_l * rect2_w

            q = f"L-vormige figuur: eerste deel {rect1_l}×{rect1_w} cm, tweede deel {rect2_l}×{rect2_w} cm. Totale oppervlakte?"
            correct = f"{area} cm²"
            wrong = [f"{area-5} cm²", f"{area+5} cm²", f"{(rect1_l+rect2_l)*(rect1_w+rect2_w)} cm²"]
        elif shape_type == 'rechthoek_plus_driehoek':
            rect_l = random.randint(6, 10)
            rect_w = random.randint(4, 7)
            tri_b = rect_w
            tri_h = random.randint(3, 5)

            area_rect = rect_l * rect_w
            area_tri = (tri_b * tri_h) / 2
            total = area_rect + area_tri

            q = f"Rechthoek {rect_l}×{rect_w} cm met driehoek erop (basis {tri_b} cm, hoogte {tri_h} cm). Totaal?"
            correct = f"{total} cm²"
            wrong = [f"{total-5} cm²", f"{total+5} cm²", f"{area_rect} cm²"]
        else:  # rechthoek minus vierkant
            rect_l = random.randint(10, 15)
            rect_w = random.randint(8, 12)
            square_s = random.randint(2, 4)

            area = rect_l * rect_w - square_s * square_s

            q = f"Rechthoek {rect_l}×{rect_w} cm met vierkante uitsparing {square_s}×{square_s} cm. Resterende oppervlakte?"
            correct = f"{area} cm²"
            wrong = [f"{area-10} cm²", f"{area+10} cm²", f"{rect_l*rect_w} cm²"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "complexe_oppervlakte"))

    return exercises[:count]

def generate_8MM2_exercises(count=17):
    """8MM2: Eigenschappen meetkundige figuren
    CSV Template: Hoeveel ribben heeft een kubus?, Wat is de som van hoeken in een driehoek?
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        question_type = random.choice(['ribben', 'vlakken', 'hoekpunten', 'hoeken_som',
                                       'symmetrie', 'identify', 'polygon_hoeken'])

        if question_type == 'ribben':
            shapes = [
                ("kubus", "12 ribben", ["8 ribben", "6 ribben", "10 ribben"]),
                ("balk", "12 ribben", ["8 ribben", "6 ribben", "10 ribben"]),
                ("piramide met vierkant grondvlak", "8 ribben", ["5 ribben", "6 ribben", "12 ribben"]),
                ("piramide met driehoek grondvlak", "6 ribben", ["3 ribben", "4 ribben", "9 ribben"]),
                ("cilinder", "2 ribben", ["0 ribben", "3 ribben", "4 ribben"]),
            ]
            shape, correct, wrong = random.choice(shapes)
            q = f"Hoeveel ribben heeft een {shape}?"
        elif question_type == 'vlakken':
            shapes = [
                ("kubus", "6 vlakken", ["4 vlakken", "8 vlakken", "12 vlakken"]),
                ("balk", "6 vlakken", ["4 vlakken", "8 vlakken", "12 vlakken"]),
                ("cilinder", "3 vlakken", ["2 vlakken", "4 vlakken", "1 vlak"]),
                ("piramide met vierkant grondvlak", "5 vlakken", ["4 vlakken", "6 vlakken", "8 vlakken"]),
                ("bol", "1 vlak", ["0 vlakken", "2 vlakken", "3 vlakken"]),
            ]
            shape, correct, wrong = random.choice(shapes)
            q = f"Hoeveel vlakken heeft een {shape}?"
        elif question_type == 'hoekpunten':
            shapes = [
                ("kubus", "8 hoekpunten", ["6 hoekpunten", "12 hoekpunten", "4 hoekpunten"]),
                ("balk", "8 hoekpunten", ["6 hoekpunten", "12 hoekpunten", "4 hoekpunten"]),
                ("piramide met vierkant grondvlak", "5 hoekpunten", ["4 hoekpunten", "6 hoekpunten", "8 hoekpunten"]),
                ("bol", "0 hoekpunten", ["1 hoekpunt", "2 hoekpunten", "4 hoekpunten"]),
                ("cilinder", "0 hoekpunten", ["2 hoekpunten", "4 hoekpunten", "6 hoekpunten"]),
            ]
            shape, correct, wrong = random.choice(shapes)
            q = f"Hoeveel hoekpunten heeft een {shape}?"
        elif question_type == 'hoeken_som':
            shapes = [
                ("driehoek", "180°", ["90°", "360°", "270°"]),
                ("vierhoek", "360°", ["180°", "540°", "270°"]),
                ("vijfhoek", "540°", ["360°", "720°", "450°"]),
            ]
            shape, correct, wrong = random.choice(shapes)
            q = f"Wat is de som van alle hoeken in een {shape}?"
        elif question_type == 'symmetrie':
            shapes = [
                ("vierkant", "4 symmetrie-assen", ["2 symmetrie-assen", "8 symmetrie-assen", "1 symmetrie-as"]),
                ("rechthoek", "2 symmetrie-assen", ["4 symmetrie-assen", "1 symmetrie-as", "3 symmetrie-assen"]),
                ("gelijkzijdige driehoek", "3 symmetrie-assen", ["1 symmetrie-as", "2 symmetrie-assen", "6 symmetrie-assen"]),
            ]
            shape, correct, wrong = random.choice(shapes)
            q = f"Hoeveel symmetrie-assen heeft een {shape}?"
        elif question_type == 'identify':
            questions = [
                ("Welke ruimtelijke figuur heeft geen hoekpunten?", "bol", ["kubus", "piramide", "balk"]),
                ("Welke vlakke figuur heeft geen hoeken?", "cirkel", ["vierkant", "driehoek", "rechthoek"]),
                ("Welke figuur heeft allemaal gelijke zijden en hoeken?", "vierkant", ["rechthoek", "driehoek", "vijfhoek"]),
            ]
            q, correct, wrong = random.choice(questions)
        else:  # polygon_hoeken
            n = random.choice([5, 6, 7, 8])
            q = f"Hoeveel hoeken heeft een {n}-hoek?"
            correct = f"{n} hoeken"
            wrong = [f"{n-1} hoeken", f"{n+1} hoeken", f"{n+2} hoeken"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "eigenschappen"))

    return exercises[:count]

def generate_8MM3_exercises(count=16):
    """8MM3: Schaalmodellen maken
    CSV Template: Teken een kamer van 4×5 meter op schaal 1:50, Bereken echte afmetingen
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        scale = random.choice([50, 100, 200])
        question_type = random.choice(['real_to_model', 'model_to_real', 'identify_scale'])

        if question_type == 'real_to_model':
            real_meters = random.randint(3, 10)
            real_cm = real_meters * 100
            model_cm = real_cm / scale

            q = f"Teken {real_meters} meter op schaal 1:{scale}. Hoeveel cm op papier?"
            correct = f"{model_cm} cm"
            wrong = [f"{model_cm-1} cm", f"{model_cm+1} cm", f"{real_meters} cm"]
        elif question_type == 'model_to_real':
            model_cm = random.choice([5, 8, 10, 15, 20])
            real_cm = model_cm * scale
            real_m = real_cm / 100

            q = f"Op schaal 1:{scale} is iets {model_cm} cm. Echte lengte in meters?"
            correct = f"{real_m} meter"
            wrong = [f"{real_m-1} meter", f"{real_m+1} meter", f"{model_cm} meter"]
        else:  # identify_scale
            real_m = 2
            model_cm = 4
            scale_result = (real_m * 100) / model_cm

            q = f"Op de tekening is {real_m} meter = {model_cm} cm. Welke schaal?"
            correct = f"1:{int(scale_result)}"
            wrong = ["1:100", "1:25", "1:200"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "schaalmodellen"))

    return exercises[:count]

def generate_8MM4_exercises(count=17):
    """8MM4: Meten - alle eenheden
    CSV Template: Mix van mm, cm, dm, m, km / g, kg, ton / ml, cl, dl, l
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        category = random.choice(['length', 'weight', 'volume', 'time'])

        if category == 'length':
            conversions = [
                (random.randint(2, 10), 'km', 'meter', 1000),
                (random.randint(100, 900), 'cm', 'meter', 0.01),
                (random.randint(20, 90), 'mm', 'cm', 0.1),
                (random.randint(10, 50), 'dm', 'cm', 10),
                (random.randint(100, 500), 'cm', 'dm', 0.1),
                (random.randint(1000, 9000), 'mm', 'meter', 0.001),
            ]
            value, from_unit, to_unit, factor = random.choice(conversions)
            result = value * factor
            q = f"Hoeveel {to_unit} is {value} {from_unit}?"
            correct = f"{result} {to_unit}"
            wrong = [f"{result*0.1} {to_unit}", f"{result*10} {to_unit}", f"{value} {to_unit}"]
        elif category == 'weight':
            conversions = [
                (random.randint(2, 10), 'ton', 'kg', 1000),
                (random.randint(1000, 9000), 'gram', 'kg', 0.001),
                (random.randint(1, 5), 'kg', 'gram', 1000),
            ]
            value, from_unit, to_unit, factor = random.choice(conversions)
            result = value * factor
            q = f"Hoeveel {to_unit} is {value} {from_unit}?"
            correct = f"{result} {to_unit}"
            wrong = [f"{result*0.1} {to_unit}", f"{result*10} {to_unit}", f"{value} {to_unit}"]
        elif category == 'volume':
            conversions = [
                (random.randint(100, 900), 'ml', 'liter', 0.001),
                (random.randint(20, 90), 'cl', 'liter', 0.01),
                (random.randint(5, 25), 'dl', 'liter', 0.1),
                (random.randint(1, 5), 'liter', 'ml', 1000),
                (random.randint(10, 50), 'cl', 'ml', 10),
            ]
            value, from_unit, to_unit, factor = random.choice(conversions)
            result = value * factor
            q = f"Hoeveel {to_unit} is {value} {from_unit}?"
            correct = f"{result} {to_unit}"
            wrong = [f"{result*0.1} {to_unit}", f"{result*10} {to_unit}", f"{value} {to_unit}"]
        else:  # time
            conversions = [
                (random.randint(60, 180), 'minuten', 'uur', 1/60),
                (random.randint(2, 10), 'uur', 'minuten', 60),
                (random.randint(120, 300), 'seconden', 'minuten', 1/60),
            ]
            value, from_unit, to_unit, factor = random.choice(conversions)
            result = value * factor
            q = f"Hoeveel {to_unit} is {value} {from_unit}?"
            correct = f"{result} {to_unit}"
            wrong = [f"{result-0.5} {to_unit}", f"{result+0.5} {to_unit}", f"{value} {to_unit}"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "alle_eenheden"))

    return exercises[:count]

def generate_8MM5_exercises(count=17):
    """8MM5: Meetkunde - alle figuren
    CSV Template: Mix van omtrek, oppervlakte, volume voor alle figuren
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        question_type = random.choice(['omtrek_vierkant', 'omtrek_rechthoek', 'oppervlakte_rechthoek',
                                       'oppervlakte_driehoek', 'volume_kubus', 'volume_balk',
                                       'properties'])

        if question_type == 'omtrek_vierkant':
            side = random.randint(4, 15)
            perimeter = 4 * side
            q = f"Omtrek vierkant met zijde {side} cm?"
            correct = f"{perimeter} cm"
            wrong = [f"{side*2} cm", f"{side*side} cm", f"{perimeter-4} cm"]
        elif question_type == 'omtrek_rechthoek':
            l = random.randint(5, 15)
            w = random.randint(3, 10)
            perimeter = 2 * (l + w)
            q = f"Omtrek rechthoek {l}×{w} cm?"
            correct = f"{perimeter} cm"
            wrong = [f"{l*w} cm", f"{l+w} cm", f"{perimeter-2} cm"]
        elif question_type == 'oppervlakte_rechthoek':
            l = random.randint(4, 12)
            w = random.randint(3, 10)
            area = l * w
            q = f"Oppervlakte rechthoek {l}×{w} cm?"
            correct = f"{area} cm²"
            wrong = [f"{2*(l+w)} cm²", f"{l+w} cm²", f"{area-l} cm²"]
        elif question_type == 'oppervlakte_driehoek':
            basis = random.randint(6, 14)
            hoogte = random.randint(4, 10)
            area = (basis * hoogte) / 2
            q = f"Oppervlakte driehoek: basis {basis} cm, hoogte {hoogte} cm?"
            correct = f"{area} cm²"
            wrong = [f"{basis*hoogte} cm²", f"{area-basis} cm²", f"{area+hoogte} cm²"]
        elif question_type == 'volume_kubus':
            ribbe = random.randint(3, 8)
            volume = ribbe ** 3
            q = f"Volume kubus met ribbe {ribbe} cm?"
            correct = f"{volume} cm³"
            wrong = [f"{ribbe*ribbe} cm³", f"{volume-ribbe} cm³", f"{ribbe*6} cm³"]
        elif question_type == 'volume_balk':
            l = random.randint(4, 10)
            w = random.randint(3, 7)
            h = random.randint(2, 6)
            volume = l * w * h
            q = f"Volume balk {l}×{w}×{h} cm?"
            correct = f"{volume} cm³"
            wrong = [f"{l*w} cm³", f"{volume-10} cm³", f"{l+w+h} cm³"]
        else:  # properties
            props = [
                (f"Hoeveel hoeken heeft een {n}-hoek?", f"{n} hoeken", [f"{n-1} hoeken", f"{n+1} hoeken", f"{n+2} hoeken"])
                for n in [5, 6, 7, 8]
            ] + [
                ("Hoeveel vlakken heeft een kubus?", "6 vlakken", ["4 vlakken", "8 vlakken", "12 vlakken"]),
                ("Hoeveel vlakken heeft een balk?", "6 vlakken", ["4 vlakken", "8 vlakken", "12 vlakken"]),
                ("Hoeveel ribben heeft een kubus?", "12 ribben", ["6 ribben", "8 ribben", "10 ribben"]),
            ]
            q, correct, wrong = random.choice(props)

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "alle_figuren"))

    return exercises[:count]

def generate_8MM6_exercises(count=16):
    """8MM6: Referentieniveau meetkunde (CITO niveau)
    CSV Template: Complexe CITO-stijl vragen, meerdere stappen, realistische context
    """
    exercises = []
    seen = set()

    for _ in range(count * 10):  # Increased multiplier to ensure enough unique questions
        if len(exercises) >= count:
            break

        question_type = random.choice(['complex_area', 'diagonal', 'volume_complex', 'scale',
                                       'angles', 'coordinates', 'combined'])

        if question_type == 'complex_area':
            l1 = random.randint(10, 15)
            w1 = random.randint(6, 10)
            area1 = l1 * w1
            l2 = random.randint(3, 6)
            w2 = random.randint(2, 5)
            area2 = l2 * w2
            total = area1 + area2
            q = f"L-vormige kamer: {l1}×{w1} m + {l2}×{w2} m. Totale oppervlakte?"
            correct = f"{total} m²"
            wrong = [f"{area1} m²", f"{total-10} m²", f"{total+10} m²"]
        elif question_type == 'diagonal':
            l = random.choice([80, 100, 120])
            w = random.choice([50, 60, 70])
            diagonal_approx = int((l**2 + w**2)**0.5)
            q = f"Schat de diagonaal van een voetbalveld van {l}×{w} meter."
            correct = f"ongeveer {diagonal_approx} meter"
            wrong = [f"ongeveer {l+w} meter", f"ongeveer {l} meter", f"ongeveer {int(diagonal_approx*1.2)} meter"]
        elif question_type == 'volume_complex':
            diameter = random.choice([8, 10, 12])
            straal = diameter / 2
            hoogte = random.randint(12, 20)
            volume = round(3.14 * straal * straal * hoogte, 1)
            q = f"Een cilinder heeft diameter {diameter} cm en hoogte {hoogte} cm. Volume? (π = 3,14)"
            correct = f"{volume} cm³"
            wrong = [f"{volume*0.5} cm³", f"{volume*2} cm³", f"{diameter*hoogte} cm³"]
        elif question_type == 'scale':
            map_cm = random.choice([5, 6, 8, 10])
            scale = random.choice([50000, 100000, 25000])
            real_km = (map_cm * scale) / 100000
            q = f"Op de kaart is {map_cm} cm. Schaal 1:{scale}. Echte afstand in km?"
            correct = f"{real_km} km"
            wrong = [f"{real_km*2} km", f"{map_cm} km", f"{real_km*10} km"]
        elif question_type == 'angles':
            angle1 = random.randint(40, 70)
            angle2 = random.randint(40, 70)
            angle3 = 180 - angle1 - angle2
            q = f"Driehoek ABC heeft hoeken van {angle1}° en {angle2}°. Hoeveel graden is hoek C?"
            correct = f"{angle3}°"
            wrong = [f"{angle3+10}°", f"{angle3-10}°", f"{180-angle1}°"]
        elif question_type == 'coordinates':
            x = random.randint(2, 8)
            y = random.randint(2, 8)
            mirror_type = random.choice(['x-as', 'y-as'])
            if mirror_type == 'x-as':
                new_coords = f"({x}, -{y})"
                wrong = [f"(-{x}, {y})", f"(-{x}, -{y})", f"({y}, {x})"]
            else:
                new_coords = f"(-{x}, {y})"
                wrong = [f"({x}, -{y})", f"(-{x}, -{y})", f"({y}, {x})"]
            q = f"Punt P ({x}, {y}) gespiegeld in {mirror_type} geeft..."
            correct = new_coords
        else:  # combined
            l = random.randint(8, 12)
            w = random.randint(5, 9)
            h = random.randint(3, 6)
            volume = l * w * h
            q = f"Balk {l}×{w}×{h} cm. Bereken het volume."
            correct = f"{volume} cm³"
            wrong = [f"{l*w} cm³", f"{volume-10} cm³", f"{2*(l+w+h)} cm³"]

        if q in seen:
            continue
        seen.add(q)

        exercises.append(create_exercise(q, correct, wrong, "cito_niveau"))

    return exercises[:count]

# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================

def generate_exercises_for_file(file_id, codes):
    """Generate exercises for a specific file based on its learning objective codes"""
    all_exercises = []

    # Map each code to its generator function
    generators = {
        # Groep 3
        '3MM1': generate_3MM1_exercises,
        '3MM2': generate_3MM2_exercises,
        '3MM3': generate_3MM3_exercises,
        '3MM4': generate_3MM4_exercises,
        '3MM5': generate_3MM5_exercises,
        '3MM6': generate_3MM6_exercises,
        # Groep 4
        '4MM1': generate_4MM1_exercises,
        '4MM2': generate_4MM2_exercises,
        '4MM3': generate_4MM3_exercises,
        '4MM4': generate_4MM4_exercises,
        '4MM5': generate_4MM5_exercises,
        '4MM6': generate_4MM6_exercises,
        '4MM7': generate_4MM7_exercises,
        # Groep 5
        '5MM1': generate_5MM1_exercises,
        '5MM2': generate_5MM2_exercises,
        '5MM3': generate_5MM3_exercises,
        '5MM4': generate_5MM4_exercises,
        '5MM5': generate_5MM5_exercises,
        '5MM6': generate_5MM6_exercises,
        '5MM7': generate_5MM7_exercises,
        # Groep 6
        '6MM1': generate_6MM1_exercises,
        '6MM2': generate_6MM2_exercises,
        '6MM3': generate_6MM3_exercises,
        '6MM4': generate_6MM4_exercises,
        '6MM5': generate_6MM5_exercises,
        '6MM6': generate_6MM6_exercises,
        '6MM7': generate_6MM7_exercises,
        # Groep 7
        '7MM1': generate_7MM1_exercises,
        '7MM2': generate_7MM2_exercises,
        '7MM3': generate_7MM3_exercises,
        '7MM4': generate_7MM4_exercises,
        '7MM5': generate_7MM5_exercises,
        '7MM6': generate_7MM6_exercises,
        # Groep 8
        '8MM1': generate_8MM1_exercises,
        '8MM2': generate_8MM2_exercises,
        '8MM3': generate_8MM3_exercises,
        '8MM4': generate_8MM4_exercises,
        '8MM5': generate_8MM5_exercises,
        '8MM6': generate_8MM6_exercises,
    }

    # Calculate exercises per code (total 50)
    per_code = 50 // len(codes)
    remainder = 50 % len(codes)

    for i, code in enumerate(codes):
        count = per_code + (1 if i < remainder else 0)
        if code in generators:
            exercises = generators[code](count)
            all_exercises.extend(exercises)
        else:
            print(f"WARNING: No generator found for code {code}")

    return all_exercises[:50]  # Ensure exactly 50

def check_duplicates(exercises, file_id):
    """Check for duplicate questions in a list of exercises"""
    questions = [ex['question']['text'] for ex in exercises]
    unique = len(set(questions))
    duplicates = len(exercises) - unique

    if duplicates == 0:
        print(f"  ✓ {file_id}: {len(exercises)} exercises, 0 duplicates")
        return True
    else:
        print(f"  ✗ {file_id}: {len(exercises)} exercises, {duplicates} duplicates")
        return False

def save_exercises_to_json(exercises, file_path):
    """Save exercises to JSON file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(exercises, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print("=" * 80)
    print("MEETKUNDE EXERCISE GENERATOR - Regenerating ALL 24 files")
    print("=" * 80)
    print()

    # Define all 12 file mappings for Groep 3-8
    file_mappings = {
        'data-v2/exercises/mk/gb_groep3_meetkunde_m3_core.json': ['3MM1', '3MM2', '3MM3'],
        'data-v2/exercises/mk/gb_groep3_meetkunde_e3_core.json': ['3MM4', '3MM5', '3MM6'],
        'data-v2/exercises/mk/gb_groep4_meetkunde_m4_core.json': ['4MM1', '4MM2', '4MM3', '4MM4'],
        'data-v2/exercises/mk/gb_groep4_meetkunde_e4_core.json': ['4MM5', '4MM6', '4MM7'],
        'data-v2/exercises/mk/gb_groep5_meetkunde_m5_core.json': ['5MM1', '5MM2', '5MM3', '5MM4'],
        'data-v2/exercises/mk/gb_groep5_meetkunde_e5_core.json': ['5MM5', '5MM6', '5MM7'],
        'data-v2/exercises/mk/gb_groep6_meetkunde_m6_core.json': ['6MM1', '6MM2', '6MM3', '6MM4'],
        'data-v2/exercises/mk/gb_groep6_meetkunde_e6_core.json': ['6MM5', '6MM6', '6MM7'],
        'data-v2/exercises/mk/gb_groep7_meetkunde_m7_core.json': ['7MM1', '7MM2', '7MM3'],
        'data-v2/exercises/mk/gb_groep7_meetkunde_e7_core.json': ['7MM4', '7MM5', '7MM6'],
        'data-v2/exercises/mk/gb_groep8_meetkunde_m8_core.json': ['8MM1', '8MM2', '8MM3'],
        'data-v2/exercises/mk/gb_groep8_meetkunde_e8_core.json': ['8MM4', '8MM5', '8MM6'],
    }

    print(f"Generating exercises for {len(file_mappings)} files...")
    print()

    all_ok = True
    results = []

    for file_path, codes in file_mappings.items():
        file_id = file_path.split('/')[-1].replace('_core.json', '')

        # Generate exercises
        exercises = generate_exercises_for_file(file_id, codes)

        # Check for duplicates
        is_ok = check_duplicates(exercises, file_id)
        all_ok = all_ok and is_ok

        # Save to file
        save_exercises_to_json(exercises, file_path)

        results.append({
            'file': file_id,
            'codes': codes,
            'count': len(exercises),
            'duplicates': len(exercises) - len(set([ex['question']['text'] for ex in exercises]))
        })

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    for result in results:
        status = "✓" if result['duplicates'] == 0 else "✗"
        print(f"{status} {result['file']}: {result['count']} exercises, {result['duplicates']} duplicates")

    print()
    if all_ok:
        print("SUCCESS: All files generated with 0 duplicates!")
    else:
        print("WARNING: Some files have duplicates. Please review.")

    print()
    print(f"Total files generated: {len(results)}")
    print(f"Total exercises: {sum(r['count'] for r in results)}")
