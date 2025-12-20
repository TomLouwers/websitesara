#!/usr/bin/env python3
import json

# Template for creating problems
def create_problem(id, title, theme, content, question, hint, correct_answer, wrong_answers, operation, sub_theme, unit=""):
    """Create a complete M4 problem structure"""

    options = []
    for wa in wrong_answers:
        options.append({
            "text": wa["text"],
            "is_correct": False,
            "error_type": wa.get("error_type", "rekenfout_basis"),
            "foutanalyse": wa["foutanalyse"],
            "visual_aid_query": wa.get("visual_aid_query"),
            "remedial_basis_id": wa.get("remedial_basis_id")
        })

    options.append({
        "text": correct_answer,
        "is_correct": True,
        "foutanalyse": ""
    })

    problem = {
        "id": id,
        "title": title,
        "theme": theme,
        "content": content,
        "questions": [{
            "question": question,
            "hint": hint,
            "options": options,
            "extra_info": {
                "concept": f"Dit is een {theme}-som",
                "berekening": [operation],
                "berekening_tabel": [
                    "| Stap | Bewerking | Uitkomst |",
                    "|------|-----------|----------|",
                    f"| 1. Berekening | {operation} | **{correct_answer}** ⭐ |"
                ]
            },
            "lova": {
                "stap1_lezen": {"ruis": [], "hoofdvraag": question, "tussenstappen": [operation]},
                "stap2_ordenen": {"relevante_getallen": {}, "tool": theme.capitalize(), "conversies": []},
                "stap3_vormen": {"bewerkingen": [{"stap": "Bereken", "berekening": operation, "resultaat": correct_answer, "uitleg": "Voer de bewerking uit"}]},
                "stap4_antwoorden": {"verwachte_eenheid": unit, "logica_check": f"{correct_answer} is logisch", "antwoord": correct_answer}
            }
        }],
        "sub_theme": sub_theme
    }

    return problem

# Read existing file
with open('verhaaltjessommen-M4.json', 'r') as f:
    problems = json.load(f)

print(f"Starting with {len(problems)} problems")

# Add remaining 33 problems
new_problems = [
    # Aftrekken (3 more: 21-23)
    create_problem(21, "Speelgoed opruimen", "aftrekken", "Er liggen 45 speelgoedblokken op de grond. Kim ruimt er 18 op.",
                   "Hoeveel blokken liggen er nog op de grond?", "💡 Tip: Trek het aantal opgeruimde blokken af!", "27 blokken",
                   [{"text": "63 blokken", "error_type": "conceptfout", "foutanalyse": "Je hebt opgeteld. Kim ruimt blokken OP, dus er liggen er minder. Trek af: 45 - 18.\n\n🤔 **Reflectievraag:** Als je iets opruimt, liggen er dan meer of minder over?", "visual_aid_query": None, "remedial_basis_id": None},
                    {"text": "33 blokken", "foutanalyse": "Bijna! Controleer: 45 - 18 = ?", "remedial_basis_id": 102},
                    {"text": "37 blokken", "foutanalyse": "Controleer je aftrekking: 45 - 18 = ?", "remedial_basis_id": 102}],
                   "45 - 18 = 27", "aftrekken tot 100", "blokken"),

    create_problem(22, "Vogels op het dak", "aftrekken", "Er zitten 52 vogels op het dak. Dan vliegen er 27 weg.",
                   "Hoeveel vogels blijven er over?", "💡 Tip: Trek de weggevlogen vogels af!", "25 vogels",
                   [{"text": "79 vogels", "error_type": "conceptfout", "foutanalyse": "Je hebt opgeteld. Vogels vliegen WEG, dus blijven er minder over. Trek af: 52 - 27.", "visual_aid_query": None, "remedial_basis_id": None},
                    {"text": "35 vogels", "foutanalyse": "Bijna! Controleer: 52 - 27 = ?", "remedial_basis_id": 102},
                    {"text": "29 vogels", "foutanalyse": "Controleer je berekening: 52 - 27 = ?", "remedial_basis_id": 102}],
                   "52 - 27 = 25", "aftrekken tot 100", "vogels"),

    create_problem(23, "Pagina's lezen", "aftrekken", "Een boek heeft 80 pagina's. Sofie heeft al 43 pagina's gelezen.",
                   "Hoeveel pagina's moet Sofie nog lezen?", "💡 Tip: Trek de gelezen pagina's af!", "37 pagina's",
                   [{"text": "123 pagina's", "error_type": "conceptfout", "foutanalyse": "Je hebt opgeteld. Bereken hoeveel Sofie NOG moet lezen: 80 - 43.", "visual_aid_query": None, "remedial_basis_id": None},
                    {"text": "47 pagina's", "foutanalyse": "Bijna! Controleer: 80 - 43 = ?", "remedial_basis_id": 102},
                    {"text": "33 pagina's", "foutanalyse": "Controleer je aftrekking: 80 - 43 = ?", "remedial_basis_id": 102}],
                   "80 - 43 = 37", "aftrekken tot 100", "pagina's"),

    # Optellen (2 more: 24-25)
    create_problem(24, "Kralen rijgen", "optellen", "Maya heeft 23 rode kralen en 19 blauwe kralen.",
                   "Hoeveel kralen heeft Maya in totaal?", "💡 Tip: Tel de rode en blauwe kralen bij elkaar op!", "42 kralen",
                   [{"text": "4 kralen", "error_type": "conceptfout", "foutanalyse": "Je hebt afgetrokken. Tel de kralen bij elkaar op: 23 + 19.", "visual_aid_query": None, "remedial_basis_id": None},
                    {"text": "52 kralen", "foutanalyse": "Bijna! Controleer: 23 + 19 = ?", "remedial_basis_id": 101},
                    {"text": "32 kralen", "foutanalyse": "Controleer je optelling: 23 + 19 = ?", "remedial_basis_id": 101}],
                   "23 + 19 = 42", "optellen tot 100", "kralen"),

    create_problem(25, "Punten scoren", "optellen", "Bij een spelletje scoort team A 38 punten en team B 27 punten.",
                   "Hoeveel punten hebben beide teams samen?", "💡 Tip: Tel de punten van beide teams op!", "65 punten",
                   [{"text": "11 punten", "error_type": "conceptfout", "foutanalyse": "Je hebt afgetrokken. Tel de punten bij elkaar op: 38 + 27.", "visual_aid_query": None, "remedial_basis_id": None},
                    {"text": "55 punten", "foutanalyse": "Bijna! Controleer: 38 + 27 = ?", "remedial_basis_id": 101},
                    {"text": "75 punten", "foutanalyse": "Controleer je optelling: 38 + 27 = ?", "remedial_basis_id": 101}],
                   "38 + 27 = 65", "optellen tot 100", "punten"),
]

# Add all new problems
problems.extend(new_problems)

# Write back to file
with open('verhaaltjessommen-M4.json', 'w') as f:
    json.dump(problems, f, indent=2, ensure_ascii=False)

print(f"Added {len(new_problems)} problems")
print(f"Total problems now: {len(problems)}")
print(f"IDs added: {[p['id'] for p in new_problems]}")
