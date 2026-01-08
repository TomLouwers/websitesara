# Exercise Schema V2.0 - Enhanced Feedback

**Version:** 2.0.0
**Date:** January 7, 2026
**Status:** Phase 1 Implementation

---

## Overview

This document defines the enhanced exercise schema for Phase 1: Foundation. The new schema adds **rich feedback**, **worked examples**, and **3-tier hints** while maintaining **backwards compatibility** with existing exercises.

---

## Core Principles

1. **Backwards Compatible:** Old exercises without new fields still work
2. **Additive Only:** No breaking changes to existing structure
3. **Progressive Enhancement:** New features gracefully degrade if not present
4. **Pedagogically Sound:** Based on learning science best practices

---

## Schema Changes

### 1. Enhanced Feedback Object

#### NEW: `feedback` field (optional, but highly recommended)

```json
{
  "question": "Waarom noemt Sofie de hamster Nibbel?",
  "options": [...],
  "feedback": {
    "correct": {
      "explanation": "Detailed explanation of why this answer is correct",
      "skill_reinforcement": "Positive reinforcement of the skill being practiced"
    },
    "incorrect": {
      "by_option": {
        "A": {
          "explanation": "Why this specific answer is wrong",
          "hint": "Directional hint for this misconception",
          "misconception": "The underlying error pattern"
        },
        "B": { ... },
        "C": { ... },
        "D": { ... }
      },
      "workedExample": {
        "steps": [
          "Step 1: First step of solution",
          "Step 2: Second step",
          "Step 3: Final step"
        ]
      }
    }
  }
}
```

---

### 2. Three-Tier Hint System

#### OLD: Single hint (still supported)
```json
{
  "hint": "Lees waarom de hamster die naam krijgt."
}
```

#### NEW: Three-tier progressive hints (recommended)
```json
{
  "hints": {
    "tier1_procedural": {
      "text": "Look for procedural guidance - WHERE to look",
      "reveal_percentage": 0.2,
      "type": "procedural"
    },
    "tier2_conceptual": {
      "text": "Conceptual understanding - WHAT to think about",
      "reveal_percentage": 0.5,
      "type": "conceptual"
    },
    "tier3_worked_example": {
      "text": "Near-complete solution - HOW to solve it",
      "reveal_percentage": 0.9,
      "type": "worked_example"
    }
  }
}
```

**Fallback Strategy:**
- If only `hint` exists: Use as tier1
- If `hints.tier1_procedural` missing: Use old `hint` field
- Missing tiers: Skip to next available tier

---

### 3. Error Classification (All Subjects)

#### For Reading Comprehension (bl):
```json
{
  "error_type": "letterlijk_gemist",
  "error_metadata": {
    "category": "reading",
    "severity": "medium",
    "remediation_exercises": ["bl_groep4_letterlijk_practice_1"]
  }
}
```

**Error Types for Reading:**
- `letterlijk_gemist`: Missed literal information in text
- `inferentie_fout`: Failed to make required inference
- `vocabulaire`: Vocabulary/word meaning issue
- `hoofdzaken`: Missed main idea/theme
- `verbanden`: Failed to identify relationships

#### For Math (gb):
```json
{
  "error_type": "conversiefout",
  "error_metadata": {
    "category": "math",
    "severity": "high",
    "remediation_exercises": ["gb_groep5_eenheden_practice_1"],
    "visual_aid_query": "eenheden_omrekenen"
  }
}
```

**Error Types for Math:**
- `conversiefout`: Unit conversion error
- `rekenfout_basis`: Basic arithmetic mistake
- `rekenfout_complex`: Complex calculation error
- `conceptfout`: Conceptual misunderstanding
- `strategie_fout`: Wrong strategy applied

---

## Complete Example: Reading Exercise

