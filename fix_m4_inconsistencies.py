#!/usr/bin/env python3
import json

with open('verhaaltjessommen-M4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix Item 19
p19 = next(p for p in data if p['id'] == 19)
p19['questions'][0]['extra_info']['berekening'] = ["20 ÷ 4 = 5 stickers per vriendin"]
p19['questions'][0]['extra_info']['berekening_tabel'][2] = "| 1. Deel stickers | 20 ÷ 4 | **5 stickers** ⭐ |"
p19['questions'][0]['lova']['stap1_lezen']['tussenstappen'] = ["Deel 20 door 4"]
p19['questions'][0]['lova']['stap2_ordenen']['relevante_getallen'] = {"Totaal stickers": "20", "Aantal vriendinnen": "4"}
bewerking19 = {"stap": "Verdeel stickers", "berekening": "20 ÷ 4", "resultaat": "5", "uitleg": "Deel het totaal door het aantal vriendinnen"}
p19['questions'][0]['lova']['stap3_vormen']['bewerkingen'][0] = bewerking19
antwoord19 = {"verwachte_eenheid": "stickers (aantal)", "logica_check": "5 stickers is logisch: 4 × 5 = 20", "antwoord": "5 stickers"}
p19['questions'][0]['lova']['stap4_antwoorden'] = antwoord19

opts = p19['questions'][0]['options']
opts[0]['foutanalyse'] = "Dat is het aantal vriendinnen, niet het aantal stickers per vriendin. Bereken: 20 ÷ 4.\n\n🤔 **Reflectievraag:** Als je 20 stickers verdeelt over 4 vriendinnen, hoeveel krijgt elk?"
opts[1]['foutanalyse'] = "Bijna! Controleer: 20 ÷ 4 = ?\n\n🤔 **Reflectievraag:** Wat is 4 × 5? Past dat bij 20?"
opts[2]['foutanalyse'] = "Te weinig! Controleer je berekening: 20 ÷ 4 = ?\n\n🤔 **Reflectievraag:** Wat is 4 × 3?"

print("✓ Item 19 fixed")

# Fix Item 20
p20 = next(p for p in data if p['id'] == 20)
p20['questions'][0]['extra_info']['berekening'] = ["50 ÷ 10 = 5 stoelen per rij"]
p20['questions'][0]['extra_info']['berekening_tabel'][2] = "| 1. Deel stoelen | 50 ÷ 10 | **5 stoelen** ⭐ |"
p20['questions'][0]['lova']['stap1_lezen']['tussenstappen'] = ["Deel 50 door 10"]
p20['questions'][0]['lova']['stap2_ordenen']['relevante_getallen'] = {"Totaal stoelen": "50", "Aantal rijen": "10"}
bewerking20 = {"stap": "Verdeel stoelen", "berekening": "50 ÷ 10", "resultaat": "5", "uitleg": "Deel het totaal aantal stoelen door het aantal rijen"}
p20['questions'][0]['lova']['stap3_vormen']['bewerkingen'][0] = bewerking20
antwoord20 = {"verwachte_eenheid": "stoelen (aantal)", "logica_check": "5 stoelen is logisch: 10 × 5 = 50", "antwoord": "5 stoelen"}
p20['questions'][0]['lova']['stap4_antwoorden'] = antwoord20

opts = p20['questions'][0]['options']
opts[0]['foutanalyse'] = "Dat is het aantal rijen. Je moet berekenen: 50 ÷ 10.\n\n🤔 **Reflectievraag:** Hoeveel stoelen zijn er in totaal?"
opts[1]['foutanalyse'] = "Bijna! Controleer: 50 ÷ 10 = ?\n\n🤔 **Reflectievraag:** Wat is 10 × 5?"
opts[2]['foutanalyse'] = "Te weinig! Controleer: 50 ÷ 10 = ?\n\n🤔 **Reflectievraag:** Wat is 10 × 4?"

print("✓ Item 20 fixed")

# Fix Item 26
p26 = next(p for p in data if p['id'] == 26)
p26['questions'][0]['extra_info']['berekening'] = ["3 × 6 = 18 eieren"]
p26['questions'][0]['extra_info']['berekening_tabel'][2] = "| 1. Vermenigvuldig | 3 × 6 | **18 eieren** ⭐ |"
p26['questions'][0]['lova']['stap1_lezen']['tussenstappen'] = ["3 × 6"]
p26['questions'][0]['lova']['stap2_ordenen']['relevante_getallen'] = {"Dozen": "3", "Eieren per doos": "6"}
bewerking26 = {"stap": "Vermenigvuldig", "berekening": "3 × 6", "resultaat": "18", "uitleg": "Vermenigvuldig aantal dozen met eieren per doos"}
p26['questions'][0]['lova']['stap3_vormen']['bewerkingen'][0] = bewerking26
antwoord26 = {"verwachte_eenheid": "eieren (aantal)", "logica_check": "18 eieren is logisch: 3 × 6 = 18", "antwoord": "18 eieren"}
p26['questions'][0]['lova']['stap4_antwoorden'] = antwoord26

opts = p26['questions'][0]['options']
opts[0]['foutanalyse'] = "Je hebt opgeteld. Je moet vermenigvuldigen: 3 × 6.\n\n🤔 **Reflectievraag:** Als elke doos 6 eieren heeft, hoeveel zijn er dan in 3 dozen?"
opts[1]['foutanalyse'] = "Bijna! Controleer: 3 × 6 = ?\n\n🤔 **Reflectievraag:** Wat is 3 × 5?"
opts[2]['foutanalyse'] = "Controleer je vermenigvuldiging: 3 × 6 = ?\n\n🤔 **Reflectievraag:** Wat is de tafel van 3?"

print("✓ Item 26 fixed")

# Fix Items 34-37 structure
print("\nFixing Items 34-37 structure...")
for item_id in [34, 35, 36, 37]:
    p = next((p for p in data if p['id'] == item_id), None)
    if p:
        if 'context' in p:
            p['content'] = p.pop('context')
        if 'question' in p:
            del p['question']
        if 'answer' in p:
            del p['answer']
        print(f"  ✓ Item {item_id} structure standardized")

with open('verhaaltjessommen-M4.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✅ ALL CORRECTIONS COMPLETE!")
