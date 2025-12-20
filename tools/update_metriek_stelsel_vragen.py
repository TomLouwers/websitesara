#!/usr/bin/env python3
"""
Update script voor metriek-stelsel-vragen in verhaaltjessommen
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
        "conversiefout": "Welke eenheid moet je eerst omrekenen en met welke factor?",
        "leesfout_ruis": "Welke extra informatie in de tekst moet je meenemen?",
        "conceptfout": "Welke formule of regel hoort bij dit type meetkundevraag?",
        "rekenfout_basis": "Controleer je vermenigvuldiging of deling nog eens - klopt dit?"
    }

    reflection = reflections.get(error_type, "Wat ging er fout in je redenering?")
    return f"{foutanalyse}\n\n🤔 **Reflectievraag:** {reflection}"

def determine_error_type(foutanalyse, option_text):
    """Bepaal error_type op basis van foutanalyse tekst"""
    foutanalyse_lower = foutanalyse.lower()

    # Conversie fouten (meest voorkomend in metriek-stelsel)
    if any(word in foutanalyse_lower for word in ['omreken', 'conversie', 'cm', 'dm', 'meter', 'liter', 'gram', 'kilogram', 'eenheid']):
        return "conversiefout"

    # Lees fouten / ruis
    if any(word in foutanalyse_lower for word in ['vergeten', 'over het hoofd', 'niet gelezen', 'genegeerd', 'gemist', 'onder de rand', 'ruimte']):
        return "leesfout_ruis"

    # Concept fouten
    if any(word in foutanalyse_lower for word in ['verkeerde', 'concept', 'methode', 'aanpak', 'formule', 'volume', 'oppervlakte', 'denkfout']):
        return "conceptfout"

    # Reken fouten
    if any(word in foutanalyse_lower for word in ['rekenfout', 'controleer', 'berekening', 'vermenigvuldig', 'deel', 'optellen', 'aftrekken']):
        return "rekenfout_basis"

    # Default
    return "conversiefout"

def generate_hint(question_text, content):
    """Genereer hint voor de vraag"""
    hints = {
        "liter": "💡 Let op: 1 liter = 1 dm³ = 1000 cm³!",
        "kubieke": "💡 Tip: Volume bereken je met lengte × breedte × hoogte!",
        "volume": "💡 Tip: Volume bereken je met lengte × breedte × hoogte!",
        "centimeter": "💡 Let op: Controleer of alle maten in dezelfde eenheid staan!",
        "meter": "💡 Let op: 1 meter = 100 cm = 10 dm!",
        "kilogram": "💡 Let op: 1 kilogram = 1000 gram!",
        "gram": "💡 Let op: 1000 gram = 1 kilogram!",
        "oppervlakte": "💡 Tip: Oppervlakte bereken je met lengte × breedte!",
    }

    question_lower = question_text.lower()
    content_lower = content.lower()

    for keyword, hint in hints.items():
        if keyword in question_lower or keyword in content_lower:
            return hint

    return "💡 Let op: Zorg dat alle maten in dezelfde eenheid staan voordat je gaat rekenen!"

def update_question(question, theme, content):
    """Update een enkele vraag met nieuwe velden"""
    if theme != "metriek-stelsel":
        return question

    # Voeg hint toe als die er nog niet is
    if "hint" not in question:
        question["hint"] = generate_hint(
            question.get("question", ""),
            content
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
            error_type = option.get("error_type", "conversiefout")
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

    # Update alle metriek-stelsel-vragen
    metriek_count = 0
    updated_count = 0

    for item in data:
        theme = item.get("theme", "")

        if theme == "metriek-stelsel":
            metriek_count += 1
            content = item.get("content", "")

            for question in item.get("questions", []):
                question_updated = update_question(question, theme, content)

                # Check of er wijzigingen zijn
                if "hint" in question_updated:
                    updated_count += 1

    print(f"🔍 Gevonden: {metriek_count} metriek-stelsel-items")
    print(f"✏️  Geüpdatet: {updated_count} vragen")

    # Schrijf terug
    print(f"💾 Schrijven naar {output_file}...")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Fout bij het schrijven: {e}")
        sys.exit(1)

    print("✅ Klaar! Alle metriek-stelsel-vragen zijn geüpdatet.")
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
