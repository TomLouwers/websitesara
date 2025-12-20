#!/usr/bin/env python3
"""
Update script voor procenten-rente-vragen in verhaaltjessommen
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
        "conceptfout": "Welke formule hoort bij het berekenen van (samengestelde) rente?",
        "percentagefout": "Hoe reken je een percentage uit? Wat is de vermenigvuldigingsfactor?",
        "leesfout_ruis": "Welke informatie is belangrijk: enkelvoudige of samengestelde rente?",
        "rekenfout_basis": "Controleer je vermenigvuldiging nog eens - klopt dit?"
    }

    reflection = reflections.get(error_type, "Wat ging er fout in je redenering?")
    return f"{foutanalyse}\n\n🤔 **Reflectievraag:** {reflection}"

def determine_error_type(foutanalyse, option_text):
    """Bepaal error_type op basis van foutanalyse tekst"""
    foutanalyse_lower = foutanalyse.lower()

    # Concept fouten (vooral bij samengestelde interest)
    if any(word in foutanalyse_lower for word in ['samengestelde', 'compound', 'verkeerde methode', 'formule', 'concept', 'aanpak', 'denkfout']):
        return "conceptfout"

    # Percentage fouten
    if any(word in foutanalyse_lower for word in ['percentage', 'procent', '%', 'vermenigvuldigingsfactor', '0,', '1,']):
        return "percentagefout"

    # Lees fouten / ruis
    if any(word in foutanalyse_lower for word in ['vergeten', 'over het hoofd', 'niet gelezen', 'genegeerd', 'gemist', 'lees']):
        return "leesfout_ruis"

    # Reken fouten
    if any(word in foutanalyse_lower for word in ['rekenfout', 'controleer', 'berekening', 'vermenigvuldig', 'optellen', 'aftrekken']):
        return "rekenfout_basis"

    # Default
    return "conceptfout"

def generate_hint(question_text, content):
    """Genereer hint voor de vraag"""
    hints = {
        "samengestelde": "💡 Let op: Bij samengestelde interest bereken je elk jaar opnieuw over het nieuwe bedrag!",
        "compound": "💡 Let op: Bij samengestelde interest bereken je elk jaar opnieuw over het nieuwe bedrag!",
        "rente": "💡 Tip: Rente bereken je met: bedrag × rentepercentage (bijv. 0,03)!",
        "procent": "💡 Tip: Om een percentage te berekenen: deel door 100 (bijv. 3% = 0,03)!",
        "korting": "💡 Let op: Korting betekent het percentage aftrekken van 100%!",
        "hoeveel percent": "💡 Tip: Deel het deel door het geheel en vermenigvuldig met 100!",
        "na 2 jaar": "💡 Let op: Gebruik voor elk jaar het nieuwe bedrag, niet het startbedrag!",
        "na 3 jaar": "💡 Let op: Gebruik voor elk jaar het nieuwe bedrag, niet het startbedrag!",
    }

    question_lower = question_text.lower()
    content_lower = content.lower()

    for keyword, hint in hints.items():
        if keyword in question_lower or keyword in content_lower:
            return hint

    return "💡 Let op: Controleer of je het percentage correct omrekent naar een decimaal getal!"

def update_question(question, theme, content):
    """Update een enkele vraag met nieuwe velden"""
    if theme != "procenten-rente":
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
            error_type = option.get("error_type", "conceptfout")
            option["foutanalyse"] = add_reflection_question(foutanalyse, error_type)

        # Voeg visual_aid_query toe (default null)
        if "visual_aid_query" not in option:
            option["visual_aid_query"] = None

        # Voeg remedial_basis_id toe (default null, behalve voor rekenfout_basis)
        if "remedial_basis_id" not in option:
            if option.get("error_type") == "rekenfout_basis":
                option["remedial_basis_id"] = 102  # Tafels oefening
            elif option.get("error_type") == "percentagefout":
                option["remedial_basis_id"] = 105  # Procenten oefening
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

    # Update alle procenten-rente-vragen
    procenten_rente_count = 0
    updated_count = 0

    for item in data:
        theme = item.get("theme", "")

        if theme == "procenten-rente":
            procenten_rente_count += 1
            content = item.get("content", "")

            for question in item.get("questions", []):
                question_updated = update_question(question, theme, content)

                # Check of er wijzigingen zijn
                if "hint" in question_updated:
                    updated_count += 1

    print(f"🔍 Gevonden: {procenten_rente_count} procenten-rente-items")
    print(f"✏️  Geüpdatet: {updated_count} vragen")

    # Schrijf terug
    print(f"💾 Schrijven naar {output_file}...")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Fout bij het schrijven: {e}")
        sys.exit(1)

    print("✅ Klaar! Alle procenten-rente-vragen zijn geüpdatet.")
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
