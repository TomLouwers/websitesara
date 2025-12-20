#!/usr/bin/env python3
"""
Script to improve verhaaltjessommen - Template.json according to CITO-style guidelines
"""

import json
import re
import copy

def load_json(filepath):
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    """Save JSON file with proper formatting"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def simplify_extra_info(problem):
    """
    Improvement 1: Remove or simplify extra_info sections
    CITO doesn't give hints/tips during tests
    """
    for question in problem.get('questions', []):
        if 'extra_info' in question:
            # Remove tips completely for test simulation
            del question['extra_info']
    return problem

def reduce_context(problem):
    """
    Improvement 2: Reduce unnecessary context
    Keep only essential information
    """
    content = problem.get('content', '')

    # Patterns that indicate verbose context
    verbose_patterns = [
        r'Hiervan is ',
        r'Ook ',
        r'Vorige week ',
        r'Halverwege ',
    ]

    # This is a gentle optimization - we'll focus on specific cases
    # For now, just ensure content is concise
    if len(content) > 200:
        # Flag for manual review if needed
        pass

    return problem

def fix_impossible_answers(problem):
    """
    Improvement 3: Fix physically impossible answers like "4,5 eieren"
    CITO avoids half eggs, half people, etc.
    """
    # Check if this is the "Taart bakken" problem with eggs
    if 'eieren' in problem.get('content', '').lower():
        for question in problem.get('questions', []):
            if 'eieren' in question.get('question', '').lower():
                # Change the question to ask about calculation instead
                if '4,5' in str(question.get('options', [])):
                    # Fix: Change to ask about the calculation result
                    question['question'] = 'Hoeveel keer moet Lisa alle hoeveelheden vermenigvuldigen?'
                    question['options'] = ['1,2 keer', '1,5 keer', '2 keer', '2,5 keer']
                    question['correct'] = 1

    return problem

def standardize_notation(problem):
    """
    Improvement 4 & 5: Standardize answer notation and rounding
    - Always use comma for decimals
    - Always use € for currency
    - Round to 1 decimal where needed
    """
    for question in problem.get('questions', []):
        options = question.get('options', [])
        standardized_options = []

        for option in options:
            # Replace periods with commas in decimal numbers
            # But be careful with thousands separators
            standardized = option

            # Fix decimal notation: 35.8 -> 35,8
            standardized = re.sub(r'(\d)\.(\d)', r'\1,\2', standardized)

            # Ensure currency always has € symbol
            if re.search(r'\d+,?\d*\s*euro', standardized, re.IGNORECASE):
                standardized = re.sub(r'(\d+,?\d*)\s*euro', r'€\1', standardized, flags=re.IGNORECASE)

            # Apply rounding to 1 decimal for numbers with more decimals
            match = re.search(r'€?(\d+),(\d{2,})', standardized)
            if match:
                integer_part = match.group(1)
                decimal_part = match.group(2)
                # Round to 1 decimal if there are 2+ decimals
                if len(decimal_part) >= 2:
                    rounded_decimal = str(round(int(decimal_part[0:2]) / 10))
                    if '€' in standardized:
                        standardized = re.sub(r'€(\d+),\d+', f'€{integer_part},{rounded_decimal}', standardized)
                    else:
                        standardized = re.sub(r'(\d+),\d+', f'{integer_part},{rounded_decimal}', standardized)

            standardized_options.append(standardized)

        question['options'] = standardized_options

    return problem

def simplify_questions(problem):
    """
    Improvement 6: Simplify multi-step questions
    CITO measures usually one thinking step per question
    """
    # This is complex and requires case-by-case analysis
    # For now, we'll flag questions that might be too complex
    for question in problem.get('questions', []):
        question_text = question.get('question', '')
        # Questions with "eerst... dan..." or multiple operations might be too complex
        if 'eerst' in question_text.lower() or 'dan' in question_text.lower():
            # Flag for potential simplification
            pass

    return problem

def add_graph_variety(problems):
    """
    Improvement 7: Add variety in graph types
    Currently only tables - add bar charts, line graphs, pie charts
    """
    new_problems = []

    # Add a bar chart problem
    bar_chart_problem = {
        "id": len(problems) + 1,
        "title": "Favoriete sport",
        "theme": "gegevensverwerking",
        "content": "De leerlingen van groep 8 hebben gestemd op hun favoriete sport.",
        "graph_type": "bar_chart",
        "graph_data": {
            "title": "Favoriete sport groep 8",
            "x_label": "Sport",
            "y_label": "Aantal leerlingen",
            "bars": [
                {"label": "Voetbal", "value": 12},
                {"label": "Hockey", "value": 8},
                {"label": "Zwemmen", "value": 6},
                {"label": "Turnen", "value": 4}
            ]
        },
        "questions": [
            {
                "question": "Hoeveel leerlingen hebben op hockey gestemd?",
                "options": ["4 leerlingen", "6 leerlingen", "8 leerlingen", "12 leerlingen"],
                "correct": 2
            },
            {
                "question": "Hoeveel leerlingen meer hebben op voetbal gestemd dan op zwemmen?",
                "options": ["2 leerlingen", "4 leerlingen", "6 leerlingen", "8 leerlingen"],
                "correct": 2
            }
        ]
    }
    new_problems.append(bar_chart_problem)

    # Add a line graph problem
    line_graph_problem = {
        "id": len(problems) + 2,
        "title": "Temperatuur",
        "theme": "gegevensverwerking",
        "content": "De grafiek toont de temperatuur gedurende één dag.",
        "graph_type": "line_graph",
        "graph_data": {
            "title": "Temperatuur op 15 juni",
            "x_label": "Tijd",
            "y_label": "Temperatuur (°C)",
            "points": [
                {"x": "06:00", "y": 12},
                {"x": "09:00", "y": 16},
                {"x": "12:00", "y": 22},
                {"x": "15:00", "y": 24},
                {"x": "18:00", "y": 20},
                {"x": "21:00", "y": 16}
            ]
        },
        "questions": [
            {
                "question": "Hoe laat was het het warmst?",
                "options": ["09:00 uur", "12:00 uur", "15:00 uur", "18:00 uur"],
                "correct": 2
            },
            {
                "question": "Hoeveel graden is het tussen 12:00 en 15:00 warmer geworden?",
                "options": ["2 graden", "4 graden", "6 graden", "8 graden"],
                "correct": 0
            }
        ]
    }
    new_problems.append(line_graph_problem)

    # Add a pie chart problem
    pie_chart_problem = {
        "id": len(problems) + 3,
        "title": "Vervoer naar school",
        "theme": "gegevensverwerking",
        "content": "Van de 120 leerlingen komen er 30% met de fiets, 45% lopend, 15% met de auto en de rest met de bus.",
        "graph_type": "pie_chart",
        "graph_data": {
            "title": "Vervoer naar school",
            "segments": [
                {"label": "Fiets", "percentage": 30, "color": "blue"},
                {"label": "Lopend", "percentage": 45, "color": "green"},
                {"label": "Auto", "percentage": 15, "color": "red"},
                {"label": "Bus", "percentage": 10, "color": "yellow"}
            ]
        },
        "questions": [
            {
                "question": "Hoeveel leerlingen komen met de fiets?",
                "options": ["30 leerlingen", "36 leerlingen", "45 leerlingen", "54 leerlingen"],
                "correct": 1
            },
            {
                "question": "Hoeveel procent van de leerlingen komt met de bus?",
                "options": ["5%", "10%", "15%", "20%"],
                "correct": 1
            }
        ]
    }
    new_problems.append(pie_chart_problem)

    return new_problems

def add_trap_questions(problems):
    """
    Improvement 8: Add trap questions
    - Percentage of percentage
    - Ratio reversal
    - Speed + time combinations
    - Tables with missing values
    """
    new_problems = []

    # Trap 1: Percentage of percentage
    percentage_trap = {
        "id": len(problems) + 4,
        "title": "Korting actie",
        "theme": "procenten",
        "content": "Een winkel geeft 20% korting. Met een klantenkaart krijg je nog eens 10% extra korting op de al verlaagde prijs. Een fiets kost normaal €200,00.",
        "questions": [
            {
                "question": "Hoeveel betaal je voor de fiets met de klantenkaart?",
                "options": ["€140,00", "€144,00", "€156,00", "€160,00"],
                "correct": 1
            },
            {
                "question": "Hoeveel korting krijg je in totaal?",
                "options": ["€28,00", "€30,00", "€44,00", "€56,00"],
                "correct": 2
            }
        ]
    }
    new_problems.append(percentage_trap)

    # Trap 2: Ratio reversal
    ratio_trap = {
        "id": len(problems) + 5,
        "title": "Verf mengen",
        "theme": "verhoudingen",
        "content": "Om groene verf te maken meng je gele en blauwe verf in de verhouding 3:2. Je hebt 15 liter gele verf.",
        "questions": [
            {
                "question": "Hoeveel liter blauwe verf heb je nodig?",
                "options": ["6 liter", "10 liter", "12 liter", "22,5 liter"],
                "correct": 1
            },
            {
                "question": "Hoeveel liter groene verf kun je maken?",
                "options": ["17 liter", "20 liter", "25 liter", "30 liter"],
                "correct": 2
            }
        ]
    }
    new_problems.append(ratio_trap)

    # Trap 3: Speed + time combination
    speed_trap = {
        "id": len(problems) + 6,
        "title": "Twee fietsers",
        "theme": "snelheid-afstand-tijd",
        "content": "Anna en Bas fietsen elkaar tegemoet. Anna vertrekt om 10:00 uur en fietst 15 km/uur. Bas vertrekt om 10:30 uur en fietst 20 km/uur. De afstand tussen hun huizen is 60 kilometer.",
        "questions": [
            {
                "question": "Hoeveel kilometer heeft Anna afgelegd als Bas vertrekt?",
                "options": ["7,5 kilometer", "10 kilometer", "15 kilometer", "20 kilometer"],
                "correct": 0
            },
            {
                "question": "Hoe laat komen ze elkaar tegen?",
                "options": ["11:00 uur", "11:15 uur", "11:30 uur", "12:00 uur"],
                "correct": 2
            }
        ]
    }
    new_problems.append(speed_trap)

    # Trap 4: Table with missing value
    table_trap = {
        "id": len(problems) + 7,
        "title": "Schoolkamp kosten",
        "theme": "geld",
        "content": "De tabel toont de kosten voor het schoolkamp.",
        "table": {
            "headers": ["Item", "Prijs per leerling", "Aantal leerlingen", "Totaal"],
            "rows": [
                ["Bus", "€8,50", "32", "€272,00"],
                ["Activiteiten", "€12,00", "32", "€384,00"],
                ["Lunch", "€6,50", "32", "?"],
                ["Totaal", "", "", "€864,00"]
            ]
        },
        "questions": [
            {
                "question": "Hoeveel kosten de lunches in totaal?",
                "options": ["€192,00", "€198,00", "€208,00", "€216,00"],
                "correct": 2
            },
            {
                "question": "Hoeveel betaalt één leerling voor het hele schoolkamp?",
                "options": ["€25,00", "€27,00", "€29,00", "€32,00"],
                "correct": 1
            }
        ]
    }
    new_problems.append(table_trap)

    return new_problems

def improve_table_formatting(problem):
    """
    Improvement 5 (from original list): Improve table formatting
    Use full column headers as CITO does
    """
    if 'table' in problem:
        table = problem['table']
        # Ensure headers are descriptive
        headers = table.get('headers', [])

        # Common abbreviations to expand
        expansions = {
            'nr': 'Nummer',
            'Nr': 'Nummer',
            'max': 'Maximaal',
            'Min': 'Minimaal',
            'gem': 'Gemiddelde',
            'tot': 'Totaal'
        }

        expanded_headers = []
        for header in headers:
            expanded = header
            for abbrev, full in expansions.items():
                if header.strip() == abbrev or header.strip() == abbrev + '.':
                    expanded = full
            expanded_headers.append(expanded)

        table['headers'] = expanded_headers

    return problem

def main():
    """Main processing function"""
    print("Loading template file...")
    filepath = '/home/user/websitesara/verhaaltjessommen - Template.json'
    problems = load_json(filepath)

    print(f"Found {len(problems)} problems")
    print("\nApplying improvements...")

    # Apply improvements to existing problems
    improved_problems = []
    for i, problem in enumerate(problems, 1):
        print(f"  Processing problem {i}/{len(problems)}: {problem.get('title', 'Untitled')}")

        problem = simplify_extra_info(problem)
        problem = reduce_context(problem)
        problem = fix_impossible_answers(problem)
        problem = standardize_notation(problem)
        problem = simplify_questions(problem)
        problem = improve_table_formatting(problem)

        improved_problems.append(problem)

    # Add new problems with graph variety
    print("\nAdding problems with graph variety...")
    graph_problems = add_graph_variety(improved_problems)
    improved_problems.extend(graph_problems)

    # Add trap questions
    print("Adding trap questions...")
    trap_problems = add_trap_questions(improved_problems)
    improved_problems.extend(trap_problems)

    print(f"\nTotal problems after improvements: {len(improved_problems)}")

    # Save improved version
    output_filepath = filepath
    print(f"\nSaving to {output_filepath}...")
    save_json(output_filepath, improved_problems)

    print("✓ Improvements complete!")
    print("\nSummary of changes:")
    print("  • Removed all extra_info tips/hints")
    print("  • Fixed physically impossible answers (like 4.5 eggs)")
    print("  • Standardized notation (commas for decimals, € for currency)")
    print("  • Applied consistent rounding rules")
    print("  • Improved table formatting")
    print(f"  • Added {len(graph_problems)} new problems with graph variety")
    print(f"  • Added {len(trap_problems)} trap questions")

if __name__ == '__main__':
    main()
