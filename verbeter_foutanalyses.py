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
