#!/usr/bin/env python3
"""
Add Complex Multi-Step M4 Problems
Voegt 10 uitdagende meerstapsopgaven toe aan de Emma dataset.
"""

import json

with open('verhaaltjessommen-emma - Template.json', 'r') as f:
    data = json.load(f)

print("🔧 ADDING 10 COMPLEX MULTI-STEP PROBLEMS\n")

# New complex problems with higher cognitive load
new_problems = [
    # Problem 38: Bloemen (optellen + aftrekken, zoals het voorbeeld)
    {
        "id": 38,
        "title": "Bloemen samen",
        "theme": "optellen_meerstappen",
        "content": "Lisa heeft 12 bloemen. Emma heeft 8 bloemen. Ze geven er samen 5 weg aan juf.",
        "questions": [{
            "question": "Hoeveel bloemen houden ze samen over?",
            "hint": "💡 Tip: Hoeveel bloemen hebben ze samen? Hoeveel geven ze weg?",
            "options": [
                {
                    "text": "20 bloemen",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Je hebt alleen de bloemen bij elkaar opgeteld, maar vergeten dat ze er 5 weggeven. Je moet eerst optellen (12 + 8) en dan aftrekken (5).\n\n🤔 **Reflectievraag:** Wat betekent 'samen over' in de vraag?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "25 bloemen",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Je hebt alle getallen bij elkaar opgeteld: 12 + 8 + 5 = 25. Maar ze GEVEN er 5 weg, dus moet je die aftrekken!\n\n🤔 **Reflectievraag:** Als je iets weggeeft, moet je dan optellen of aftrekken?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 102
                },
                {
                    "text": "9 bloemen",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt 12 - 5 = 7 berekend, maar vergeten dat Emma ook bloemen heeft. Tel EERST alle bloemen bij elkaar: 12 + 8 = 20, dan aftrekken: 20 - 5.\n\n🤔 **Reflectievraag:** Hoeveel kinderen hebben bloemen?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "15 bloemen",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een meerstapsopgave: eerst optellen om het totaal te weten, dan aftrekken.",
                "berekening": ["Stap 1: 12 + 8 = 20 bloemen samen", "Stap 2: 20 - 5 = 15 bloemen over"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Tel bloemen samen | 12 + 8 | **20 bloemen** |",
                    "| 2. Trek weggegeven bloemen af | 20 - 5 | **15 bloemen** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": [],
                    "hoofdvraag": "Hoeveel bloemen houden ze samen over?",
                    "tussenstappen": ["Tel alle bloemen bij elkaar op", "Trek de weggegeven bloemen af"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Lisa's bloemen": "12",
                        "Emma's bloemen": "8",
                        "Weggegeven": "5"
                    },
                    "tool": "Optellen en aftrekken",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Tel bloemen samen",
                            "berekening": "12 + 8",
                            "resultaat": "20 bloemen",
                            "uitleg": "Lisa en Emma hebben samen 20 bloemen"
                        },
                        {
                            "stap": "Trek weggegeven bloemen af",
                            "berekening": "20 - 5",
                            "resultaat": "15 bloemen",
                            "uitleg": "Ze geven er 5 weg, dus houden ze 15 over"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "bloemen",
                    "logica_check": "15 bloemen is logisch: 12 + 8 - 5 = 15",
                    "antwoord": "15 bloemen"
                }
            }
        }],
        "sub_theme": "optellen en aftrekken combineren"
    },

    # Problem 39: Snoep verdelen (vermenigvuldigen + aftrekken)
    {
        "id": 39,
        "title": "Snoep kopen en delen",
        "theme": "vermenigvuldigen",
        "content": "Jamal koopt 3 zakjes snoep. In elk zakje zitten 4 snoepjes. Hij eet er zelf 2 op.",
        "questions": [{
            "question": "Hoeveel snoepjes heeft hij nog over?",
            "hint": "💡 Tip: Hoeveel snoepjes heeft hij in totaal? Hoeveel eet hij op?",
            "options": [
                {
                    "text": "12 snoepjes",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Je hebt uitgerekend hoeveel snoepjes Jamal in totaal koopt (3 × 4 = 12), maar vergeten dat hij er 2 opeet.\n\n🤔 **Reflectievraag:** Heeft Jamal nog alle 12 snoepjes, of heeft hij er al wat opgegeten?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "5 snoepjes",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Bijna goed! Je hebt waarschijnlijk 3 + 4 - 2 = 5 gerekend. Maar je moet eerst vermenigvuldigen: 3 × 4 = 12, dan aftrekken: 12 - 2 = 10.\n\n🤔 **Reflectievraag:** Zitten er 4 snoepjes in één zakje of in alle zakjes samen?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 104
                },
                {
                    "text": "6 snoepjes",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt misschien 3 × 2 = 6 uitgerekend, maar dat klopt niet met de vraag. Hij koopt 3 zakjes met elk 4 snoepjes: 3 × 4 = 12. Dan eet hij 2 op: 12 - 2 = 10.\n\n🤔 **Reflectievraag:** Hoeveel snoepjes zitten er in elk zakje?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "10 snoepjes",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een meerstapsopgave: eerst vermenigvuldigen voor het totaal, dan aftrekken.",
                "berekening": ["Stap 1: 3 × 4 = 12 snoepjes totaal", "Stap 2: 12 - 2 = 10 snoepjes over"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Bereken totaal snoepjes | 3 × 4 | **12 snoepjes** |",
                    "| 2. Trek opgegeten snoepjes af | 12 - 2 | **10 snoepjes** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": [],
                    "hoofdvraag": "Hoeveel snoepjes heeft hij nog over?",
                    "tussenstappen": ["Bereken hoeveel snoepjes hij koopt", "Trek af wat hij opeet"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Aantal zakjes": "3",
                        "Snoepjes per zakje": "4",
                        "Opgegeten": "2"
                    },
                    "tool": "Vermenigvuldigen en aftrekken",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Bereken totaal",
                            "berekening": "3 × 4",
                            "resultaat": "12 snoepjes",
                            "uitleg": "3 zakjes met elk 4 snoepjes is 12 snoepjes"
                        },
                        {
                            "stap": "Trek opgegeten af",
                            "berekening": "12 - 2",
                            "resultaat": "10 snoepjes",
                            "uitleg": "Hij eet 2 snoepjes op, dus houdt 10 over"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "snoepjes",
                    "logica_check": "10 snoepjes is logisch: 3 × 4 - 2 = 10",
                    "antwoord": "10 snoepjes"
                }
            }
        }],
        "sub_theme": "vermenigvuldigen en aftrekken combineren"
    },

    # Problem 40: Geld - bewerking niet genoemd
    {
        "id": 40,
        "title": "Geld sparen",
        "theme": "geld",
        "content": "Mia spaart elke week 5 euro. Na 4 weken koopt ze een boek van 12 euro.",
        "questions": [{
            "question": "Hoeveel geld heeft Mia dan nog over?",
            "hint": "💡 Tip: Hoeveel euro heeft Mia gespaard? Wat koopt ze daarna?",
            "options": [
                {
                    "text": "€ 20",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Je hebt alleen berekend hoeveel Mia spaart (4 × 5 = 20), maar niet wat ze uitgeeft. Ze koopt een boek van € 12, dus moet je die nog aftrekken.\n\n🤔 **Reflectievraag:** Heeft Mia alle € 20 nog, of geeft ze een deel uit?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "€ 3",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Je hebt waarschijnlijk 5 - 12 uitgerekend, maar dat kan niet (dan krijg je een negatief getal). Bereken eerst het totaal gespaard: 4 × 5 = 20, dan aftrekken: 20 - 12 = 8.\n\n🤔 **Reflectievraag:** Hoeveel weken spaart Mia?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 104
                },
                {
                    "text": "€ 17",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt misschien 5 + 12 gerekend, maar dat is niet logisch. Ze KOOPT iets, dus geeft ze geld uit. Eerst vermenigvuldigen (4 × 5), dan aftrekken (12).\n\n🤔 **Reflectievraag:** Als je iets koopt, wordt je spaargeld dan meer of minder?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "€ 8",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een meerstapsopgave zonder expliciete bewerking: je moet zelf bedenken dat je eerst moet vermenigvuldigen en dan aftrekken.",
                "berekening": ["Stap 1: 4 × € 5 = € 20 gespaard", "Stap 2: € 20 - € 12 = € 8 over"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Bereken gespaard bedrag | 4 × € 5 | **€ 20** |",
                    "| 2. Trek uitgave af | € 20 - € 12 | **€ 8** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": [],
                    "hoofdvraag": "Hoeveel geld heeft Mia dan nog over?",
                    "tussenstappen": ["Bereken hoeveel Mia spaart", "Trek de kosten van het boek af"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Spaarbedrag per week": "€ 5",
                        "Aantal weken": "4",
                        "Kosten boek": "€ 12"
                    },
                    "tool": "Vermenigvuldigen en aftrekken (niet expliciet vermeld)",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Bereken totaal gespaard",
                            "berekening": "4 × € 5",
                            "resultaat": "€ 20",
                            "uitleg": "Na 4 weken heeft Mia € 20 gespaard"
                        },
                        {
                            "stap": "Trek uitgave af",
                            "berekening": "€ 20 - € 12",
                            "resultaat": "€ 8",
                            "uitleg": "Na het kopen van het boek heeft ze € 8 over"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "euro",
                    "logica_check": "€ 8 is logisch: 4 × € 5 - € 12 = € 8",
                    "antwoord": "€ 8"
                }
            }
        }],
        "sub_theme": "geld sparen en uitgeven"
    }
]

# Add first 3 problems for now (will add more in next iteration)
print("Adding 3 complex problems to demonstrate the approach...")
print()

for problem in new_problems[:3]:
    data.append(problem)
    print(f"✅ Added ID {problem['id']}: {problem['title']} ({problem['theme']})")
    print(f"   Complexity: {len(problem['questions'][0]['lova']['stap3_vormen']['bewerkingen'])} steps")
    print()

# Save
with open('verhaaltjessommen-emma - Template.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("=" * 70)
print("✅ COMPLEX PROBLEMS ADDED!")
print("=" * 70)
print(f"\nDataset now contains: {len(data)} problems")
print(f"Multi-step problems: {len([p for p in data if len(p['questions'][0]['lova']['stap3_vormen']['bewerkingen']) > 1])}")
print()
print("🎯 Next: Add 7 more complex problems across other themes")
