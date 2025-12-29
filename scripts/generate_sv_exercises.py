#!/usr/bin/env python3
"""
Studievaardigheden Exercise Generator
Generates exercises for study skills aligned with SLO goals and CITO requirements
"""

import json
import os
from typing import List, Dict, Any

# Output directory
OUTPUT_DIR = "data-v2/exercises/sv"

def create_studievaardigheden_items(grade: int, level: str, count: int) -> List[Dict]:
    """Generate Studievaardigheden (study skills) items"""
    items = []
    item_id = 1

    # Grade 3: Basic study habits
    if grade == 3:
        # Planning and organization
        for i in range(8):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "planning",
                "question": {
                    "text": "Je moet huiswerk maken en ook nog buiten spelen. Wat doe je het beste?"
                },
                "options": [
                    {"text": "Eerst huiswerk, dan spelen"},
                    {"text": "Eerst spelen, dan huiswerk"},
                    {"text": "Alleen spelen"},
                    {"text": "Huiswerk vergeten"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Plan je taken: eerst werk, dan plezier!"
            })
            item_id += 1

        # Concentration
        for i in range(7):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "concentratie",
                "question": {
                    "text": "Waar kun je het beste leren?"
                },
                "options": [
                    {"text": "In een rustige ruimte"},
                    {"text": "Voor de TV"},
                    {"text": "Met muziek heel hard"},
                    {"text": "Tijdens het spelen"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Een rustige plek helpt je om je beter te concentreren"
            })
            item_id += 1

        # Reading strategies
        for i in range(10):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "lezen",
                "question": {
                    "text": "Je moet een stuk lezen. Wat doe je eerst?"
                },
                "options": [
                    {"text": "Kijken naar de titel en plaatjes"},
                    {"text": "Meteen beginnen bij het eerste woord"},
                    {"text": "De laatste zin lezen"},
                    {"text": "Het boek dichtdoen"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Eerst de titel en plaatjes bekijken helpt je begrijpen waar het over gaat"
            })
            item_id += 1

        # Memory strategies
        for i in range(5):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "onthouden",
                "question": {
                    "text": "Hoe kun je woorden het beste onthouden?"
                },
                "options": [
                    {"text": "Meerdere keren oefenen"},
                    {"text": "Eén keer lezen"},
                    {"text": "Niet oefenen"},
                    {"text": "Alleen ernaar kijken"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Herhaling helpt je om dingen te onthouden"
            })
            item_id += 1

    # Grade 4: Planning and self-regulation
    elif grade == 4:
        # Time management
        for i in range(10):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "tijdplanning",
                "question": {
                    "text": "Je moet voor morgen een werkstuk maken. Wanneer begin je?"
                },
                "options": [
                    {"text": "Vandaag al beginnen"},
                    {"text": "Vanavond laat"},
                    {"text": "Morgenochtend vroeg"},
                    {"text": "Helemaal niet"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Op tijd beginnen voorkomt stress"
            })
            item_id += 1

        # Note-taking
        for i in range(8):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "notities",
                "question": {
                    "text": "Wat is handig om te doen tijdens het lezen van een tekst?"
                },
                "options": [
                    {"text": "Belangrijke woorden onderstrepen"},
                    {"text": "Niets opschrijven"},
                    {"text": "Alles uit je hoofd leren"},
                    {"text": "De tekst meteen wegleggen"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Onderstrepen helpt je de belangrijkste informatie te vinden"
            })
            item_id += 1

        # Learning strategies
        for i in range(12):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "leerstrategieen",
                "question": {
                    "text": "Je snapt iets niet uit de les. Wat doe je?"
                },
                "options": [
                    {"text": "Vragen aan de juf of meester"},
                    {"text": "Het negeren"},
                    {"text": "Doen alsof je het snapt"},
                    {"text": "Stoppen met leren"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Vragen stellen helpt je om het te begrijpen"
            })
            item_id += 1

        # Self-assessment
        for i in range(10):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "zelfevaluatie",
                "question": {
                    "text": "Na het maken van een oefening, wat doe je?"
                },
                "options": [
                    {"text": "Nakijken of het goed is"},
                    {"text": "Meteen inleveren"},
                    {"text": "Niet controleren"},
                    {"text": "Het weggooien"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Controleren helpt je fouten te vinden en te verbeteren"
            })
            item_id += 1

    # Grades 5-6: Advanced study skills
    elif grade in [5, 6]:
        # Information processing
        for i in range(12):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "informatieverwerking",
                "question": {
                    "text": "Je leest een lange tekst over dieren. Hoe verwerk je de informatie?"
                },
                "options": [
                    {"text": "Kernwoorden opschrijven en een samenvatting maken"},
                    {"text": "Alles letterlijk uit je hoofd leren"},
                    {"text": "Alleen de eerste alinea lezen"},
                    {"text": "De tekst één keer doorlezen"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Kernwoorden en samenvattingen helpen je informatie te onthouden"
            })
            item_id += 1

        # Mindmapping
        for i in range(8):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "mindmap",
                "question": {
                    "text": "Een mindmap is handig om:"
                },
                "options": [
                    {"text": "Ideeën overzichtelijk te ordenen"},
                    {"text": "Te tekenen tijdens de les"},
                    {"text": "Tijd te vullen"},
                    {"text": "Je huiswerk te versieren"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Een mindmap helpt je verbanden te zien tussen verschillende onderwerpen"
            })
            item_id += 1

        # Test preparation
        for i in range(15):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "toetsvoorbereiding",
                "question": {
                    "text": "De toets is over een week. Hoe bereid je je voor?"
                },
                "options": [
                    {"text": "Elke dag een beetje oefenen"},
                    {"text": "De avond ervoor alles leren"},
                    {"text": "Helemaal niet voorbereiden"},
                    {"text": "Alleen de dag zelf oefenen"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Spreiding in je oefentijd geeft betere resultaten"
            })
            item_id += 1

        # Critical thinking
        for i in range(15):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "kritisch-denken",
                "question": {
                    "text": "Je vindt informatie op internet. Wat doe je?"
                },
                "options": [
                    {"text": "Controleren of de bron betrouwbaar is"},
                    {"text": "Alles meteen geloven"},
                    {"text": "De eerste zin kopiëren"},
                    {"text": "Niets lezen"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Niet alle informatie op internet is betrouwbaar"
            })
            item_id += 1

    # Grades 7-8: CITO preparation and advanced skills
    elif grade in [7, 8]:
        # CITO strategies
        for i in range(15):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "cito-strategieen",
                "question": {
                    "text": "Bij een meerkeuzevraag weet je het antwoord niet. Wat doe je?"
                },
                "options": [
                    {"text": "Onzekere antwoorden wegstrepen en kiezen uit wat overblijft"},
                    {"text": "Willekeurig een antwoord kiezen"},
                    {"text": "De vraag overslaan en vergeten"},
                    {"text": "Gokken zonder na te denken"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Elimineren van foute antwoorden vergroot je kans op succes"
            })
            item_id += 1

        # Time management during tests
        for i in range(12):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "tijdbeheer-toets",
                "question": {
                    "text": "Je hebt 60 minuten voor 30 vragen. Hoeveel tijd per vraag?"
                },
                "options": [
                    {"text": "Ongeveer 2 minuten per vraag"},
                    {"text": "5 minuten per vraag"},
                    {"text": "Alle tijd aan de eerste 5 vragen"},
                    {"text": "Geen plan maken"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Verdeel je tijd: 60 minuten ÷ 30 vragen = 2 minuten per vraag"
            })
            item_id += 1

        # Reading comprehension strategies
        for i in range(15):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "leesvaardigheid",
                "question": {
                    "text": "Bij begrijpend lezen is het handig om:"
                },
                "options": [
                    {"text": "Eerst de vragen lezen, dan de tekst"},
                    {"text": "Meteen de tekst van begin tot eind lezen"},
                    {"text": "Alleen de titel lezen"},
                    {"text": "De tekst overslaan"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "De vragen eerst lezen helpt je te weten waar je op moet letten"
            })
            item_id += 1

        # Stress management
        for i in range(10):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "stressmanagement",
                "question": {
                    "text": "Je bent zenuwachtig voor een toets. Wat helpt?"
                },
                "options": [
                    {"text": "Rustig ademhalen en positief denken"},
                    {"text": "In paniek raken"},
                    {"text": "Niet naar de toets gaan"},
                    {"text": "Je zorgen maken"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "Rustig ademhalen kalmeert je lichaam en geest"
            })
            item_id += 1

        # Goal setting
        for i in range(8):
            items.append({
                "id": item_id,
                "type": "multiple_choice",
                "theme": "doelen-stellen",
                "question": {
                    "text": "Een goed leerdoel is:"
                },
                "options": [
                    {"text": "Specifiek en haalbaar"},
                    {"text": "Vaag en onduidelijk"},
                    {"text": "Onmogelijk moeilijk"},
                    {"text": "Niet belangrijk"}
                ],
                "answer": {
                    "type": "single",
                    "correct_index": 0
                },
                "hint": "SMART doelen (Specifiek, Meetbaar, Acceptabel, Realistisch, Tijdgebonden) werken het beste"
            })
            item_id += 1

    # Ensure we have enough items
    while len(items) < count:
        items.append({
            "id": item_id,
            "type": "multiple_choice",
            "theme": "algemeen",
            "question": {
                "text": "Wat is een goede studiegewoonte?"
            },
            "options": [
                {"text": "Regelmatig oefenen en herhalen"},
                {"text": "Alles op het laatste moment doen"},
                {"text": "Niet oefenen"},
                {"text": "Alleen maar spelen"}
            ],
            "answer": {
                "type": "single",
                "correct_index": 0
            },
            "hint": "Goede gewoontes bouwen zich op door regelmatige oefening"
        })
        item_id += 1

    return items[:count]


