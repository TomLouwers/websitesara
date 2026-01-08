# Exercise Enhancement Workflow Guide

**Status:** Phase 2B - Manual Enhancement in Progress
**Date:** January 8, 2026
**Batch:** Groep 4 Foundation (413 questions)

---

## 📋 Current Batch: Groep 4 Foundation

### ✅ Templates Generated

1. **bl_groep4_e4_1_TEMPLATE.json** - 153 reading questions
   - 30 exercises with stories for Grade 4
   - 3,060 TODOs to complete
   - Estimated time: 765 minutes (~13 hours)

2. **gb_groep4_m4_TEMPLATE.json** - 260 math questions
   - 260 exercises covering: addition, subtraction, multiplication, division, time, money, measurement
   - 5,460 TODOs to complete
   - Estimated time: 1,300 minutes (~22 hours)

**Total for Groep 4:** 413 questions, 8,520 TODOs, ~35 hours

---

## 🎯 Recommended Workflow

### Step 1: Pick One Exercise to Start

**For Reading (bl_groep4_e4_1_TEMPLATE.json):**
```bash
# Open in your editor
code data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json

# Search for first exercise: "De verdwenen sleutel"
```

**For Math (gb_groep4_m4_TEMPLATE.json):**
```bash
# Open in your editor
code data/exercises/gb/gb_groep4_m4_TEMPLATE.json

# Search for first exercise: "Optellen tot 100"
```

### Step 2: Read the Original Content

For each exercise:
1. Read the `text` field (for reading) or `question` (for math)
2. Review all options and identify the correct answer
3. Understand what skill is being tested

### Step 3: Fill in TODOs Systematically

**For EACH question in the exercise:**

#### A. Correct Feedback (Always Required)
```json
"feedback": {
  "correct": {
    "explanation": "📝 TODO: Explain WHY this answer is correct",
    "skill_reinforcement": "💪 TODO: What skill did the student demonstrate?"
  }
}
```

**Example transformation (Reading):**
```json
// BEFORE
"explanation": "📝 TODO: Explain WHY this answer is correct"

// AFTER
"explanation": "Helemaal goed! In de tekst staat: 'de sleutel lag onder de bank'. Je hebt deze letterlijke informatie goed gevonden."
```

**Example transformation (Math):**
```json
// BEFORE
"explanation": "📝 TODO: Explain WHY this answer is correct"

// AFTER
"explanation": "Goed gedaan! $47 + 28$ kun je splitsen: $40 + 20 = 60$ en $7 + 8 = 15$, dus $60 + 15 = 75$."
```

#### B. Incorrect Feedback - Per Option (For Each Wrong Answer)
```json
"by_option": {
  "A": {
    "explanation": "TODO: Why is this incorrect?",
    "hint": "TODO: Hint to guide toward correct answer",
    "misconception": "TODO: What error pattern?",
    "error_type": "TODO: letterlijk_gemist | inferentie_fout | ..."
  }
}
```

**Error types for Reading:**
- `letterlijk_gemist` - Missed literal information
- `inferentie_fout` - Failed to infer/conclude
- `vocabulaire` - Vocabulary misunderstanding
- `structuur` - Text structure confusion
- `detail_vergeten` - Forgot important detail

**Error types for Math:**
- `rekenfout_basis` - Basic calculation error
- `conceptfout` - Conceptual misunderstanding
- `procedurele_fout` - Wrong procedure/method
- `afleesfout` - Misread the question
- `eenhedenfout` - Units confusion (cm/mm, €/ct)

**Example (Reading - wrong option):**
```json
// BEFORE
"A": {
  "explanation": "TODO: Why is this incorrect?",
  "hint": "TODO: Hint to guide toward correct answer",
  "misconception": "TODO: What error pattern?",
  "error_type": "TODO: letterlijk_gemist | inferentie_fout | ..."
}

// AFTER
"A": {
  "explanation": "In de tekst staat niet dat de sleutel in de keuken lag. Lees de laatste alinea nog eens.",
  "hint": "Zoek naar de zin waarin staat waar de sleutel werd gevonden.",
  "misconception": "Verwarring over locatie in het verhaal",
  "error_type": "letterlijk_gemist"
}
```

**Example (Math - wrong option):**
```json
// BEFORE
"0": {
  "explanation": "TODO: Why is this incorrect?",
  "hint": "TODO: Hint to guide toward correct answer",
  "misconception": "TODO: What error pattern?",
  "error_type": "TODO: rekenfout_basis | conceptfout | ..."
}

// AFTER
"0": {
  "explanation": "Let op: $7 + 8 = 15$, niet $5$. Je hebt vergeten de tiental mee te nemen.",
  "hint": "Splits de berekening op: eerst de tientallen ($40 + 20$), dan de eenheden ($7 + 8$).",
  "misconception": "Vergeet tiental bij optellen van eenheden",
  "error_type": "rekenfout_basis"
}
```

#### C. Worked Example (For Incorrect Answers)
```json
"workedExample": {
  "steps": [
    "TODO: Step 1 - What to do first",
    "TODO: Step 2 - Next action",
    "TODO: Step 3 - How to arrive at answer",
    "TODO: Step 4 - Conclusion"
  ]
}
```

