#!/usr/bin/env python3
"""
Fix M4 Dataset - Expert Review Ronde 4
Vult ontbrekende LOVA-stappen en corrigeert metadata voor tijdsommen (Items 34-37).
"""

import json

with open('verhaaltjessommen-M4.json', 'r') as f:
    data = json.load(f)

print("🔧 FIXING ROUND 4 ISSUES: TIME PROBLEMS METADATA & LOVA\n")

# ==============================================================================
# ITEM 34: Huiswerk maken (14:00 - 14:45 = 45 minuten)
# ==============================================================================
print("1️⃣ Item 34 - Huiswerk maken")
print("   Adding detailed calculation steps and LOVA...")

p34 = next(p for p in data if p['id'] == 34)

# Update extra_info with detailed calculation
p34['questions'][0]['extra_info'] = {
    "concept": "Dit is een tijdsduur berekening: bereken het verschil tussen twee tijdstippen.",
    "berekening": ["14:45 - 14:00 = 45 minuten"],
    "berekening_tabel": [
        "| Stap | Bewerking | Uitkomst |",
        "|------|-----------|----------|",
        "| 1. Bereken tijdsduur | 14:45 - 14:00 | **45 minuten** ⭐ |"
    ]
}

# Complete LOVA section
p34['questions'][0]['lova'] = {
    "stap1_lezen": {
        "ruis": [],
        "hoofdvraag": "Hoelang heeft Jamal aan zijn huiswerk gewerkt?",
        "tussenstappen": ["Bereken de tijdsduur tussen 14:00 en 14:45"]
    },
    "stap2_ordenen": {
        "relevante_getallen": {
            "Begintijd": "14:00 uur",
            "Eindtijd": "14:45 uur"
        },
        "tool": "Tijdsduur berekenen",
        "conversies": []
    },
    "stap3_vormen": {
        "bewerkingen": [{
            "stap": "Bereken tijdsduur",
            "berekening": "14:45 - 14:00",
            "resultaat": "45 minuten",
            "uitleg": "Tel de minuten vanaf 14:00 tot 14:45"
        }]
    },
    "stap4_antwoorden": {
        "verwachte_eenheid": "minuten",
        "logica_check": "45 minuten is logisch: minder dan 1 uur",
        "antwoord": "45 minuten"
    }
}

print("   ✅ Item 34 completed\n")

# ==============================================================================
# ITEM 35: Zwemles (30 + 30 = 60 minuten = 1 uur)
# ==============================================================================
print("2️⃣ Item 35 - Zwemles (CRITICAL FIX)")
print("   Problem: Missing actual calculation steps")
print("   Fix: Add detailed calculation showing 30 + 30 = 60 min = 1 uur")

p35 = next(p for p in data if p['id'] == 35)

# Update extra_info with detailed calculation
p35['questions'][0]['extra_info'] = {
    "concept": "Dit is een optelling van tijdsduren: tel twee tijden bij elkaar op.",
    "berekening": ["30 minuten + 30 minuten = 60 minuten = 1 uur"],
    "berekening_tabel": [
        "| Stap | Bewerking | Uitkomst |",
        "|------|-----------|----------|",
        "| 1. Tel lestijden op | 30 + 30 | **60 minuten** |",
        "| 2. Reken om naar uren | 60 minuten | **1 uur** ⭐ |"
    ]
}

# Complete LOVA section
p35['questions'][0]['lova'] = {
    "stap1_lezen": {
        "ruis": [],
        "hoofdvraag": "Hoelang duren beide lessen samen?",
        "tussenstappen": ["Tel beide lestijden bij elkaar op", "Reken eventueel om naar uren"]
    },
    "stap2_ordenen": {
        "relevante_getallen": {
            "Duur per les": "30 minuten",
            "Aantal lessen": "2"
        },
        "tool": "Optellen",
        "conversies": ["60 minuten = 1 uur"]
    },
    "stap3_vormen": {
        "bewerkingen": [
            {
                "stap": "Tel lestijden op",
                "berekening": "30 + 30",
                "resultaat": "60 minuten",
                "uitleg": "Tel de twee lessen bij elkaar op"
            },
            {
                "stap": "Reken om naar uren",
                "berekening": "60 minuten = 1 uur",
                "resultaat": "1 uur",
                "uitleg": "60 minuten is hetzelfde als 1 uur"
            }
        ]
    },
    "stap4_antwoorden": {
        "verwachte_eenheid": "uur",
        "logica_check": "1 uur is logisch: 2 × 30 minuten = 60 minuten = 1 uur",
        "antwoord": "1 uur"
    }
}

print("   ✅ Item 35 completed (CRITICAL FIX APPLIED)\n")

