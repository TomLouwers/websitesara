# 🎯 Geometry Exercise Enrichment Guide

## Overview

This guide will help you enrich the 14 geometry exercises with AI-generated:
- **Progressive hints** (3 levels of help)
- **Per-option feedback** (why each answer is right/wrong)
- **LOVA learning strategies**

**Cost:** ~$0.56 (14 exercises × $0.04 each)
**Time:** ~20-30 minutes
**Result:** 700 questions upgraded from 0% → 70-85% quality

---

## Prerequisites

### 1. Get Anthropic API Key

1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Navigate to: API Keys
4. Create a new key
5. Copy the key (starts with `sk-ant-...`)

### 2. Set Environment Variable

**On Linux/Mac:**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**On Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

---

## Method 1: Batch Enrichment (Recommended)

Run the bash script to enrich all 14 geometry exercises at once:

```bash
cd /home/user/websitesara
chmod +x scripts/enrich-geometry.sh
./scripts/enrich-geometry.sh
```

This will:
- Find all 14 geometry core files
- Enrich each with Claude Haiku
- Generate support files with hints/feedback
- Show progress for each file

---

## Method 2: Individual File Enrichment

Enrich exercises one at a time:

```bash
python3 scripts/enrich-exercises.py \
    --file data-v2/exercises/mk/gb_groep3_meetkunde_m3_core.json \
    --force \
    --output-dir data-v2/exercises
```

**All 14 files to enrich:**
```
data-v2/exercises/mk/gb_groep3_meetkunde_m3_core.json
data-v2/exercises/mk/gb_groep3_meetkunde_e3_core.json
data-v2/exercises/mk/gb_groep4_meetkunde_m4_core.json
data-v2/exercises/mk/gb_groep4_meetkunde_e4_core.json
data-v2/exercises/mk/gb_groep5_meetkunde_m5_core.json
data-v2/exercises/mk/gb_groep5_meetkunde_e5_core.json
data-v2/exercises/mk/gb_groep6_meetkunde_m6_core.json
data-v2/exercises/mk/gb_groep6_meetkunde_e6_core.json
data-v2/exercises/mk/gb_groep7_meetkunde_m7_core.json
data-v2/exercises/mk/gb_groep7_meetkunde_e7_core.json
data-v2/exercises/mk/gb_groep8_meetkunde_m8_core.json
data-v2/exercises/mk/gb_groep8_meetkunde_e8_core.json
```

---

## What Happens During Enrichment

For each exercise, the AI will:

1. **Analyze** the question and answer
2. **Generate** 3 progressive hints:
   - Hint 1: Gentle nudge in right direction
   - Hint 2: More specific guidance
   - Hint 3: Almost gives it away
3. **Create** feedback for each option:
   - Why correct answer is right
   - Why wrong answers are wrong
4. **Add** LOVA learning strategies
5. **Write** enriched support file

---

## Validation

After enrichment, validate the results:

```bash
python3 scripts/comprehensive_validation.py \
    --category mk \
    --report geometry-enriched.html
```

**Expected Results:**
- Before: 0% quality (no hints/feedback)
- After: 70-85% quality (full support)

---

## Example Output

### Before Enrichment:
```json
{
  "id": "ex_000001",
  "question": {
    "text": "Hoe lang is deze boek in centimeters? De liniaal laat 17 cm zien."
  },
  "options": ["16 cm", "18 cm", "17 cm", "19 cm"],
  "answer": {
    "type": "single",
    "correct_index": 2
  }
}
```

### After Enrichment:
```json
{
  "id": "ex_000001",
  "support": {
    "hints": [
      {
        "level": 1,
        "text": "Kijk goed naar wat de liniaal aangeeft. Welk getal zie je?"
      },
      {
        "level": 2,
        "text": "De liniaal laat 17 cm zien. Zoek het antwoord dat 17 cm is."
      },
      {
        "level": 3,
        "text": "Als de liniaal 17 cm laat zien, dan is het antwoord 17 cm."
      }
    ],
    "option_feedback": [
      {
        "option_index": 0,
        "text": "Dit is niet correct. 16 cm is 1 cm minder dan wat de liniaal laat zien."
      },
      {
        "option_index": 1,
        "text": "Dit is niet correct. 18 cm is 1 cm meer dan wat de liniaal laat zien."
      },
      {
        "option_index": 2,
        "text": "Correct! De liniaal laat 17 cm zien, dus het boek is 17 cm lang."
      },
      {
        "option_index": 3,
        "text": "Dit is niet correct. 19 cm is 2 cm meer dan wat de liniaal laat zien."
      }
    ],
    "lova_strategy": {
      "approach": "Direct aflezen van een meetinstrument",
      "common_errors": ["Verkeerd getal aflezen", "1 cm er naast zitten"]
    }
  }
}
```

---

## Cost Tracking

The enrichment tool shows cost for each exercise:

```
[1/14] Processing: gb_groep3_meetkunde_m3_core.json
   ✅ Success
   Tokens: 1,234 input, 2,456 output
   Cost: $0.04

[2/14] Processing: gb_groep3_meetkunde_e3_core.json
   ✅ Success
   Tokens: 1,345 input, 2,567 output
   Cost: $0.04

...

Total Cost: $0.56
```

---

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
Make sure you set the environment variable:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### "File not found" Error
Make sure you're in the project root directory:
```bash
cd /home/user/websitesara
```

### API Rate Limits
If you hit rate limits, the script will pause and retry automatically.

### Cost Concerns
- Each exercise costs ~$0.04
- You can test with one file first using Method 2
- Total cost for all 14: ~$0.56

---

## After Enrichment

Once enriched, the geometry exercises will have:
- ✅ Full pedagogical support
- ✅ Progressive hints for struggling students
- ✅ Clear feedback on mistakes
- ✅ 70-85% quality score (vs 0% before)

**Next steps:**
1. Validate results
2. Commit changes
3. Deploy to production
4. Students benefit immediately!

---

## Alternative: Pay Someone Else

If you prefer not to handle API keys, you can:
1. Export the core files
2. Send to a developer with API access
3. They run the enrichment
4. Import the enriched support files

The enrichment tool is completely automated - just needs the API key!
