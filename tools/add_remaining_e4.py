#!/usr/bin/env python3
"""
Add Remaining 7 E4 Doortoets Problems (IDs 48-54)
"""

import json

with open('verhaaltjessommen-emma - Template.json', 'r') as f:
    data = json.load(f)

print("🔧 ADDING REMAINING 7 E4 PROBLEMS\n")

remaining_e4 = [
    # Problem 48: Tijd - duur in meerdere stappen
    {
        "id": 48,
        "title": "Gymles en pauze",
        "theme": "tijd",
        "content": "De gymles start om 09:15. De les duurt 45 minuten. Daarna pauzeren ze nog 15 minuten.",
        "questions": [{
            "question": "Hoe laat gaan ze weer terug naar de klas?",
            "hint": "💡 Tip: Hoe laat is de les klaar? En na de pauze?",
            "options": [
                {
                    "text": "09:30",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt waarschijnlijk alleen de 15 minuten pauze bij 09:15 opgeteld. Maar de gymles duurt ook nog 45 minuten! Bereken: 09:15 + 45 min = 10:00, dan +15 min = 10:15.\n\n🤔 **Reflectievraag:** Hoelang duurt de gymles?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "10:00",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Dat is het tijdstip waarop de gymles klaar is (09:15 + 45 = 10:00), maar daarna pauzeren ze nog 15 minuten! Het antwoord is 10:00 + 15 = 10:15.\n\n🤔 **Reflectievraag:** Gaan ze meteen terug na de les, of is er nog een pauze?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "10:45",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Je hebt misschien 45 + 15 = 60 minuten bij 09:15 opgeteld: 09:15 + 1 uur = 10:15. Maar dat geeft 10:15, niet 10:45. Check je berekening.\n\n🤔 **Reflectievraag:** Hoeveel minuten is 45 + 15 samen?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "10:15",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een E4 tijdopgave: twee tijdsduren achter elkaar optellen bij een starttijd.",
                "berekening": ["Stap 1: 09:15 + 45 minuten = 10:00 (einde gymles)", "Stap 2: 10:00 + 15 minuten = 10:15 (terug naar klas)"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Start gymles | gegeven | **09:15** |",
                    "| 2. Einde gymles | 09:15 + 45 min | **10:00** |",
                    "| 3. Na pauze | 10:00 + 15 min | **10:15** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": [],
                    "hoofdvraag": "Hoe laat gaan ze weer terug naar de klas?",
                    "tussenstappen": ["Bereken eindtijd gymles", "Tel pauze erbij"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Starttijd": "09:15",
                        "Duur gymles": "45 minuten",
                        "Duur pauze": "15 minuten"
                    },
                    "tool": "Tijd optellen (meerdere stappen)",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Bereken einde gymles",
                            "berekening": "09:15 + 45 minuten",
                            "resultaat": "10:00",
                            "uitleg": "45 minuten na 09:15 is 10:00"
                        },
                        {
                            "stap": "Tel pauze erbij",
                            "berekening": "10:00 + 15 minuten",
                            "resultaat": "10:15",
                            "uitleg": "Na 15 minuten pauze is het 10:15"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "tijd (uur:minuten)",
                    "logica_check": "10:15 is logisch: 1 uur na start (09:15 + 60 min)",
                    "antwoord": "10:15"
                }
            }
        }],
        "sub_theme": "E4 tijd meerdere duren combineren"
    },

    # Problem 49: Lengte - omrekenen + optellen
    {
        "id": 49,
        "title": "Linten vastknopen",
        "theme": "lengte",
        "content": "Tom knipt twee linten: één lint van 75 cm en één lint van 1 meter. Hij knoopt ze aan elkaar vast.",
        "questions": [{
            "question": "Hoe lang is het lint in totaal? (in cm)",
            "hint": "💡 Tip: Hoeveel cm is 1 meter? Tel dan beide lengtes bij elkaar.",
            "options": [
                {
                    "text": "76 cm",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Je hebt 75 + 1 = 76 gerekend, maar 1 meter is niet 1 centimeter! 1 meter = 100 cm. De juiste berekening is 75 + 100 = 175 cm.\n\n🤔 **Reflectievraag:** Hoeveel centimeter is 1 meter?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "85 cm",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Je hebt misschien gedacht dat 1 meter = 10 cm. Maar 1 meter = 100 cm! Bereken: 75 cm + 100 cm = 175 cm.\n\n🤔 **Reflectievraag:** Wat is groter: 1 centimeter of 1 meter?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "1,75 cm",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Dit lijkt op het juiste antwoord, maar je hebt de eenheid verkeerd. 1,75 is correct als METER, maar de vraag vraagt om centimeters: 175 cm.\n\n🤔 **Reflectievraag:** Vraagt de opgave om meters of centimeters?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "175 cm",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een E4 lengtesom met omrekenen: eerst 1 meter omzetten naar 100 cm, dan optellen.",
                "berekening": ["Stap 1: 1 meter = 100 cm", "Stap 2: 75 cm + 100 cm = 175 cm"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Reken om | 1 meter | **100 cm** |",
                    "| 2. Tel lengtes op | 75 + 100 | **175 cm** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": ["vastknopen (niet relevant voor lengte)"],
                    "hoofdvraag": "Hoe lang is het lint in totaal? (in cm)",
                    "tussenstappen": ["Reken 1 meter om naar cm", "Tel beide lengtes bij elkaar"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Lint 1": "75 cm",
                        "Lint 2": "1 meter"
                    },
                    "tool": "Omrekenen en optellen",
                    "conversies": ["1 meter = 100 cm"]
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Reken om naar cm",
                            "berekening": "1 meter = 100 cm",
                            "resultaat": "100 cm",
                            "uitleg": "1 meter is hetzelfde als 100 centimeter"
                        },
                        {
                            "stap": "Tel lengtes op",
                            "berekening": "75 + 100",
                            "resultaat": "175 cm",
                            "uitleg": "Beide linten samen zijn 175 cm"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "centimeter",
                    "logica_check": "175 cm is logisch: meer dan 1 meter (100 cm)",
                    "antwoord": "175 cm"
                }
            }
        }],
        "sub_theme": "E4 lengte omrekenen en optellen"
    },

    # Problem 50: Inhoud - meerdere keren aftrekken
    {
        "id": 50,
        "title": "Limonade inschenken",
        "theme": "inhoud",
        "content": "In een fles zit 1 liter limonade (1000 ml). Er wordt 350 ml ingeschonken en later nog eens 200 ml.",
        "questions": [{
            "question": "Hoeveel limonade zit er nog in de fles?",
            "hint": "💡 Tip: Begin met 1000 ml. Hoeveel wordt er in totaal uitgeschonken?",
            "options": [
                {
                    "text": "800 ml",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Je hebt alleen de eerste keer inschenken afgetrokken: 1000 - 200 = 800. Maar er wordt TWEE keer ingeschonken! Bereken: 1000 - 350 - 200 = 450 ml.\n\n🤔 **Reflectievraag:** Hoeveel keer wordt er limonade ingeschonken?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "650 ml",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Je hebt alleen de eerste keer inschenken afgetrokken: 1000 - 350 = 650. Maar er wordt later NOG EENS 200 ml ingeschonken! Bereken: 650 - 200 = 450 ml.\n\n🤔 **Reflectievraag:** Wordt er later nog meer limonade uitgeschonken?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "550 ml",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Je hebt een rekenfout gemaakt. Check: 1000 - 350 = 650, dan 650 - 200 = 450. Of direct: 1000 - (350 + 200) = 1000 - 550 = 450 ml.\n\n🤔 **Reflectievraag:** Wat is 350 + 200?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 102
                },
                {
                    "text": "450 ml",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een E4 inhoudopgave: twee keer aftrekken of eerst optellen dan aftrekken.",
                "berekening": ["Stap 1: 1000 ml - 350 ml = 650 ml", "Stap 2: 650 ml - 200 ml = 450 ml", "Of: 1000 - (350 + 200) = 450 ml"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Begin | gegeven | **1000 ml** |",
                    "| 2. Eerste inschenking | 1000 - 350 | **650 ml** |",
                    "| 3. Tweede inschenking | 650 - 200 | **450 ml** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": [],
                    "hoofdvraag": "Hoeveel limonade zit er nog in de fles?",
                    "tussenstappen": ["Trek eerste inschenking af", "Trek tweede inschenking af"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Begin hoeveelheid": "1000 ml (1 liter)",
                        "Eerste inschenking": "350 ml",
                        "Tweede inschenking": "200 ml"
                    },
                    "tool": "Meerdere keren aftrekken",
                    "conversies": ["1 liter = 1000 ml"]
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Eerste inschenking",
                            "berekening": "1000 - 350",
                            "resultaat": "650 ml",
                            "uitleg": "Na eerste keer inschenken blijft 650 ml over"
                        },
                        {
                            "stap": "Tweede inschenking",
                            "berekening": "650 - 200",
                            "resultaat": "450 ml",
                            "uitleg": "Na tweede keer inschenken blijft 450 ml over"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "milliliter",
                    "logica_check": "450 ml is logisch: minder dan helft van 1 liter",
                    "antwoord": "450 ml"
                }
            }
        }],
        "sub_theme": "E4 inhoud meerdere bewerkingen"
    },

    # Problem 51: Parkeerplaats met irrelevante info
    {
        "id": 51,
        "title": "Auto's op de parkeerplaats",
        "theme": "optellen_meerstappen",
        "content": "Op de parkeerplaats staan 9 blauwe auto's, 7 rode en 5 groene. Later rijden er 6 rode auto's weg.",
        "questions": [{
            "question": "Hoeveel auto's staan er daarna nog?",
            "hint": "💡 Tip: Hoeveel auto's zijn er in totaal? Hoeveel rijden er weg?",
            "options": [
                {
                    "text": "21 auto's",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Je hebt alle auto's bij elkaar opgeteld (9 + 7 + 5 = 21), maar vergeten dat er 6 rode auto's wegrijden. Trek die nog af: 21 - 6 = 15 auto's.\n\n🤔 **Reflectievraag:** Blijven alle auto's op de parkeerplaats?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "27 auto's",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt alle getallen bij elkaar opgeteld: 9 + 7 + 5 + 6 = 27. Maar 6 auto's RIJDEN WEG, dus moet je die aftrekken! Bereken: 9 + 7 + 5 - 6 = 15.\n\n🤔 **Reflectievraag:** Als auto's wegrijden, moet je dat getal dan optellen of aftrekken?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 102
                },
                {
                    "text": "1 auto",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt waarschijnlijk 7 - 6 = 1 gerekend (alleen de rode auto's). Maar er staan ook nog blauwe en groene auto's! Bereken: 9 + 7 + 5 = 21 totaal, dan 21 - 6 = 15.\n\n🤔 **Reflectievraag:** Zijn er alleen rode auto's, of ook andere kleuren?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "15 auto's",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een E4 opgave met irrelevante info (kleuren): tel alle auto's, trek weggegane auto's af.",
                "berekening": ["Stap 1: 9 + 7 + 5 = 21 auto's totaal", "Stap 2: 21 - 6 = 15 auto's blijven"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Tel alle auto's | 9 + 7 + 5 | **21 auto's** |",
                    "| 2. Auto's rijden weg | 21 - 6 | **15 auto's** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": ["blauwe, rode, groene (kleuren zijn niet relevant voor telling)"],
                    "hoofdvraag": "Hoeveel auto's staan er daarna nog?",
                    "tussenstappen": ["Tel alle auto's bij elkaar", "Trek weggegane auto's af"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Blauwe auto's": "9",
                        "Rode auto's": "7",
                        "Groene auto's": "5",
                        "Wegrijden": "6"
                    },
                    "tool": "Optellen en aftrekken (met irrelevante info)",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Tel alle auto's",
                            "berekening": "9 + 7 + 5",
                            "resultaat": "21 auto's",
                            "uitleg": "In totaal staan er 21 auto's"
                        },
                        {
                            "stap": "Trek weggegane af",
                            "berekening": "21 - 6",
                            "resultaat": "15 auto's",
                            "uitleg": "6 auto's weg, dus 15 blijven over"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "auto's",
                    "logica_check": "15 auto's is logisch: minder dan 21 (begin)",
                    "antwoord": "15 auto's"
                }
            }
        }],
        "sub_theme": "E4 meerstaps met irrelevante informatie"
    },

    # Problem 52: Vermenigvuldigen + optellen
    {
        "id": 52,
        "title": "Koekjes in dozen en los",
        "theme": "vermenigvuldigen",
        "content": "Een doos heeft 8 koekjes. Emma koopt 3 dozen en krijgt er thuis nog 5 losse koekjes bij.",
        "questions": [{
            "question": "Hoeveel koekjes heeft ze in totaal?",
            "hint": "💡 Tip: Hoeveel koekjes zitten er in 3 dozen? En dan nog de losse erbij?",
            "options": [
                {
                    "text": "16 koekjes",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt waarschijnlijk 8 + 8 = 16 gerekend (2 dozen), maar Emma koopt 3 dozen! Bereken: 3 × 8 = 24, dan + 5 losse = 29 koekjes.\n\n🤔 **Reflectievraag:** Hoeveel dozen koopt Emma?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "24 koekjes",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Dat zijn de koekjes in de 3 dozen (3 × 8 = 24), maar Emma krijgt er thuis NOG 5 losse koekjes bij! Tel die ook op: 24 + 5 = 29 koekjes.\n\n🤔 **Reflectievraag:** Krijgt Emma alleen koekjes in dozen, of ook losse?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "13 koekjes",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Je hebt misschien 8 + 5 = 13 gerekend, maar vergeten te vermenigvuldigen met 3 dozen. Bereken: 3 × 8 = 24 koekjes in dozen, dan + 5 losse = 29.\n\n🤔 **Reflectievraag:** Hoeveel koekjes zitten er in 3 dozen van elk 8 koekjes?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 104
                },
                {
                    "text": "29 koekjes",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een E4 opgave: vermenigvuldigen voor dozen, dan losse erbij optellen.",
                "berekening": ["Stap 1: 3 × 8 = 24 koekjes in dozen", "Stap 2: 24 + 5 = 29 koekjes totaal"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Koekjes in dozen | 3 × 8 | **24 koekjes** |",
                    "| 2. Losse koekjes erbij | 24 + 5 | **29 koekjes** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": ["thuis (niet relevant voor telling)"],
                    "hoofdvraag": "Hoeveel koekjes heeft ze in totaal?",
                    "tussenstappen": ["Bereken koekjes in 3 dozen", "Tel losse koekjes erbij"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Koekjes per doos": "8",
                        "Aantal dozen": "3",
                        "Losse koekjes": "5"
                    },
                    "tool": "Vermenigvuldigen en optellen",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Bereken koekjes in dozen",
                            "berekening": "3 × 8",
                            "resultaat": "24 koekjes",
                            "uitleg": "3 dozen met elk 8 koekjes"
                        },
                        {
                            "stap": "Tel losse erbij",
                            "berekening": "24 + 5",
                            "resultaat": "29 koekjes",
                            "uitleg": "Koekjes in dozen plus losse koekjes"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "koekjes",
                    "logica_check": "29 koekjes is logisch: meer dan 24 (alleen dozen)",
                    "antwoord": "29 koekjes"
                }
            }
        }],
        "sub_theme": "E4 vermenigvuldigen en optellen"
    },

    # Problem 53: Delen met redenering
    {
        "id": 53,
        "title": "Stickers verdelen en gebruiken",
        "theme": "delen",
        "content": "Er zijn 42 stickers. Ze worden verdeeld over 7 kinderen. Ieder kind gebruikt 3 stickers zelf.",
        "questions": [{
            "question": "Hoeveel stickers blijven er dan over per kind?",
            "hint": "💡 Tip: Hoeveel stickers krijgt elk kind eerst? Hoeveel gebruiken ze?",
            "options": [
                {
                    "text": "6 stickers",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Dat is hoeveel stickers elk kind KRIJGT (42 ÷ 7 = 6), maar ze GEBRUIKEN er 3. Dus houden ze 6 - 3 = 3 stickers over per kind.\n\n🤔 **Reflectievraag:** Hoeveel stickers gebruikt elk kind?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "21 stickers",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt het totaal aantal over berekend (7 × 3 = 21), maar de vraag gaat over hoeveel elk kind overhoudt, niet het totaal. Elk kind houdt 6 - 3 = 3 stickers over.\n\n🤔 **Reflectievraag:** Vraagt de som naar het totaal of per kind?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "39 stickers",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Je hebt misschien 42 - 3 = 39 gerekend, maar dat is niet correct. Eerst verdelen: 42 ÷ 7 = 6 per kind, dan elk kind gebruikt 3: 6 - 3 = 3 over per kind.\n\n🤔 **Reflectievraag:** Moet je eerst verdelen of eerst aftrekken?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 103
                },
                {
                    "text": "3 stickers",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een E4 deelsom met redenering: eerst verdelen, dan aftrekken per kind.",
                "berekening": ["Stap 1: 42 ÷ 7 = 6 stickers per kind", "Stap 2: 6 - 3 = 3 stickers blijven over per kind"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Verdelen | 42 ÷ 7 | **6 stickers per kind** |",
                    "| 2. Gebruiken | 6 - 3 | **3 stickers over** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": [],
                    "hoofdvraag": "Hoeveel stickers blijven er dan over per kind?",
                    "tussenstappen": ["Verdeel 42 stickers over 7 kinderen", "Trek gebruikte stickers af"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Totaal stickers": "42",
                        "Aantal kinderen": "7",
                        "Gebruikt per kind": "3"
                    },
                    "tool": "Delen en aftrekken",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Verdeel stickers",
                            "berekening": "42 ÷ 7",
                            "resultaat": "6 stickers",
                            "uitleg": "Elk kind krijgt 6 stickers"
                        },
                        {
                            "stap": "Trek gebruikte af",
                            "berekening": "6 - 3",
                            "resultaat": "3 stickers",
                            "uitleg": "Elk kind gebruikt 3, dus 3 blijven over"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "stickers per kind",
                    "logica_check": "3 stickers per kind is logisch: helft van 6 (gekregen)",
                    "antwoord": "3 stickers"
                }
            }
        }],
        "sub_theme": "E4 delen met redenering"
    },

    # Problem 54: Geld delen (exact deelbaar)
    {
        "id": 54,
        "title": "Spaargeld verdelen",
        "theme": "geld",
        "content": "Vier kinderen sparen samen €28. Ze willen het geld verdelen, maar elk kind moet evenveel krijgen.",
        "questions": [{
            "question": "Hoeveel euro krijgt ieder kind?",
            "hint": "💡 Tip: Verdeel €28 eerlijk over 4 kinderen.",
            "options": [
                {
                    "text": "€ 4",
                    "is_correct": False,
                    "error_type": "rekenfout_basis",
                    "foutanalyse": "Je hebt waarschijnlijk verkeerd gedeeld. Check: 4 × 4 = 16, maar ze hebben €28. De juiste berekening is 28 ÷ 4 = 7 euro per kind.\n\n🤔 **Reflectievraag:** Hoeveel is 28 gedeeld door 4?",
                    "visual_aid_query": None,
                    "remedial_basis_id": 103
                },
                {
                    "text": "€ 24",
                    "is_correct": False,
                    "error_type": "conceptfout",
                    "foutanalyse": "Je hebt misschien 28 - 4 = 24 gerekend, maar de vraag gaat over VERDELEN, niet aftrekken. Je moet delen: 28 ÷ 4 = 7 euro per kind.\n\n🤔 **Reflectievraag:** Als je geld eerlijk verdeelt, moet je dan delen of aftrekken?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "€ 32",
                    "is_correct": False,
                    "error_type": "leesfout_ruis",
                    "foutanalyse": "Je hebt 28 + 4 = 32 uitgerekend, maar dat is niet wat de vraag vraagt. De vraag is hoeveel elk kind KRIJGT als je €28 eerlijk verdeelt: 28 ÷ 4 = 7 euro.\n\n🤔 **Reflectievraag:** Wordt er geld bij elkaar opgeteld of verdeeld?",
                    "visual_aid_query": None,
                    "remedial_basis_id": None
                },
                {
                    "text": "€ 7",
                    "is_correct": True,
                    "foutanalyse": ""
                }
            ],
            "extra_info": {
                "concept": "Dit is een E4 geldopgave met delen: eerlijk verdelen over een aantal kinderen.",
                "berekening": ["€28 ÷ 4 kinderen = €7 per kind"],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    "| 1. Verdeel geld eerlijk | €28 ÷ 4 | **€7 per kind** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {
                    "ruis": ["samen, sparen (context maar niet relevant voor berekening)"],
                    "hoofdvraag": "Hoeveel euro krijgt ieder kind?",
                    "tussenstappen": ["Verdeel €28 over 4 kinderen"]
                },
                "stap2_ordenen": {
                    "relevante_getallen": {
                        "Totaal spaargeld": "€28",
                        "Aantal kinderen": "4"
                    },
                    "tool": "Delen (geld)",
                    "conversies": []
                },
                "stap3_vormen": {
                    "bewerkingen": [
                        {
                            "stap": "Verdeel geld eerlijk",
                            "berekening": "€28 ÷ 4",
                            "resultaat": "€7",
                            "uitleg": "€28 eerlijk verdelen over 4 kinderen geeft €7 per kind"
                        }
                    ]
                },
                "stap4_antwoorden": {
                    "verwachte_eenheid": "euro",
                    "logica_check": "€7 per kind is logisch: 4 × €7 = €28",
                    "antwoord": "€7"
                }
            }
        }],
        "sub_theme": "E4 geld delen exact"
    }
]

# Add all remaining E4 problems
for problem in remaining_e4:
    data.append(problem)
    print(f"✅ Added ID {problem['id']}: {problem['title']} ({problem['theme']})")
    steps = len(problem['questions'][0]['lova']['stap3_vormen']['bewerkingen'])
    print(f"   E4 Complexity: {steps} steps")
    print()

# Save
with open('verhaaltjessommen-emma - Template.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("=" * 70)
print(f"✅ All E4 doortoets problems added!")
print(f"✅ Dataset now contains: {len(data)} problems")
print("=" * 70)

# Calculate complexity distribution
one_step = len([p for p in data if len(p['questions'][0]['lova']['stap3_vormen']['bewerkingen']) == 1])
two_step = len([p for p in data if len(p['questions'][0]['lova']['stap3_vormen']['bewerkingen']) == 2])
three_step = len([p for p in data if len(p['questions'][0]['lova']['stap3_vormen']['bewerkingen']) == 3])

print(f"\n📊 FINAL COMPLEXITY DISTRIBUTION:")
print(f"  1-staps: {one_step} ({one_step/len(data)*100:.1f}%)")
print(f"  2-staps: {two_step} ({two_step/len(data)*100:.1f}%)")
print(f"  3-staps: {three_step} ({three_step/len(data)*100:.1f}%)")
print()
print("🎯 Dataset compleet met M4 én E4 doortoetsing!")
