#!/usr/bin/env python3
"""
GB Exercise Generator - Verhoudingen & Meten/Meetkunde
Generates both core and support JSON files for all grade levels
"""

import json
import os
from typing import List, Dict, Any

# Output directories per domain
OUTPUT_DIRS = {
    "verhoudingen": "data-v2/exercises/vh",
    "meetkunde": "data-v2/exercises/mk"
}

def create_verhoudingen_items(grade: int, level: str, count: int) -> List[Dict]:
    """Generate Verhoudingen (fractions, decimals, percentages) items"""
    items = []
    item_id = 1

    # Grade 3: Visual fractions, basic parts of wholes
    if grade == 3:
        # Visual fractions with emoji representations
        for i in range(10):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "breuken-visueel",
                "question": {
                    "text": f"Welke breuk zie je? 🟦🟦⬜⬜ (2 van 4 vakjes zijn blauw)"
                },
                "options": [
                    {"text": "1/2"},
                    {"text": "1/4"},
                    {"text": "2/4"},
                    {"text": "3/4"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 2 if i % 2 == 0 else 0  # 2/4 or 1/2 (equivalent)
                },
                "hint": "Tel hoeveel vakjes blauw zijn (2) en hoeveel er in totaal zijn (4). Dat is 2/4 = 1/2"
            })
            item_id += 1

        # Simple fraction of quantity (half of N)
        for i in range(5):
            num = (i + 1) * 4
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "fractie-hoeveelheid",
                "question": {
                    "text": f"De helft van {num} is..."
                },
                "options": [
                    {"text": str(num // 2 - 1)},
                    {"text": str(num // 2)},
                    {"text": str(num // 2 + 1)},
                    {"text": str(num)}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 1
                },
                "hint": f"De helft = delen door 2. {num} ÷ 2 = {num // 2}"
            })
            item_id += 1

        # Quarter of quantity
        for i in range(5):
            num = (i + 2) * 4
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "fractie-hoeveelheid",
                "question": {
                    "text": f"Een kwart van {num} is..."
                },
                "options": [
                    {"text": str(num // 4)},
                    {"text": str(num // 2)},
                    {"text": str(num)},
                    {"text": str(num // 4 + 1)}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": f"Een kwart = delen door 4. {num} ÷ 4 = {num // 4}"
            })
            item_id += 1

        # Visual comparison
        for i in range(5):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "vergelijken",
                "question": {
                    "text": "Wat is meer: de helft of een kwart?"
                },
                "options": [
                    {"text": "de helft"},
                    {"text": "een kwart"},
                    {"text": "ze zijn gelijk"},
                    {"text": "weet ik niet"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "De helft (1/2) is groter dan een kwart (1/4)"
            })
            item_id += 1

        # Add more for M3
        if level == "M3":
            for i in range(10):
                items.append({
                    "id": item_id,
                    "type": "multiple_choice",
                    "theme": "breuken-derde",
                    "question": {
                        "text": f"Een derde van {(i+1)*3} is..."
                    },
                    "options": [
                        {"text": str(i+1)},
                        {"text": str((i+1)*2)},
                        {"text": str((i+1)*3)},
                        {"text": str(i)}
                    ],
                    "answer": {
                        "type": "single",
                        "correct_index": 0
                    },
                    "hint": f"Een derde = delen door 3. {(i+1)*3} ÷ 3 = {i+1}"
                })
                item_id += 1

        return items[:count]

    # Grade 4: Fraction notation, simple operations
    elif grade == 4:
        themes = ["fractie-notatie", "fractie-hoeveelheid", "vergelijken", "equivalent"]

        # Fraction notation (1/2, 1/4, 1/3, 1/5, 1/10)
        for i in range(8):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "fractie-notatie",
                "question": {
                    "text": f"Schrijf als breuk: {'de helft' if i % 3 == 0 else 'een kwart' if i % 3 == 1 else 'een vijfde'}"
                },
                "options": [
                    {"text": "1/2"},
                    {"text": "1/4"},
                    {"text": "1/5"},
                    {"text": "1/10"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": i % 3
                },
                "hint": "De helft = 1/2, een kwart = 1/4, een vijfde = 1/5"
            })
            item_id += 1

        # Fraction of quantity
        quantities = [20, 100, 40, 50, 30, 60]
        for i, q in enumerate(quantities):
            fraction = "1/4" if i % 2 == 0 else "1/5"
            divisor = 4 if i % 2 == 0 else 5
            answer = q // divisor

            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "fractie-hoeveelheid",
                "question": {
                    "text": f"Wat is {fraction} van {q}?"
                },
                "options": [
                    {"text": str(answer - 1)},
                    {"text": str(answer)},
                    {"text": str(answer + 1)},
                    {"text": str(q // 2)}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 1
                },
                "hint": f"{fraction} betekent delen door {divisor}. {q} ÷ {divisor} = ?"
            })
            item_id += 1

        # Ordering fractions (same denominator)
        for i in range(6):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "vergelijken",
                "question": {
                    "text": f"Wat is groter: {i+1}/5 of {i+2}/5?"
                },
                "options": [
                    {"text": f"{i+1}/5"},
                    {"text": f"{i+2}/5"},
                    {"text": "ze zijn gelijk"},
                    {"text": "weet ik niet"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 1
                },
                "hint": "Bij dezelfde noemer is de breuk met grotere teller groter"
            })
            item_id += 1

        # Equivalent fractions
        equivalents = [("2/4", "1/2"), ("5/10", "1/2"), ("2/6", "1/3"), ("3/6", "1/2")]
        for i, (frac1, frac2) in enumerate(equivalents):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "equivalent",
                "question": {
                    "text": f"Welke breuk is hetzelfde als {frac1}?"
                },
                "options": [
                    {"text": "1/4"},
                    {"text": frac2},
                    {"text": "3/4"},
                    {"text": "1/5"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 1
                },
                "hint": f"{frac1} = {frac2}"
            })
            item_id += 1

        # Add more items for M4 if needed
        if level == "M4":
            # Mixed numbers introduction
            for i in range(8):
                items.append({
                    "id": item_id,
                    "type": "multiple_choice",
                    "theme": "gemengd",
                    "question": {
                        "text": f"1 heel en nog 1/2 is..."
                    },
                    "options": [
                        {"text": "1"},
                        {"text": "1 1/2"},
                        {"text": "2"},
                        {"text": "1/2"}
                    ],
                    "answer": {
                        "type": "single",
                        "correct_index": 1
                    },
                    "hint": "1 + 1/2 = 1 1/2 (gemengd getal)"
                })
                item_id += 1

    # Grade 5: Decimals, percentages
    elif grade == 5:
        # Decimals to tenths
        for i in range(10):
            decimal = round(0.1 * (i + 1), 1)
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "decimalen",
                "question": {
                    "text": f"Schrijf als breuk: {decimal}"
                },
                "options": [
                    {"text": f"{i+1}/10"},
                    {"text": f"{i+1}/100"},
                    {"text": f"1/{i+1}"},
                    {"text": f"{i+1}/5"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": f"{decimal} = {i+1} tiende = {i+1}/10"
            })
            item_id += 1

        # Money context (decimals)
        prices = [(2.50, 1.75), (5.25, 3.50), (10.00, 4.75), (7.50, 2.25)]
        for p1, p2 in prices:
            total = p1 + p2
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "decimalen-geld",
                "question": {
                    "text": f"€{p1:.2f} + €{p2:.2f} = ?"
                },
                "options": [
                    {"text": f"€{total - 1:.2f}"},
                    {"text": f"€{total:.2f}"},
                    {"text": f"€{total + 1:.2f}"},
                    {"text": f"€{total * 2:.2f}"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 1
                },
                "hint": "Tel eerst de euro's, dan de centen"
            })
            item_id += 1

        # Percentages basics
        percentages = [(50, 100), (25, 100), (10, 100), (50, 200), (25, 80)]
        for perc, total in percentages:
            answer = (perc * total) // 100
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "procenten",
                "question": {
                    "text": f"Wat is {perc}% van {total}?"
                },
                "options": [
                    {"text": str(answer - 5)},
                    {"text": str(answer)},
                    {"text": str(answer + 5)},
                    {"text": str(total)}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 1
                },
                "hint": f"{perc}% = {perc}/100. Dus {perc}% van {total} = ({perc} × {total}) ÷ 100"
            })
            item_id += 1

        # Add more for M5
        if level == "M5":
            # Decimals to hundredths
            for i in range(5):
                decimal = round(0.25 * (i + 1), 2)
                items.append({
                    "id": item_id,
                    "type": "multiple_choice",
                    "theme": "decimalen-honderdsten",
                    "question": {
                        "text": f"{decimal} = ?"
                    },
                    "options": [
                        {"text": f"{int(decimal * 100)}/10"},
                        {"text": f"{int(decimal * 100)}/100"},
                        {"text": f"{int(decimal * 10)}/10"},
                        {"text": f"1/{int(1/decimal) if decimal > 0 else 1}"}
                    ],
                    "answer": {
                        "type": "single",
                        "correct_index": 1
                    },
                    "hint": "Tel hoeveel honderdsten"
                })
                item_id += 1

    # Grades 6-8: Progressively more complex
    elif grade >= 6:
        # Complex fractions, all operations
        operations = ["+", "-", "×"]
        for i in range(15):
            op = operations[i % 3]
            if op == "+":
                items.append({
                    "id": item_id,
                    "type": "multiple_choice",
                    "theme": "breuken-optellen",
                    "question": {
                        "text": f"1/4 + 2/4 = ?"
                    },
                    "options": [
                        {"text": "1/4"},
                        {"text": "2/4"},
                        {"text": "3/4"},
                        {"text": "3/8"}
                    ],
                    "answer": {
                        "type": "single",
                        "correct_index": 2
                    },
                    "hint": "Tel de tellers op, de noemer blijft hetzelfde"
                })
            elif op == "-":
                items.append({
                    "id": item_id,
                    "type": "multiple_choice",
                    "theme": "breuken-aftrekken",
                    "question": {
                        "text": f"3/5 - 1/5 = ?"
                    },
                    "options": [
                        {"text": "1/5"},
                        {"text": "2/5"},
                        {"text": "2/0"},
                        {"text": "4/5"}
                    ],
                    "answer": {
                        "type": "single",
                        "correct_index": 1
                    },
                    "hint": "Trek de tellers af, de noemer blijft hetzelfde"
                })
            else:  # ×
                items.append({
                    "id": item_id,
                    "type": "multiple_choice",
                    "theme": "breuken-vermenigvuldigen",
                    "question": {
                        "text": f"1/3 × 6 = ?"
                    },
                    "options": [
                        {"text": "1"},
                        {"text": "2"},
                        {"text": "3"},
                        {"text": "6"}
                    ],
                    "answer": {
                        "type": "single",
                        "correct_index": 1
                    },
                    "hint": "1/3 van 6 = 6 ÷ 3 = 2"
                })
            item_id += 1

        # Percentage applications
        for i in range(10):
            price = 50 + (i * 10)
            discount = 20
            answer = price - (price * discount // 100)
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "procenten-korting",
                "question": {
                    "text": f"Een artikel kost €{price}. Je krijgt {discount}% korting. Wat betaal je?"
                },
                "options": [
                    {"text": f"€{answer - 5}"},
                    {"text": f"€{answer}"},
                    {"text": f"€{answer + 5}"},
                    {"text": f"€{price}"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 1
                },
                "hint": f"Eerst de korting: {discount}% van €{price} = €{price * discount // 100}. Dan aftrekken."
            })
            item_id += 1

        # Scale/ratio for higher grades
        if grade >= 7:
            ratios = [(1, 100), (1, 50), (1, 1000), (2, 3)]
            for i, (num, denom) in enumerate(ratios):
                items.append({
                    "id": item_id,
                    "type": "multiple_choice",
                    "theme": "schaal",
                    "question": {
                        "text": f"Op een kaart is de schaal 1:{denom}. 1 cm op de kaart is ... in het echt"
                    },
                    "options": [
                        {"text": f"{denom // 10} cm"},
                        {"text": f"{denom} cm"},
                        {"text": f"{denom * 10} cm"},
                        {"text": f"1 cm"}
                    ],
                    "answer": {
                        "type": "single",
                        "correct_index": 1
                    },
                    "hint": f"Schaal 1:{denom} betekent dat 1 cm op de kaart {denom} cm in werkelijkheid is"
                })
                item_id += 1

    # Ensure we have enough items
    while len(items) < count:
        items.append({
            "id": item_id,
            "type": "multiple_choice",
            "theme": "oefening",
            "question": {
                "text": f"Oefenvraag {item_id}: 1/2 + 1/4 = ?"
            },
            "options": [
                {"text": "1/4"},
                {"text": "1/2"},
                {"text": "3/4"},
                {"text": "1"}
            ],
            "answer": {
                "type": "single",
                "correct_index": 2
            },
            "hint": "1/2 = 2/4, dus 2/4 + 1/4 = 3/4"
        })
        item_id += 1

    return items[:count]


def create_meetkunde_items(grade: int, level: str, count: int) -> List[Dict]:
    """Generate Meten & Meetkunde (measurement & geometry) items"""
    items = []
    item_id = 1

    # Grade 3: Basic measurement, shape recognition
    if grade == 3:
        # Length measurements
        for i in range(8):
            cm = (i + 1) * 10
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "lengte",
                "question": {
                    "text": f"{cm} cm = ... meter"
                },
                "options": [
                    {"text": f"{cm / 100} m"},
                    {"text": f"{cm / 10} m"},
                    {"text": f"{cm} m"},
                    {"text": f"{cm * 100} m"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "100 cm = 1 meter"
            })
            item_id += 1

        # Time (clock reading)
        times = [("3:00", "drie uur"), ("6:30", "half zeven"), ("9:00", "negen uur")]
        for digital, analog in times:
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "tijd",
                "question": {
                    "text": f"De klok wijst {digital} aan. Hoe laat is het?"
                },
                "options": [
                    {"text": analog},
                    {"text": "weet ik niet"},
                    {"text": "twaalf uur"},
                    {"text": "één uur"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": f"{digital} = {analog}"
            })
            item_id += 1

        # Money
        for i in range(5):
            euros = (i + 1) * 2
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "geld",
                "question": {
                    "text": f"Je hebt {euros} munten van €1. Hoeveel euro heb je?"
                },
                "options": [
                    {"text": f"€{euros - 1}"},
                    {"text": f"€{euros}"},
                    {"text": f"€{euros + 1}"},
                    {"text": f"€{euros * 2}"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 1
                },
                "hint": f"{euros} × €1 = €{euros}"
            })
            item_id += 1

        # Shapes
        shapes = [("cirkel", "0"), ("driehoek", "3"), ("vierkant", "4"), ("rechthoek", "4")]
        for shape, corners in shapes:
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "vormen",
                "question": {
                    "text": f"Hoeveel hoeken heeft een {shape}?"
                },
                "options": [
                    {"text": "0"},
                    {"text": "3"},
                    {"text": "4"},
                    {"text": "5"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": ["0", "3", "4", "5"].index(corners)
                },
                "hint": f"Tel de hoeken van een {shape}"
            })
            item_id += 1

    # Grade 4: Measurement tools, conversions
    elif grade == 4:
        # Length conversions
        conversions = [(100, "cm", "1 m"), (1000, "m", "1 km"), (10, "cm", "1 dm")]
        for value, unit1, unit2 in conversions:
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "lengte-omrekenen",
                "question": {
                    "text": f"{value} {unit1} = ?"
                },
                "options": [
                    {"text": unit2},
                    {"text": f"{value} {unit1}"},
                    {"text": f"10 {unit1}"},
                    {"text": "weet ik niet"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": f"{value} {unit1} = {unit2}"
            })
            item_id += 1

        # Weight
        for i in range(5):
            kg = i + 1
            g = kg * 1000
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "gewicht",
                "question": {
                    "text": f"{kg} kg = ... gram"
                },
                "options": [
                    {"text": f"{g // 10} g"},
                    {"text": f"{g} g"},
                    {"text": f"{g * 10} g"},
                    {"text": f"{kg} g"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 1
                },
                "hint": "1 kg = 1000 gram"
            })
            item_id += 1

        # Perimeter
        for i in range(5):
            side = (i + 2) * 2
            perim = side * 4
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "omtrek",
                "question": {
                    "text": f"Een vierkant heeft zijden van {side} cm. Wat is de omtrek?"
                },
                "options": [
                    {"text": f"{side} cm"},
                    {"text": f"{side * 2} cm"},
                    {"text": f"{perim} cm"},
                    {"text": f"{side ** 2} cm"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 2
                },
                "hint": f"Omtrek vierkant = 4 × zijde = 4 × {side} = {perim} cm"
            })
            item_id += 1

        # 3D shapes
        shapes_3d = [("kubus", "vierkanten"), ("bol", "geen"), ("cilinder", "cirkels")]
        for shape, faces in shapes_3d:
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "ruimtefiguren",
                "question": {
                    "text": f"Welke vlakken heeft een {shape}?"
                },
                "options": [
                    {"text": "vierkanten"},
                    {"text": "cirkels"},
                    {"text": "driehoeken"},
                    {"text": "geen vlakken"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": ["vierkanten", "cirkels", "driehoeken", "geen"].index(faces) if faces in ["vierkanten", "cirkels", "driehoeken", "geen"] else 0
                },
                "hint": f"Denk aan de vorm van een {shape}"
            })
            item_id += 1

    # Grade 5+: Area, volume, angles
    elif grade >= 5:
        # Area of rectangle
        for i in range(10):
            length = (i + 2) * 3
            width = i + 2
            area = length * width
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "oppervlakte",
                "question": {
                    "text": f"Een rechthoek is {length} cm lang en {width} cm breed. Wat is de oppervlakte?"
                },
                "options": [
                    {"text": f"{area - 5} cm²"},
                    {"text": f"{area} cm²"},
                    {"text": f"{length + width} cm²"},
                    {"text": f"{area + 5} cm²"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 1
                },
                "hint": f"Oppervlakte = lengte × breedte = {length} × {width}"
            })
            item_id += 1

        # Volume (grade 6+)
        if grade >= 6:
            for i in range(8):
                side = i + 2
                volume = side ** 3
                items.append({
                    "id": item_id,
                    "type": "multiple_choice",
                    "theme": "volume",
                    "question": {
                        "text": f"Een kubus heeft zijden van {side} cm. Wat is de inhoud?"
                    },
                    "options": [
                        {"text": f"{volume - 5} cm³"},
                        {"text": f"{volume} cm³"},
                        {"text": f"{side * 6} cm³"},
                        {"text": f"{side ** 2} cm³"}
                    ],
                    "answer": {
                        "type": "single",
                        "correct_index": 1
                    },
                    "hint": f"Volume kubus = zijde³ = {side}³ = {volume} cm³"
                })
                item_id += 1

        # Angles (grade 6+)
        if grade >= 6:
            angle_types = [("90°", "rechte hoek"), ("45°", "scherpe hoek"), ("120°", "stompe hoek")]
            for angle, atype in angle_types:
                items.append({
                    "id": item_id,
                    "type": "multiple_choice",
                    "theme": "hoeken",
                    "question": {
                        "text": f"Een hoek van {angle} is een..."
                    },
                    "options": [
                        {"text": "scherpe hoek"},
                        {"text": "rechte hoek"},
                        {"text": "stompe hoek"},
                        {"text": "gestrekte hoek"}
                    ],
                    "answer": {
                        "type": "single",
                        "correct_index": ["scherpe hoek", "rechte hoek", "stompe hoek", "gestrekte hoek"].index(atype)
                    },
                    "hint": f"{angle} = {atype}"
                })
                item_id += 1

    # Ensure we have enough items
    while len(items) < count:
        items.append({
            "id": item_id,
            "type": "multiple_choice",
            "theme": "oefening",
            "question": {
                "text": f"Oefenvraag {item_id}: 100 cm = ... meter"
            },
            "options": [
                {"text": "0.1 m"},
                {"text": "1 m"},
                {"text": "10 m"},
                {"text": "100 m"}
            ],
            "answer": {
                "type": "single",
                "correct_index": 1
            },
            "hint": "100 cm = 1 meter"
        })
        item_id += 1

    return items[:count]


