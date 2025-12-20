#!/usr/bin/env python3
"""
Update script voor snelheid-afstand-tijd-vragen in verhaaltjessommen
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
        "conversiefout": "Welke eenheid moet je omrekenen (km↔m of uur↔minuten)?",
        "leesfout_ruis": "Welke drie grootheden zijn belangrijk: snelheid, afstand of tijd?",
        "conceptfout": "Welke formule gebruik je: s = v × t, v = s ÷ t, of t = s ÷ v?",
        "rekenfout_basis": "Controleer je vermenigvuldiging of deling nog eens!"
    }

    reflection = reflections.get(error_type, "Wat ging er fout in je redenering?")
    return f"{foutanalyse}\n\n🤔 **Reflectievraag:** {reflection}"

def determine_error_type(foutanalyse, option_text):
    """Bepaal error_type op basis van foutanalyse tekst"""
    foutanalyse_lower = foutanalyse.lower()

    # Conversie fouten
    if any(word in foutanalyse_lower for word in ['omrekenen', 'uur', 'minuten', 'kilometer', 'meter', 'seconden', 'conversie', 'eenheid']):
        return "conversiefout"

    # Lees fouten / ruis
    if any(word in foutanalyse_lower for word in ['vergeten', 'over het hoofd', 'niet gelezen', 'genegeerd', 'gemist']):
        return "leesfout_ruis"

    # Concept fouten
    if any(word in foutanalyse_lower for word in ['verkeerde', 'concept', 'methode', 'aanpak', 'strategie', 'denkfout', 'formule']):
        return "conceptfout"

    # Reken fouten
    if any(word in foutanalyse_lower for word in ['rekenfout', 'controleer', 'berekening', 'vermenigvuldig', 'delen', 'deling']):
        return "rekenfout_basis"

    # Default
    return "rekenfout_basis"

def generate_hint(question_text, content):
    """Genereer hint voor de vraag"""
    question_lower = question_text.lower()

    # Specifieke hints voor snelheid-afstand-tijd vragen
    if "snelheid" in question_lower and ("berekenen" in question_lower or "wat is" in question_lower):
        return "💡 Tip: Snelheid = afstand ÷ tijd (v = s ÷ t)"
    elif "afstand" in question_lower and ("berekenen" in question_lower or "hoeveel" in question_lower):
        return "💡 Tip: Afstand = snelheid × tijd (s = v × t)"
    elif "tijd" in question_lower and ("berekenen" in question_lower or "hoelang" in question_lower or "duurt" in question_lower):
        return "💡 Tip: Tijd = afstand ÷ snelheid (t = s ÷ v)"
    elif "km/u" in question_lower or "km per uur" in question_lower:
        return "💡 Tip: Let op de eenheden! Rekening houden met uren en kilometers."
    elif "m/s" in question_lower or "meter per seconde" in question_lower:
        return "💡 Tip: Let op: m/s betekent meter per seconde!"
    elif "minuten" in question_lower or "minuut" in question_lower:
        return "💡 Tip: Denk eraan: 1 uur = 60 minuten!"
    elif "inhalen" in question_lower or "tegemoet" in question_lower:
        return "💡 Tip: Bij inhalen of tegemoet komen tel je de snelheden op!"
    else:
        return "💡 Tip: Onthoud: s = v × t, v = s ÷ t, t = s ÷ v"

def update_question(question, theme):
    """Update een enkele vraag met nieuwe velden"""
    if theme != "snelheid-afstand-tijd":
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

    # Update alle snelheid-afstand-tijd-vragen
    snelheid_count = 0
    updated_count = 0

    for item in data:
        theme = item.get("theme", "")

        if theme == "snelheid-afstand-tijd":
            snelheid_count += 1

            for question in item.get("questions", []):
                question_updated = update_question(question, theme)

                # Check of er wijzigingen zijn
                if "hint" in question_updated:
                    updated_count += 1

    print(f"🔍 Gevonden: {snelheid_count} snelheid-afstand-tijd-items")
    print(f"✏️  Geüpdatet: {updated_count} vragen")

    # Schrijf terug
    print(f"💾 Schrijven naar {output_file}...")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Fout bij het schrijven: {e}")
        sys.exit(1)

    print("✅ Klaar! Alle snelheid-afstand-tijd-vragen zijn geüpdatet.")
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