**Guidelines:**
- 3-5 steps typically
- Each step builds on the previous
- Use clear, age-appropriate language
- Final step gives the answer
- **Use KaTeX notation for math:** `$47 + 28 = 75$`

**Example (Reading):**
```json
"steps": [
  "Stap 1: Lees de vraag: 'Waar vond Tim de sleutel?'",
  "Stap 2: Zoek in de tekst naar het woord 'sleutel'",
  "Stap 3: Lees de zin: 'Tim keek onder de bank en vond daar de sleutel'",
  "Stap 4: Het antwoord is dus: onder de bank",
  "Antwoord: C - Onder de bank"
]
```

**Example (Math):**
```json
"steps": [
  "Stap 1: Schrijf de som op: $47 + 28 = ?$",
  "Stap 2: Split de getallen: $40 + 20$ en $7 + 8$",
  "Stap 3: Tel de tientallen op: $40 + 20 = 60$",
  "Stap 4: Tel de eenheden op: $7 + 8 = 15$",
  "Stap 5: Tel alles bij elkaar: $60 + 15 = 75$",
  "Antwoord: 75"
]
```

#### D. Three-Tier Hints
```json
"hints": {
  "tier1_procedural": {
    "text": "Existing hint (preserved from original)",
    "reveal_percentage": 0.2,
    "type": "procedural"
  },
  "tier2_conceptual": {
    "text": "TODO: WHAT to think about",
    "reveal_percentage": 0.5,
    "type": "conceptual"
  },
  "tier3_worked_example": {
    "text": "TODO: HOW to solve it",
    "reveal_percentage": 0.9,
    "type": "worked_example"
  }
}
```

**Tier 1 (Procedural):** WHERE to look - Already filled from original hint
**Tier 2 (Conceptual):** WHAT to think about - Fill this
**Tier 3 (Worked Example):** HOW to solve - Nearly complete solution - Fill this

**Example (Reading):**
```json
"tier2_conceptual": {
  "text": "Denk na: waar speelt het einde van het verhaal zich af? Daar wordt de sleutel gevonden.",
  "reveal_percentage": 0.5
},
"tier3_worked_example": {
  "text": "In de laatste alinea staat: 'Tim keek onder de bank.' Daar vond hij de sleutel.",
  "reveal_percentage": 0.9
}
```

**Example (Math):**
```json
"tier2_conceptual": {
  "text": "Gebruik de splitsingsmethode: split beide getallen in tientallen en eenheden.",
  "reveal_percentage": 0.5
},
"tier3_worked_example": {
  "text": "Reken zo: $40 + 20 = 60$, dan $7 + 8 = 15$, en tot slot $60 + 15 = 75$.",
  "reveal_percentage": 0.9
}
```

### Step 4: Remove TODO Markers

Search for "TODO:" in your file and ensure ALL are replaced with actual content.

**Quick search:**
```bash
# Count remaining TODOs
grep -o "TODO:" data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json | wc -l

# Should be 0 when done!
```

### Step 5: Rename Template to Final File

**Option A: Replace original (BACKUP FIRST!)**
```bash
# Backup original
cp data/exercises/bl/bl_groep4_e4_1.json data/exercises/bl/bl_groep4_e4_1_BACKUP.json

# Replace with enhanced version
mv data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json data/exercises/bl/bl_groep4_e4_1.json
```

**Option B: Create separate enhanced file**
```bash
# Keep both versions
mv data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json data/exercises/bl/bl_groep4_e4_1_enhanced.json
```

### Step 6: Test in Browser

1. Open the website locally
2. Navigate to the enhanced exercise
3. Test correct answers - verify feedback displays
4. Test incorrect answers - verify per-option feedback and worked examples
5. Check math rendering (if math exercise)
6. Verify no console errors

### Step 7: Validate with Scanner

```bash
# Run validator to confirm enhancement
node scripts/schema-validator-v2.js

# Check that the question count increased:
# Before: Enhanced (V2.0): 4 (0.1%)
# After:  Enhanced (V2.0): 157 (5.6%)  <- if you did bl_groep4_e4_1
```

---

## 💡 Quality Tips

### Writing Good Explanations

✅ **DO:**
- Be specific and reference the text/question
- Use age-appropriate language (Grade 4 = 8-9 years old)
- Explain the WHY, not just confirm correctness
- Use positive, encouraging tone
- Include KaTeX math notation for formulas: `$2 + 3 = 5$`

❌ **DON'T:**
- Generic responses: "Goed gedaan!" / "Dat klopt niet."
- Repeat the answer without explaining
- Use complex terminology
- Assume prior knowledge
- Make students feel bad about mistakes

### Reading Exercise Examples

**Good explanation (correct):**
> "Helemaal goed! In de tekst staat letterlijk: 'de kat zat op het dak'. Je hebt deze informatie goed gevonden in de eerste alinea."

**Bad explanation (correct):**
> "Goed gedaan!"

**Good explanation (incorrect):**
> "In de tekst staat niet dat de kat in de boom zat. Lees de eerste alinea nog eens en zoek waar de kat precies zat."