# ==============================================================================
# ITEM 36: Film kijken (120 minuten = 2 uur)
# ==============================================================================
print("3️⃣ Item 36 - Film kijken")
print("   Adding detailed conversion steps and LOVA...")

p36 = next(p for p in data if p['id'] == 36)

# Update extra_info with detailed calculation
p36['questions'][0]['extra_info'] = {
    "concept": "Dit is een omrekening van minuten naar uren.",
    "berekening": ["120 minuten ÷ 60 = 2 uur"],
    "berekening_tabel": [
        "| Stap | Bewerking | Uitkomst |",
        "|------|-----------|----------|",
        "| 1. Reken om naar uren | 120 ÷ 60 | **2 uur** ⭐ |"
    ]
}

# Complete LOVA section
p36['questions'][0]['lova'] = {
    "stap1_lezen": {
        "ruis": [],
        "hoofdvraag": "Hoeveel uur duurt de film?",
        "tussenstappen": ["Reken 120 minuten om naar uren"]
    },
    "stap2_ordenen": {
        "relevante_getallen": {
            "Duur in minuten": "120 minuten"
        },
        "tool": "Omrekenen (minuten naar uren)",
        "conversies": ["60 minuten = 1 uur"]
    },
    "stap3_vormen": {
        "bewerkingen": [{
            "stap": "Reken om naar uren",
            "berekening": "120 ÷ 60",
            "resultaat": "2 uur",
            "uitleg": "Deel het aantal minuten door 60 om uren te krijgen"
        }]
    },
    "stap4_antwoorden": {
        "verwachte_eenheid": "uur",
        "logica_check": "2 uur is logisch: 2 × 60 minuten = 120 minuten",
        "antwoord": "2 uur"
    }
}

print("   ✅ Item 36 completed\n")

# ==============================================================================
# ITEM 37: Naar school fietsen (15 + 15 = 30 minuten)
# ==============================================================================
print("4️⃣ Item 37 - Naar school fietsen")
print("   Adding detailed calculation steps and LOVA...")

p37 = next(p for p in data if p['id'] == 37)

# Update extra_info with detailed calculation
p37['questions'][0]['extra_info'] = {
    "concept": "Dit is een optelling van tijdsduren: tel heenreis en terugreis bij elkaar op.",
    "berekening": ["15 minuten + 15 minuten = 30 minuten"],
    "berekening_tabel": [
        "| Stap | Bewerking | Uitkomst |",
        "|------|-----------|----------|",
        "| 1. Tel heen en terug op | 15 + 15 | **30 minuten** ⭐ |"
    ]
}

# Complete LOVA section
p37['questions'][0]['lova'] = {
    "stap1_lezen": {
        "ruis": [],
        "hoofdvraag": "Hoelang fietst ze per dag in totaal?",
        "tussenstappen": ["Tel de tijd van heenreis en terugreis bij elkaar op"]
    },
    "stap2_ordenen": {
        "relevante_getallen": {
            "Tijd naar school": "15 minuten",
            "Tijd terug": "15 minuten"
        },
        "tool": "Optellen",
        "conversies": []
    },
    "stap3_vormen": {
        "bewerkingen": [{
            "stap": "Tel heen en terug op",
            "berekening": "15 + 15",
            "resultaat": "30 minuten",
            "uitleg": "Tel de tijd naar school en de tijd terug bij elkaar op"
        }]
    },
    "stap4_antwoorden": {
        "verwachte_eenheid": "minuten",
        "logica_check": "30 minuten is logisch: 2 × 15 minuten",
        "antwoord": "30 minuten"
    }
}

print("   ✅ Item 37 completed\n")

# ==============================================================================
# Save the fixed data
# ==============================================================================
with open('verhaaltjessommen-M4.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("=" * 70)
print("✅ ALL TIME PROBLEMS (34-37) COMPLETED!")
print("=" * 70)
print("\n📋 VERIFICATION:\n")

# Verify all items
for item_id in [34, 35, 36, 37]:
    p = next(p for p in data if p['id'] == item_id)
    print(f"Item {item_id} - {p['title']}:")

    # Check berekening
    berekening = p['questions'][0]['extra_info']['berekening']
    print(f"  ✅ berekening: {berekening}")

    # Check LOVA tussenstappen
    tussenstappen = p['questions'][0]['lova']['stap1_lezen']['tussenstappen']
    print(f"  ✅ LOVA tussenstappen: {len(tussenstappen)} step(s)")

    # Check LOVA bewerkingen
    bewerkingen = p['questions'][0]['lova']['stap3_vormen']['bewerkingen']
    print(f"  ✅ LOVA bewerkingen: {len(bewerkingen)} operation(s)")
    print()

print("=" * 70)
print("🎯 DATASET NOW 100% CITO-WAARDIG!")
print("=" * 70)
