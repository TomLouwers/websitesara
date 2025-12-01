#!/usr/bin/env python3
"""
Add Remaining 7 Complex Multi-Step M4 Problems
"""

import json

with open('verhaaltjessommen-emma - Template.json', 'r') as f:
    data = json.load(f)

print("🔧 ADDING 7 MORE COMPLEX PROBLEMS\n")

additional_problems = [
    # Problem 41: Delen met redeneren
    {
        "id": 41,
        "title": "Koekjes verdelen",
        "theme": "delen",
        "content": "De juf heeft 2 pakken koekjes. In elk pak zitten 10 koekjes. Ze wil ze eerlijk verdelen over 4 kinderen.",
        "questions": [{
            "question": "Hoeveel koekjes krijgt elk kind?",
            "hint": "💡 Tip: Hoeveel koekjes zijn er in totaal? Over hoeveel kinderen?",
            "options": [
                {
                    "text": "2 koekjes",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt alleen het aantal pakken (2) gedeeld door het aantal kinderen (4), maar vergeten dat in elk pak 10 koekjes zitten!\n\n🤔 **Reflectievraag:** Hoeveel koekjes zijn er in totaal in 2 pakken?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "10 koekjes",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Dat is het aantal koekjes in één pak, niet per kind. Bereken eerst het totaal (2 × 10 = 20), dan verdelen (20 ÷ 4).\n\n🤔 **Reflectievraag:** Hoeveel kinderen krijgen koekjes?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "8 koekjes",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Je hebt misschien 2 × 4 = 8 uitgerekend, maar dat klopt niet. Eerst vermenigvuldigen: 2 × 10 = 20 koekjes totaal. Dan delen: 20 ÷ 4 = 5.\n\n🤔 **Reflectievraag:** Welke bewerkingen moet je doen?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 103
                },
                {
                    "text": "5 koekjes",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een meerstapsopgave: eerst vermenigvuldigen om het totaal te weten, dan delen.",
                "berekening": ["Stap 1: 2 × 10 = 20 koekjes totaal", "Stap 2: 20 ÷ 4 = 5 koekjes per kind"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Bereken totaal koekjes | 2 × 10 | **20 koekjes** |",
                    "| 2. Verdeel over kinderen | 20 ÷ 4 | **5 koekjes** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": [],
                    "hoofdvraag": "Hoeveel koekjes krijgt elk kind?",
                    "tussenstappen": ["Bereken totaal aantal koekjes", "Verdeel eerlijk over 4 kinderen"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Aantal pakken": "2",
                        "Koekjes per pak": "10",
                        "Aantal kinderen": "4"
                    },
                    "tool": "Vermenigvuldigen en delen",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Bereken totaal",
                            "berekening": "2 × 10",
                            "resultaat": "20 koekjes",
                            "uitleg": "2 pakken met elk 10 koekjes is 20 koekjes"
                        },
                        {
                            "stap": "Verdeel eerlijk",
                            "berekening": "20 ÷ 4",
                            "resultaat": "5 koekjes",
                            "uitleg": "20 koekjes eerlijk verdelen over 4 kinderen"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "koekjes",
                    "logica_check": "5 koekjes is logisch: 2 × 10 ÷ 4 = 5",
                    "antwoord": "5 koekjes"
                }
            }
        }],
        "sub_theme": "vermenigvuldigen en delen combineren"
    },

    # Problem 42: Lengte met vergelijken
    {
        "id": 42,
        "title": "Wie is het langst?",
        "theme": "lengte",
        "content": "Tim is 125 cm lang. Lisa is 15 cm langer dan Tim. Jamal is 10 cm korter dan Lisa.",
        "questions": [{
            "question": "Hoe lang is Jamal?",
            "hint": "💡 Tip: Hoe lang is Lisa eerst? En dan Jamal?",
            "options": [
                {
                    "text": "115 cm",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Je hebt 125 - 10 = 115 gerekend, maar Jamal is 10 cm korter dan Lisa, niet dan Tim! Bereken eerst Lisa's lengte: 125 + 15 = 140. Dan Jamal: 140 - 10 = 130.\n\n🤔 **Reflectievraag:** Met wie moet je Jamal vergelijken?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "150 cm",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt waarschijnlijk alle lengtes bij elkaar opgeteld. Dat is niet wat de vraag vraagt. Volg de stappen: Tim 125, Lisa 125+15=140, Jamal 140-10=130.\n\n🤔 **Reflectievraag:** Is Jamal langer of korter dan Lisa?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "140 cm",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Dat is de lengte van Lisa (125 + 15 = 140), maar de vraag gaat over Jamal. Hij is 10 cm korter dan Lisa: 140 - 10 = 130.\n\n🤔 **Reflectievraag:** Wie meet 140 cm?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "130 cm",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een meerstapsopgave met afleiden: eerst Lisa's lengte berekenen, dan Jamal's lengte.",
                "berekening": ["Stap 1: Tim = 125 cm", "Stap 2: Lisa = 125 + 15 = 140 cm", "Stap 3: Jamal = 140 - 10 = 130 cm"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Tim's lengte | gegeven | **125 cm** |",
                    "| 2. Lisa's lengte | 125 + 15 | **140 cm** |",
                    "| 3. Jamal's lengte | 140 - 10 | **130 cm** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": [],
                    "hoofdvraag": "Hoe lang is Jamal?",
                    "tussenstappen": ["Bereken eerst Lisa's lengte", "Bereken dan Jamal's lengte"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Tim's lengte": "125 cm",
                        "Lisa langer dan Tim": "15 cm",
                        "Jamal korter dan Lisa": "10 cm"
                    },
                    "tool": "Optellen en aftrekken (met vergelijken)",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Bereken Lisa's lengte",
                            "berekening": "125 + 15",
                            "resultaat": "140 cm",
                            "uitleg": "Lisa is 15 cm langer dan Tim"
                        },
                        {
                            "stap": "Bereken Jamal's lengte",
                            "berekening": "140 - 10",
                            "resultaat": "130 cm",
                            "uitleg": "Jamal is 10 cm korter dan Lisa"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "centimeter",
                    "logica_check": "130 cm is logisch: tussen Tim (125) en Lisa (140) in",
                    "antwoord": "130 cm"
                }
            }
        }],
        "sub_theme": "lengtes vergelijken en afleiden"
    },

    # Problem 43: Gewicht met meerdere bewerkingen
    {
        "id": 43,
        "title": "Fruit wegen",
        "theme": "gewicht",
        "content": "Mia koopt 3 appels van elk 100 gram en 2 peren van elk 150 gram.",
        "questions": [{
            "question": "Hoeveel gram fruit koopt ze in totaal?",
            "hint": "💡 Tip: Hoeveel wegen de appels samen? En de peren?",
            "options": [
                {
                    "text": "250 gram",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt alleen de getallen bij elkaar opgeteld: 100 + 150 = 250. Maar Mia koopt 3 appels en 2 peren! Bereken: (3 × 100) + (2 × 150).\n\n🤔 **Reflectievraag:** Hoeveel stuks fruit koopt Mia in totaal?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "500 gram",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Je hebt misschien alleen de appels berekend (3 × 100 = 300) en de peren vergeten, of andersom. Bereken beide: 3 × 100 = 300 én 2 × 150 = 300, dan optellen: 300 + 300 = 600.\n\n🤔 **Reflectievraag:** Zijn er appels én peren?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 104
                },
                {
                    "text": "450 gram",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Bijna! Je hebt waarschijnlijk één berekening fout gedaan. Check: 3 × 100 = 300 gram appels, 2 × 150 = 300 gram peren, samen 600 gram.\n\n🤔 **Reflectievraag:** Hoeveel wegen 2 peren van 150 gram?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 104
                },
                {
                    "text": "600 gram",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een meerstapsopgave: twee vermenigvuldigingen en dan optellen.",
                "berekening": ["Stap 1: 3 × 100 = 300 gram appels", "Stap 2: 2 × 150 = 300 gram peren", "Stap 3: 300 + 300 = 600 gram totaal"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Gewicht appels | 3 × 100 | **300 gram** |",
                    "| 2. Gewicht peren | 2 × 150 | **300 gram** |",
                    "| 3. Totaal fruit | 300 + 300 | **600 gram** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": [],
                    "hoofdvraag": "Hoeveel gram fruit koopt ze in totaal?",
                    "tussenstappen": ["Bereken gewicht van alle appels", "Bereken gewicht van alle peren", "Tel beide bij elkaar op"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Aantal appels": "3",
                        "Gewicht per appel": "100 gram",
                        "Aantal peren": "2",
                        "Gewicht per peer": "150 gram"
                    },
                    "tool": "Vermenigvuldigen en optellen",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Bereken gewicht appels",
                            "berekening": "3 × 100",
                            "resultaat": "300 gram",
                            "uitleg": "3 appels van elk 100 gram"
                        },
                        {
                            "stap": "Bereken gewicht peren",
                            "berekening": "2 × 150",
                            "resultaat": "300 gram",
                            "uitleg": "2 peren van elk 150 gram"
                        },
                        {
                            "stap": "Tel samen",
                            "berekening": "300 + 300",
                            "resultaat": "600 gram",
                            "uitleg": "Totaal gewicht van alle fruit"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "gram",
                    "logica_check": "600 gram is logisch: 5 stuks fruit van gemiddeld 120 gram",
                    "antwoord": "600 gram"
                }
            }
        }],
        "sub_theme": "gewicht berekenen met meerdere soorten"
    },

    # Problem 44: Verhoudingen met redeneren
    {
        "id": 44,
        "title": "Kleuren verdelen",
        "theme": "verhoudingen",
        "content": "In een doos zitten rode en blauwe ballen. Er zijn 12 rode ballen. Voor elke rode bal zijn er 2 blauwe ballen.",
        "questions": [{
            "question": "Hoeveel ballen zitten er in totaal in de doos?",
            "hint": "💡 Tip: Hoeveel blauwe ballen zijn er? Hoeveel totaal?",
            "options": [
                {
                    "text": "14 ballen",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Je hebt 12 + 2 = 14 uitgerekend, maar '2' is niet het aantal blauwe ballen, maar de verhouding! Voor elke rode bal zijn er 2 blauwe: 12 × 2 = 24 blauwe. Totaal: 12 + 24 = 36.\n\n🤔 **Reflectievraag:** Zijn er meer rode of meer blauwe ballen?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "24 ballen",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Dat is alleen het aantal blauwe ballen (12 × 2 = 24). Maar de vraag gaat over ALLE ballen: rode + blauwe = 12 + 24 = 36.\n\n🤔 **Reflectievraag:** Moet je alleen de blauwe ballen tellen, of alle ballen?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "30 ballen",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Je hebt waarschijnlijk een rekenfout gemaakt. Check: 12 rode ballen, voor elke rode 2 blauwe = 12 × 2 = 24 blauwe. Totaal: 12 + 24 = 36.\n\n🤔 **Reflectievraag:** Hoeveel blauwe ballen zijn er per rode bal?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 104
                },
                {
                    "text": "36 ballen",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een verhoudingsopgave: eerst afleiden hoeveel blauwe ballen er zijn, dan optellen.",
                "berekening": ["Stap 1: 12 × 2 = 24 blauwe ballen", "Stap 2: 12 + 24 = 36 ballen totaal"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Bereken blauwe ballen | 12 × 2 | **24 blauwe** |",
                    "| 2. Tel alle ballen | 12 + 24 | **36 ballen** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": [],
                    "hoofdvraag": "Hoeveel ballen zitten er in totaal in de doos?",
                    "tussenstappen": ["Leid af hoeveel blauwe ballen er zijn", "Tel rode en blauwe ballen bij elkaar"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Rode ballen": "12",
                        "Verhouding blauwe per rode": "2"
                    },
                    "tool": "Vermenigvuldigen en optellen (verhouding)",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Bereken blauwe ballen",
                            "berekening": "12 × 2",
                            "resultaat": "24 ballen",
                            "uitleg": "Voor elke rode bal zijn er 2 blauwe ballen"
                        },
                        {
                            "stap": "Tel totaal",
                            "berekening": "12 + 24",
                            "resultaat": "36 ballen",
                            "uitleg": "Rode en blauwe ballen samen"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "ballen",
                    "logica_check": "36 ballen is logisch: verhouding rood:blauw = 1:2",
                    "antwoord": "36 ballen"
                }
            }
        }],
        "sub_theme": "verhoudingen en totaal berekenen"
    }
]

# Add these 4 problems
for problem in additional_problems:
    data.append(problem)
    print(f"✅ Added ID {problem['id']}: {problem['title']} ({problem['theme']})")
    print(f"   Complexity: {len(problem['questions'][0]['lova']['stap3_vormen']['bewerkingen'])} steps")
    print()

# Save
with open('verhaaltjessommen-emma - Template.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("=" * 70)
print(f"✅ Dataset now contains: {len(data)} problems")
multi_step = [p for p in data if len(p['questions'][0]['lova']['stap3_vormen']['bewerkingen']) > 1]
print(f"✅ Multi-step problems: {len(multi_step)} ({len(multi_step)/len(data)*100:.1f}%)")
print("=" * 70)
