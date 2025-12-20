#!/usr/bin/env python3
"""
Script to add enhanced error analysis to all verhoudingen questions
in basisvaardigheden - Template.json
"""

import json
import re


def determine_error_type(option_index, correct_index, question_text, option_text):
    """Determine the error type based on the question and option"""

    # First option is often using wrong number or conceptual error
    if option_index == 0:
        if "vereenvoudig" in question_text.lower():
            return "conceptfout"
        return "conceptfout"

    # Second and third options are often calculation errors
    elif option_index in [1, 2] and option_index != correct_index:
        # Check if close to correct answer (likely calculation error)
        return "rekenfout_basis"

    # Last option is often leesfout or wrong approach
    else:
        if "vereenvoudig" in question_text.lower():
            return "leesfout_ruis"
        return "leesfout_ruis"


def generate_hint(title, question_text):
    """Generate contextual hints based on question type"""

    title_lower = title.lower()
    question_lower = question_text.lower()

    if "via 1" in title_lower:
        return "💡 Tip: Bereken eerst wat 1 eenheid (1 kg, 1 broodje, etc.) kost!"
    elif "dubbelen" in title_lower:
        return "💡 Tip: Kijk of je kunt dubbelen - dat is vaak makkelijker dan via 1!"
    elif "halveren" in title_lower:
        return "💡 Tip: Herken je dat het nieuwe aantal precies de helft is? Dan kan je ook de prijs halveren!"
    elif "vereenvoudig" in question_lower:
        return "💡 Tip: Zoek de grootste gemene deler (GGD) van beide getallen!"
    elif "omgekeerd" in title_lower:
        return "💡 Tip: Let op de eenheden - wat is gegeven en wat moet je berekenen?"
    elif "complex" in title_lower:
        return "💡 Tip: Ga altijd via 1 - dat is de veiligste methode bij kommagetallen!"
    else:
        return "💡 Tip: Maak een verhoudingstabel om het overzichtelijk te houden!"


def generate_foutanalyse(error_type, option_index, title, question_text, correct_option_text):
    """Generate error analysis text with reflection questions"""

    title_lower = title.lower()
    question_lower = question_text.lower()

    # Check title for question type since it's more reliable
    is_vereenvoudig = "vereenvoudig" in title_lower or "vereenvoudig" in question_lower

    if error_type == "conceptfout":
        if is_vereenvoudig:
            if option_index == 0:
                return "Je hebt de verhouding omgedraaid! Bij vereenvoudigen moet je beide getallen door hetzelfde getal delen.\n\n🤔 **Reflectievraag:** Wat betekent het om een verhouding te vereenvoudigen?"
            else:
                return "Dit is niet de meest vereenvoudigde vorm. Je moet beide getallen delen door de grootste gemene deler (GGD).\n\n🤔 **Reflectievraag:** Kun je beide getallen nog door een groter getal delen?"
        else:
            if "via 1" in title_lower:
                return "Je hebt niet via 1 gerekend. Bereken eerst wat 1 eenheid kost door te delen, en vermenigvuldig dan.\n\n🤔 **Reflectievraag:** Wat is de eerste stap bij 'via 1' methode?"
            elif "dubbelen" in title_lower:
                return "Je hebt de verkeerde factor gebruikt. Let op: dubbelen betekent keer 2!\n\n🤔 **Reflectievraag:** Als iets 2 keer zo groot wordt, wordt de prijs dan ook 2 keer zo groot?"
            elif "halveren" in title_lower:
                return "Je hebt de verkeerde factor gebruikt. Let op: halveren betekent delen door 2!\n\n🤔 **Reflectievraag:** Als je de helft koopt, betaal je dan de helft?"
            else:
                return f"Dit is niet de juiste aanpak voor deze verhouding. Gebruik de verhoudingsmethode: als het aantal groter wordt, wordt de prijs ook groter.\n\n🤔 **Reflectievraag:** Welke rekenbewerking gebruik je bij verhoudingen: optellen of vermenigvuldigen?"

    elif error_type == "rekenfout_basis":
        if is_vereenvoudig:
            return "Je berekening klopt niet helemaal. Controleer of je beide getallen door hetzelfde getal hebt gedeeld.\n\n🤔 **Reflectievraag:** Door welk getal heb je beide kanten gedeeld?"
        elif "via 1" in title_lower:
            return "Je methode is goed (via 1), maar er zit een rekenfout in je berekening. Controleer beide stappen!\n\n🤔 **Reflectievraag:** Heb je eerst correct gedeeld om 1 eenheid te vinden?"
        else:
            return "Je zit dichtbij! Er zit waarschijnlijk een kleine rekenfout in je vermenigvuldiging of deling.\n\n🤔 **Reflectievraag:** Heb je de juiste vermenigvuldigingsfactor gebruikt?"

    else:  # leesfout_ruis
        if is_vereenvoudig:
            return "Dit is niet de vereenvoudigde vorm. Je hebt de verhouding niet volledig vereenvoudigd.\n\n🤔 **Reflectievraag:** Kun je beide getallen nog verder delen?"
        else:
            return "Let goed op de getallen in de vraag! Je hebt waarschijnlijk de verkeerde getallen gebruikt of de vraag verkeerd gelezen.\n\n🤔 **Reflectievraag:** Wat wordt er precies gevraagd in de vraag?"