**Bad explanation (incorrect):**
> "Dat klopt niet."

### Math Exercise Examples

**Good explanation (correct):**
> "Prima gedaan! Je hebt $47 + 28$ slim opgelost door te splitsen: $40 + 20 = 60$ en $7 + 8 = 15$, dus samen $75$."

**Bad explanation (correct):**
> "Dat is juist!"

**Good explanation (incorrect):**
> "Let op: $7 + 8 = 15$, niet $14$. Je bent vergeten dat $7 + 8$ over de tien gaat: $7 + 3 = 10$, en dan nog $+ 5 = 15$."

**Bad explanation (incorrect):**
> "Je rekent verkeerd."

---

## 📊 Progress Tracking

### Check Progress Anytime

```bash
# Run validator to see current status
node scripts/schema-validator-v2.js

# Look for:
# Enhanced (V2.0): X (Y%)
```

### Groep 4 Milestones

- ☐ 50 questions enhanced (12%)
- ☐ 100 questions enhanced (24%)
- ☐ 153 questions enhanced (37%) - Reading complete! 🎉
- ☐ 250 questions enhanced (60%)
- ☐ 413 questions enhanced (100%) - Groep 4 complete! 🎉🎉

---

## 🚀 Time-Saving Strategies

### 1. Batch Similar Questions

If you see multiple questions testing the same skill, write feedback for the first one, then adapt for others.

**Example:** 10 questions about "Tafel van 3" (3 times table)
1. Write detailed feedback for first question
2. Copy and adapt for questions 2-10
3. Change only the specific numbers

### 2. Use Patterns from Sample Exercises

Reference the enhanced samples:
- `data/exercises/bl/bl_groep4_enhanced_sample.json` - Reading patterns
- `data/exercises/gb/gb_groep4_enhanced_sample.json` - Math patterns

### 3. Work in Focused Sessions

**Recommended:** 90-minute sessions
- 60 minutes: Fill in feedback
- 15 minutes: Review and check TODOs
- 15 minutes: Test in browser

**Realistic pace:**
- Reading: ~20 questions per session
- Math: ~30 questions per session (more repetitive)

### 4. Use Find & Replace for Common Phrases

**Common patterns (adapt as needed):**
- "In de tekst staat:" → Use for literal comprehension
- "Let op:" → Use for math corrections
- "Goed gevonden!" → Use for correct reading answers
- "Prima gedaan!" → Use for correct math answers

---

## 🐛 Common Issues

### Issue: Too many TODOs - where do I start?

**Solution:** Do ONE exercise at a time. Complete all fields for one exercise before moving to the next.

### Issue: Stuck on what to write for misconception

**Solution:** Think: "What did the student misunderstand?" Common patterns:
- **Reading:** Confused character/location, missed keyword, wrong inference
- **Math:** Wrong operation, calculation error, unit confusion

### Issue: Worked example too short or too long

**Solution:** Aim for 3-5 steps:
1. Read/understand the question
2. Identify what to do
3. Execute the calculation/search
4. Arrive at answer
5. State conclusion

### Issue: Math notation not rendering

**Solution:** Use KaTeX syntax:
- Inline math: `$2 + 3 = 5$`
- DO NOT use: `2 + 3 = 5` (plain text)
- DO USE: `$2 + 3 = 5$` (with dollar signs)

---

## ✅ Completion Checklist (Per Exercise)

Before moving to the next exercise, verify:

- [ ] All questions in exercise have feedback.correct filled
- [ ] All wrong options have by_option feedback
- [ ] All workedExample.steps are complete (3-5 steps)
- [ ] Tier 2 and Tier 3 hints are filled
- [ ] No "TODO:" markers remain in this exercise
- [ ] Math notation uses KaTeX syntax (`$...$`)
- [ ] Language is age-appropriate (Grade 4 = 8-9 years)
- [ ] Tone is positive and encouraging

---

## 🎯 Next After Groep 4

Once Groep 4 is complete, move to **Batch 2: Groep 5**

**Generate templates:**
```bash
# Reading
node scripts/exercise-enhancer.js data/exercises/bl/bl_groep5_e5_1.json data/exercises/bl/bl_groep5_e5_1_TEMPLATE.json

# Math
node scripts/exercise-enhancer.js data/exercises/gb/gb_groep5_m5.json data/exercises/gb/gb_groep5_m5_TEMPLATE.json
```

**Note:** `bl_groep5_m5_1_TEMPLATE.json` already exists!

---

## 📞 Need Help?

**Documentation:**
- **SCHEMA_V2.md** - Full schema specification
- **PHASE_2A_TOOLS_GUIDE.md** - Tool usage guide
- **INTEGRATION_TESTING_GUIDE.md** - Testing procedures

**Sample Exercises:**
- `data/exercises/bl/bl_groep4_enhanced_sample.json` - Reading example
- `data/exercises/gb/gb_groep4_enhanced_sample.json` - Math example

---

**Ready to start?** Open `bl_groep4_e4_1_TEMPLATE.json` and begin with the first exercise! 🚀
