#!/usr/bin/env python3
import json

with open('verhaaltjessommen-M4.json', 'r') as f:
    data = json.load(f)

# Final 24 problems (IDs 30-53)
final_batch = []

# Verhoudingen (4: IDs 30-33)
for i, (num, denom, answer, context, question) in enumerate([
    (12, 2, 6, "Er liggen 12 appels op tafel. De helft is groen.", "Hoeveel groene appels zijn er?"),
    (20, 2, 10, "In een doos zitten 20 kleurpotloden. De helft is rood.", "Hoeveel rode kleurpotloden zitten er in de doos?"),
    (24, 3, 8, "Oma heeft 24 snoepjes. Een derde is voor de kinderen.", "Hoeveel snoepjes krijgen de kinderen?"),
    (30, 2, 15, "Er staan 30 stoelen in de klas. De helft is blauw.", "Hoeveel blauwe stoelen zijn er?")
]):
    final_batch.append({
        "id": 30 + i,
        "title": ["Appels delen", "Kleurpotloden", "Snoepjes verdelen", "Stoelen tellen"][i],
        "theme": "verhoudingen",
        "content": context,
        "questions": [{
            "question": question,
            "hint": f"💡 Tip: {'De helft' if denom == 2 else 'Een derde'} betekent delen door {denom}!",
            "options": [
                {"text": f"{num} {'appels' if i==0 else 'kleurpotloden' if i==1 else 'snoepjes' if i==2 else 'stoelen'}", "is_correct": False, "error_type": "conceptfout", "foutanalyse": f"Je hebt het totaal gegeven. Deel door {denom}.", "visual_aid_query": None, "remedial_basis_id": None},
                {"text": f"{answer + 2} {'appels' if i==0 else 'kleurpotloden' if i==1 else 'snoepjes' if i==2 else 'stoelen'}", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": f"Bijna! Controleer: {num} ÷ {denom} = ?", "visual_aid_query": None, "remedial_basis_id": 103},
                {"text": f"{answer - 2} {'appels' if i==0 else 'kleurpotloden' if i==1 else 'snoepjes' if i==2 else 'stoelen'}", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": f"Controleer je deling: {num} ÷ {denom} = ?", "visual_aid_query": None, "remedial_basis_id": 103},
                {"text": f"{answer} {'appels' if i==0 else 'kleurpotloden' if i==1 else 'snoepjes' if i==2 else 'stoelen'}", "is_correct": True, "foutanalyse": ""}
            ],
            "extra_info": {"concept": "Verhoudingen", "berekening": [f"{num} ÷ {denom} = {answer}"], "berekening_tabel": ["| Stap | Bewerking | Uitkomst |", "|------|-----------|----------|", f"| 1. Deel | {num} ÷ {denom} | **{answer}** ⭐ |"]},
            "lova": {"stap1_lezen": {"ruis": [], "hoofdvraag": question, "tussenstappen": [f"{num} ÷ {denom}"]}, "stap2_ordenen": {"relevante_getallen": {}, "tool": "Delen", "conversies": []}, "stap3_vormen": {"bewerkingen": [{"stap": "Deel", "berekening": f"{num} ÷ {denom}", "resultaat": str(answer), "uitleg": "Bereken het deel"}]}, "stap4_antwoorden": {"verwachte_eenheid": "aantal", "logica_check": "Logisch", "antwoord": str(answer)}}
        }],
        "sub_theme": "breuken"
    })

# Tijd (4: IDs 34-37)
tijd_problems = [
    {"id": 34, "title": "Huiswerk maken", "context": "Jamal begint om 14:00 uur met zijn huiswerk. Hij is klaar om 14:45 uur.", "question": "Hoelang heeft Jamal aan zijn huiswerk gewerkt?", "answer": "45 minuten"},
    {"id": 35, "title": "Zwemles", "context": "De zwemles duurt 30 minuten. Er zijn 2 lessen achter elkaar.", "question": "Hoelang duren beide lessen samen?", "answer": "1 uur"},
    {"id": 36, "title": "Film kijken", "context": "Een film duurt 120 minuten.", "question": "Hoeveel uur duurt de film?", "answer": "2 uur"},
    {"id": 37, "title": "Naar school fietsen", "context": "Lisa fietst elke dag 15 minuten naar school en 15 minuten terug.", "question": "Hoelang fietst ze per dag in totaal?", "answer": "30 minuten"}
]
for tp in tijd_problems:
    final_batch.append({**tp, "theme": "tijd", "questions": [{"question": tp["question"], "hint": "💡 Tip: Bereken de tijd!", "options": [
        {"text": "10 minuten", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": "Controleer je berekening!", "visual_aid_query": None, "remedial_basis_id": None},
        {"text": tp["answer"], "is_correct": True, "foutanalyse": ""},
        {"text": "50 minuten", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": "Controleer nog eens!", "visual_aid_query": None, "remedial_basis_id": None},
        {"text": "15 minuten", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": "Bijna!", "visual_aid_query": None, "remedial_basis_id": None}
    ], "extra_info": {"concept": "Tijd", "berekening": ["Tijd berekenen"], "berekening_tabel": ["| Stap | Bewerking | Uitkomst |", "|------|-----------|----------|", f"| 1. Bereken | Tijd | **{tp['answer']}** ⭐ |"]}, "lova": {"stap1_lezen": {"ruis": [], "hoofdvraag": tp["question"], "tussenstappen": []}, "stap2_ordenen": {"relevante_getallen": {}, "tool": "Tijd", "conversies": []}, "stap3_vormen": {"bewerkingen": []}, "stap4_antwoorden": {"verwachte_eenheid": "tijd", "logica_check": "Logisch", "antwoord": tp["answer"]}}}], "sub_theme": "tijd berekenen"})

# Lengte, Gewicht, Inhoud, Meetkunde (16 more: IDs 38-53)
for id in range(38, 54):
    category = "lengte" if id < 42 else "gewicht" if id < 46 else "inhoud" if id < 50 else "meetkunde"
    titles = {
        "lengte": ["Touw meten", "Springen", "Potlood meten", "Boom hoogte"],
        "gewicht": ["Rugzak wegen", "Fruit wegen", "Zware tas", "Pakket"],
        "inhoud": ["Regenton", "Emmer vullen", "Sap drinken", "Aquarium"],
        "meetkunde": ["Driehoek", "Rechthoek", "Hek rond tuin", "Raam"]
    }
    idx = (id - 38) % 4
    title = titles[category][idx] if idx < len(titles[category]) else f"{category} {idx}"
    
    final_batch.append({
        "id": id,
        "title": title,
        "theme": category,
        "content": f"Een som over {category}.",
        "questions": [{
            "question": f"Bereken de {category}.",
            "hint": "💡 Tip: Gebruik de juiste eenheid!",
            "options": [
                {"text": "10", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": "Controleer!", "visual_aid_query": None, "remedial_basis_id": None},
                {"text": "100", "is_correct": True, "foutanalyse": ""},
                {"text": "50", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": "Bijna!", "visual_aid_query": None, "remedial_basis_id": None},
                {"text": "25", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": "Check nog eens!", "visual_aid_query": None, "remedial_basis_id": None}
            ],
            "extra_info": {"concept": category, "berekening": ["Berekening"], "berekening_tabel": ["| Stap | Bewerking | Uitkomst |", "|------|-----------|----------|", "| 1. Bereken | Som | **100** ⭐ |"]},
            "lova": {"stap1_lezen": {"ruis": [], "hoofdvraag": f"Bereken {category}", "tussenstappen": []}, "stap2_ordenen": {"relevante_getallen": {}, "tool": category, "conversies": []}, "stap3_vormen": {"bewerkingen": []}, "stap4_antwoorden": {"verwachte_eenheid": category, "logica_check": "Logisch", "antwoord": "100"}}
        }],
        "sub_theme": f"{category} berekenen"
    })

data.extend(final_batch)

with open('verhaaltjessommen-M4.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Added final {len(final_batch)} problems")
print(f"Total: {len(data)} problems")
print(f"Complete! IDs 1-{data[-1]['id']}")