def generate_visual_aid_query(title):
    """Determine if visual aid is needed"""
    # For now, we'll use the verhoudingstabel visualizer for ratio tables
    if "verhoudingstabel" in title.lower():
        return "Verhoudingstabel visualisatie"
    return None


def get_remedial_basis_id(error_type):
    """Get remedial exercise ID based on error type"""
    if error_type == "rekenfout_basis":
        # 102 = basic multiplication/division exercises
        return 102
    return None


def create_berekening_tabel(lova_data):
    """Create markdown table from L.O.V.A. berekeningen"""
    if "stap3_vormen" not in lova_data:
        return []

    bewerkingen = lova_data["stap3_vormen"].get("bewerkingen", [])
    if not bewerkingen:
        return []

    tabel = [
        "| Stap | Bewerking | Uitkomst |",
        "|------|-----------|----------|"
    ]

    for i, bewerking in enumerate(bewerkingen, 1):
        stap = bewerking.get("stap", f"Stap {i}")
        calc = bewerking.get("berekening", "")
        result = bewerking.get("resultaat", "")

        # Add star to last row
        if i == len(bewerkingen):
            row = f"| {i}. {stap} | {calc} | **{result}** ⭐ |"
        else:
            row = f"| {i}. {stap} | {calc} | {result} |"
        tabel.append(row)

    return tabel


def update_question(question, title):
    """Update a single question with enhanced error analysis"""

    # Add hint if not present
    if "hint" not in question:
        question["hint"] = generate_hint(title, question["question"])

    # Convert options from array of strings to array of objects
    # OR update existing objects with new foutanalyse
    if isinstance(question["options"][0], str):
        old_options = question["options"]
        correct_index = question["correct"]
        new_options = []

        for i, option_text in enumerate(old_options):
            option_obj = {
                "text": option_text,
                "is_correct": i == correct_index
            }

            if i != correct_index:
                # Add error analysis for incorrect options
                error_type = determine_error_type(i, correct_index, question["question"], option_text)
                option_obj["error_type"] = error_type
                option_obj["foutanalyse"] = generate_foutanalyse(
                    error_type, i, title, question["question"], old_options[correct_index]
                )
                option_obj["visual_aid_query"] = generate_visual_aid_query(title)
                option_obj["remedial_basis_id"] = get_remedial_basis_id(error_type)
            else:
                # Correct option
                option_obj["foutanalyse"] = ""

            new_options.append(option_obj)

        question["options"] = new_options
    else:
        # Options are already objects - update foutanalyse for better messages
        correct_index = question["correct"]
        for i, option_obj in enumerate(question["options"]):
            if i != correct_index and "error_type" in option_obj:
                # Update the foutanalyse with improved message
                error_type = option_obj["error_type"]
                correct_text = question["options"][correct_index].get("text", "")
                option_obj["foutanalyse"] = generate_foutanalyse(
                    error_type, i, title, question["question"], correct_text
                )

    # Add berekening_tabel to extra_info if L.O.V.A. data exists
    if "lova" in question and "extra_info" in question:
        if "berekening_tabel" not in question["extra_info"]:
            berekening_tabel = create_berekening_tabel(question["lova"])
            if berekening_tabel:
                question["extra_info"]["berekening_tabel"] = berekening_tabel

    return question


def main():
    """Main function to update all verhoudingen questions"""

    filename = "basisvaardigheden - Template.json"

    print(f"Reading {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    question_count = 0

    print(f"Processing {len(data)} quizzes...")

    for quiz in data:
        if quiz.get("theme") == "verhoudingen":
            updated_count += 1
            print(f"  Updating quiz {quiz['id']}: {quiz['title']}")

            for question in quiz.get("questions", []):
                question_count += 1
                update_question(question, quiz["title"])

    print(f"\nUpdated {updated_count} verhoudingen quizzes ({question_count} questions)")

    # Write back to file
    print(f"Writing updated data to {filename}...")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ Done!")
    print(f"\nSummary:")
    print(f"  - {updated_count} verhoudingen quizzes updated")
    print(f"  - {question_count} questions enhanced with error analysis")
    print(f"  - Added hints, error types, reflection questions, and visual aids")


if __name__ == "__main__":
    main()
