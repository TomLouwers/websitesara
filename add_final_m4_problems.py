#!/usr/bin/env python3
import json

# Read current file
with open('verhaaltjessommen-M4.json', 'r') as f:
    data = json.load(f)

# Remaining problems data (IDs 26-53)
remaining_problems = []

# Vermenigvuldigen (2 more: 26-27)
remaining_problems.append({
    "id": 26,
    "title": "Eieren in dozen",
    "theme": "vermenigvuldigen",
    "content": "In een doos zitten 6 eieren. De boer heeft 7 dozen.",
    "questions": [{
        "question": "Hoeveel eieren heeft de boer in totaal?",
        "hint": "💡 Tip: Vermenigvuldig het aantal dozen met het aantal eieren per doos!",
        "options": [
            {"text": "13 eieren", "is_correct": False, "error_type": "conceptfout", "foutanalyse": "Je hebt opgeteld. Je moet vermenigvuldigen: 7 × 6.\n\n🤔 **Reflectievraag:** Als elke doos 6 eieren heeft, hoeveel zijn er dan in 7 dozen?", "visual_aid_query": None, "remedial_basis_id": None},
            {"text": "36 eieren", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": "Bijna! Controleer: 7 × 6 = ?", "visual_aid_query": None, "remedial_basis_id": 104},
            {"text": "48 eieren", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": "Controleer je vermenigvuldiging: 7 × 6 = ?", "visual_aid_query": None, "remedial_basis_id": 104},
            {"text": "42 eieren", "is_correct": True, "foutanalyse": ""}
        ],
        "extra_info": {"concept": "Vermenigvuldigen", "berekening": ["7 × 6 = 42 eieren"], "berekening_tabel": ["| Stap | Bewerking | Uitkomst |", "|------|-----------|----------|", "| 1. Vermenigvuldig | 7 × 6 | **42 eieren** ⭐ |"]},
        "lova": {"stap1_lezen": {"ruis": [], "hoofdvraag": "Hoeveel eieren in totaal?", "tussenstappen": ["7 × 6"]}, "stap2_ordenen": {"relevante_getallen": {"Dozen": "7", "Eieren per doos": "6"}, "tool": "Vermenigvuldigen", "conversies": []}, "stap3_vormen": {"bewerkingen": [{"stap": "Vermenigvuldig", "berekening": "7 × 6", "resultaat": "42", "uitleg": "Vermenigvuldig aantal dozen met eieren per doos"}]}, "stap4_antwoorden": {"verwachte_eenheid": "eieren", "logica_check": "42 is logisch", "antwoord": "42 eieren"}}
    }],
    "sub_theme": "tafel van 7"
})

remaining_problems.append({
    "id": 27,
    "title": "Wielen van fietsen",
    "theme": "vermenigvuldigen",
    "content": "Er staan 8 fietsen in de schuur. Elke fiets heeft 2 wielen.",
    "questions": [{
        "question": "Hoeveel wielen zijn er in totaal?",
        "hint": "💡 Tip: Vermenigvuldig het aantal fietsen met het aantal wielen per fiets!",
        "options": [
            {"text": "10 wielen", "is_correct": False, "error_type": "conceptfout", "foutanalyse": "Je hebt opgeteld. Je moet vermenigvuldigen: 8 × 2.", "visual_aid_query": None, "remedial_basis_id": None},
            {"text": "14 wielen", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": "Bijna! Controleer: 8 × 2 = ?", "visual_aid_query": None, "remedial_basis_id": 104},
            {"text": "18 wielen", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": "Controleer je vermenigvuldiging: 8 × 2 = ?", "visual_aid_query": None, "remedial_basis_id": 104},
            {"text": "16 wielen", "is_correct": True, "foutanalyse": ""}
        ],
        "extra_info": {"concept": "Vermenigvuldigen", "berekening": ["8 × 2 = 16 wielen"], "berekening_tabel": ["| Stap | Bewerking | Uitkomst |", "|------|-----------|----------|", "| 1. Vermenigvuldig | 8 × 2 | **16 wielen** ⭐ |"]},
        "lova": {"stap1_lezen": {"ruis": [], "hoofdvraag": "Hoeveel wielen in totaal?", "tussenstappen": ["8 × 2"]}, "stap2_ordenen": {"relevante_getallen": {"Fietsen": "8", "Wielen per fiets": "2"}, "tool": "Vermenigvuldigen", "conversies": []}, "stap3_vormen": {"bewerkingen": [{"stap": "Vermenigvuldig", "berekening": "8 × 2", "resultaat": "16", "uitleg": "Vermenigvuldig aantal fietsen met wielen per fiets"}]}, "stap4_antwoorden": {"verwachte_eenheid": "wielen", "logica_check": "16 is logisch", "antwoord": "16 wielen"}}
    }],
    "sub_theme": "tafel van 2"
})

# Geld (2 more: 28-29)
remaining_problems.append({
    "id": 28,
    "title": "Spaarpot",
    "theme": "geld",
    "content": "Liam heeft 10 munten van 50 cent in zijn spaarpot.",
    "questions": [{
        "question": "Hoeveel euro heeft Liam gespaard?",
        "hint": "💡 Tip: 10 munten van 50 cent = 10 × €0,50!",
        "options": [
            {"text": "€10", "is_correct": False, "error_type": "conceptfout", "foutanalyse": "Je hebt het aantal munten als euro's geteld. Bereken: 10 × €0,50.", "visual_aid_query": None, "remedial_basis_id": None},
            {"text": "€50", "is_correct": False, "error_type": "conceptfout", "foutanalyse": "Je hebt 10 × 50 gedaan, maar vergeten dat 50 cent = €0,50 is.", "visual_aid_query": None, "remedial_basis_id": None},
            {"text": "€4", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": "Bijna! Controleer: 10 × €0,50 = ?", "visual_aid_query": None, "remedial_basis_id": None},
            {"text": "€5", "is_correct": True, "foutanalyse": ""}
        ],
        "extra_info": {"concept": "Geld berekenen", "berekening": ["10 × €0,50 = €5"], "berekening_tabel": ["| Stap | Bewerking | Uitkomst |", "|------|-----------|----------|", "| 1. Vermenigvuldig | 10 × €0,50 | **€5** ⭐ |"]},
        "lova": {"stap1_lezen": {"ruis": [], "hoofdvraag": "Hoeveel euro gespaard?", "tussenstappen": ["10 × €0,50"]}, "stap2_ordenen": {"relevante_getallen": {"Munten": "10", "Waarde": "€0,50"}, "tool": "Vermenigvuldigen", "conversies": []}, "stap3_vormen": {"bewerkingen": [{"stap": "Bereken totaal", "berekening": "10 × €0,50", "resultaat": "€5", "uitleg": "Vermenigvuldig aantal munten met waarde"}]}, "stap4_antwoorden": {"verwachte_eenheid": "euro", "logica_check": "€5 is logisch", "antwoord": "€5"}}
    }],
    "sub_theme": "munten tellen"
})

remaining_problems.append({
    "id": 29,
    "title": "Speelgoed kopen",
    "theme": "geld",
    "content": "Een speelgoedauto kost €6. Isa geeft een briefje van €10.",
    "questions": [{
        "question": "Hoeveel wisselgeld krijgt Isa terug?",
        "hint": "💡 Tip: Trek de prijs af van het betaalde bedrag!",
        "options": [
            {"text": "€16", "is_correct": False, "error_type": "conceptfout", "foutanalyse": "Je hebt opgeteld. Wisselgeld bereken je door af te trekken: €10 - €6.", "visual_aid_query": None, "remedial_basis_id": None},
            {"text": "€6", "is_correct": False, "error_type": "conceptfout", "foutanalyse": "Dat is de prijs van de auto, niet het wisselgeld. Bereken: €10 - €6.", "visual_aid_query": None, "remedial_basis_id": None},
            {"text": "€5", "is_correct": False, "error_type": "rekenfout_basis", "foutanalyse": "Bijna! Controleer: €10 - €6 = ?", "visual_aid_query": None, "remedial_basis_id": 102},
            {"text": "€4", "is_correct": True, "foutanalyse": ""}
        ],
        "extra_info": {"concept": "Wisselgeld berekenen", "berekening": ["€10 - €6 = €4"], "berekening_tabel": ["| Stap | Bewerking | Uitkomst |", "|------|-----------|----------|", "| 1. Trek af | €10 - €6 | **€4** ⭐ |"]},
        "lova": {"stap1_lezen": {"ruis": [], "hoofdvraag": "Hoeveel wisselgeld?", "tussenstappen": ["€10 - €6"]}, "stap2_ordenen": {"relevante_getallen": {"Betaald": "€10", "Prijs": "€6"}, "tool": "Aftrekken", "conversies": []}, "stap3_vormen": {"bewerkingen": [{"stap": "Bereken wisselgeld", "berekening": "€10 - €6", "resultaat": "€4", "uitleg": "Trek prijs af van betaald bedrag"}]}, "stap4_antwoorden": {"verwachte_eenheid": "euro", "logica_check": "€4 is logisch", "antwoord": "€4"}}
    }],
    "sub_theme": "wisselgeld"
})

# Add the remaining problems to the data
data.extend(remaining_problems)

# Write back
with open('verhaaltjessommen-M4.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Added {len(remaining_problems)} problems")
print(f"Total now: {len(data)} problems")
print(f"IDs: {[p['id'] for p in data[-4:]]}")
