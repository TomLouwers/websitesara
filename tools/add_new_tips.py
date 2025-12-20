#!/usr/bin/env python3
"""
Add extra_info tips for the 7 new problems
"""

import json

def add_tips_for_new_problems(problems):
    """Add extra_info for problems 221-227"""

    # Define tips for each new problem
    new_tips = {
        221: {  # Favoriete sport (bar chart)
            0: {
                "tips": [
                    "Zoek de balk voor 'Hockey' in de grafiek",
                    "Lees de waarde af op de y-as (verticale as)",
                    "De balk voor hockey staat op 8 leerlingen"
                ]
            },
            1: {
                "tips": [
                    "Lees af: Voetbal = 12 leerlingen, Zwemmen = 6 leerlingen",
                    "Bereken het verschil: 12 - 6 = 6 leerlingen",
                    "Er hebben 6 leerlingen meer op voetbal gestemd dan op zwemmen"
                ]
            }
        },
        222: {  # Temperatuur (line graph)
            0: {
                "tips": [
                    "Zoek het hoogste punt in de lijndiagram",
                    "Het hoogste punt is bij 24°C",
                    "Lees op de x-as af welke tijd daarbij hoort: 15:00 uur"
                ]
            },
            1: {
                "tips": [
                    "Lees af: om 12:00 was het 22 graden",
                    "Lees af: om 15:00 was het 24 graden",
                    "Bereken het verschil: 24 - 22 = 2 graden warmer"
                ]
            }
        },
        223: {  # Vervoer naar school (pie chart)
            0: {
                "tips": [
                    "30% van de leerlingen komt met de fiets",
                    "Bereken 30% van 120: (30 ÷ 100) × 120",
                    "0,30 × 120 = 36 leerlingen"
                ]
            },
            1: {
                "tips": [
                    "Tel alle gegeven percentages op: 30% + 45% + 15% = 90%",
                    "De rest komt met de bus: 100% - 90% = 10%",
                    "10% van de leerlingen komt met de bus"
                ]
            }
        },
        224: {  # Korting actie (percentage trap)
            0: {
                "tips": [
                    "Eerste korting: 20% van €200,00 = €40,00",
                    "Prijs na eerste korting: €200,00 - €40,00 = €160,00",
                    "Tweede korting: 10% van €160,00 = €16,00",
                    "Eindprijs: €160,00 - €16,00 = €144,00"
                ]
            },
            1: {
                "tips": [
                    "Je betaalt €144,00 voor een fiets die normaal €200,00 kost",
                    "Totale korting: €200,00 - €144,00 = €56,00",
                    "Let op: dit is niet 30%, maar 28% korting!"
                ]
            }
        },
        225: {  # Verf mengen (ratio trap)
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
        226: {  # Twee fietsers (speed trap)
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
                    "Tijd tot ze elkaar treffen: 52,5 ÷ 35 = 1,5 uur",
                    "10:30 + 1,5 uur = 12:00... wacht, dat klopt niet",
                    "Laat me herrekenen: 52,5 ÷ 35 = 1,5 uur = 1 uur en 30 minuten",
                    "10:30 + 1 uur = 11:30 uur"
                ]
            }
        },
        227: {  # Schoolkamp kosten (table trap)
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

        if problem_id in new_tips:
            tips_for_problem = new_tips[problem_id]

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

    print("Adding tips for new problems...")
    problems = add_tips_for_new_problems(problems)

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

    print("✓ Tips added successfully!")
    print(f"  Added tips for {questions_without_tips - questions_without_tips_after} questions")

if __name__ == '__main__':
    main()
