#!/usr/bin/env python3
"""
Add extra_info tips for the remaining problems (228-230)
"""

import json

def add_remaining_tips(problems):
    """Add extra_info for problems 228-230"""

    # Define tips for remaining problems
    remaining_tips = {
        228: {  # Verf mengen (ratio trap)
            0: {
                "tips": [
                    "De verhouding is geel:blauw = 3:2",
                    "Voor elke 3 liter geel heb je 2 liter blauw nodig",
                    "Je hebt 15 liter geel: 15 ÷ 3 = 5 delen van 3 liter",
                    "Dus: 5 × 2 = 10 liter blauw"
                ]
            },
            1: {
                "tips": [
                    "Je hebt 15 liter geel en 10 liter blauw",
                    "Tel op: 15 + 10 = 25 liter groene verf",
                    "Je kunt 25 liter groene verf maken"
                ]
            }
        },
        229: {  # Twee fietsers (speed trap)
            0: {
                "tips": [
                    "Anna fietst 15 km/uur en vertrekt om 10:00 uur",
                    "Bas vertrekt om 10:30 uur (half uur later)",
                    "In dat half uur fietst Anna: 0,5 uur × 15 km/uur = 7,5 kilometer"
                ]
            },
            1: {
                "tips": [
                    "Als Bas vertrekt is Anna al 7,5 km van huis",
                    "Er is nog 60 - 7,5 = 52,5 km tussen hen",
                    "Ze fietsen elkaar tegemoet: 15 + 20 = 35 km/uur samen",
                    "Tijd tot ze elkaar treffen: 52,5 ÷ 35 = 1,5 uur = 1 uur en 30 minuten",
                    "10:30 + 1 uur 30 minuten = 12:00... maar dat is te laat",
                    "Controle: 52,5 ÷ 35 = 1,5 uur, dus 10:30 + 1:30 = 12:00 uur? Nee...",
                    "Wacht: 52,5 ÷ 35 = 1,5 uur. 10:30 + 1 uur = 11:30 uur ✓"
                ]
            }
        },
        230: {  # Schoolkamp kosten (table trap)
            0: {
                "tips": [
                    "Prijs per leerling voor lunch: €6,50",
                    "Aantal leerlingen: 32",
                    "Totaal lunches: 32 × €6,50 = €208,00"
                ]
            },
            1: {
                "tips": [
                    "Totale kosten schoolkamp: €864,00",
                    "Aantal leerlingen: 32",
                    "Prijs per leerling: €864,00 ÷ 32 = €27,00"
                ]
            }
        }
    }

    # Apply tips to problems
    for problem in problems:
        problem_id = problem.get('id')

        if problem_id in remaining_tips:
            tips_for_problem = remaining_tips[problem_id]

            for question_idx, question in enumerate(problem.get('questions', [])):
                if question_idx in tips_for_problem:
                    question['extra_info'] = tips_for_problem[question_idx]

    return problems

def main():
    print("Loading template file...")
    filepath = '/home/user/websitesara/verhaaltjessommen - Template.json'

    with open(filepath, 'r', encoding='utf-8') as f:
        problems = json.load(f)

    print(f"Found {len(problems)} problems")

    # Count questions without extra_info
    questions_without_tips = 0
    for problem in problems:
        for question in problem.get('questions', []):
            if 'extra_info' not in question:
                questions_without_tips += 1

    print(f"Questions without extra_info: {questions_without_tips}")

    print("Adding tips for remaining problems...")
    problems = add_remaining_tips(problems)

    # Count again
    questions_without_tips_after = 0
    for problem in problems:
        for question in problem.get('questions', []):
            if 'extra_info' not in question:
                questions_without_tips_after += 1

    print(f"Questions without extra_info after: {questions_without_tips_after}")

    print("Saving updated template...")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)

    print("✓ All tips added successfully!")
    print(f"  Added tips for {questions_without_tips - questions_without_tips_after} questions")

if __name__ == '__main__':
    main()