def create_support_item(item_id: int, theme: str) -> Dict:
    """Generate support/learning data for an item"""

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

    # Theme-specific tips
    theme_tips = {
        "planning": [
            "Maak een to-do lijstje voor je taken",
            "Plan moeilijke taken als je nog fris bent",
            "Verdeel grote taken in kleinere stukjes"
        ],
        "concentratie": [
            "Zorg voor een rustige werkplek",
            "Zet je telefoon weg tijdens het leren",
            "Neem pauzes om je concentratie te behouden"
        ],
        "lezen": [
            "Kijk eerst naar titels en tussenkopjes",
            "Stel jezelf vragen over de tekst",
            "Lees actief door aantekeningen te maken"
        ],
        "onthouden": [
            "Herhaling is de sleutel tot onthouden",
            "Maak ezelsbruggetjes voor moeilijke woorden",
            "Test jezelf regelmatig"
        ],
        "tijdplanning": [
            "Begin op tijd met je huiswerk",
            "Maak een planning voor langere opdrachten",
            "Reserveer tijd voor herhaling"
        ],
        "notities": [
            "Schrijf kernwoorden op, niet hele zinnen",
            "Gebruik je eigen woorden",
            "Maak gebruik van symbolen en tekeningen"
        ]
    }

    tips = theme_tips.get(theme, [
        "Oefen regelmatig",
        "Vraag om hulp als je het niet snapt",
        "Blijf positief en gemotiveerd"
    ])

    skill_descriptions = {
        "planning": "Planning en organisatie",
        "concentratie": "Concentratie en focus",
        "lezen": "Leesstrategieën",
        "onthouden": "Geheugenstrategieën",
        "tijdplanning": "Tijdmanagement",
        "notities": "Notities maken",
        "leerstrategieen": "Leerstrategieën",
        "zelfevaluatie": "Zelfreflectie",
        "informatieverwerking": "Informatie verwerken",
        "mindmap": "Mindmapping",
        "toetsvoorbereiding": "Toetsvoorbereiding",
        "kritisch-denken": "Kritisch denken",
        "cito-strategieen": "CITO-strategieën",
        "tijdbeheer-toets": "Tijdbeheer tijdens toetsen",
        "leesvaardigheid": "Leesvaardigheid",
        "stressmanagement": "Stress management",
        "doelen-stellen": "Doelen stellen"
    }

    skill = skill_descriptions.get(theme, "Studievaardigheden")

    return {
        "item_id": item_id,
        "learning": {
            "tips": tips,
            "skill_description": skill,
            "reading_strategies": ["Lees de vraag aandachtig", "Denk na over wat je al weet"],
            "common_errors": [
                {
                    "type": "overhaast",
                    "description": "Te snel geantwoord zonder na te denken",
                    "remedy": "Neem de tijd om de vraag goed te lezen"
                },
                {
                    "type": "strategie",
                    "description": "Geen goede strategie toegepast",
                    "remedy": "Gebruik de tips om een betere aanpak te kiezen"
                }
            ]
        },
        "feedback": feedback,
        "adaptive": adaptive
    }