```json
{
  "id": 1,
  "title": "De nieuwe hamster",
  "theme": "Dieren / gezin",
  "text_type": "verhalend",
  "text": "Sofie krijgt op een zaterdag een nieuwe hamster...",
  "questions": [
    {
      "item_id": "1a",
      "skill": "letterlijk",
      "strategy": "informatie_zoeken",
      "question": "Waarom noemt Sofie de hamster Nibbel?",

      // NEW: Three-tier hints
      "hints": {
        "tier1_procedural": {
          "text": "Kijk naar de zin waar Nibbel voor het eerst genoemd wordt.",
          "reveal_percentage": 0.2,
          "type": "procedural"
        },
        "tier2_conceptual": {
          "text": "Let op het woord 'omdat' - dat geeft altijd een reden.",
          "reveal_percentage": 0.5,
          "type": "conceptual"
        },
        "tier3_worked_example": {
          "text": "De zin is: 'Ze noemt hem Nibbel, omdat hij graag op zonnebloempitten kauwt.' Het woord 'nibbelen' betekent knabbelen.",
          "reveal_percentage": 0.9,
          "type": "worked_example"
        }
      },

      "options": [
        {
          "label": "A",
          "text": "Hij slaapt veel.",
          "is_correct": false
        },
        {
          "label": "B",
          "text": "Hij knabbelt graag aan pitten.",
          "is_correct": true
        },
        {
          "label": "C",
          "text": "Hij rent heel snel.",
          "is_correct": false
        },
        {
          "label": "D",
          "text": "Hij is geel van kleur.",
          "is_correct": false
        }
      ],

      // NEW: Rich feedback
      "feedback": {
        "correct": {
          "explanation": "Goed gevonden! In de tekst staat: 'omdat hij graag op zonnebloempitten kauwt'. Je hebt de belangrijke informatie goed gelezen.",
          "skill_reinforcement": "Je kunt letterlijke informatie goed vinden in de tekst! Deze vaardigheid is heel belangrijk bij het begrijpen van wat je leest."
        },
        "incorrect": {
          "by_option": {
            "A": {
              "explanation": "Nibbel slaapt wel in het huisje, maar dat is niet de reden voor zijn naam.",
              "hint": "Zoek in de tekst naar het woord 'omdat' na de naam Nibbel.",
              "misconception": "Verwarring tussen gebeurtenissen in het verhaal"
            },
            "C": {
              "explanation": "Nibbel rent inderdaad, maar dat gebeurt pas later in het verhaal en is niet de reden voor zijn naam.",
              "hint": "De naam wordt uitgelegd in de eerste zin over Nibbel.",
              "misconception": "Focus op latere gebeurtenissen in plaats van de directe verklaring"
            },
            "D": {
              "explanation": "Er staat niets in de tekst over de kleur van Nibbel.",
              "hint": "Zoek naar informatie die in de tekst staat, niet wat je denkt.",
              "misconception": "Informatie toevoegen die niet in de tekst staat"
            }
          },
          "workedExample": {
            "steps": [
              "Stap 1: Lees de zin: 'Ze noemt hem Nibbel, omdat...'",
              "Stap 2: Het woord 'omdat' geeft de reden voor iets",
              "Stap 3: Wat staat er na 'omdat'? → 'hij graag op zonnebloempitten kauwt'",
              "Stap 4: Knabbelen = nibbelen → daarom heet hij Nibbel!",
              "Antwoord: B - Hij knabbelt graag aan pitten."
            ]
          }
        }
      }
    }
  ]
}
```

---

## Complete Example: Math Exercise