def create_support_item(item_id: int, theme: str, domain: str) -> Dict:
    """Generate support/learning data for an item"""

    # Base feedback structure
    feedback = {
        "correct": {
            "default": "Goed gedaan!",
            "on_first_try": "Uitstekend! Je hebt het meteen goed! 🎯",
            "after_hint": "Mooi! De hint heeft je geholpen."
        },
        "incorrect": {
            "first_attempt": "Nog niet helemaal. Probeer het nog eens.",
            "second_attempt": "Denk goed na. Wil je een hint?",
            "third_attempt": "Laten we samen kijken naar de vraag."
        },
        "explanation": {
            "text": "Het juiste antwoord is..."
        }
    }

    # Adaptive learning
    adaptive = {
        "if_correct_quickly": {
            "action": "increase_difficulty",
            "message": "Je bent hier goed in! Laten we het wat uitdagender maken."
        },
        "if_wrong_multiple": {
            "action": "decrease_difficulty",
            "message": "Laten we eerst wat makkelijkere vragen doen."
        }
    }

    # Domain-specific tips
    if domain == "verhoudingen":
        if "breuk" in theme or "fractie" in theme:
            tips = [
                "Denk aan een taart die je in stukken verdeelt",
                "De onderste getal (noemer) zegt in hoeveel stukken",
                "De bovenste getal (teller) zegt hoeveel stukken je hebt"
            ]
            skill = "Breuken begrijpen"
        elif "decimaal" in theme or "decimalen" in theme:
            tips = [
                "Decimalen zijn getallen met een komma",
                "0.5 is hetzelfde als 1/2",
                "Tel het aantal cijfers achter de komma"
            ]
            skill = "Decimale getallen"
        elif "procent" in theme:
            tips = [
                "Procent betekent 'per 100'",
                "50% = 50/100 = 1/2",
                "Om een percentage te berekenen: (deel × percentage) ÷ 100"
            ]
            skill = "Percentages berekenen"
        else:
            tips = ["Lees de vraag goed", "Denk na over wat je weet", "Probeer het stap voor stap"]
            skill = "Verhoudingen"

    elif domain == "meetkunde":
        if "lengte" in theme:
            tips = [
                "1 meter = 100 centimeter",
                "1 kilometer = 1000 meter",
                "Gebruik de juiste eenheid"
            ]
            skill = "Lengte meten"
        elif "oppervlakte" in theme or "area" in theme:
            tips = [
                "Oppervlakte rechthoek = lengte × breedte",
                "Antwoord in cm² of m²",
                "Vermenigvuldig de twee zijden"
            ]
            skill = "Oppervlakte berekenen"
        elif "volume" in theme or "inhoud" in theme:
            tips = [
                "Volume = lengte × breedte × hoogte",
                "Bij een kubus: zijde × zijde × zijde",
                "Antwoord in cm³ of m³"
            ]
            skill = "Volume berekenen"
        elif "hoek" in theme:
            tips = [
                "Rechte hoek = 90°",
                "Scherpe hoek < 90°",
                "Stompe hoek > 90° maar < 180°"
            ]
            skill = "Hoeken herkennen"
        else:
            tips = ["Gebruik de juiste formule", "Let op de eenheden", "Controleer je antwoord"]
            skill = "Meetkunde"
    else:
        tips = ["Lees de vraag goed", "Denk na over wat je weet", "Controleer je antwoord"]
        skill = "Rekenen"

    return {
        "item_id": item_id,
        "learning": {
            "tips": tips,
            "skill_description": skill,
            "reading_strategies": ["Lees de vraag aandachtig", "Onderstreep belangrijke getallen"],
            "common_errors": [
                {
                    "type": "rekenfouten",
                    "description": "Fout bij het rekenen",
                    "remedy": "Controleer je berekening stap voor stap"
                },
                {
                    "type": "verkeerde_bewerking",
                    "description": "Verkeerde rekenbewerking gekozen",
                    "remedy": "Lees goed wat er gevraagd wordt"
                }
            ]
        },
        "feedback": feedback,
        "adaptive": adaptive
    }


