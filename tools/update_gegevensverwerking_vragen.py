#!/usr/bin/env python3
"""
Update script voor gegevensverwerking-vragen in verhaaltjessommen
Voegt toe: hint, error_type, is_correct, reflectievragen, visual_aid_query, remedial_basis_id
"""

import json
import sys

def add_reflection_question(foutanalyse, error_type):
    """Voeg reflectievraag toe aan foutanalyse op basis van error type"""
    if not foutanalyse or foutanalyse.strip() == "":
        return ""

    # Als er al een reflectievraag is, skip
    if "**Reflectievraag:**" in foutanalyse:
        return foutanalyse

    # Genereer reflectievraag per error type
    reflections = {
        "conversiefout": "Zijn alle gegevens in dezelfde eenheid?",
        "leesfout_ruis": "Welke gegevens uit de tabel/grafiek heb je nodig?",
        "conceptfout": "Moet je optellen, aftrekken, of iets anders doen met de gegevens?",
        "rekenfout_basis": "Controleer je berekening met de juiste getallen uit de tabel/grafiek!"
    }

    reflection = reflections.get(error_type, "Wat ging er fout bij het interpreteren van de gegevens?")
    return f"{foutanalyse}\n\n🤔 **Reflectievraag:** {reflection}"

def determine_error_type(foutanalyse, option_text):
    """Bepaal error_type op basis van foutanalyse tekst"""
    foutanalyse_lower = foutanalyse.lower()

    # Conversie fouten
    if any(word in foutanalyse_lower for word in ['omrekenen', 'eenheid', 'verschillende']):
        return "conversiefout"

    # Lees fouten / ruis
    if any(word in foutanalyse_lower for word in ['vergeten', 'over het hoofd', 'niet gelezen', 'genegeerd', 'gemist', 'verkeerde kolom', 'verkeerde rij', 'fout afgelezen']):
        return "leesfout_ruis"

    # Concept fouten
    if any(word in foutanalyse_lower for word in ['verkeerde', 'concept', 'methode', 'aanpak', 'strategie', 'denkfout', 'optellen', 'aftrekken']):
        return "conceptfout"

    # Reken fouten
    if any(word in foutanalyse_lower for word in ['rekenfout', 'controleer', 'berekening', 'som', 'verschil']):
        return "rekenfout_basis"

    # Default
    return "rekenfout_basis"

def generate_hint(question_text, content):
    """Genereer hint voor de vraag"""
    question_lower = question_text.lower()

    # Specifieke hints voor gegevensverwerking vragen
    if "tabel" in question_lower or "grafiek" in question_lower or "staafdiagram" in question_lower:
        if "hoeveel" in question_lower and ("meer" in question_lower or "minder" in question_lower):
            return "💡 Tip: Lees de getallen af en bereken het verschil!"
        elif "totaal" in question_lower or "samen" in question_lower or "bij elkaar" in question_lower:
            return "💡 Tip: Tel alle relevante getallen bij elkaar op!"
        elif "meeste" in question_lower or "grootste" in question_lower:
            return "💡 Tip: Zoek de hoogste waarde in de tabel of grafiek!"
        elif "minste" in question_lower or "kleinste" in question_lower:
            return "💡 Tip: Zoek de laagste waarde in de tabel of grafiek!"
        else:
            return "💡 Tip: Lees de tabel/grafiek nauwkeurig af - let op de juiste rij en kolom!"
    elif "gemiddeld" in question_lower:
        return "💡 Tip: Tel alle waarden op en deel door het aantal!"
    elif "verschil" in question_lower:
        return "💡 Tip: Trek het kleinste getal af van het grootste getal!"
    elif "percentage" in question_lower or "procent" in question_lower:
        return "💡 Tip: Bereken (deel ÷ totaal) × 100!"
    else:
        return "💡 Tip: Lees de vraag en de gegevens zorgvuldig - welke informatie heb je nodig?"

def update_question(question, theme):
    """Update een enkele vraag met nieuwe velden"""
    if theme != "gegevensverwerking":
        return question

    # Voeg hint toe als die er nog niet is
    if "hint" not in question:
        question["hint"] = generate_hint(
            question.get("question", ""),
            ""  # content is hier niet beschikbaar
        )

    # Update opties
    correct_index = question.get("correct", 0)

    for i, option in enumerate(question.get("options", [])):
        # Voeg is_correct toe
        if "is_correct" not in option:
            option["is_correct"] = (i == correct_index)

        # Skip correcte opties
        if option.get("is_correct"):
            if "error_type" in option:
                del option["error_type"]
            if "visual_aid_query" in option:
                del option["visual_aid_query"]
            if "remedial_basis_id" in option:
                del option["remedial_basis_id"]
            continue

        foutanalyse = option.get("foutanalyse", "")

        # Voeg error_type toe als die er nog niet is
        if "error_type" not in option and foutanalyse:
            option["error_type"] = determine_error_type(foutanalyse, option.get("text", ""))

        # Voeg reflectievraag toe
        if foutanalyse and "**Reflectievraag:**" not in foutanalyse:
            error_type = option.get("error_type", "rekenfout_basis")
            option["foutanalyse"] = add_reflection_question(foutanalyse, error_type)

        # Voeg visual_aid_query toe (default null)
        if "visual_aid_query" not in option:
            option["visual_aid_query"] = None

        # Voeg remedial_basis_id toe (default null, behalve voor rekenfout_basis)
        if "remedial_basis_id" not in option:
            if option.get("error_type") == "rekenfout_basis":
                option["remedial_basis_id"] = 102  # Tafels oefening
            else:
                option["remedial_basis_id"] = None

    # Voeg berekening_tabel toe aan extra_info als die er nog niet is
    if "extra_info" in question and "berekening_tabel" not in question["extra_info"]:
        berekening = question["extra_info"].get("berekening", [])
        if berekening:
            # Maak simpele tabel
            tabel = [
                "| Stap | Berekening |",
                "|------|------------|"
            ]
            for i, stap in enumerate(berekening, 1):
                tabel.append(f"| {i} | {stap} |")
            question["extra_info"]["berekening_tabel"] = tabel

    return question

def main():
    input_file = "/home/user/websitesara/verhaaltjessommen - Template.json"
    output_file = input_file  # Overschrijf origineel

    print(f"📖 Lezen van {input_file}...")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Fout bij het lezen: {e}")
        sys.exit(1)

    print(f"✅ {len(data)} vragen geladen")

    # Update alle gegevensverwerking-vragen
    gegevensverwerking_count = 0
    updated_count = 0

    for item in data:
        theme = item.get("theme", "")

        if theme == "gegevensverwerking":
            gegevensverwerking_count += 1

            for question in item.get("questions", []):
                question_updated = update_question(question, theme)

                # Check of er wijzigingen zijn
                if "hint" in question_updated:
                    updated_count += 1

    print(f"🔍 Gevonden: {gegevensverwerking_count} gegevensverwerking-items")
    print(f"✏️  Geüpdatet: {updated_count} vragen")

    # Schrijf terug
    print(f"💾 Schrijven naar {output_file}...")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Fout bij het schrijven: {e}")
        sys.exit(1)

    print("✅ Klaar! Alle gegevensverwerking-vragen zijn geüpdatet.")
    print("\nNieuwe velden toegevoegd:")
    print("  ✓ hint")
    print("  ✓ is_correct")
    print("  ✓ error_type")
    print("  ✓ reflectievraag (in foutanalyse)")
    print("  ✓ visual_aid_query")
    print("  ✓ remedial_basis_id")
    print("  ✓ berekening_tabel")

if __name__ == "__main__":
    main()
