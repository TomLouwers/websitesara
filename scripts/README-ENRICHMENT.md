# Exercise Enrichment Tool

Automatically enhance existing exercises by adding AI-generated pedagogical features:
- Progressive hints (3 levels)
- Per-option feedback
- Learning strategies (LOVA framework)
- Common errors documentation

This transforms basic exercises (questions + answers only) into high-quality learning experiences.

## The Problem

Most of your **3000+ existing exercises** have:
- ❌ No hints (7% have basic hints)
- ❌ No per-option feedback
- ❌ No learning strategies
- ❌ Quality score: 30-40%

## The Solution

The enrichment tool uses AI to generate comprehensive support files that add:
- ✅ 3-level progressive hints for every question
- ✅ Specific feedback for each answer option (why wrong?)
- ✅ LOVA learning strategies (reading + math)
- ✅ Common errors documentation
- ✅ Quality score: 70-85%

**Result:** Students get the same pedagogical support as newly generated exercises!

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r scripts/requirements-ai-generation.txt
```

### 2. Set API Key

```bash
export ANTHROPIC_API_KEY='your-key-here'
```

### 3. Enrich Exercises

```bash
# Enrich single exercise
python3 scripts/enrich-exercises.py \
  --file data-v2/exercises/gb/gb_groep3_e3_core.json

# Enrich all exercises in category (recommended)
python3 scripts/enrich-exercises.py \
  --category gb \
  --validate

# Enrich all exercises (be careful - costs $$$)
python3 scripts/enrich-exercises.py \
  --all \
  --validate
```

---

## How It Works

### Input: Basic Exercise (30% quality)

```json
{
  "metadata": {
    "id": "gb_groep3_e3",
    "grade": 3,
    "title": "Basisvaardigheden Groep 3"
  },
  "items": [
    {
      "id": 1,
      "question": { "text": "Bereken: 7 × 8" },
      "options": [
        {"text": "54"},
        {"text": "56"},  // correct
        {"text": "63"},
        {"text": "64"}
      ],
      "answer": { "correct_index": 1 }
    }
  ]
}
```

**Missing:** Hints, feedback, strategies → **Quality: 30%**

---

### Output: Enriched Exercise (85% quality)

```json
{
  "support_items": [
    {
      "item_id": 1,
      "hints": [
        {
          "level": 1,
          "text": "Denk aan de tafel van 7. Probeer het rijtje op te zeggen.",
          "cost_points": 0
        },
        {
          "level": 2,
          "text": "Je kunt ook splitsen: 7 × 8 = 7 × (5 + 3) = 35 + 21",
          "cost_points": 1
        },
        {
          "level": 3,
          "text": "7 × 8 = 56. Tel na: 7+7+7+7+7+7+7+7 = 56",
          "cost_points": 2
        }
      ],
      "feedback": {
        "correct": "Uitstekend! Je beheerst de tafel van 7 goed.",
        "incorrect": [
          {
            "option_index": 0,
            "text": "Let op! 54 is het antwoord bij 6 × 9. Je hebt de tafel van 7 nodig."
          },
          {
            "option_index": 2,
            "text": "63 is het antwoord bij 7 × 9. Je zit dicht bij het goede antwoord!"
          },
          {
            "option_index": 3,
            "text": "64 is het antwoord bij 8 × 8. Check: we rekenen 7 × 8."
          }
        ]
      },
      "learning_strategies": {
        "reading_strategy": {
          "name": "LOVA - Lezen",
          "description": "Lees zorgvuldig: welke twee getallen vermenigvuldig je?"
        },
        "math_strategy": {
          "name": "Tafelkennis automatiseren",
          "description": "Oefen tafels regelmatig. Bij twijfel: splits of tel op."
        }
      },
      "common_errors": [
        {
          "error": "Verwisselen van nabije tafels",
          "explanation": "Leerlingen verwarren 7×8 met 7×9 of 8×8"
        }
      ]
    }
  ]
}
```

**Added:** Progressive hints, per-option feedback, strategies → **Quality: 85%**

---

## Usage Examples

### Enrich Single File

```bash
python3 scripts/enrich-exercises.py \
  --file data-v2/exercises/gb/gb_groep3_e3_core.json
