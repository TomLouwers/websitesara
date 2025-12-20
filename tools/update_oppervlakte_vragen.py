#!/usr/bin/env python3
"""
Update script voor oppervlakte-vragen in verhaaltjessommen
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
        "conversiefout": "Welke eenheid moet je gebruiken: m², cm², dm²?",
        "leesfout_ruis": "Welke maten zijn belangrijk voor het berekenen van de oppervlakte?",
        "conceptfout": "Welke formule hoort bij deze vorm (rechthoek, driehoek, cirkel)?",
        "rekenfout_basis": "Controleer je vermenigvuldiging nog eens!"
    }

    reflection = reflections.get(error_type, "Wat ging er fout bij het berekenen van de oppervlakte?")
    return f"{foutanalyse}\n\n🤔 **Reflectievraag:** {reflection}"

def determine_error_type(foutanalyse, option_text):
    """Bepaal error_type op basis van foutanalyse tekst"""
    foutanalyse_lower = foutanalyse.lower()

    # Conversie fouten
    if any(word in foutanalyse_lower for word in ['omrekenen', 'eenheid', 'cm²', 'm²', 'dm²', 'mm²', 'conversie']):
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

    # Specifieke hints voor oppervlakte vragen
    if "rechthoek" in question_lower:
        return "💡 Tip: Oppervlakte rechthoek = lengte × breedte!"
    elif "vierkant" in question_lower:
        return "💡 Tip: Oppervlakte vierkant = zijde × zijde!"
    elif "driehoek" in question_lower:
        return "💡 Tip: Oppervlakte driehoek = (basis × hoogte) ÷ 2!"
    elif "cirkel" in question_lower:
        return "💡 Tip: Oppervlakte cirkel = π × straal² (π ≈ 3,14)!"
    elif "omtrek" in question_lower and "rechthoek" in question_lower:
        return "💡 Tip: Let op! Omtrek = 2 × (lengte + breedte), niet oppervlakte!"
    elif "omtrek" in question_lower and "vierkant" in question_lower:
        return "💡 Tip: Let op! Omtrek vierkant = 4 × zijde, niet oppervlakte!"
    elif "tuin" in question_lower or "veld" in question_lower or "kamer" in question_lower:
        return "💡 Tip: Bereken eerst de vorm (rechthoek, vierkant?) en gebruik dan de juiste formule!"
    elif "tegels" in question_lower or "tegeltjes" in question_lower:
        return "💡 Tip: Oppervlakte totaal ÷ oppervlakte per tegel = aantal tegels!"
    elif "cm²" in question_text or "m²" in question_text:
        return "💡 Tip: Let op de eenheden! 1 m² = 10.000 cm²!"
    else:
        return "💡 Tip: Bepaal eerst welke vorm het is, en gebruik dan de juiste formule!"

def update_question(question, theme):
    """Update een enkele vraag met nieuwe velden"""
    if theme != "oppervlakte":
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

    # Update alle oppervlakte-vragen
    oppervlakte_count = 0
    updated_count = 0

    for item in data:
        theme = item.get("theme", "")

        if theme == "oppervlakte":
            oppervlakte_count += 1

            for question in item.get("questions", []):
                question_updated = update_question(question, theme)

                # Check of er wijzigingen zijn
                if "hint" in question_updated:
                    updated_count += 1

    print(f"🔍 Gevonden: {oppervlakte_count} oppervlakte-items")
    print(f"✏️  Geüpdatet: {updated_count} vragen")

    # Schrijf terug
    print(f"💾 Schrijven naar {output_file}...")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Fout bij het schrijven: {e}")
        sys.exit(1)

    print("✅ Klaar! Alle oppervlakte-vragen zijn geüpdatet.")
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
