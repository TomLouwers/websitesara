#!/usr/bin/env python3
"""
Add 10 E4 Doortoets Problems
E4-niveau: Eind groep 4 met verhoogde complexiteit en meerstaps redenering
"""

import json

with open('verhaaltjessommen-emma - Template.json', 'r') as f:
    data = json.load(f)

print("🔧 ADDING 10 E4 DOORTOETS PROBLEMS\n")
print("E4 kenmerken: meerstaps, redeneren, irrelevante info filteren\n")

e4_problems = [
    # Problem 45: Meerstaps optellen
    {
        "id": 45,
        "title": "Kinderen in de klas",
        "theme": "optellen_meerstappen",
        "content": "In de klas hebben 12 kinderen een boek bij zich. Later komen er 7 kinderen binnen. Aan het einde gaan er 5 kinderen naar een andere ruimte.",
        "questions": [{
            "question": "Hoeveel kinderen blijven er in het lokaal?",
            "hint": "💡 Tip: Begin met het totaal aantal kinderen. Wat gebeurt er daarna?",
            "options": [
                {
                    "text": "19 kinderen",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Je hebt alleen 12 + 7 = 19 gerekend, maar vergeten dat er 5 kinderen weggaan. Je moet nog een derde stap doen: 19 - 5 = 14.\n\n🤔 **Reflectievraag:** Gaan er aan het einde kinderen weg of komen er kinderen bij?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "24 kinderen",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt alle getallen bij elkaar opgeteld: 12 + 7 + 5 = 24. Maar 5 kinderen GAAN WEG, dus moet je die aftrekken! Bereken: 12 + 7 - 5 = 14.\n\n🤔 **Reflectievraag:** Als kinderen naar een andere ruimte gaan, moet je dat getal dan optellen of aftrekken?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 102
                },
                {
                    "text": "10 kinderen",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Je hebt waarschijnlijk 12 - 7 + 5 of een andere verkeerde volgorde gebruikt. Volg de tijdlijn: eerst 12, dan +7 (=19), dan -5 (=14).\n\n🤔 **Reflectievraag:** In welke volgorde gebeuren de dingen?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 101
                },
                {
                    "text": "14 kinderen",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een E4 meerstaps opgave: drie gebeurtenissen in chronologische volgorde verwerken.",
                "berekening": ["Stap 1: 12 kinderen beginnen", "Stap 2: 12 + 7 = 19 kinderen", "Stap 3: 19 - 5 = 14 kinderen blijven"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Begin | gegeven | **12 kinderen** |",
                    "| 2. Komen erbij | 12 + 7 | **19 kinderen** |",
                    "| 3. Gaan weg | 19 - 5 | **14 kinderen** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": ["boek bij zich (niet relevant voor tellen)"],
                    "hoofdvraag": "Hoeveel kinderen blijven er in het lokaal?",
                    "tussenstappen": ["Begin met 12 kinderen", "Tel 7 kinderen erbij", "Trek 5 kinderen af"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Beginaantal": "12 kinderen",
                        "Komen erbij": "7 kinderen",
                        "Gaan weg": "5 kinderen"
                    },
                    "tool": "Optellen en aftrekken in volgorde",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Begin situatie",
                            "berekening": "12",
                            "resultaat": "12 kinderen",
                            "uitleg": "Er zijn 12 kinderen met een boek"
                        },
                        {
                            "stap": "Kinderen komen erbij",
                            "berekening": "12 + 7",
                            "resultaat": "19 kinderen",
                            "uitleg": "Na binnenkomst zijn er 19 kinderen"
                        },
                        {
                            "stap": "Kinderen gaan weg",
                            "berekening": "19 - 5",
                            "resultaat": "14 kinderen",
                            "uitleg": "5 kinderen gaan naar andere ruimte, 14 blijven"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "kinderen",
                    "logica_check": "14 kinderen is logisch: tussen 12 (begin) en 19 (maximum)",
                    "antwoord": "14 kinderen"
                }
            }
        }],
        "sub_theme": "E4 meerstaps chronologisch"
    },

    # Problem 46: Wisselgeld combinatie
    {
        "id": 46,
        "title": "Boodschappen doen",
        "theme": "geld",
        "content": "Sarah koopt een pak melk van €2, brood voor €3 en appels voor €4. Ze betaalt met een briefje van €10.",
        "questions": [{
            "question": "Hoeveel wisselgeld krijgt zij terug?",
            "hint": "💡 Tip: Hoeveel kosten alle boodschappen samen? Hoeveel betaalt Sarah?",
            "options": [
                {
                    "text": "€ 6",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Je hebt waarschijnlijk €10 - €4 = €6 gerekend (alleen de appels). Maar Sarah koopt 3 dingen! Tel eerst alle kosten: €2 + €3 + €4 = €9, dan wisselgeld: €10 - €9 = €1.\n\n🤔 **Reflectievraag:** Hoeveel verschillende dingen koopt Sarah?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "€ 9",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Dat zijn de totale kosten (€2 + €3 + €4 = €9), maar de vraag gaat over het WISSELGELD. Trek de kosten af van wat ze betaalt: €10 - €9 = €1.\n\n🤔 **Reflectievraag:** Krijgt Sarah €9 terug, of moet ze €9 betalen?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "€ 19",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt alle getallen bij elkaar opgeteld: €2 + €3 + €4 + €10 = €19. Maar €10 is wat ze BETAALT, niet wat ze koopt. Bereken: kosten €9, betaald €10, wisselgeld €10 - €9 = €1.\n\n🤔 **Reflectievraag:** Is €10 een prijs van een product of het bedrag waarmee ze betaalt?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 102
                },
                {
                    "text": "€ 1",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een E4 geldopgave: eerst alle kosten optellen, dan wisselgeld berekenen.",
                "berekening": ["Stap 1: €2 + €3 + €4 = €9 totale kosten", "Stap 2: €10 - €9 = €1 wisselgeld"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Tel kosten op | €2 + €3 + €4 | **€9** |",
                    "| 2. Bereken wisselgeld | €10 - €9 | **€1** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": [],
                    "hoofdvraag": "Hoeveel wisselgeld krijgt zij terug?",
                    "tussenstappen": ["Tel alle kosten bij elkaar", "Trek totaal af van €10"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Melk": "€2",
                        "Brood": "€3",
                        "Appels": "€4",
                        "Betaald": "€10"
                    },
                    "tool": "Optellen en aftrekken (geld)",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Bereken totale kosten",
                            "berekening": "€2 + €3 + €4",
                            "resultaat": "€9",
                            "uitleg": "Alle drie producten samen kosten €9"
                        },
                        {
                            "stap": "Bereken wisselgeld",
                            "berekening": "€10 - €9",
                            "resultaat": "€1",
                            "uitleg": "Van €10 blijft €1 over als wisselgeld"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "euro",
                    "logica_check": "€1 wisselgeld is logisch: kosten bijna €10",
                    "antwoord": "€1"
                }
            }
        }],
        "sub_theme": "E4 wisselgeld meerdere producten"
    },

    # Problem 47: Tafel omgekeerd + redeneren
    {
        "id": 47,
        "title": "Kralen in bakjes",
        "theme": "delen",
        "content": "Een juf legt 48 kralen in bakjes met steeds 6 kralen. Daarna neemt ze 2 bakjes weg.",
        "questions": [{
            "question": "Met hoeveel kralen werkt ze nu?",
            "hint": "💡 Tip: Hoeveel bakjes maakt ze eerst? Hoeveel blijven er over?",
            "options": [
                {
                    "text": "46 kralen",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt 48 - 2 = 46 gerekend, maar er gaan 2 BAKJES weg, niet 2 kralen! Bereken eerst hoeveel bakjes: 48 ÷ 6 = 8. Dan 2 bakjes weg: 8 - 2 = 6 bakjes. Elk bakje heeft 6 kralen: 6 × 6 = 36.\n\n🤔 **Reflectievraag:** Gaan er bakjes weg of losse kralen?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "8 kralen",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Dat is het aantal bakjes (48 ÷ 6 = 8), maar de vraag gaat over KRALEN. Na het wegnemen van 2 bakjes blijven er 6 bakjes over met elk 6 kralen: 6 × 6 = 36 kralen.\n\n🤔 **Reflectievraag:** Wat is het verschil tussen bakjes en kralen?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "12 kralen",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Je hebt waarschijnlijk alleen de weggegooide kralen berekend: 2 × 6 = 12. Maar de vraag is hoeveel kralen er OVERBLIJVEN. Bereken: 8 bakjes - 2 bakjes = 6 bakjes, en 6 × 6 = 36 kralen.\n\n🤔 **Reflectievraag:** Blijven er kralen over of gaan alle kralen weg?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 103
                },
                {
                    "text": "36 kralen",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een E4 opgave met delen en vermenigvuldigen: eerst delen om bakjes te tellen, dan aftrekken, dan vermenigvuldigen.",
                "berekening": ["Stap 1: 48 ÷ 6 = 8 bakjes", "Stap 2: 8 - 2 = 6 bakjes blijven over", "Stap 3: 6 × 6 = 36 kralen"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Aantal bakjes | 48 ÷ 6 | **8 bakjes** |",
                    "| 2. Bakjes weg | 8 - 2 | **6 bakjes** |",
                    "| 3. Kralen totaal | 6 × 6 | **36 kralen** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": [],
                    "hoofdvraag": "Met hoeveel kralen werkt ze nu?",
                    "tussenstappen": ["Bereken aantal bakjes", "Trek 2 bakjes af", "Bereken hoeveel kralen in overgebleven bakjes"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Totaal kralen": "48",
                        "Kralen per bakje": "6",
                        "Bakjes weg": "2"
                    },
                    "tool": "Delen, aftrekken en vermenigvuldigen",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Bereken aantal bakjes",
                            "berekening": "48 ÷ 6",
                            "resultaat": "8 bakjes",
                            "uitleg": "48 kralen verdeeld over bakjes van 6"
                        },
                        {
                            "stap": "Bakjes wegnemen",
                            "berekening": "8 - 2",
                            "resultaat": "6 bakjes",
                            "uitleg": "2 bakjes gaan weg, 6 blijven over"
                        },
                        {
                            "stap": "Bereken overgebleven kralen",
                            "berekening": "6 × 6",
                            "resultaat": "36 kralen",
                            "uitleg": "6 bakjes met elk 6 kralen"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "kralen",
                    "logica_check": "36 kralen is logisch: minder dan 48 (beginaantal)",
                    "antwoord": "36 kralen"
                }
            }
        }],
        "sub_theme": "E4 omgekeerde tafelbewerking met redeneren"
    }
]

# Add first 3 E4 problems
for problem in e4_problems:
    data.append(problem)
    print(f"✅ Added ID {problem['id']}: {problem['title']} ({problem['theme']})")
    steps = len(problem['questions'][0]['lova']['stap3_vormen']['bewerkingen'])
    print(f"   E4 Complexity: {steps} steps")
    print()

# Save
with open('verhaaltjessommen-emma - Template.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("=" * 70)
print(f"✅ Added {len(e4_problems)} E4 doortoets problems")
print(f"✅ Dataset now contains: {len(data)} problems")
print("=" * 70)
print("\n🎯 Continue with remaining 7 E4 problems...")