```

**Output:**
```
📝 Enriching: gb_groep3_e3
   Tokens: 1,234 in + 2,456 out = $0.0234
   ✅ Saved support to data-v2-draft/exercises/gb/gb_groep3_e3_support.json
```

---

### Enrich Entire Category

```bash
# Enrich all "Getallen & Bewerkingen" exercises
python3 scripts/enrich-exercises.py \
  --category gb \
  --validate

# With limit (test first 10)
python3 scripts/enrich-exercises.py \
  --category gb \
  --limit 10
```

**Output:**
```
================================================================================
EXERCISE ENRICHMENT
================================================================================

📁 Found 45 exercises to enrich

[1/45] 📝 Enriching: gb_groep3_e3
   Tokens: 1,234 in + 2,456 out = $0.0234
   ✅ Saved support to data-v2-draft/exercises/gb/gb_groep3_e3_support.json

[2/45] 📝 Enriching: gb_groep3_m3
   ...

================================================================================
SUMMARY
================================================================================
Enriched: 45 exercises ✅
Failed:   0 exercises

Total tokens: 55,530 in + 110,520 out
Total cost:   $1.82
================================================================================

🔍 Running validation...
   gb_groep3_e3: 82.5% quality
   gb_groep3_m3: 78.0% quality
   ...
```

---

### Enrich All Exercises

⚠️ **Warning:** This enriches ALL exercises in data-v2/exercises/ - could cost $50-100 depending on how many need enrichment!

```bash
# Dry-run first to see what would be enriched
python3 scripts/enrich-exercises.py \
  --all \
  --dry-run

# Then enrich for real
python3 scripts/enrich-exercises.py \
  --all \
  --validate
```

---

## Model Selection

Choose AI model based on speed/cost tradeoff:

```bash
# Default: Claude Haiku (fast & cheap - recommended)
python3 scripts/enrich-exercises.py \
  --category gb

# Claude Sonnet (better quality, slower, more expensive)
python3 scripts/enrich-exercises.py \
  --category gb \
  --model claude-3-5-sonnet-20241022

# GPT-4o-mini (OpenAI alternative)
python3 scripts/enrich-exercises.py \
  --category gb \
  --model gpt-4o-mini
```

### Cost Comparison (per exercise):

| Model | Quality | Speed | Cost/Exercise |
|-------|---------|-------|---------------|
| Claude Haiku (default) | Good | Fast | $0.02-0.04 |
| Claude Sonnet | Excellent | Medium | $0.08-0.12 |
| GPT-4o-mini | Good | Fast | $0.01-0.03 |

**Recommendation:** Start with Claude Haiku. It's 3-4x cheaper than Sonnet and produces excellent results for enrichment.

---

## Workflow Integration

### Complete Enrichment Workflow

```bash
# Step 1: Find exercises that need enrichment
python3 scripts/enrich-exercises.py \
  --category gb \
  --dry-run

# Step 2: Enrich exercises (to draft folder)
python3 scripts/enrich-exercises.py \
  --category gb \
  --validate

# Step 3: Review enriched exercises
open tools/review-exercises.html
# Load files from data-v2-draft/exercises/gb/
# Review quality scores and approve

# Step 4: Publish approved enrichments
python3 scripts/publish-approved.py \
  --from data-v2-draft/exercises/gb/ \
  --to data-v2/exercises/gb/ \
  --validate \
  --update-index

