# Phase 2A: Exercise Enhancement Tools

**Purpose:** Scale enhanced feedback (Schema V2.0) to all 2,780 exercises efficiently

**Tools:**
1. `schema-validator-v2.js` - Scanner & quality reporter
2. `exercise-enhancer.js` - Template generator

---

## 📊 Current Status (from scan)

```
Total Questions:      2,784
Enhanced (V2.0):      4 (0.1%)
Legacy (need work):   2,780 (99.9%)

By Category:
  Reading (bl):  1,529 questions
  Math (gb):     1,255 questions

Time Estimate:
  Manual work:       232 hours
  With these tools:  93 hours (60% faster!)
```

---

## 🔍 Tool 1: Schema Validator

**What it does:** Scans all exercises and generates quality report

### Usage

```bash
node scripts/schema-validator-v2.js
```

### Output

**Console Report:**
- Total files/exercises/questions
- Enhancement status (% complete)
- Issues found (errors/warnings)
- Time estimates

**JSON Report:** `quality-report.json`
- Detailed statistics
- Issue list
- Priority files (most questions to enhance)
- Quick wins (partially enhanced)

### Example Output

```
📊 Overall Statistics
   Files scanned:      53
   Total exercises:    4,268
   Total questions:    2,784

✨ Enhancement Status
   Enhanced (V2.0):    4 (0.1%)
   Legacy:             2,780 (99.9%)

📚 By Category
   BL   → 1,529 questions, 2 enhanced (0.1%)
   GB   → 1,255 questions, 2 enhanced (0.2%)
```

---

## ✨ Tool 2: Exercise Enhancer

**What it does:** Generates Schema V2.0 template with TODO placeholders

### Usage

```bash
# Basic usage (creates _enhanced.json file)
node scripts/exercise-enhancer.js <input-file>

# Custom output file
node scripts/exercise-enhancer.js <input-file> <output-file>
```

### Examples

```bash
# Enhance a reading exercise
node scripts/exercise-enhancer.js data/exercises/bl/bl_groep4_m4_1.json

# Enhance a math exercise with custom output
node scripts/exercise-enhancer.js data/exercises/gb/gb_groep4_m4.json enhanced_gb.json

# Batch process (using shell loop)
for file in data/exercises/bl/bl_groep4_*.json; do
    node scripts/exercise-enhancer.js "$file" "${file%.json}_TEMPLATE.json"
done
```

### What It Generates

**For each question:**

1. **feedback.correct**
   ```json
   "explanation": "📝 TODO: Explain WHY this answer is correct",
   "skill_reinforcement": "💪 TODO: What skill did the student demonstrate?"
   ```

2. **feedback.incorrect.by_option** (for each wrong answer)
   ```json
   "A": {
     "explanation": "TODO: Why is this incorrect?",
     "hint": "TODO: Hint to guide toward correct answer",
     "misconception": "TODO: What error pattern?",
     "error_type": "TODO: letterlijk_gemist | inferentie_fout | ..."
   }
   ```

3. **feedback.incorrect.workedExample**
   ```json
   "steps": [
     "TODO: Step 1 - What to do first",
     "TODO: Step 2 - Next action",
     "TODO: Step 3 - How to arrive at answer",
     "TODO: Step 4 - Conclusion"
   ]
   ```

4. **hints (3-tier)**
   ```json
   "tier1_procedural": {
     "text": "Existing hint (preserved)",
     "reveal_percentage": 0.2
   },
   "tier2_conceptual": {
     "text": "TODO: WHAT to think about",
     "reveal_percentage": 0.5
   },
   "tier3_worked_example": {
     "text": "TODO: HOW to solve it",
     "reveal_percentage": 0.9
   }
   ```

### Output Statistics

After running, you'll see:
```
📊 Statistics
   Questions to enhance: 153
   TODOs to complete:    3,060
   Estimated time:       765 minutes
```

---

## 📝 Workflow: Enhancing Exercises

### Step 1: Scan to Find Work

```bash
node scripts/schema-validator-v2.js
```

**Look at:** `quality-report.json` → Find files with most legacy questions

### Step 2: Generate Template

```bash
node scripts/exercise-enhancer.js data/exercises/bl/[filename].json
```

**Creates:** `[filename]_enhanced.json` with TODOs

### Step 3: Fill in TODOs

Open the `_enhanced.json` file and search for "TODO:"

**Focus on these fields:**
1. `feedback.correct.explanation` - Why answer is correct
2. `feedback.incorrect.by_option[X].explanation` - Why each wrong answer is wrong
3. `feedback.incorrect.workedExample.steps` - Step-by-step solution
4. `hints.tier2_conceptual` - Conceptual understanding hint
5. `hints.tier3_worked_example` - Near-complete solution hint

**Example transformation:**

```json
// BEFORE (generated template)
"explanation": "TODO: Explain WHY this answer is correct"

// AFTER (you fill in)
"explanation": "Goed gevonden! In de tekst staat dat de robot over een plank moet rijden en een blokje oppakken. Je hebt beide handelingen correct geïdentificeerd."
```

### Step 4: Remove TODOs

Search for "TODO:" and ensure all are replaced with real content.

### Step 5: Test

1. Copy enhanced file to replace original (or use new name)
2. Open website
3. Load the exercise
4. Test correct/incorrect answers
5. Verify feedback displays properly

### Step 6: Repeat

Pick next file from priority list and repeat!

---

## ⚡ Speed Tips

### 1. Batch Processing

Process multiple exercises at once:

