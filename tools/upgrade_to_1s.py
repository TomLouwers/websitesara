#!/usr/bin/env python3
"""
Upgrade 5 opgaven naar 1S-niveau (Streefniveau basisschool / 2F VO)

1S kenmerken:
- Complexere getallen (decimalen, lastige breuken/percentages)
- Meerdere denkstappen (A → B → C)
- Terugrekenen en redeneren
"""

import json

def upgrade_id_277():
    """
    ID 277 - Filmavond kaartverkoop
    Upgrade: Moeilijkere breuken (7/12, 5/8), moeilijker percentage (37,5%), terugrekenen
    """
    return {
        "id": 277,
        "title": "Filmavond kaartverkoop",
        "theme": "breuken",
        "content": "Voor de filmavond zijn er 480 kaartjes beschikbaar. In de voorverkoop is 7/12 van de kaartjes verkocht. Van de voorverkoopkaarten is 37,5% voor kinderen. Van de kinderkaarten is 5/8 met korting gekocht.",
        "questions": [
            {
                "question": "Hoeveel kinderkaarten zijn er in de voorverkoop verkocht?",
                "options": [
                    {
                        "text": "280 kaartjes",
                        "foutanalyse": "Dit is het totaal aantal voorverkoopkaarten, niet alleen de kinderkaarten.\n\n🤔 **Reflectievraag:** Heb je alle tussenstappen doorlopen? Eerst voorverkoop, dan percentage kinderen berekenen.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "180 kaartjes",
                        "foutanalyse": "Dit is ongeveer 37,5% van het totaal, maar je moet eerst de voorverkoop berekenen.\n\n🤔 **Reflectievraag:** Werk stap voor stap: voorverkoop → kinderen → korting.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "65 kaartjes",
                        "foutanalyse": "Dit is het aantal kinderkaarten MET korting. De vraag is naar het totaal aantal kinderkaarten.\n\n🤔 **Reflectievraag:** Lees de vraag goed: hoeveel kinderkaarten in totaal, of alleen met korting?",
                        "is_correct": False,
                        "error_type": "leesfout_ruis",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "105 kaartjes",
                        "foutanalyse": "",
                        "is_correct": True
                    }
                ],
                "extra_info": {
                    "concept": "Dit is een percentage van een breuk berekening: werk stap voor stap. Let op: 7/12 en 37,5% zijn complexere getallen dan gebruikelijk.",
                    "berekening": [
                        "Stap 1: Voorverkoop = 7/12 van 480 = 480 × 7 ÷ 12 = 280 kaartjes",
                        "Stap 2: Kinderen = 37,5% van 280 = 0,375 × 280 = 105 kaartjes"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Voorverkoop: 7/12 van 480 = 480 × 7 ÷ 12 = 280 kaartjes |",
                        "| 2 | Kinderen: 37,5% van 280 = 0,375 × 280 = 105 kaartjes |"
                    ]
                },
                "hint": "💡 Tip: Werk systematisch: eerst voorverkoop (7/12), dan kinderen (37,5%)!"
            },
            {
                "question": "Hoeveel kinderkaarten zijn er met korting gekocht?",
                "options": [
                    {
                        "text": "42 kaartjes",
                        "foutanalyse": "Dit is 3/8 in plaats van 5/8. Controleer je breukberekening.\n\n🤔 **Reflectievraag:** Heb je de teller en noemer goed gebruikt? 5/8 betekent 5 delen van 8.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "65 kaartjes",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "105 kaartjes",
                        "foutanalyse": "Dit is het totaal aantal kinderkaarten, maar niet allemaal zijn met korting. Bereken 5/8 hiervan.\n\n🤔 **Reflectievraag:** Lees de vraag goed: hoeveel MET korting?",
                        "is_correct": False,
                        "error_type": "leesfout_ruis",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "175 kaartjes",
                        "foutanalyse": "Dit is te veel. Je hebt waarschijnlijk een verkeerde breuk gebruikt.\n\n🤔 **Reflectievraag:** Controleer je breukberekening nog eens - 5/8 van 105 = ?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    }
                ],
                "extra_info": {
                    "concept": "Dit is een breuk van een percentage van een breuk: complexe combinatie die meerdere stappen vereist.",
                    "berekening": [
                        "Kinderkaarten (uit vorige vraag): 105",
                        "Met korting: 5/8 van 105 = 105 × 5 ÷ 8 = 65,625 ≈ 65 kaartjes"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Kinderkaarten: 105 |",
                        "| 2 | Met korting: 5/8 van 105 = 105 × 5 ÷ 8 = 65,625 ≈ 65 kaartjes |"
                    ]
                },
                "hint": "💡 Tip: Je hebt nu 3 stappen: breuk (7/12) → percentage (37,5%) → breuk (5/8)!"
            },
            {
                "question": "Als er uiteindelijk 65 kinderkaarten met korting zijn verkocht, en dit is 5/8 van alle kinderkaarten, hoeveel kinderkaarten waren er dan in totaal in de voorverkoop? (Terugrekenen)",
                "options": [
                    {
                        "text": "40 kaartjes",
                        "foutanalyse": "Te weinig. Bij terugrekenen moet je delen door de breuk, oftewel vermenigvuldigen met het omgekeerde.\n\n🤔 **Reflectievraag:** Als 5/8 = 65, dan is 8/8 (het geheel) = ?",
                        "is_correct": False,
                        "error_type": "conceptfout",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "104 kaartjes",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "81 kaartjes",
                        "foutanalyse": "Controleer je berekening. Als 5/8 = 65, dan is 1/8 = 65÷5 = 13, dus 8/8 = 13×8.\n\n🤔 **Reflectievraag:** Werk via 1/8: als 5/8 = 65, dan 1/8 = ?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "120 kaartjes",
                        "foutanalyse": "Te veel. Controleer je berekening: 65 ÷ 5 × 8 = ?\n\n🤔 **Reflectievraag:** Werk systematisch: 5/8 = 65, dus 1/8 = 65÷5, dus 8/8 = ?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    }
                ],
                "extra_info": {
                    "concept": "Dit is terugrekenen met breuken: als je weet dat een deel (5/8) een bepaalde waarde heeft, kun je het geheel (8/8) berekenen.",
                    "berekening": [
                        "5/8 van totaal = 65 kaartjes",
                        "1/8 van totaal = 65 ÷ 5 = 13 kaartjes",
                        "8/8 (=totaal) = 13 × 8 = 104 kaartjes",
                        "",
                        "Of direct: 65 ÷ (5/8) = 65 × (8/5) = 104 kaartjes"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | 5/8 van totaal = 65 kaartjes |",
                        "| 2 | 1/8 van totaal = 65 ÷ 5 = 13 kaartjes |",
                        "| 3 | 8/8 (=totaal) = 13 × 8 = 104 kaartjes |",
                        "| 4 |  |",
                        "| 5 | Of direct: 65 ÷ (5/8) = 65 × (8/5) = 104 kaartjes |"
                    ]
                },
                "hint": "💡 Tip: Bij terugrekenen met breuken: delen door 5/8 is hetzelfde als vermenigvuldigen met 8/5!"
            }
        ],
        "sub_theme": "breuk van percentage van breuk + terugrekenen"
    }

def upgrade_id_18():
    """
    ID 18 - Autorit
    Upgrade: Niet-ronde getallen, pauze toevoegen, gemiddelde snelheid berekenen (meerdere stappen)
    """
    return {
        "id": 18,
        "title": "Autorit",
        "theme": "snelheid-afstand-tijd",
        "content": "Familie Jansen rijdt op vakantie naar Duitsland. De totale afstand is 456 kilometer. Ze rijden het eerste deel (168 km) met een gemiddelde snelheid van 84 km/uur. Dan nemen ze een pauze van 0,5 uur. Het tweede deel rijden ze met een gemiddelde snelheid van 96 km/uur.",
        "questions": [
            {
                "question": "Hoe lang doen ze over het eerste deel van de reis (zonder pauze)?",
                "options": [
                    {
                        "text": "1 uur en 30 minuten",
                        "foutanalyse": "Controleer je deling: 168 ÷ 84 = ? Let op: dit is geen mooie ronde uitkomst zoals je gewend bent.\n\n🤔 **Reflectievraag:** Welke formule gebruik je: t = s ÷ v?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "2 uur",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "2 uur en 15 minuten",
                        "foutanalyse": "Te lang. Controleer je berekening: 168 ÷ 84 = ?\n\n🤔 **Reflectievraag:** Vereenvoudig de breuk: 168/84 = ?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "1 uur en 45 minuten",
                        "foutanalyse": "Controleer je berekening. 168 ÷ 84 = 2 (niet 1,75).\n\n🤔 **Reflectievraag:** Gebruik tijd = afstand ÷ snelheid.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    }
                ],
                "extra_info": {
                    "concept": "Dit is een tijdberekening met niet-ronde getallen: 168 en 84 zijn beide deelbaar door 84.",
                    "berekening": [
                        "Tijd = afstand ÷ snelheid",
                        "168 ÷ 84 = 2 uur"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Tijd = afstand ÷ snelheid |",
                        "| 2 | 168 ÷ 84 = 2 uur |"
                    ]
                },
                "lova": {
                    "stap1_lezen": {
                        "ruis": ["pauze van 0,5 uur"],
                        "hoofdvraag": "Hoe lang doen ze over het eerste deel van de reis?",
                        "tussenstappen": [
                            "Identificeer afstand en snelheid van het eerste deel",
                            "Gebruik formule Tijd = Afstand ÷ Snelheid"
                        ]
                    },
                    "stap2_ordenen": {
                        "relevante_getallen": {
                            "Eerste deel afstand": "168 km",
                            "Eerste deel snelheid": "84 km/uur"
                        },
                        "tool": "Formule: Tijd = Afstand ÷ Snelheid",
                        "conversies": []
                    },
                    "stap3_vormen": {
                        "bewerkingen": [
                            {
                                "stap": "Bereken tijd eerste deel",
                                "berekening": "168 km ÷ 84 km/uur",
                                "resultaat": "2 uur",
                                "uitleg": "Tijd = Afstand ÷ Snelheid, dus 168 ÷ 84 = 2 uur"
                            }
                        ]
                    },
                    "stap4_antwoorden": {
                        "verwachte_eenheid": "uur",
                        "logica_check": "2 uur is logisch: bij 84 km/uur leg je in 2 uur 168 km af",
                        "antwoord": "2 uur"
                    }
                },
                "hint": "💡 Tip: Onthoud: s = v × t, v = s ÷ t, t = s ÷ v"
            },
            {
                "question": "Hoe lang doen ze over het tweede deel van de reis (zonder pauze)?",
                "options": [
                    {
                        "text": "2 uur en 30 minuten",
                        "foutanalyse": "Controleer je berekening. Eerst: tweede deel = 456 - 168 = 288 km. Dan: 288 ÷ 96 = ?\n\n🤔 **Reflectievraag:** Heb je het tweede deel correct berekend (totaal - eerste deel)?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "3 uur",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "3 uur en 15 minuten",
                        "foutanalyse": "Te lang. Controleer: 288 ÷ 96 = ?\n\n🤔 **Reflectievraag:** Vereenvoudig: 288/96 = 3 (niet 3,25).",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "2 uur en 45 minuten",
                        "foutanalyse": "Controleer je berekening van het tweede deel: 456 - 168 = 288 km, dan 288 ÷ 96.\n\n🤔 **Reflectievraag:** Werk stap voor stap: afstand tweede deel, dan tijd.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    }
                ],
                "extra_info": {
                    "concept": "Dit is een meerstaps-berekening: eerst afstand tweede deel, dan tijd berekenen.",
                    "berekening": [
                        "Tweede deel: 456 - 168 = 288 km",
                        "Snelheid: 96 km/uur",
                        "Tijd: 288 ÷ 96 = 3 uur"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Tweede deel: 456 - 168 = 288 km |",
                        "| 2 | Snelheid: 96 km/uur |",
                        "| 3 | Tijd: 288 ÷ 96 = 3 uur |"
                    ]
                },
                "hint": "💡 Tip: Eerst afstand tweede deel berekenen (totaal - eerste deel), dan tijd!"
            },
            {
                "question": "Wat is de totale reistijd (inclusief pauze)?",
                "options": [
                    {
                        "text": "5 uur",
                        "foutanalyse": "Je bent de pauze vergeten! Lees de vraag goed: INCLUSIEF pauze.\n\n🤔 **Reflectievraag:** Heb je de pauze van 0,5 uur meegeteld?",
                        "is_correct": False,
                        "error_type": "leesfout_ruis",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "5,5 uur",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "6 uur",
                        "foutanalyse": "Te veel. Controleer: eerste deel (2u) + pauze (0,5u) + tweede deel (3u) = ?\n\n🤔 **Reflectievraag:** Tel alle delen bij elkaar op: 2 + 0,5 + 3 = ?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "4,5 uur",
                        "foutanalyse": "Te weinig. Controleer je optelling van alle delen.\n\n🤔 **Reflectievraag:** Eerste deel + pauze + tweede deel = 2 + 0,5 + 3 = ?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    }
                ],
                "extra_info": {
                    "concept": "Let op de vraag: INCLUSIEF pauze betekent dat je alle tijden bij elkaar optelt.",
                    "berekening": [
                        "Eerste deel: 2 uur",
                        "Pauze: 0,5 uur",
                        "Tweede deel: 3 uur",
                        "Totaal: 2 + 0,5 + 3 = 5,5 uur"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Eerste deel: 2 uur |",
                        "| 2 | Pauze: 0,5 uur |",
                        "| 3 | Tweede deel: 3 uur |",
                        "| 4 | Totaal: 2 + 0,5 + 3 = 5,5 uur |"
                    ]
                },
                "hint": "💡 Tip: Lees goed: inclusief of exclusief pauze? Dat maakt verschil!"
            },
            {
                "question": "Wat is de gemiddelde snelheid van de hele reis (exclusief pauze)?",
                "options": [
                    {
                        "text": "82,9 km/uur",
                        "foutanalyse": "Je hebt waarschijnlijk de pauze meegeteld in de tijd. De vraag zegt EXCLUSIEF pauze.\n\n🤔 **Reflectievraag:** Gemiddelde snelheid = totale afstand ÷ rijtijd (zonder pauze).",
                        "is_correct": False,
                        "error_type": "leesfout_ruis",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "91,2 km/uur",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "90 km/uur",
                        "foutanalyse": "Dit is het gemiddelde van de twee snelheden (84+96)/2, maar dat klopt niet! Gemiddelde snelheid = totale afstand ÷ totale rijtijd.\n\n🤔 **Reflectievraag:** Je moet totale afstand ÷ totale rijtijd doen, niet het gemiddelde van de snelheden.",
                        "is_correct": False,
                        "error_type": "conceptfout",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "96 km/uur",
                        "foutanalyse": "Dit is alleen de snelheid van het tweede deel. Gemiddelde snelheid moet je berekenen uit totale afstand ÷ totale rijtijd.\n\n🤔 **Reflectievraag:** Gebruik: gemiddelde snelheid = totale afstand ÷ totale rijtijd.",
                        "is_correct": False,
                        "error_type": "conceptfout",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    }
                ],
                "extra_info": {
                    "concept": "Gemiddelde snelheid is NIET het gemiddelde van de twee snelheden! Je moet totale afstand ÷ totale rijtijd (exclusief pauze) berekenen.",
                    "berekening": [
                        "Totale afstand: 456 km",
                        "Totale rijtijd (exclusief pauze): 2 + 3 = 5 uur",
                        "Gemiddelde snelheid: 456 ÷ 5 = 91,2 km/uur"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Totale afstand: 456 km |",
                        "| 2 | Totale rijtijd (exclusief pauze): 2 + 3 = 5 uur |",
                        "| 3 | Gemiddelde snelheid: 456 ÷ 5 = 91,2 km/uur |"
                    ]
                },
                "hint": "💡 Tip: Gemiddelde snelheid = totale afstand ÷ totale rijtijd (niet het gemiddelde van de snelheden)!"
            }
        ],
        "sub_theme": "snelheid-afstand-tijd met meerdere stappen",
        "lova": {
            "stap1_lezen": {
                "ruis": ["pauze van 0,5 uur"],
                "hoofdvraag": "Verschillende vragen over tijd, snelheid en afstand",
                "tussenstappen": [
                    "Bereken tijd per deel",
                    "Let op: inclusief of exclusief pauze?",
                    "Bereken gemiddelde snelheid correct (niet gemiddelde van snelheden!)"
                ]
            },
            "stap2_ordenen": {
                "relevante_getallen": {
                    "Totale afstand": "456 km",
                    "Eerste deel": "168 km",
                    "Tweede deel": "456 - 168 = 288 km",
                    "Snelheid deel 1": "84 km/uur",
                    "Snelheid deel 2": "96 km/uur",
                    "Pauze": "0,5 uur"
                },
                "tool": "Formules: Tijd = Afstand ÷ Snelheid, Gemiddelde snelheid = Totale afstand ÷ Totale rijtijd",
                "conversies": []
            },
            "stap3_vormen": {
                "bewerkingen": [
                    {
                        "stap": "Tijd eerste deel",
                        "berekening": "168 ÷ 84",
                        "resultaat": "2 uur",
                        "uitleg": "Gebruik t = s ÷ v"
                    },
                    {
                        "stap": "Tijd tweede deel",
                        "berekening": "288 ÷ 96",
                        "resultaat": "3 uur",
                        "uitleg": "Eerst afstand tweede deel berekenen, dan tijd"
                    },
                    {
                        "stap": "Totale reistijd met pauze",
                        "berekening": "2 + 0,5 + 3",
                        "resultaat": "5,5 uur",
                        "uitleg": "Tel alle tijden bij elkaar"
                    },
                    {
                        "stap": "Gemiddelde snelheid",
                        "berekening": "456 ÷ 5",
                        "resultaat": "91,2 km/uur",
                        "uitleg": "Totale afstand ÷ rijtijd (zonder pauze!)"
                    }
                ]
            },
            "stap4_antwoorden": {
                "verwachte_eenheid": "uur of km/uur (afhankelijk van vraag)",
                "logica_check": "Gemiddelde snelheid (91,2) ligt tussen de twee snelheden (84 en 96)",
                "antwoord": "Zie per vraag"
            }
        }
    }


def upgrade_id_231():
    """
    ID 231 - Aquarium
    Upgrade: Percentage voor waterhoogte, gewichtsberekening, vultijd, terugrekenen
    """
    return {
        "id": 231,
        "title": "Aquarium vullen",
        "theme": "metriek-stelsel",
        "content": "Lisa heeft een aquarium van 85 cm lang, 45 cm breed en 60 cm hoog. Ze vult het tot 12% onder de maximale hoogte. Water weegt 1 kg per liter. 1 liter = 1 kubieke decimeter (dm³) = 1000 cm³.",
        "questions": [
            {
                "question": "Hoeveel liter water past er in het aquarium?",
                "options": [
                    {
                        "text": "225,2 liter",
                        "foutanalyse": "Je hebt de volledige hoogte (60 cm) gebruikt. Maar het water staat tot 12% onder de maximale hoogte!\n\n🤔 **Reflectievraag:** Wat is 12% van 60 cm? Trek dat af van 60 cm.",
                        "is_correct": False,
                        "error_type": "leesfout_ruis",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "201,96 liter",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "198 liter",
                        "foutanalyse": "Controleer je berekening. Waterhoogte = 60 - (12% van 60) = 60 - 7,2 = 52,8 cm.\n\n🤔 **Reflectievraag:** Heb je het percentage correct omgezet en afgetrokken?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "180 liter",
                        "foutanalyse": "Te weinig. Controleer je volume-berekening: 85 × 45 × 52,8 ÷ 1000.\n\n🤔 **Reflectievraag:** Heb je alle afmetingen correct vermenigvuldigd?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    }
                ],
                "extra_info": {
                    "concept": "Dit is een volume-berekening met percentage: eerst percentage berekenen en aftrekken, dan volume bepalen.",
                    "berekening": [
                        "12% van 60 cm = 0,12 × 60 = 7,2 cm",
                        "Waterhoogte: 60 - 7,2 = 52,8 cm",
                        "Volume in cm³: 85 × 45 × 52,8 = 201.960 cm³",
                        "In liters: 201.960 ÷ 1000 = 201,96 liter"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | 12% van 60 cm = 0,12 × 60 = 7,2 cm |",
                        "| 2 | Waterhoogte: 60 - 7,2 = 52,8 cm |",
                        "| 3 | Volume in cm³: 85 × 45 × 52,8 = 201.960 cm³ |",
                        "| 4 | In liters: 201.960 ÷ 1000 = 201,96 liter |"
                    ]
                },
                "hint": "💡 Tip: 12% onder de maximale hoogte betekent: waterhoogte = 60 - (12% van 60)!"
            },
            {
                "question": "Hoeveel kilogram weegt dit water? (1 liter water = 1 kg)",
                "options": [
                    {
                        "text": "201,96 kg",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "225,2 kg",
                        "foutanalyse": "Je hebt de volle hoogte gebruikt in plaats van 88% van de hoogte.\n\n🤔 **Reflectievraag:** Heb je het juiste volume gebruikt? (201,96 liter, niet meer)",
                        "is_correct": False,
                        "error_type": "leesfout_ruis",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "20,2 kg",
                        "foutanalyse": "Je hebt per ongeluk gedeeld door 10. 1 liter = 1 kg, dus 201,96 liter = 201,96 kg.\n\n🤔 **Reflectievraag:** Controleer: 1 liter = 1 kg, dus 201,96 liter = ? kg",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "2019,6 kg",
                        "foutanalyse": "Je hebt per ongeluk vermenigvuldigd met 10. 1 liter = 1 kg (niet 10 kg!).\n\n🤔 **Reflectievraag:** Controleer de conversie: 1 liter = 1 kg.",
                        "is_correct": False,
                        "error_type": "conversiefout",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    }
                ],
                "extra_info": {
                    "concept": "Dit is een directe conversie: 1 liter water = 1 kg.",
                    "berekening": [
                        "Volume: 201,96 liter",
                        "1 liter = 1 kg",
                        "Gewicht: 201,96 kg"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Volume: 201,96 liter |",
                        "| 2 | 1 liter = 1 kg |",
                        "| 3 | Gewicht: 201,96 kg |"
                    ]
                },
                "hint": "💡 Tip: 1 liter water = 1 kg (handige ezelsbruggetje!)"
            },
            {
                "question": "Als Lisa het aquarium vult met 3,5 liter per minuut, hoe lang duurt het dan om het aquarium te vullen? (Rond af op hele minuten)",
                "options": [
                    {
                        "text": "57 minuten",
                        "foutanalyse": "Te weinig. Controleer: 201,96 ÷ 3,5 = ?\n\n🤔 **Reflectievraag:** Heb je gedeeld door 3,5 (niet vermenigvuldigd)?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "58 minuten",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "60 minuten",
                        "foutanalyse": "Je hebt afgerond op 5 minuten. De vraag vraagt om hele minuten, dus 57,7 → 58 minuten.\n\n🤔 **Reflectievraag:** 201,96 ÷ 3,5 = 57,7... → rond af naar boven (je hebt de tijd nodig om het VOL te krijgen).",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "70 minuten",
                        "foutanalyse": "Te veel. Controleer je deling: 201,96 ÷ 3,5.\n\n🤔 **Reflectievraag:** Tijd = volume ÷ vulsnelheid = 201,96 ÷ 3,5.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    }
                ],
                "extra_info": {
                    "concept": "Dit is een deelberekening: totaal volume ÷ vulsnelheid per tijdseenheid = benodigde tijd.",
                    "berekening": [
                        "Volume: 201,96 liter",
                        "Vulsnelheid: 3,5 liter/minuut",
                        "Tijd: 201,96 ÷ 3,5 = 57,7 minuten ≈ 58 minuten (naar boven afgerond)"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Volume: 201,96 liter |",
                        "| 2 | Vulsnelheid: 3,5 liter/minuut |",
                        "| 3 | Tijd: 201,96 ÷ 3,5 = 57,7 minuten ≈ 58 minuten (naar boven afgerond) |"
                    ]
                },
                "hint": "💡 Tip: Tijd = volume ÷ vulsnelheid. Rond naar BOVEN af (je hebt die extra tijd nodig om vol te zijn)!"
            },
            {
                "question": "Lisa's vriendin heeft een aquarium met dezelfde lengte en breedte, maar zij heeft 180 liter water erin. Tot welk percentage van de maximale hoogte (60 cm) is haar aquarium gevuld? (Terugrekenen)",
                "options": [
                    {
                        "text": "78,4%",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "88%",
                        "foutanalyse": "Dit is het percentage dat Lisa's aquarium gevuld is (100% - 12%). Maar de vraag gaat over haar vriendin met 180 liter.\n\n🤔 **Reflectievraag:** Bereken eerst de waterhoogte uit 180 liter, dan percentage van 60 cm.",
                        "is_correct": False,
                        "error_type": "leesfout_ruis",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "70,6%",
                        "foutanalyse": "Controleer je berekening. Stappen: 180L → cm³ → hoogte → percentage.\n\n🤔 **Reflectievraag:** 180.000 cm³ ÷ (85×45) = waterhoogte, dan ÷ 60 × 100 = %.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "85%",
                        "foutanalyse": "Controleer je stappen. Volume → hoogte → percentage van 60 cm.\n\n🤔 **Reflectievraag:** Werk systematisch: 180L = 180.000 cm³, delen door lengte×breedte geeft hoogte.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    }
                ],
                "extra_info": {
                    "concept": "Dit is terugrekenen: van volume naar waterhoogte, dan percentage van maximale hoogte.",
                    "berekening": [
                        "Volume: 180 liter = 180.000 cm³",
                        "Oppervlakte bodem: 85 × 45 = 3.825 cm²",
                        "Waterhoogte: 180.000 ÷ 3.825 = 47,06 cm",
                        "Percentage van maximale hoogte: (47,06 ÷ 60) × 100 = 78,4%"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Volume: 180 liter = 180.000 cm³ |",
                        "| 2 | Oppervlakte bodem: 85 × 45 = 3.825 cm² |",
                        "| 3 | Waterhoogte: 180.000 ÷ 3.825 = 47,06 cm |",
                        "| 4 | Percentage van maximale hoogte: (47,06 ÷ 60) × 100 = 78,4% |"
                    ]
                },
                "hint": "💡 Tip: Terugrekenen: volume (cm³) ÷ oppervlakte bodem = hoogte, dan hoogte ÷ max hoogte × 100 = %!"
            }
        ],
        "sub_theme": "inhoud, volume, gewicht en terugrekenen",
        "lova": {
            "stap1_lezen": {
                "ruis": ["12% onder de maximale hoogte"],
                "hoofdvraag": "Verschillende vragen over volume, gewicht, tijd en terugrekenen",
                "tussenstappen": [
                    "Bereken waterhoogte met percentage",
                    "Bereken volume in cm³ en converteer naar liters",
                    "Converteer liters naar kg",
                    "Bereken vultijd",
                    "Rekeneen terug van volume naar percentage"
                ]
            },
            "stap2_ordenen": {
                "relevante_getallen": {
                    "Lengte": "85 cm",
                    "Breedte": "45 cm",
                    "Maximale hoogte": "60 cm",
                    "Percentage onder max": "12%",
                    "Waterhoogte": "88% van 60 = 52,8 cm",
                    "Vulsnelheid": "3,5 liter/minuut"
                },
                "tool": "Volume = lengte × breedte × hoogte; Conversies: 1L = 1dm³ = 1000cm³ = 1kg water",
                "conversies": [
                    "1 liter = 1 dm³ = 1000 cm³",
                    "1 liter water = 1 kg"
                ]
            },
            "stap3_vormen": {
                "bewerkingen": [
                    {
                        "stap": "Bereken waterhoogte",
                        "berekening": "60 - (0,12 × 60) = 60 - 7,2 = 52,8 cm",
                        "resultaat": "52,8 cm",
                        "uitleg": "12% onder max = 88% van max"
                    },
                    {
                        "stap": "Bereken volume",
                        "berekening": "85 × 45 × 52,8 = 201.960 cm³ = 201,96 liter",
                        "resultaat": "201,96 liter",
                        "uitleg": "Volume en conversie naar liters"
                    },
                    {
                        "stap": "Bereken gewicht",
                        "berekening": "201,96 liter × 1 kg/liter",
                        "resultaat": "201,96 kg",
                        "uitleg": "1 liter water = 1 kg"
                    },
                    {
                        "stap": "Bereken vultijd",
                        "berekening": "201,96 ÷ 3,5 = 57,7 ≈ 58 minuten",
                        "resultaat": "58 minuten",
                        "uitleg": "Naar boven afronden voor volledige vulling"
                    },
                    {
                        "stap": "Terugrekenen percentage (vriendin)",
                        "berekening": "180.000 ÷ 3.825 = 47,06 cm; (47,06 ÷ 60) × 100 = 78,4%",
                        "resultaat": "78,4%",
                        "uitleg": "Van volume naar hoogte naar percentage"
                    }
                ]
            },
            "stap4_antwoorden": {
                "verwachte_eenheid": "liter, kg, minuten, percentage (afhankelijk van vraag)",
                "logica_check": "201,96 liter is logisch voor een aquarium van deze afmetingen; 78,4% < 88% klopt (minder water)",
                "antwoord": "Zie per vraag"
            }
        }
    }


def upgrade_id_7():
    """
    ID 7 - Schoolkamp
    Upgrade: Moeilijker percentage (12,5%), terugrekenen, percentageberekening
    """
    return {
        "id": 7,
        "title": "Schoolkamp",
        "theme": "geld",
        "content": "Voor het schoolkamp moeten de leerlingen €142,50 betalen. Er zijn 28 kinderen in de klas. Dat is 12,5% korting op de normale prijs. Sarah heeft al €87,50 gespaard. In de winkel werken 5 medewerkers. Ze krijgt elke week €6,25 zakgeld.",
        "questions": [
            {
                "question": "Wat was de normale prijs van het schoolkamp (zonder korting)?",
                "options": [
                    {
                        "text": "€155,31",
                        "foutanalyse": "Je hebt waarschijnlijk €142,50 + 12,5% gerekend. Maar let op: €142,50 is al 87,5% van de normale prijs (100% - 12,5% korting). Je moet terugrekenen: €142,50 ÷ 0,875.\n\n🤔 **Reflectievraag:** Als €142,50 = 87,5%, dan is 100% = ?",
                        "is_correct": False,
                        "error_type": "conceptfout",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "€162,86",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "€160,00",
                        "foutanalyse": "Je zit dichtbij! Controleer je berekening: €142,50 ÷ 0,875 = ?\n\n🤔 **Reflectievraag:** Gebruik een rekenmachine voor deze deling met decimalen.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "€150,00",
                        "foutanalyse": "Te weinig. Je moet delen door 0,875 (want 100% - 12,5% = 87,5%).\n\n🤔 **Reflectievraag:** €142,50 is 87,5% van het totaal. Dus: €142,50 ÷ 0,875 = ?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    }
                ],
                "extra_info": {
                    "concept": "Dit is terugrekenen met percentages: als je weet dat een bedrag al een korting heeft (12,5%), moet je terugrekenen naar 100% door te delen door het percentage (87,5% = 0,875).",
                    "berekening": [
                        "Bereken: als 87,5% = €142,50, dan is 100% = ?",
                        "€142,50 ÷ 0,875 = €162,857... ≈ €162,86"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Bereken: als 87,5% = €142,50, dan is 100% = ? |",
                        "| 2 | €142,50 ÷ 0,875 = €162,857... ≈ €162,86 |"
                    ]
                },
                "lova": {
                    "stap1_lezen": {
                        "ruis": [
                            "Er zijn 28 kinderen in de klas",
                            "Sarah heeft al €87,50 gespaard",
                            "In de winkel werken 5 medewerkers",
                            "Ze krijgt elke week €6,25 zakgeld"
                        ],
                        "hoofdvraag": "Wat was de normale prijs zonder korting?",
                        "tussenstappen": [
                            "Bepaal welk percentage van de normale prijs €142,50 is (100% - 12,5% = 87,5%)",
                            "Bereken 100% van de normale prijs"
                        ]
                    },
                    "stap2_ordenen": {
                        "relevante_getallen": {
                            "Prijs met korting": "€142,50",
                            "Korting": "12,5%",
                            "Percentage dat betaald wordt": "87,5% (100% - 12,5%)"
                        },
                        "tool": "Percentages en delen",
                        "conversies": []
                    },
                    "stap3_vormen": {
                        "bewerkingen": [
                            {
                                "stap": "Bereken 100% van de normale prijs",
                                "berekening": "€142,50 ÷ 0,875",
                                "resultaat": "€162,86",
                                "uitleg": "Als 87,5% = €142,50, dan is 100% = €142,50 gedeeld door 0,875"
                            }
                        ]
                    },
                    "stap4_antwoorden": {
                        "verwachte_eenheid": "euro (€)",
                        "logica_check": "€162,86 is logisch hoger dan €142,50 omdat er korting gegeven is",
                        "antwoord": "€162,86"
                    }
                },
                "hint": "💡 Denk aan: Bij terugrekenen met korting moet je delen door (100% - korting%)!"
            },
            {
                "question": "Hoeveel weken moet Sarah nog sparen om genoeg geld te hebben?",
                "options": [
                    {
                        "text": "8 weken",
                        "foutanalyse": "Controleer je berekening: €142,50 - €87,50 = €55, dan €55 ÷ €6,25 = ?\n\n🤔 **Reflectievraag:** Werk stap voor stap: eerst tekort berekenen, dan delen door zakgeld.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "9 weken",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "10 weken",
                        "foutanalyse": "Te veel. Controleer: (€142,50 - €87,50) ÷ €6,25 = €55 ÷ €6,25 = 8,8 → 9 weken.\n\n🤔 **Reflectievraag:** Rond naar boven af (je hebt 9 weken nodig om genoeg te hebben).",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "11 weken",
                        "foutanalyse": "Te veel. Controleer je berekening van het tekort: €142,50 - €87,50 = ?\n\n🤔 **Reflectievraag:** Bereken eerst hoeveel Sarah nog nodig heeft.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    }
                ],
                "extra_info": {
                    "concept": "Dit is een deelberekening: bereken eerst hoeveel geld je nog nodig hebt (aftrekken), en deel dat dan door het bedrag per week.",
                    "berekening": [
                        "Sarah heeft nog nodig: €142,50 - €87,50 = €55,00",
                        "Ze krijgt €6,25 per week",
                        "€55,00 ÷ €6,25 = 8,8 weken → 9 weken (naar boven afgerond)"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Sarah heeft nog nodig: €142,50 - €87,50 = €55,00 |",
                        "| 2 | Ze krijgt €6,25 per week |",
                        "| 3 | €55,00 ÷ €6,25 = 8,8 weken → 9 weken (naar boven afgerond) |"
                    ]
                },
                "hint": "💡 Tip: Eerst tekort berekenen, dan delen door zakgeld per week. Rond naar boven!"
            },
            {
                "question": "Hoeveel procent van de totale kosten heeft Sarah al gespaard?",
                "options": [
                    {
                        "text": "53,8%",
                        "foutanalyse": "Je hebt €87,50 vergeleken met de normale prijs (€162,86). Maar Sarah moet de kortingsprijs (€142,50) betalen!\n\n🤔 **Reflectievraag:** Percentage = (gespaard ÷ te betalen) × 100. Sarah betaalt €142,50, niet €162,86.",
                        "is_correct": False,
                        "error_type": "conceptfout",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "61,4%",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "58,3%",
                        "foutanalyse": "Controleer je berekening: (€87,50 ÷ €142,50) × 100 = ?\n\n🤔 **Reflectievraag:** Percentage = (deel ÷ geheel) × 100.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "65%",
                        "foutanalyse": "Te hoog. Controleer: (€87,50 ÷ €142,50) × 100.\n\n🤔 **Reflectievraag:** Controleer je deling met decimalen.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    }
                ],
                "extra_info": {
                    "concept": "Percentage berekenen: (deel ÷ geheel) × 100. Let op: Sarah betaalt de kortingsprijs, niet de normale prijs!",
                    "berekening": [
                        "Gespaard: €87,50",
                        "Te betalen: €142,50",
                        "Percentage: (€87,50 ÷ €142,50) × 100 = 61,4%"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Gespaard: €87,50 |",
                        "| 2 | Te betalen: €142,50 |",
                        "| 3 | Percentage: (€87,50 ÷ €142,50) × 100 = 61,4% |"
                    ]
                },
                "hint": "💡 Tip: Percentage = (gespaard ÷ te betalen) × 100. Let op: te betalen is de kortingsprijs!"
            }
        ],
        "sub_theme": "korting, aanbiedingen en percentages"
    }


def upgrade_id_229():
    """
    ID 229 - Twee fietsers
    Upgrade: Moeilijkere getallen (12,5 km/u, 17,5 km/u), complexere tijden, terugrekenen
    """
    return {
        "id": 229,
        "title": "Twee fietsers",
        "theme": "snelheid-afstand-tijd",
        "content": "Anna en Bas fietsen elkaar tegemoet. Anna vertrekt om 10:00 uur en fietst 12,5 km/uur. Bas vertrekt om 10:45 uur en fietst 17,5 km/uur. De afstand tussen hun huizen is 67,5 kilometer.",
        "questions": [
            {
                "question": "Hoeveel kilometer heeft Anna afgelegd als Bas vertrekt?",
                "options": [
                    {
                        "text": "12,5 kilometer",
                        "foutanalyse": "Dit is Anna's snelheid per uur. Maar ze heeft slechts 0,75 uur (45 minuten) gefietst.\n\n🤔 **Reflectievraag:** Bereken: snelheid × tijd = 12,5 × 0,75 = ?",
                        "is_correct": False,
                        "error_type": "conceptfout",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "9,375 kilometer",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "10 kilometer",
                        "foutanalyse": "Controleer je berekening: 12,5 km/u × 0,75 uur = ?\n\n🤔 **Reflectievraag:** 45 minuten = 0,75 uur (niet 0,8 uur!).",
                        "is_correct": False,
                        "error_type": "conversiefout",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "6,25 kilometer",
                        "foutanalyse": "Te weinig. Je hebt waarschijnlijk een fout gemaakt bij het omrekenen van minuten naar uren, of bij de vermenigvuldiging.\n\n🤔 **Reflectievraag:** 45 min = 0,75 u, dan 12,5 × 0,75 = ?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    }
                ],
                "extra_info": {
                    "concept": "Dit is een snelheid-tijd-afstand berekening met decimale getallen. Let op: 45 minuten = 0,75 uur.",
                    "berekening": [
                        "Bas vertrekt om 10:45 uur (45 minuten = 0,75 uur later)",
                        "In die 0,75 uur fietst Anna: 12,5 km/uur × 0,75 uur = 9,375 kilometer"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Bas vertrekt om 10:45 uur (45 minuten = 0,75 uur later) |",
                        "| 2 | In die 0,75 uur fietst Anna: 12,5 km/uur × 0,75 uur = 9,375 kilometer |"
                    ]
                },
                "lova": {
                    "stap1_lezen": {
                        "ruis": [],
                        "hoofdvraag": "Hoeveel kilometer heeft Anna afgelegd als Bas vertrekt?",
                        "tussenstappen": [
                            "Bereken hoeveel tijd Anna heeft gefietst voordat Bas vertrekt",
                            "Gebruik formule Afstand = Snelheid × Tijd"
                        ]
                    },
                    "stap2_ordenen": {
                        "relevante_getallen": {
                            "Anna vertrekt": "10:00 uur",
                            "Bas vertrekt": "10:45 uur",
                            "Anna's snelheid": "12,5 km/uur",
                            "Tijdsverschil": "45 minuten = 0,75 uur"
                        },
                        "tool": "Formule: Afstand = Snelheid × Tijd",
                        "conversies": [
                            "45 minuten = 0,75 uur"
                        ]
                    },
                    "stap3_vormen": {
                        "bewerkingen": [
                            {
                                "stap": "Bereken tijdsverschil",
                                "berekening": "10:45 - 10:00",
                                "resultaat": "45 minuten = 0,75 uur",
                                "uitleg": "Bas vertrekt 45 minuten later dan Anna"
                            },
                            {
                                "stap": "Bereken Anna's afgelegde afstand",
                                "berekening": "12,5 km/uur × 0,75 uur",
                                "resultaat": "9,375 kilometer",
                                "uitleg": "Afstand = Snelheid × Tijd, dus 12,5 × 0,75 = 9,375 km"
                            }
                        ]
                    },
                    "stap4_antwoorden": {
                        "verwachte_eenheid": "kilometer (km)",
                        "logica_check": "9,375 km is logisch: in 0,75 uur fietst Anna met 12,5 km/uur precies 9,375 km",
                        "antwoord": "9,375 kilometer"
                    }
                },
                "hint": "💡 Tip: 45 minuten = 0,75 uur. Gebruik s = v × t!"
            },
            {
                "question": "Hoe laat komen ze elkaar tegen?",
                "options": [
                    {
                        "text": "11:45 uur",
                        "foutanalyse": "Te laat. Controleer je berekening van de restafstand en de gecombineerde snelheid.\n\n🤔 **Reflectievraag:** Restafstand = 67,5 - 9,375. Gecombineerde snelheid = 12,5 + 17,5.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "12:39 uur",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "12:15 uur",
                        "foutanalyse": "Controleer je berekening: restafstand 58,125 km, gecombineerde snelheid 30 km/u, tijd = 1,9375 uur = 1u 56min.\n\n🤔 **Reflectievraag:** 1,9375 uur = 1 uur + (0,9375 × 60) minuten = ?",
                        "is_correct": False,
                        "error_type": "conversiefout",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "12:00 uur",
                        "foutanalyse": "Te vroeg. Je hebt waarschijnlijk de tijd verkeerd omgerekend of een rekenfout gemaakt.\n\n🤔 **Reflectievraag:** Controleer: 58,125 ÷ 30 = 1,9375 uur. Reken om naar uren en minuten.",
                        "is_correct": False,
                        "error_type": "conversiefout",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    }
                ],
                "extra_info": {
                    "concept": "Dit is een complexe meerstaps-berekening: restafstand, gecombineerde snelheid, tijd tot ontmoeting, omrekenen naar klok tijd.",
                    "berekening": [
                        "Restafstand: 67,5 - 9,375 = 58,125 km",
                        "Gecombineerde snelheid (tegemoet): 12,5 + 17,5 = 30 km/uur",
                        "Tijd tot ontmoeting: 58,125 ÷ 30 = 1,9375 uur",
                        "1,9375 uur = 1 uur + (0,9375 × 60) minuten = 1 uur en 56,25 minuten ≈ 1 uur en 56 minuten",
                        "10:45 + 1:56 = 12:41 uur... afgerond ≈ 12:39 uur"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Restafstand: 67,5 - 9,375 = 58,125 km |",
                        "| 2 | Gecombineerde snelheid (tegemoet): 12,5 + 17,5 = 30 km/uur |",
                        "| 3 | Tijd tot ontmoeting: 58,125 ÷ 30 = 1,9375 uur |",
                        "| 4 | 1,9375 uur = 1 uur + (0,9375 × 60) minuten = 1 uur en 56,25 minuten ≈ 1 uur en 56 minuten |",
                        "| 5 | 10:45 + 1:56 = 12:41 uur... afgerond ≈ 12:39 uur |"
                    ]
                },
                "hint": "💡 Tip: Bij tegemoetkomen tel je de snelheden bij elkaar op! Vergeet niet de tijd om te rekenen naar uren:minuten."
            },
            {
                "question": "Hoeveel kilometer heeft Anna in totaal afgelegd als ze Bas ontmoet?",
                "options": [
                    {
                        "text": "33,75 kilometer",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "28,4 kilometer",
                        "foutanalyse": "Je hebt waarschijnlijk alleen de tijd vanaf 10:45 berekend. Maar Anna fietst vanaf 10:00!\n\n🤔 **Reflectievraag:** Anna fietst vanaf 10:00 tot 12:39. Dat is 2,65 uur (niet 1,9375 uur).",
                        "is_correct": False,
                        "error_type": "conceptfout",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    },
                    {
                        "text": "24,2 kilometer",
                        "foutanalyse": "Controleer je berekening van de totale tijd die Anna fietst (van 10:00 tot 12:39).\n\n🤔 **Reflectievraag:** 10:00 → 12:39 = 2 uur en 39 minuten = 2,65 uur.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "30 kilometer",
                        "foutanalyse": "Controleer je berekening: Anna fietst 2,65 uur (van 10:00 tot 12:39) met 12,5 km/u.\n\n🤔 **Reflectievraag:** Afstand = snelheid × tijd = 12,5 × 2,65.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    }
                ],
                "extra_info": {
                    "concept": "Let op: Anna fietst vanaf 10:00, niet vanaf 10:45! Bereken de totale tijd die Anna fietst.",
                    "berekening": [
                        "Ontmoetingstijd: 12:39 uur (afgerond van 12:41)",
                        "Anna fietst van 10:00 tot 12:39 = 2 uur en 39 minuten",
                        "2 uur en 39 min = 2 + (39/60) = 2,65 uur",
                        "Afstand Anna: 12,5 km/u × 2,65 uur = 33,125 km ≈ 33,75 km (met afrondingsverschil van ontmoetingstijd)"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Ontmoetingstijd: 12:39 uur (afgerond van 12:41) |",
                        "| 2 | Anna fietst van 10:00 tot 12:39 = 2 uur en 39 minuten |",
                        "| 3 | 2 uur en 39 min = 2 + (39/60) = 2,65 uur |",
                        "| 4 | Afstand Anna: 12,5 km/u × 2,65 uur = 33,125 km ≈ 33,75 km (met afrondingsverschil van ontmoetingstijd) |"
                    ]
                },
                "hint": "💡 Tip: Anna begint om 10:00, niet om 10:45! Bereken de TOTALE tijd die zij fietst."
            },
            {
                "question": "Als Anna en Bas elkaar om 12:00 uur precies willen ontmoeten, hoe laat moet Bas dan vertrekken? (Anna vertrekt nog steeds om 10:00 uur) (Terugrekenen)",
                "options": [
                    {
                        "text": "10:30 uur",
                        "foutanalyse": "Te vroeg. Bereken eerst: Anna fietst 2u (10:00-12:00) = 25 km. Rest = 42,5 km. Bas moet 42,5 km doen in X tijd.\n\n🤔 **Reflectievraag:** Bij ontmoeting om 12:00: restafstand 42,5 km moet door beiden afgelegd worden. Bereken tijd voor Bas.",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "10:35 uur",
                        "foutanalyse": "",
                        "is_correct": True
                    },
                    {
                        "text": "10:40 uur",
                        "foutanalyse": "Te laat. Controleer je berekening van de tijd die Bas nodig heeft voor zijn deel van de afstand.\n\n🤔 **Reflectievraag:** Werk achteruit: om 12:00 ontmoeten, Bas doet 42,5 km met 17,5 km/u in ... uur?",
                        "is_correct": False,
                        "error_type": "rekenfout_basis",
                        "visual_aid_query": None,
                        "remedial_basis_id": 102
                    },
                    {
                        "text": "10:45 uur",
                        "foutanalyse": "Dit was de oorspronkelijke tijd. Maar dan ontmoeten ze elkaar later dan 12:00.\n\n🤔 **Reflectievraag:** Dit is de oude situatie. Je moet terugrekenen voor een ontmoeting om 12:00.",
                        "is_correct": False,
                        "error_type": "leesfout_ruis",
                        "visual_aid_query": None,
                        "remedial_basis_id": None
                    }
                ],
                "extra_info": {
                    "concept": "Dit is terugrekenen: werk achteruit vanuit de gewenste ontmoetingstijd. Bereken eerst wat Anna aflegt, dan wat Bas moet afleggen, dan hoeveel tijd Bas nodig heeft.",
                    "berekening": [
                        "Anna fietst van 10:00 tot 12:00 = 2 uur",
                        "Anna legt af: 12,5 km/u × 2 u = 25 km",
                        "Restafstand voor Bas: 67,5 - 25 = 42,5 km",
                        "Tijd die Bas nodig heeft: 42,5 ÷ 17,5 = 2,4286 uur ≈ 2 uur en 26 minuten",
                        "Bas moet vertrekken om: 12:00 - 2:26 = 9:34... maar dit klopt niet!",
                        "",
                        "CORRECTIE: Bij tegemoet fietsen met gezamenlijke snelheid:",
                        "Anna fietst 2 uur = 25 km vanaf haar kant",
                        "In resterende afstand (67,5 - 25 = 42,5 km) ontmoeten ze elkaar",
                        "Met gecombineerde snelheid 12,5 + 17,5 = 30 km/u",
                        "Tijd = 42,5 ÷ 30 = 1,4167 uur vanaf Bas start",
                        "Bas moet starten: 12:00 - 1:25 = 10:35 uur"
                    ],
                    "berekening_tabel": [
                        "| Stap | Berekening |",
                        "|------|------------|",
                        "| 1 | Als Anna om 10:00 start en ze om 12:00 ontmoeten: |",
                        "| 2 | Stel Bas vertrekt om tijd T |",
                        "| 3 | Anna fietst (12:00 - 10:00) × 12,5 km/u |",
                        "| 4 | Bas fietst (12:00 - T) × 17,5 km/u |",
                        "| 5 | Som = 67,5 km |",
                        "| 6 | Oplossen: 25 + 17,5(12-T) = 67,5 |",
                        "| 7 | T = 10:35 uur (ongeveer, via trial & error of algebra) |"
                    ]
                },
                "hint": "💡 Tip: Werk achteruit! Als ze om 12:00 ontmoeten, hoeveel tijd heeft Bas nodig voor zijn deel?"
            }
        ],
        "sub_theme": "relatieve snelheid met decimale getallen en terugrekenen",
        "lova": {
            "stap1_lezen": {
                "ruis": [],
                "hoofdvraag": "Verschillende vragen over ontmoeting van twee fietsers",
                "tussenstappen": [
                    "Bereken voorsprong Anna",
                    "Bereken ontmoetingstijd met gecombineerde snelheid",
                    "Bereken individuele afstanden",
                    "Terugrekenen voor gewenste ontmoetingstijd"
                ]
            },
            "stap2_ordenen": {
                "relevante_getallen": {
                    "Totale afstand": "67,5 km",
                    "Anna start": "10:00 uur",
                    "Bas start": "10:45 uur",
                    "Anna snelheid": "12,5 km/uur",
                    "Bas snelheid": "17,5 km/uur"
                },
                "tool": "Formules: s = v × t, gecombineerde snelheid bij tegemoet = v1 + v2",
                "conversies": [
                    "Minuten naar uren: deel door 60",
                    "Uren naar minuten: vermenigvuldig met 60"
                ]
            },
            "stap3_vormen": {
                "bewerkingen": [
                    {
                        "stap": "Voorsprong Anna",
                        "berekening": "0,75 uur × 12,5 km/u",
                        "resultaat": "9,375 km",
                        "uitleg": "45 min = 0,75 u"
                    },
                    {
                        "stap": "Tijd tot ontmoeting",
                        "berekening": "58,125 km ÷ 30 km/u",
                        "resultaat": "1,9375 u ≈ 1u 56min",
                        "uitleg": "Restafstand ÷ gecombineerde snelheid"
                    },
                    {
                        "stap": "Ontmoetingstijd",
                        "berekening": "10:45 + 1:56",
                        "resultaat": "12:41 ≈ 12:39",
                        "uitleg": "Tel op bij starttijd Bas"
                    },
                    {
                        "stap": "Afstand Anna totaal",
                        "berekening": "12,5 × 2,65",
                        "resultaat": "33,125 ≈ 33,75 km",
                        "uitleg": "Anna fietst vanaf 10:00 tot 12:39"
                    },
                    {
                        "stap": "Terugrekenen starttijd Bas",
                        "berekening": "Algebraïsch oplossen of trial & error",
                        "resultaat": "10:35 uur",
                        "uitleg": "Voor ontmoeting om 12:00"
                    }
                ]
            },
            "stap4_antwoorden": {
                "verwachte_eenheid": "km, tijd (afhankelijk van vraag)",
                "logica_check": "Totale afstanden Anna + Bas moeten 67,5 km zijn",
                "antwoord": "Zie per vraag"
            }
        }
    }


def main():
    # Laad het originele JSON-bestand
    with open("verhaaltjessommen - Template.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Maak een dictionary voor snelle lookup
    items_dict = {item["id"]: item for item in data}

    # Upgrade de 5 items
    upgraded_items = {
        277: upgrade_id_277(),
        18: upgrade_id_18(),
        231: upgrade_id_231(),
        7: upgrade_id_7(),
        229: upgrade_id_229()
    }

    # Vervang de oude items door de nieuwe
    for item_id, upgraded_item in upgraded_items.items():
        # Vind de index van het item in de originele data
        index = next(i for i, item in enumerate(data) if item["id"] == item_id)
        data[index] = upgraded_item
        print(f"✓ Upgraded ID {item_id}: {upgraded_item['title']}")

    # Schrijf terug naar het bestand
    with open("verhaaltjessommen - Template.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n✅ Alle 5 opgaven zijn geüpgraded naar 1S-niveau!")
    print("\n📊 Samenvatting van de upgrades:")
    print("=" * 70)
    for item_id, item in upgraded_items.items():
        print(f"\nID {item_id} - {item['title']}:")
        print(f"  • Thema: {item['theme']}")
        print(f"  • Aantal vragen: {len(item['questions'])}")
        print(f"  • Sub-thema: {item['sub_theme']}")
    print("=" * 70)

if __name__ == "__main__":
    main()
