#!/usr/bin/env python3
"""
Script om foutanalyses te verbeteren in verhaaltjessommen - Template.json
Voegt diagnostische uitleg en reflectievragen toe waar deze ontbreken.
"""

import json

def verbeter_foutanalyses():
    # Laad de template
    with open('verhaaltjessommen - Template.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Verbeteringen per ID
    verbeteringen = {
        6: {  # Zwembad vullen - Optellen debiet
            0: {  # Vraag 1
                0: "Je hebt waarschijnlijk 240 - 180 = 60 berekend (aftrekken in plaats van optellen). Als beide kranen TEGELIJK open staan, moet je de hoeveelheden OPTELLEN: 240 + 180 = ?\n\n🤔 **Reflectievraag:** Als er 240 liter uit kraan A komt en 180 liter uit kraan B, hoeveel liter komt er dan in totaal in het zwembad?",
                # Optie 1 is correct
                2: "Je hebt alleen kraan A genomen (240 L/min) en kraan B vergeten! De vraag zegt 'beide kranen tegelijk'. Je moet beide debietsnelheden optellen: 240 + 180 = ?\n\n🤔 **Reflectievraag:** Hoeveel kranen staan er open volgens de vraag?",
                3: "Je hebt waarschijnlijk 240 × 2 = 480 berekend (verdubbeld), maar kraan B stroomt NIET even snel als kraan A! Kraan B = 180 L/min. Je moet OPTELLEN, niet verdubbelen: 240 + 180 = ?\n\n🤔 **Reflectievraag:** Zijn beide kranen even snel, of hebben ze verschillende snelheden?"
            },
            1: {  # Vraag 2
                0: "Je hebt een rekenfout gemaakt. Controleer je deling: 84.000 ÷ 420 = ? (niet 420). Let op dat je de juiste deler gebruikt (het antwoord uit vraag 1).\n\n🤔 **Reflectievraag:** Hoeveel liter per minuut stroomt er in het zwembad volgens vraag 1?",
                1: "Je hebt waarschijnlijk 84.000 ÷ 240 = 350 gerekend (alleen kraan A). Maar beide kranen staan open! Gebruik het juiste debiet uit vraag 1: 84.000 ÷ 420 = ?\n\n🤔 **Reflectievraag:** Heb je het antwoord uit vraag 1 (420 L/min) gebruikt voor deze berekening?",
                # Optie 2 is correct
                3: "Controleer je berekening. Je moet de totale inhoud (84.000 L) delen door het debiet per minuut uit vraag 1 (420 L/min). Bereken: 84.000 ÷ 420 = ?\n\n🤔 **Reflectievraag:** Welke rekenregel gebruik je om tijd te berekenen: delen of vermenigvuldigen?"
            }
        },
        9: {  # Groentekwekerij - Breuk van totaal
            0: {  # Vraag 1
                1: "Dit is de opbrengst van VORIG jaar! Je hebt je laten afleiden door ruis in de tekst. De vraag gaat over DIT seizoen. Je moet berekenen: als 45 kg = ⅓, dan is het totaal = 45 × 3.\n\n🤔 **Reflectievraag:** Gaat de vraag over vorig jaar of dit seizoen?",
                2: "Je hebt 45 × 2 = 90 berekend, maar 45 kg is ⅓ van het totaal, niet de helft! Om het totaal te vinden: 45 × 3 = ?\n\n🤔 **Reflectievraag:** Als 45 kg = ⅓ is, met hoeveel moet je dan vermenigvuldigen voor het hele totaal?",
                3: "Controleer je berekening. Als 45 kg = ⅓ van het totaal is, dan bereken je het totaal zo: 45 × 3 = ?\n\n🤔 **Reflectievraag:** Hoeveel keer past ⅓ in een heel (1)?"
            }
        },
        19: {  # Fruit verkopen - Verhoudingen
            0: {  # Vraag 1
                0: "Je hebt het aantal PEREN berekend in plaats van appels! De verhouding is 5:3 (appels:peren). Je berekende (3/8) × 64 = 24 peren. Voor appels moet je (5/8) × 64 berekenen.\n\n🤔 **Reflectievraag:** Staat het getal 5 voor appels of voor peren in de verhouding 5:3?",
                1: "Je hebt 64 ÷ 2 = 32 berekend (gehalveerd), maar vergeten dat de verhouding 5:3 is (NIET 1:1)! Je moet eerst de verhouding optellen: 5 + 3 = 8 delen. Appels = (5/8) × 64 = ?\n\n🤔 **Reflectievraag:** Zijn er evenveel appels als peren, of is de verhouding anders?",
                # Optie 2 is correct
                3: "Controleer je berekening met verhoudingen. Eerst bereken je het totaal aantal delen: 5 + 3 = 8. Dan bereken je appels: (5/8) × 64 = ?\n\n🤔 **Reflectievraag:** Hoeveel delen zijn er in totaal bij de verhouding 5:3?"
            }
        },
        2: {  # Voetbaltoernooi - Combinatoriek
            0: {  # Vraag 1
                0: "Je hebt waarschijnlijk 6 + 6 gerekend of een andere verkeerde berekening gemaakt. Bij 'elk team speelt tegen elk ander team' moet je bedenken: elk team speelt tegen 5 andere teams (niet tegen zichzelf). Dat is 6 × 5 = 30, maar dan tel je elke wedstrijd dubbel!\n\n🤔 **Reflectievraag:** Als team A tegen team B speelt, is dat dan 1 wedstrijd of 2 wedstrijden?",
                # Optie 1 is correct
                2: "Je bent dichtbij! Je hebt waarschijnlijk een rekenfout gemaakt. De formule is: (aantal teams × tegenstanders per team) ÷ 2. Controleer: (6 × 5) ÷ 2 = ?\n\n🤔 **Reflectievraag:** Hoeveel tegenstanders heeft elk team? (Hint: het totaal minus 1)",
                3: "Je hebt 6 × 5 = 30 berekend, maar vergeten te delen door 2! Als team A tegen team B speelt, tel je die wedstrijd twee keer: één keer bij A en één keer bij B. Je moet dus delen door 2 om dubbeltellingen te voorkomen.\n\n🤔 **Reflectievraag:** Als team A tegen team B speelt, is dat dan 1 wedstrijd of 2 verschillende wedstrijden?"
            },
            1: {  # Vraag 2
                0: "Je hebt waarschijnlijk alleen 12 toeschouwers genomen en vergeten te vermenigvuldigen. Je moet berekenen: aantal toeschouwers × aantal wedstrijden. Gebruik je antwoord uit vraag 1!\n\n🤔 **Reflectievraag:** Als er 12 toeschouwers bij elke wedstrijd zijn, hoeveel mensen zijn er dan in totaal bij 2 wedstrijden?",
                # Optie 1 is correct
                2: "Controleer je berekening. Heb je het juiste aantal wedstrijden gebruikt uit vraag 1? Het moet zijn: 12 toeschouwers × 15 wedstrijden = ?\n\n🤔 **Reflectievraag:** Hoeveel wedstrijden waren er volgens vraag 1?",
                3: "Je hebt waarschijnlijk het verkeerde aantal wedstrijden gebruikt (30 in plaats van 15). Controleer eerst je antwoord bij vraag 1. Het juiste aantal wedstrijden is 15, dus: 12 × 15 = ?\n\n🤔 **Reflectievraag:** Heb je de dubbeltelling bij vraag 1 correct verwerkt? Het antwoord moet 15 wedstrijden zijn, niet 30."
            }
        }
    }

    # Pas verbeteringen toe
    aanpassingen_gemaakt = 0
    for item in data:
        item_id = item.get('id')
        if item_id in verbeteringen and 'questions' in item:
            for q_idx, question in enumerate(item['questions']):
                if q_idx in verbeteringen[item_id] and 'options' in question:
                    for opt_idx, option in enumerate(question['options']):
                        if opt_idx in verbeteringen[item_id][q_idx]:
                            nieuwe_analyse = verbeteringen[item_id][q_idx][opt_idx]
                            oude_analyse = option.get('foutanalyse', '')

                            # Alleen updaten als de oude analyse zwak is (kort of leeg)
                            if len(oude_analyse) < 50 or '🤔' not in oude_analyse:
                                option['foutanalyse'] = nieuwe_analyse
                                aanpassingen_gemaakt += 1
                                print(f"✅ Verbeterd: ID {item_id}, Vraag {q_idx + 1}, Optie {opt_idx + 1}")
                                print(f"   OUD: {oude_analyse[:60]}...")
                                print(f"   NIEUW: {nieuwe_analyse[:60]}...")
                                print()

    # Schrijf terug
    with open('verhaaltjessommen - Template.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Klaar! {aanpassingen_gemaakt} foutanalyses verbeterd.")
    return aanpassingen_gemaakt

if __name__ == '__main__':
    verbeter_foutanalyses()