def generate_exercise(domain: str, grade: int, level: str):
    """Generate both core and support files for an exercise"""

    # Determine item count based on grade and level
    base_counts = {
        3: {"E3": 30, "M3": 35},
        4: {"E4": 40, "M4": 45},
        5: {"E5": 50, "M5": 55},
        6: {"E6": 60, "M6": 65},
        7: {"E7": 60, "M7": 65},
        8: {"E8": 70, "M8": 75}
    }
    item_count = base_counts[grade][level]

    # Generate items
    if domain == "verhoudingen":
        items = create_verhoudingen_items(grade, level, item_count)
        display_title = f"Breuken en Procenten Groep {grade}"
        instruction = "Kies het goede antwoord:"
    else:  # meetkunde
        items = create_meetkunde_items(grade, level, item_count)
        display_title = f"Meetkunde Groep {grade}"
        instruction = "Kies het goede antwoord:"

    # Create exercise ID
    exercise_id = f"gb_groep{grade}_{domain}_{level.lower()}"

    # Core JSON
    core = {
        "schema_version": "2.0.0",
        "metadata": {
            "id": exercise_id,
            "type": "multiple_choice",
            "category": "gb",
            "grade": grade,
            "level": level,
            "language": "nl-NL",
            "domain": domain,
            "slo_alignment": {
                "kerndoelen": ["K28", "K32", "K33"] if domain == "meetkunde" else ["K28", "R2"],
                "rekendomeinen": [domain],
                "tussendoelen": [f"{grade}R_{domain}_{level.lower()}"],
                "referentieniveau": "1F" if grade <= 6 else "1S",
                "cognitive_level": "toepassen"
            }
        },
        "display": {
            "title": display_title
        },
        "content": {
            "instruction": instruction
        },
        "items": items,
        "settings": {
            "allow_review": True
        }
    }

    # Support JSON
    support_items = []
    for item in items:
        support_items.append(create_support_item(
            item["id"],
            item.get("theme", "oefening"),
            domain
        ))

    support = {
        "schema_version": "2.0.0",
        "exercise_id": exercise_id,
        "items": support_items
    }

    return core, support