def generate_exercise(grade: int, level: str):
    """Generate both core and support files for an exercise"""

    # Determine item count based on grade and level
    base_counts = {
        3: {"E3": 30, "M3": 35},
        4: {"E4": 40, "M4": 45},
        5: {"E5": 50, "M5": 55},
        6: {"E6": 55, "M6": 60},
        7: {"E7": 60, "M7": 65},
        8: {"E8": 65, "M8": 70}
    }
    item_count = base_counts[grade][level]

    # Generate items
    items = create_studievaardigheden_items(grade, level, item_count)
    display_title = f"Studievaardigheden Groep {grade}"
    instruction = "Kies het beste antwoord:"

    # Create exercise ID
    exercise_id = f"sv_groep{grade}_{level.lower()}"

    # Determine SLO alignment based on grade
    if grade <= 4:
        kerndoelen = ["K1", "K2"]  # Leren leren
        cognitive_level = "begrijpen"
    elif grade <= 6:
        kerndoelen = ["K1", "K2", "K3"]  # Leren leren + informatievaardigheden
        cognitive_level = "toepassen"
    else:
        kerndoelen = ["K1", "K2", "K3", "K4"]  # Full range including critical thinking
        cognitive_level = "analyseren"

    # Core JSON
    core = {
        "schema_version": "2.0.0",
        "metadata": {
            "id": exercise_id,
            "type": "multiple_choice",
            "category": "sv",
            "grade": grade,
            "level": level,
            "language": "nl-NL",
            "domain": "studievaardigheden",
            "slo_alignment": {
                "kerndoelen": kerndoelen,
                "domeinen": ["leren-leren", "informatievaardigheden"],
                "tussendoelen": [f"{grade}S_studievaardigheden_{level.lower()}"],
                "referentieniveau": "1F" if grade <= 6 else "1S",
                "cognitive_level": cognitive_level,
                "cito_relevant": True if grade >= 7 else False
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
            item.get("theme", "algemeen")
        ))

    support = {
        "schema_version": "2.0.0",
        "exercise_id": exercise_id,
        "items": support_items
    }

    return core, support


def main():
    """Generate all studievaardigheden exercise files"""

    print("🎓 Studievaardigheden Exercise Generator - Starting...")
    print("=" * 60)

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"📁 Created directory: {OUTPUT_DIR}")

    total_files = 0

    # Generate Studievaardigheden exercises for all grades
    print("\n📚 Generating STUDIEVAARDIGHEDEN exercises...")
    for grade in range(3, 9):  # Grades 3-8
        for level in ["E", "M"]:
            level_code = f"{level}{grade}"

            core, support = generate_exercise(grade, level_code)

            # Write core file
            core_filename = f"sv_groep{grade}_{level_code.lower()}_core.json"
            core_path = os.path.join(OUTPUT_DIR, core_filename)
            with open(core_path, 'w', encoding='utf-8') as f:
                json.dump(core, f, ensure_ascii=False, indent=2)

            # Write support file
            support_filename = f"sv_groep{grade}_{level_code.lower()}_support.json"
            support_path = os.path.join(OUTPUT_DIR, support_filename)
            with open(support_path, 'w', encoding='utf-8') as f:
                json.dump(support, f, ensure_ascii=False, indent=2)

            print(f"  ✅ Groep {grade} {level_code} - {len(core['items'])} items")
            total_files += 2

    print("\n" + "=" * 60)
    print(f"✨ Generation complete! Created {total_files} files")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print("\nNext steps:")
    print("  1. Add to level-selector.html")
    print("  2. Add file mappings to app.js")
    print("  3. Update config.js")
    print("  4. Minify and commit")


if __name__ == "__main__":
    main()