```bash
# Generate templates for all Groep 4 reading exercises
for file in data/exercises/bl/bl_groep4_*.json; do
    node scripts/exercise-enhancer.js "$file"
done
```

### 2. Use Examples

Copy feedback patterns from the sample exercises:
- `data/exercises/bl/bl_groep4_enhanced_sample.json`
- `data/exercises/gb/gb_groep4_enhanced_sample.json`

### 3. Focus on High-Value

According to `quality-report.json`, prioritize:
1. Files with most questions (biggest impact)
2. Most commonly used exercises
3. Exercises for lower grades (foundational)

### 4. Work in Parallel

Multiple people can enhance different files simultaneously:
- Person A: Reading (bl) exercises
- Person B: Math (gb) exercises
- Person C: Vocabulary (ws) exercises

---

## 🎯 Quality Guidelines

When filling in TODOs:

### Correct Explanations
- ✅ Explain WHY the answer is correct
- ✅ Reference the text/question
- ✅ Use age-appropriate language
- ❌ Don't just say "Good job!"

**Example:**
```
Good: "Goed gevonden! In de tekst staat: 'de robot kan over een plank rijden en een blokje oppakken'. Je hebt beide handelingen herkend."
Bad: "Dat is goed!"
```

### Incorrect Explanations
- ✅ Explain the specific misconception
- ✅ Be gentle and constructive
- ✅ Guide toward the right answer
- ❌ Don't just say "Wrong"

**Example:**
```
Good: "Deze handelingen staan niet in de tekst. De robot moet specifieke taken uitvoeren die in de eerste alinea beschreven worden."
Bad: "Dat klopt niet."
```

### Worked Examples
- ✅ Clear step-by-step progression
- ✅ 3-5 steps typically
- ✅ Each step builds on previous
- ✅ Final step gives answer

### Hints (3-tier)
- **Tier 1 (procedural):** WHERE to look
- **Tier 2 (conceptual):** WHAT to think about
- **Tier 3 (worked example):** HOW to solve (almost complete)

---

## 📈 Tracking Progress

### Check Current Status

```bash
node scripts/schema-validator-v2.js
```

Watch the percentage go up! 🎉

### Goal

```
Enhanced (V2.0):    2,784 (100%)
```

### Milestones

- ☐ 10% enhanced (278 questions)
- ☐ 25% enhanced (696 questions)
- ☐ 50% enhanced (1,392 questions)
- ☐ 75% enhanced (2,088 questions)
- ☐ 100% enhanced (2,784 questions) 🎉

---

## 🤖 Future: AI-Assisted Enhancement

**Phase 2B** (Next step):
- Use OpenAI/Claude API
- Generate feedback automatically
- Human review and approval
- 10x faster than manual

**For now:** These tools make manual enhancement 3-5x faster!

---

## 📞 Questions?

**Tool Issues:** Check console error messages
**Schema Questions:** See `SCHEMA_V2.md`
**Examples:** See `bl_groep4_enhanced_sample.json`

---

## 🎓 Example: Complete Enhancement

**Before (Legacy):**
```json
{
  "question": "Wat moet de robot doen?",
  "hint": "Zoek naar twee handelingen.",
  "options": [
    {"label": "A", "text": "Springen", "is_correct": false},
    {"label": "B", "text": "Over plank en blokje pakken", "is_correct": true}
  ]
}
```

**After (Enhanced V2.0):**
```json
{
  "question": "Wat moet de robot doen?",
  "hint": "Zoek naar twee handelingen.",
  "hints": {
    "tier1_procedural": {
      "text": "Zoek naar twee handelingen.",
      "reveal_percentage": 0.2
    },
    "tier2_conceptual": {
      "text": "Kijk naar de eerste alinea waar beschreven wordt wat de robot moet kunnen.",
      "reveal_percentage": 0.5
    },
    "tier3_worked_example": {
      "text": "In de tekst staat: 'kan over een plank rijden en een blokje oppakken'. Dit zijn twee duidelijke handelingen.",
      "reveal_percentage": 0.9
    }
  },
  "options": [
    {"label": "A", "text": "Springen", "is_correct": false},
    {"label": "B", "text": "Over plank en blokje pakken", "is_correct": true}
  ],
  "feedback": {
    "correct": {
      "explanation": "Helemaal goed! Je hebt de twee handelingen correct geïdentificeerd: over de plank rijden en het blokje oppakken.",
      "skill_reinforcement": "Je kunt letterlijke informatie goed uit de tekst halen!"
    },
    "incorrect": {
      "by_option": {
        "A": {
          "explanation": "Springen wordt niet genoemd in de tekst. De robot moet andere handelingen uitvoeren.",
          "hint": "Lees de eerste alinea nog eens. Welke twee dingen moet de robot kunnen?",
          "misconception": "Informatie toevoegen die niet in de tekst staat",
          "error_type": "letterlijk_gemist"
        }
      },
      "workedExample": {
        "steps": [
          "Stap 1: Lees de vraag: 'Wat moet de robot doen?'",
          "Stap 2: Zoek in de eerste alinea naar de beschrijving van de robot",
          "Stap 3: Vind de zin: 'kan over een plank rijden en een blokje oppakken'",
          "Stap 4: Dit zijn twee handelingen: (1) over plank rijden (2) blokje oppakken",
          "Antwoord: B - Over plank en blokje pakken"
        ]
      }
    }
  }
}
```

---

**Ready to enhance? Start with:** `node scripts/schema-validator-v2.js`
