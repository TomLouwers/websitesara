# AI-Powered Exercise Generation

Automatically generate high-quality exercises using AI (Claude or GPT) from CSV prompt templates.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r scripts/requirements-ai-generation.txt
```

### 2. Set API Key

**For Claude (Recommended):**
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

**For GPT (Alternative):**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### 3. Generate Exercises

```bash
# Generate 10 exercises for Groep 4, row 15 from rekenen CSV
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --row 15 \
  --validate

# Generate all Groep 4 exercises
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --grade 4 \
  --validate

# Batch generate entire CSV
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --batch \
  --validate
```

## Features

### ✨ What It Does

1. **Reads CSV prompt templates** from `docs/reference/*.csv`
2. **Generates structured JSON** matching schema v2.0.0 (core + support)
3. **Creates both files:**
   - Core file: Questions, options, answers
   - Support file: Hints, feedback, learning strategies
4. **Automatic validation** with comprehensive_validation.py
5. **Cost tracking** and token usage reporting
6. **Progress saving** (resume interrupted generations)

### 📊 Quality Features

Generated exercises include:
- ✅ 3-level progressive hints (general → specific → near-solution)
- ✅ Per-option feedback (specific feedback for each wrong answer)
- ✅ Learning strategies (reading/math strategies)
- ✅ Common errors documentation
- ✅ SLO alignment metadata
- ✅ Age-appropriate language
- ✅ Diverse contexts and names

Target quality score: **70-85%** on first generation

## Usage Guide

### Generate from Specific Row

```bash
# Row 15 only (1-indexed)
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --row 15
```

### Generate by Grade/Level

```bash
# All Groep 4 exercises
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --grade 4

# Only "Midden" level (M)
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --level M

# Groep 5, Eind level
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --grade 5 \
  --level E
```

### Override Exercise Count

```bash
# Generate 20 exercises instead of default
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --row 10 \
  --count 20
```

### Choose AI Model

```bash
# Use Claude Sonnet (default, best quality)
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --model claude-3-5-sonnet-20241022

# Use Claude Haiku (faster, cheaper)
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --model claude-3-haiku-20240307

# Use GPT-4o
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --model gpt-4o

# Use GPT-4o-mini (cheapest)
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --model gpt-4o-mini
```

### Validation Options

```bash
# Validate after generation (recommended)
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --validate

# Continue even if validation fails
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --validate \
  --skip-validation-failures
```

### Output Directory

```bash
# Custom output location
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --output my-custom-output/exercises
```

## Available Models

| Model | Provider | Input Cost | Output Cost | Speed | Quality | Best For |
|-------|----------|------------|-------------|-------|---------|----------|
| `claude-3-5-sonnet-20241022` | Anthropic | $3.00/M | $15.00/M | Medium | ⭐⭐⭐⭐⭐ | **Default, best quality** |
| `claude-3-haiku-20240307` | Anthropic | $0.25/M | $1.25/M | Fast | ⭐⭐⭐⭐ | High volume, cost-sensitive |
| `gpt-4o` | OpenAI | $2.50/M | $10.00/M | Medium | ⭐⭐⭐⭐ | Alternative to Claude |
| `gpt-4o-mini` | OpenAI | $0.15/M | $0.60/M | Fast | ⭐⭐⭐ | Testing, drafts |

**M = Million tokens**

### Cost Estimates

**Generating 10 exercises** (typical):
- **Claude Sonnet**: ~$0.15 - $0.30
- **Claude Haiku**: ~$0.02 - $0.05
- **GPT-4o**: ~$0.10 - $0.25
- **GPT-4o-mini**: ~$0.01 - $0.03

**Generating 100 exercises** (batch):
- **Claude Sonnet**: ~$1.50 - $3.00
- **Claude Haiku**: ~$0.20 - $0.50

**Generating entire CSV** (~200 exercises):
- **Claude Sonnet**: ~$3.00 - $6.00
- **Claude Haiku**: ~$0.40 - $1.00

## Example Output

```
📚 Loading tasks from docs/reference/rekenen-getallen.csv...
   Found 3 tasks to generate

🤖 Initializing AI generator with claude-3-5-sonnet-20241022...

================================================================================
GENERATING EXERCISES
================================================================================

[1/3] 4G1: Tafels 1-10 automatiseren

📝 Generating 25 exercises for 4G1 (Groep 4, M)...
   Tokens: 3,245 in + 8,912 out = $0.1441
   ✅ Saved to data-v2-draft/exercises/gb/gb_groep4_m_4g1_core.json
   ✅ Validation passed! Quality: 78.5%

[2/3] 4G2: Plaatswaarde E, T, H

📝 Generating 12 exercises for 4G2 (Groep 4, M)...
   Tokens: 2,987 in + 6,234 out = $0.1027
   ✅ Saved to data-v2-draft/exercises/gb/gb_groep4_m_4g2_core.json
   ✅ Validation passed! Quality: 82.1%

[3/3] 4G3: Optellen en aftrekken tot 100

📝 Generating 15 exercises for 4G3 (Groep 4, M)...
   Tokens: 3,102 in + 7,445 out = $0.1209
   ✅ Saved to data-v2-draft/exercises/gb/gb_groep4_m_4g3_core.json
   ✅ Validation passed! Quality: 75.3%

================================================================================
GENERATION SUMMARY
================================================================================
Total tasks:       3
Successful:        3 ✅
Failed:            0 ❌

Tokens used:       9,334 in + 22,591 out
Total cost:        $0.3677 USD

Validation passed: 3/3
Avg quality score: 78.6%
================================================================================

📁 Generated files saved to: data-v2-draft/exercises/
   - data-v2-draft/exercises/gb/gb_groep4_m_4g1_core.json
   - data-v2-draft/exercises/gb/gb_groep4_m_4g2_core.json
   - data-v2-draft/exercises/gb/gb_groep4_m_4g3_core.json
```

## Workflow Integration

### 1. Generate → 2. Review → 3. Publish

#### Step 1: Generate Drafts

```bash
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --grade 4 \
  --output data-v2-draft/exercises \
  --validate
```

Outputs to: `data-v2-draft/exercises/gb/`

#### Step 2: Review in Browser

```bash
# Open review tool (to be created)
open tools/review-exercises.html
```

- Review each exercise
- Edit inline if needed
- Approve/Reject
- Flag for AI revision

#### Step 3: Publish Approved

```bash
# Move approved exercises to production
python3 scripts/publish-approved.py \
  --from data-v2-draft/exercises/gb/ \
  --to data-v2/exercises/gb/

# Rebuild index
python3 scripts/build-index.py
```

## CSV Format Requirements

Your CSV must have these columns:

| Column | Required | Description |
|--------|----------|-------------|
| `Groep` | ✅ | Grade level (1-8) |
| `Code` | ✅ | Learning objective code (e.g., "4G1") |
| `Beschrijving` | ✅ | Short description |
| `Level` | ✅ | Difficulty level ("E" or "M") |
| `Toelichting` | ✅ | Detailed explanation |
| `Prompt_Template` | ✅ | Detailed AI generation prompt |

### Example Prompt Template

```
Genereer 25 oefeningen voor Groep 4 (midden schooljaar).
Kerndoel: K23 (Automatiseren van cijferen en hoofdrekenen).
Inhoudslijn: Getallen - Bewerkingen - Vermenigvuldigen en delen - Alle tafels.
Leerdoel (4G1): Alle tafels tot en met 10 volledig automatisch beheersen binnen 3 seconden per som.
Niveau: M (midden groep 4, cruciaal voor alle verdere rekenen).

Vraagtypen:
- 7×8=?, 6×9=?, 8×4=?
- Ook deelsommen: 56:7=?, 72:9=?
- Mix alle tafels 1-10 willekeurig
- Woordprobleem: 8 dozen met 6 appels per doos =?

Format: Snelle automatiseringsoefeningen met 4 antwoordopties per vraag, CITO-stijl tempometing.
```

The more detailed the prompt, the better the quality!

## Troubleshooting

### "API key not set"

```bash
# Make sure to export the correct key
export ANTHROPIC_API_KEY='sk-ant-...'

# Verify it's set
echo $ANTHROPIC_API_KEY
```

### "Could not find JSON in AI response"

The AI output wasn't valid JSON. This can happen with:
- Very complex prompts
- Low-quality models (use Sonnet instead of Haiku)
- Insufficient max_tokens

**Solution:** Try again with `--model claude-3-5-sonnet-20241022`

### Low Quality Scores

Generated exercises scoring < 60%:

**Common Issues:**
1. Missing per-option feedback → Add to prompt emphasis
2. Only 1-2 hints instead of 3 → Specify "exactly 3 progressive hints"
3. Missing learning strategies → Check prompt includes this

**Solution:** Regenerate with more explicit prompt or use better model

### Validation Failures

**Critical/Error issues:**
- Invalid answer index
- Missing required fields
- Duplicate options

**Solution:** Usually indicates AI didn't follow schema. Check:
1. System prompt is correct
2. Model is capable enough (use Sonnet)
3. Prompt isn't too complex

### High Costs

Generated 100 exercises and spent $10+?

**Check:**
- Are you using the right model? (Sonnet vs Haiku)
- Is `--count` set too high per task?
- Are prompt templates extremely long?

**Reduce costs:**
```bash
# Use cheaper model for drafts
--model claude-3-haiku-20240307

# Generate fewer per task
--count 10

# Generate one row at a time
--row 5
```

## Advanced Usage

### Custom System Prompt

Edit `_build_system_prompt()` in the script to customize:
- Output format
- Quality requirements
- Pedagogical rules
- Dutch language specifics

### Retry Failed Generations

```bash
# Generate report of failures
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --batch \
  --validate \
  > generation-log.txt 2>&1

# Review failures
grep "❌" generation-log.txt

# Retry specific row
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --row 23  # The failed row
```

### Parallel Generation (Advanced)

```bash
# Split CSV into chunks and run in parallel
split -l 10 docs/reference/rekenen-getallen.csv chunk_

# Run each chunk in background
for chunk in chunk_*; do
    python3 scripts/ai-bulk-generator.py --csv $chunk --batch &
done

# Wait for all to complete
wait
```

## Best Practices

### 1. Start Small

Don't generate 500 exercises on first try:

```bash
# Test with 1 row first
python3 scripts/ai-bulk-generator.py --csv docs/reference/rekenen-getallen.csv --row 1

# Review quality
# Adjust prompts if needed
# Then scale up
```

### 2. Use Validation

Always use `--validate` to catch issues early:

```bash
--validate  # Always include this!
```

### 3. Review Before Publishing

Generated ≠ Published. Always human review:
- Check 2-3 exercises manually
- Verify answer correctness
- Test readability
- Approve batch if samples look good

### 4. Iterate on Prompts

Low quality? Improve CSV prompts:
- Add more examples
- Be more specific about format
- Emphasize quality features (hints, feedback)
- Reference existing high-quality exercises

### 5. Track Costs

Monitor spending:

```bash
# Small test
--row 5 --count 5  # ~$0.05

# Before full batch, estimate
# 20 rows × 10 exercises × $0.02 = $4.00

# Set daily budget limit with API provider
```

## Related Scripts

- `scripts/comprehensive_validation.py` - Validates generated exercises
- `tools/review-exercises.html` - Manual review interface (to be created)
- `scripts/publish-approved.py` - Moves from draft to production (to be created)
- `scripts/enrich-existing-exercises.py` - Enhances legacy content (to be created)

## Future Enhancements

### Planned Features

- [ ] Resume interrupted batch generation
- [ ] Generate images for geometry exercises
- [ ] Multi-step problem generation
- [ ] Automatic distractor analysis (are wrong answers plausible?)
- [ ] A/B testing of different prompts
- [ ] Fine-tuning on high-quality examples

### Integration Ideas

- CI/CD pipeline: Auto-generate on CSV commit
- Webhook: Trigger generation from CMS
- Slack bot: Generate on command
- Analytics: Track which AI-generated exercises perform best

## Support

**Issues?**
1. Check this README
2. Verify API key is set
3. Test with single row first
4. Check model availability and quota
5. Review generation logs

**Quality concerns?**
1. Use Claude Sonnet (best quality)
2. Improve CSV prompt templates
3. Add more explicit requirements
4. Use validation to catch issues

---

**Version:** 1.0.0
**Last Updated:** 2026-01-05
**Maintainer:** Product Team