```json
{
  "id": 201,
  "title": "Optellen met overstappen",
  "theme": "basis-rekenen",
  "content": "Bereken:",
  "questions": [
    {
      "question": "$47 + 28 = ?$",
      "skill": "optellen",
      "strategy": "getalsplitsing",

      // NEW: Three-tier hints
      "hints": {
        "tier1_procedural": {
          "text": "Begin met het optellen van de tientallen.",
          "reveal_percentage": 0.2,
          "type": "procedural"
        },
        "tier2_conceptual": {
          "text": "Splits de getallen in tientallen en eenheden: 47 = 40 + 7 en 28 = 20 + 8",
          "reveal_percentage": 0.5,
          "type": "conceptual"
        },
        "tier3_worked_example": {
          "text": "40 + 20 = 60, dan 7 + 8 = 15, dus 60 + 15 = 75",
          "reveal_percentage": 0.9,
          "type": "worked_example"
        }
      },

      "options": ["65", "67", "75", "77"],
      "correct": 2,

      // NEW: Rich feedback
      "feedback": {
        "correct": {
          "explanation": "Helemaal goed! Je hebt de getallen slim gesplitst: 40 + 20 = 60, en 7 + 8 = 15, dus 60 + 15 = 75.",
          "skill_reinforcement": "Je beheerst het optellen met overstappen prima! Deze strategie helpt je bij grotere sommen."
        },
        "incorrect": {
          "by_option": {
            "0": {
              "explanation": "Let op: 7 + 8 = 15, niet 5. Je bent vergeten de 1 van de 15 bij de tientallen op te tellen.",
              "hint": "Bij 7 + 8 krijg je 15. Dat is 1 tiental en 5 eenheden.",
              "misconception": "Vergeten om over te stappen bij de eenheden",
              "error_type": "rekenfout_basis"
            },
            "1": {
              "explanation": "Bijna! Je hebt misschien 40 + 20 = 60 gedaan, en 7 + 8 = 15, maar dan moet je 60 + 15 uitrekenen, niet 60 + 7.",
              "hint": "7 + 8 = 15, dus je moet 60 + 15 berekenen.",
              "misconception": "Fout bij het samenvoegen van tientallen en eenheden",
              "error_type": "conceptfout"
            },
            "3": {
              "explanation": "Let op: 40 + 20 = 60, niet 70. Begin opnieuw met het optellen van de tientallen.",
              "hint": "Check je rekenwerk: 4 tientallen + 2 tientallen = 6 tientallen.",
              "misconception": "Fout in basis optelling van tientallen",
              "error_type": "rekenfout_basis"
            }
          },
          "workedExample": {
            "steps": [
              "Stap 1: Split beide getallen - 47 = 40 + 7 en 28 = 20 + 8",
              "Stap 2: Tel de tientallen op - 40 + 20 = 60",
              "Stap 3: Tel de eenheden op - 7 + 8 = 15",
              "Stap 4: Tel alles samen - 60 + 15 = 75",
              "Antwoord: 75"
            ]
          }
        }
      }
    }
  ]
}
```

---

## Migration Guide

### For Existing Exercises

**Phase 1:** Enhance 2 sample exercises (1 reading, 1 math)
**Phase 2:** Scale to all 1,500+ exercises using templates and AI

### Adding New Fields to Old Exercises

1. **Keep existing fields:** Don't remove `hint`, `correct`, etc.
2. **Add `feedback` object:** Start with correct explanation
3. **Add `hints` object:** Create 3 progressive hints
4. **Add error types:** Classify common misconceptions
5. **Test fallback:** Ensure old rendering still works

---

## Rendering Priority

The app will check for fields in this order:

### For Feedback:
1. `feedback.correct.explanation` (new) → use rich feedback
2. Fall back to generic "Goed gedaan!" (old)

### For Hints:
1. `hints.tier1_procedural` (new) → use 3-tier system
2. `hint` (old) → use as tier1 only
3. No hint → skip hint display

### For Worked Examples:
1. `feedback.incorrect.workedExample.steps` (new) → render steps
2. `extra_info.tips` (old, math only) → render as list
3. No worked example → skip display

---

## Validation Rules

### Required Fields (unchanged):
- `question` or `title`
- `options` or `correct`
- `is_correct` boolean OR `correct` index

### Recommended New Fields:
- `feedback.correct.explanation`
- `feedback.incorrect.workedExample.steps`
- `hints.tier1_procedural` (minimum)

### Validation Script:
```javascript
// Run: node scripts/validators/schema-validator.js

function validateExerciseV2(exercise) {
  const issues = [];

  // Check for new feedback fields
  if (!exercise.feedback?.correct?.explanation) {
    issues.push({ severity: 'warning', message: 'Missing correct explanation' });
  }

  if (!exercise.feedback?.incorrect?.workedExample) {
    issues.push({ severity: 'warning', message: 'Missing worked example' });
  }

  // Check for 3-tier hints
  if (!exercise.hints?.tier1_procedural && !exercise.hint) {
    issues.push({ severity: 'error', message: 'No hints provided' });
  }

  return issues;
}
```

---

## Performance Considerations

- **File Size:** New fields add ~30% to JSON size
- **Load Time:** No impact (lazy loading unchanged)
- **Backwards Compatibility:** 100% - old exercises work as-is
- **Cache Busting:** Update version in HTML: `?v=20260107`

---

## Next Steps

### Phase 1 (Q1 2026):
- [x] Define schema (this document)
- [ ] Enhance 2 sample exercises
- [ ] Update rendering logic
- [ ] Test backwards compatibility

### Phase 2 (Q2 2026):
- [ ] Create exercise templates
- [ ] Build content generator tool
- [ ] Scale to all 1,500+ exercises

---

**Document Version:** 1.0
**Last Updated:** January 7, 2026
**Maintained By:** Development Team