# Step 5: Clean up draft
rm -rf data-v2-draft/exercises/gb/*_support.json
```

---

## Safety Features

### 1. **No Overwriting**

By default, enrichment skips exercises that already have support files:

```
⚠️  Support file already exists: gb_groep3_e3_support.json
Skipping (use --force to overwrite)
```

Use `--force` to overwrite existing support files.

---

### 2. **Draft Directory**

Enriched support files go to `data-v2-draft/` by default, not production:

```bash
# Safe: goes to draft
python3 scripts/enrich-exercises.py --category gb

# Custom output
python3 scripts/enrich-exercises.py \
  --category gb \
  --output-dir custom/path
```

---

### 3. **Validation**

Use `--validate` to check quality after enrichment:

```bash
python3 scripts/enrich-exercises.py \
  --category gb \
  --validate
```

Validation checks:
- ✅ Schema compliance
- ✅ All items have hints
- ✅ All items have per-option feedback
- ✅ Learning strategies present
- ✅ Quality score 70-100%

---

### 4. **Dry-Run**

Preview what will be enriched without spending money:

```bash
python3 scripts/enrich-exercises.py \
  --category gb \
  --dry-run
```

Output:
```
🔍 DRY RUN MODE - No files will be created

   Would enrich: data-v2/exercises/gb/gb_groep3_e3_core.json
   Would enrich: data-v2/exercises/gb/gb_groep3_m3_core.json
   ...
```

---

## Cost Estimation

### Per Exercise

**Average exercise:**
- 5-10 questions
- ~1,500 input tokens (questions + context)
- ~3,000 output tokens (hints + feedback + strategies)

**Cost with Claude Haiku:**
- Input: (1,500 / 1M) × $0.25 = $0.000375
- Output: (3,000 / 1M) × $1.25 = $0.00375
- **Total: ~$0.004 per exercise**

### By Scale

| Exercises | Haiku Cost | Sonnet Cost | Time (Haiku) |
|-----------|------------|-------------|--------------|
| 10 | $0.04 | $0.12 | 30 seconds |
| 50 | $0.20 | $0.60 | 2 minutes |
| 100 | $0.40 | $1.20 | 5 minutes |
| 500 | $2.00 | $6.00 | 25 minutes |
| 1000 | $4.00 | $12.00 | 50 minutes |
| 3000 | $12.00 | $36.00 | 2.5 hours |

**Recommendation:** Start with one category (50-100 exercises) to validate quality, then scale up.

---

## Quality Impact

### Before Enrichment

**Typical legacy exercise:**
```
✓ Has questions and answers
✗ No hints
✗ No feedback
✗ No strategies
Quality: 30-40%
```

**Student experience:**
- Gets question wrong → just sees "incorrect"
- No guidance on how to improve
- No scaffolding for learning

---

### After Enrichment

**Enriched exercise:**
```
✓ Has questions and answers
✓ 3-level progressive hints
✓ Per-option feedback (explains misconceptions)
✓ LOVA learning strategies
✓ Common errors documented
Quality: 70-85%
```

**Student experience:**
- Gets question wrong → sees specific feedback: "You confused 7×8 with 7×9"
- Can request hints (3 levels of scaffolding)
- Learns strategies: "Use splitting: 7×8 = 7×(5+3)"

---

## Troubleshooting

### Problem: "Anthropic SDK not installed"

```bash
pip install anthropic
# or
pip install -r scripts/requirements-ai-generation.txt
```

---

### Problem: "API key not found"

```bash
export ANTHROPIC_API_KEY='your-key-here'

# Verify it's set
echo $ANTHROPIC_API_KEY
```

---

### Problem: "Support file already exists"

Use `--force` to overwrite:

```bash
python3 scripts/enrich-exercises.py \
  --category gb \
  --force
```

---

### Problem: "Failed to parse AI response as JSON"

The AI occasionally produces invalid JSON. This is rare with Haiku/Sonnet. Try:

1. Re-run the same exercise (AI is non-deterministic)
2. Use a different model (`--model claude-3-5-sonnet-20241022`)
3. Check the error message for details

---

## Advanced Usage

### Limit Number of Exercises

```bash
# Enrich only first 10 exercises (for testing)
python3 scripts/enrich-exercises.py \
  --category gb \
  --limit 10
```

---

### Custom Output Directory

```bash
# Save to custom location
python3 scripts/enrich-exercises.py \
  --category gb \
  --output-dir /custom/path/exercises
```

---

### Combine with Other Tools

```bash
# Enrich, validate, and publish in one workflow
python3 scripts/enrich-exercises.py --category gb --validate && \
python3 scripts/publish-approved.py \
  --from data-v2-draft/exercises/gb/ \
  --to data-v2/exercises/gb/ \
  --update-index
```

---

## Best Practices

### 1. **Start Small**

Test with 10-20 exercises first:

```bash
python3 scripts/enrich-exercises.py \
  --category gb \
  --limit 10 \
  --validate
```

Review the quality before scaling up.

---

### 2. **Review Before Publishing**

Always review enriched exercises in the review tool:

```bash
# After enrichment
open tools/review-exercises.html
```

Check:
- Are hints helpful and age-appropriate?
- Is feedback accurate and constructive?
- Are strategies clear and actionable?

---

### 3. **Use Haiku for Volume**

For enriching hundreds of exercises, use Claude Haiku:
- 3-4x cheaper than Sonnet
- Still produces excellent quality
- Fast enough for batch processing

---

### 4. **Track Costs**

The script outputs total cost at the end:

```
Total tokens: 55,530 in + 110,520 out
Total cost:   $1.82
```

Monitor costs as you scale up.

---

## FAQ

### Q: Will this overwrite my existing exercises?

**A:** No! Enrichment:
1. Reads core file (questions/answers) from `data-v2/exercises/`
2. Generates support file (hints/feedback) to `data-v2-draft/exercises/`
3. Never modifies the original core file

---

### Q: What if an exercise already has a support file?

**A:** By default, enrichment skips it. Use `--force` to overwrite.

---

### Q: Can I enrich exercises that were manually created?

**A:** Yes! The enrichment tool works with any core exercise file, whether it was:
- Manually created
- Generated by the old system
- Generated by the new AI system

As long as it has questions and answers, it can be enriched.

---

### Q: How long does it take?

**A:** With Claude Haiku:
- Single exercise: ~3-5 seconds
- 100 exercises: ~5 minutes
- 1000 exercises: ~50 minutes

---

### Q: Can I stop and resume?

**A:** Yes! The script:
- Skips exercises that already have support files
- Saves each enrichment immediately
- Can be safely interrupted (Ctrl+C)
- Resume by running the same command again

---

### Q: What's the quality difference between Haiku and Sonnet?

**A:** For enrichment tasks:
- **Haiku:** 70-85% quality, great hints/feedback, fast, cheap
- **Sonnet:** 75-90% quality, slightly better nuance, slower, 3-4x more expensive

**Recommendation:** Haiku is sufficient for most enrichment. Use Sonnet only if you need the absolute highest quality.

---

## Next Steps

1. **Test with small batch:**
   ```bash
   python3 scripts/enrich-exercises.py --category gb --limit 10
   ```

2. **Review quality in browser:**
   ```bash
   open tools/review-exercises.html
   ```

3. **If satisfied, scale up:**
   ```bash
   python3 scripts/enrich-exercises.py --category gb --validate
   ```

4. **Publish to production:**
   ```bash
   python3 scripts/publish-approved.py \
     --from data-v2-draft/exercises/gb/ \
     --to data-v2/exercises/gb/ \
     --update-index
   ```

5. **Repeat for other categories:**
   ```bash
   python3 scripts/enrich-exercises.py --category bl  # Begrijpend lezen
   python3 scripts/enrich-exercises.py --category sp  # Spelling
   # etc.
   ```

---

**Transform your 3000+ exercises from basic Q&A to comprehensive learning experiences!** 🚀