def main():
    """Generate all exercise files"""

    print("🚀 GB Exercise Generator - Starting...")
    print("=" * 60)

    # Create output directories if they don't exist
    for domain, output_dir in OUTPUT_DIRS.items():
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 Created directory: {output_dir}")

    # Skip grade 3 verhoudingen (already created manually)
    skip_verhoudingen_3 = False  # Regenerate to fix JSON issues

    total_files = 0

    # Generate Verhoudingen exercises
    print("\n📊 Generating VERHOUDINGEN exercises...")
    output_dir = OUTPUT_DIRS["verhoudingen"]
    for grade in range(3, 9):  # Grades 3-8
        for level in ["E", "M"]:
            level_code = f"{level}{grade}"

            # Skip grade 3 if already created
            if grade == 3 and skip_verhoudingen_3:
                print(f"  ⏭️  Groep {grade} {level_code} - SKIPPED (already exists)")
                continue

            core, support = generate_exercise("verhoudingen", grade, level_code)

            # Write core file
            core_filename = f"gb_groep{grade}_verhoudingen_{level_code.lower()}_core.json"
            core_path = os.path.join(output_dir, core_filename)
            with open(core_path, 'w', encoding='utf-8') as f:
                json.dump(core, f, ensure_ascii=False, indent=2)

            # Write support file
            support_filename = f"gb_groep{grade}_verhoudingen_{level_code.lower()}_support.json"
            support_path = os.path.join(output_dir, support_filename)
            with open(support_path, 'w', encoding='utf-8') as f:
                json.dump(support, f, ensure_ascii=False, indent=2)

            print(f"  ✅ Groep {grade} {level_code} - {len(core['items'])} items")
            total_files += 2

    # Generate Meetkunde exercises
    print("\n📐 Generating MEETKUNDE exercises...")
    output_dir = OUTPUT_DIRS["meetkunde"]
    for grade in range(3, 9):  # Grades 3-8
        for level in ["E", "M"]:
            level_code = f"{level}{grade}"

            core, support = generate_exercise("meetkunde", grade, level_code)

            # Write core file
            core_filename = f"gb_groep{grade}_meetkunde_{level_code.lower()}_core.json"
            core_path = os.path.join(output_dir, core_filename)
            with open(core_path, 'w', encoding='utf-8') as f:
                json.dump(core, f, ensure_ascii=False, indent=2)

            # Write support file
            support_filename = f"gb_groep{grade}_meetkunde_{level_code.lower()}_support.json"
            support_path = os.path.join(output_dir, support_filename)
            with open(support_path, 'w', encoding='utf-8') as f:
                json.dump(support, f, ensure_ascii=False, indent=2)

            print(f"  ✅ Groep {grade} {level_code} - {len(core['items'])} items")
            total_files += 2

    print("\n" + "=" * 60)
    print(f"✨ Generation complete! Created {total_files} files")
    print(f"📁 Verhoudingen: {OUTPUT_DIRS['verhoudingen']}")
    print(f"📁 Meetkunde: {OUTPUT_DIRS['meetkunde']}")
    print("\nNext steps:")
    print("  1. Update data-v2/exercises/index.json")
    print("  2. Test exercise loading")
    print("  3. Commit and push")


if __name__ == "__main__":
    main()
