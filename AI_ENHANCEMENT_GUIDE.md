# AI-Assisted Exercise Enhancement Guide

**Status:** AI Enhancement Tool Ready
**Date:** January 8, 2026
**Time Savings:** 174 hours → 20-30 hours (85% reduction!)

---

## 🚀 Quick Start

### Step 1: Get API Key

**Option A: Anthropic Claude (Recommended)**
1. Go to https://console.anthropic.com/
2. Sign up / Log in
3. Navigate to API Keys
4. Create new key
5. Copy the key (starts with `sk-ant-...`)

**Option B: OpenAI**
1. Go to https://platform.openai.com/
2. Sign up / Log in
3. Navigate to API Keys
4. Create new key
5. Copy the key (starts with `sk-...`)

### Step 2: Set Environment Variable

**On Linux/Mac:**
```bash
# Add to your ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Or for this session only
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**On Windows:**
```cmd
# Command Prompt
set ANTHROPIC_API_KEY=sk-ant-your-key-here

# PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**Or create a .env file in project root:**
```bash
# Create .env file
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > .env

# Add to .gitignore (IMPORTANT!)
echo ".env" >> .gitignore
```

### Step 3: Test on Small Sample

```bash
# Create a test file with just 1-2 exercises
node scripts/ai-enhancer.js data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json

# Follow the interactive prompts
# Review the AI-generated feedback
# Approve or reject each question
```

### Step 4: Batch Process All Templates

```bash
# See "Batch Processing" section below for full workflow
```

---

## 📖 Usage Guide

### Basic Usage

```bash
node scripts/ai-enhancer.js <template-file>
```

**Example:**
```bash
node scripts/ai-enhancer.js data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json
```

**Output:**
- Creates `bl_groep4_e4_1_AI_ENHANCED.json`
- Interactive review for each question
- Progress saved automatically

### Command Line Options

```bash
# Use specific provider
node scripts/ai-enhancer.js <file> --provider=anthropic  # Default
node scripts/ai-enhancer.js <file> --provider=openai

# Use specific model
node scripts/ai-enhancer.js <file> --model=claude-sonnet-4-5-20250929
node scripts/ai-enhancer.js <file> --model=gpt-4o

# Custom output file
node scripts/ai-enhancer.js <file> --output=custom_output.json

# Batch size (questions per batch)
node scripts/ai-enhancer.js <file> --batch-size=10

# Auto-approve (skip review - USE WITH CAUTION!)
node scripts/ai-enhancer.js <file> --auto-approve

# Pass API key directly (not recommended - use env var)
node scripts/ai-enhancer.js <file> --api-key=sk-ant-...
```

### Interactive Review Mode

When you run the tool, you'll see:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Exercise: De verdwenen sleutel
Question: 1a
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Question:
Waarom noemt Lisa de hamster 'Nibbel'?

✓ Correct Feedback:
  Explanation: Helemaal goed! In de tekst staat letterlijk...
  Reinforcement: Je kunt letterlijke informatie goed vinden!

✗ Incorrect Feedback (sample - Option A):
  Explanation: Dit antwoord is niet correct omdat...
  Hint: Zoek in de tekst naar het woord 'omdat'...
  Error type: letterlijk_gemist

📝 Worked Example:
  1. Lees de vraag: 'Waarom noemt Lisa...'
  2. Zoek in de tekst naar 'Nibbel'
  3. Lees de zin met 'omdat'
  4. Het antwoord staat na 'omdat'

Approve this enhancement? (y/n/edit/quit):
```

**Your options:**
- `y` or `yes` - Approve and save this enhancement
- `n` or `no` - Skip this question (keep template)
- `edit` or `e` - Save for manual editing later
- `quit` or `q` - Stop and save progress

---

## 🔄 Batch Processing Workflow

### Process All Templates Systematically

**Step 1: Start with Groep 4 (Foundation)**

```bash
# Reading (153 questions)
node scripts/ai-enhancer.js data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json

# Math (260 questions)
node scripts/ai-enhancer.js data/exercises/gb/gb_groep4_m4_TEMPLATE.json
```

**Review time:** ~2-3 hours for both files

**Step 2: Groep 5 (Development)**

```bash
# Reading - Set 1 (153 questions)
node scripts/ai-enhancer.js data/exercises/bl/bl_groep5_e5_1_TEMPLATE.json

# Reading - Set 2 (already templated from Phase 2A)
node scripts/ai-enhancer.js data/exercises/bl/bl_groep5_m5_1_TEMPLATE.json

# Math (240 questions)
node scripts/ai-enhancer.js data/exercises/gb/gb_groep5_m5_TEMPLATE.json
```

**Review time:** ~2-3 hours

**Step 3: Groep 6 (Intermediate)**

```bash
# Reading - Set 1
node scripts/ai-enhancer.js data/exercises/bl/bl_groep6_e6_1_TEMPLATE.json

# Reading - Set 2
node scripts/ai-enhancer.js data/exercises/bl/bl_groep6_m6_1_TEMPLATE.json

# Math
node scripts/ai-enhancer.js data/exercises/gb/gb_groep6_m6_TEMPLATE.json
```

**Review time:** ~2 hours

**Step 4: Groep 7 (Advanced)**

```bash
node scripts/ai-enhancer.js data/exercises/bl/bl_groep7_e7_1_TEMPLATE.json
node scripts/ai-enhancer.js data/exercises/bl/bl_groep7_m7_1_TEMPLATE.json
node scripts/ai-enhancer.js data/exercises/gb/gb_groep7_m7_TEMPLATE.json
```

**Review time:** ~2 hours

**Step 5: Groep 8 (Mastery)**

```bash
node scripts/ai-enhancer.js data/exercises/bl/bl_groep8_e8_1_TEMPLATE.json
node scripts/ai-enhancer.js data/exercises/bl/bl_groep8_m8_1_TEMPLATE.json
node scripts/ai-enhancer.js data/exercises/gb/gb_groep8_e8_TEMPLATE.json  # Largest file!
```

**Review time:** ~3 hours

**Total Review Time:** 12-15 hours for all 2,087 questions

---

## 🎯 Auto-Approve Mode (Fast Track)

If you trust the AI and want maximum speed:

```bash
# Process entire file without review
node scripts/ai-enhancer.js data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json --auto-approve
```

**Benefits:**
- No manual review needed
- Process 153 questions in ~15-20 minutes
- All 2,087 questions in ~3-4 hours

**Risks:**
- No human quality check
- May contain some inaccuracies
- Requires post-processing validation

**Recommended approach:**
1. Review first 20-30 questions manually to check quality
2. If consistently good, switch to auto-approve for remainder
3. Do final spot-check validation at the end

---

## 📊 Cost Estimates

### Anthropic Claude (Recommended)

**Model:** Claude Sonnet 4.5
**Input:** ~1,000 tokens per question
**Output:** ~1,500 tokens per question

**Costs:**
- Input: $3.00 per million tokens
- Output: $15.00 per million tokens

**Per question:**
- Input: ~$0.003
- Output: ~$0.0225
- **Total: ~$0.026 per question**

**All 2,087 questions:**
- **Total cost: ~$54**

### OpenAI GPT-4o

**Model:** GPT-4o
**Similar token usage**

**Costs:**
- Input: $2.50 per million tokens
- Output: $10.00 per million tokens

**Per question:**
- Input: ~$0.0025
- Output: ~$0.015
- **Total: ~$0.018 per question**

**All 2,087 questions:**
- **Total cost: ~$38**

---

## 💡 Quality Control Tips

### What the AI Does Well

✅ **Excellent at:**
- Generating age-appropriate explanations
- Creating step-by-step worked examples
- Identifying misconceptions
- Providing encouraging feedback
- Maintaining consistent tone

✅ **Good at:**
- Categorizing error types
- Creating conceptual hints
- Adapting to different grade levels
- Following Schema V2.0 structure

### What to Watch For

⚠️ **Review carefully:**
- Math calculations (verify correctness)
- Reading text references (check quotes)
- Dutch language quality (grammar, spelling)
- Cultural appropriateness
- Logical consistency

⚠️ **Common AI issues:**
- Overly generic feedback (ask for more specificity)
- Missing text references
- Inconsistent error type classification
- Too complex language for younger grades

### Quality Checklist

For each enhanced question, verify:

- [ ] Feedback is specific (not generic)
- [ ] References actual question content
- [ ] Age-appropriate language
- [ ] Encouraging, positive tone
- [ ] Math notation correct (if applicable)
- [ ] Worked example has 3-5 clear steps
- [ ] Error types match allowed list
- [ ] All incorrect options have feedback
- [ ] Hints follow tier 1→2→3 progression

---

## 🔍 Post-Processing Workflow

After AI enhancement, follow this process:

### Step 1: Spot Check Quality

```bash
# Check random questions from enhanced file
# Look for patterns in quality
# Identify any systematic issues
```

### Step 2: Run Validator

```bash
node scripts/schema-validator-v2.js

# Check:
# - Enhanced count increased
# - No validation errors
# - Schema compliance
```

### Step 3: Test in Browser

1. Replace template with AI_ENHANCED version
2. Load in browser
3. Test several exercises
4. Verify:
   - Feedback displays correctly
   - Math renders properly (KaTeX)
   - No console errors
   - Positive student experience

### Step 4: Manual Refinement

```bash
# Open AI_ENHANCED file
# Search for any remaining issues
# Refine specific feedback as needed
# Focus on outliers, not every question
```

### Step 5: Finalize

```bash
# Rename AI_ENHANCED to final filename
mv data/exercises/bl/bl_groep4_e4_1_AI_ENHANCED.json data/exercises/bl/bl_groep4_e4_1.json

# Commit
git add data/exercises/bl/bl_groep4_e4_1.json
git commit -m "Groep 4 Reading - AI-enhanced with human review"
```

---

## 🚀 Accelerated Timeline

### Fast Track: 1 Week Timeline

**Day 1-2: Setup & Groep 4**
- Set up API keys
- Test on small sample
- Process Groep 4 (413 questions)
- Review time: 3-4 hours

**Day 3-4: Groep 5 & 6**
- Process Groep 5 (393 questions)
- Process Groep 6 (386 questions)
- Review time: 4-5 hours

**Day 5-6: Groep 7 & 8**
- Process Groep 7 (386 questions)
- Process Groep 8 (509 questions)
- Review time: 5-6 hours

**Day 7: Quality Control**
- Spot check all files
- Run validator
- Test in browser
- Manual refinements

**Total time: 15-20 hours spread over 1 week**

---

## 🛠️ Troubleshooting

### API Key Issues

**Error:** `API key not found`
```bash
# Check environment variable is set
echo $ANTHROPIC_API_KEY

# If empty, set it
export ANTHROPIC_API_KEY="sk-ant-your-key"

# Or use --api-key flag
node scripts/ai-enhancer.js <file> --api-key=sk-ant-your-key
```

### Rate Limiting

**Error:** `429 Too Many Requests`
```bash
# Tool has built-in 1-second delay
# If still hitting limits, increase batch size
node scripts/ai-enhancer.js <file> --batch-size=3  # Slower but safer
```

### JSON Parse Errors

**Error:** `Could not parse JSON from AI response`
- Usually self-corrects on retry
- If persistent, file an issue
- Workaround: Use --auto-approve with manual review later

### Network Issues

**Error:** `ECONNRESET` or timeout
- Check internet connection
- Retry the same file (progress is saved)
- Tool will skip already-enhanced questions

---

## 📈 Success Metrics

Track your progress:

```bash
# Before AI enhancement
node scripts/schema-validator-v2.js
# Enhanced (V2.0): 4 (0.1%)

# After Groep 4
# Enhanced (V2.0): 417 (15%)

# After Groep 5
# Enhanced (V2.0): 810 (29%)

# After all grades
# Enhanced (V2.0): 2,091 (75%)

# After remaining 693 questions
# Enhanced (V2.0): 2,784 (100%) 🎉
```

---

## 💡 Tips for Best Results

### 1. Review First Batch Carefully

The first 20-30 questions set your quality baseline. Review these thoroughly to understand AI patterns.

### 2. Use Consistent Approval Criteria

Decide on your quality threshold:
- **Strict:** Only approve near-perfect feedback
- **Moderate:** Approve good-enough, fix outliers later
- **Lenient:** Auto-approve, spot-check after

### 3. Process Similar Content Together

- All Groep 4 reading in one session
- All math exercises in one session
- Builds pattern recognition

### 4. Take Breaks

Reviewing AI output requires focus. Take breaks every 50-100 questions to maintain quality judgment.

### 5. Document Patterns

If you notice recurring issues, document them:
- "Math feedback needs more KaTeX notation"
- "Reading feedback too generic in option explanations"
- Share with AI by refining prompts

---

## 🔄 Iterative Improvement

After processing a few files:

### Analyze Quality Patterns

```bash
# Review approved vs. skipped ratio
# If many skips, investigate why
# Adjust expectations or improve prompts
```

### Refine Prompts (Advanced)

Edit `scripts/ai-enhancer.js` line ~100+ to customize prompts:
- Add examples of excellent feedback
- Emphasize specific requirements
- Adjust tone guidelines

### Share Results

Document what works:
- Best models for your use case
- Optimal review workflow
- Quality patterns observed

---

## 🎯 Next Steps

**You're ready to start AI enhancement!**

1. **Get API key** (5 minutes)
2. **Set environment variable** (2 minutes)
3. **Test on small sample** (15 minutes)
4. **Process Groep 4** (3-4 hours)
5. **Continue with remaining grades** (12-15 hours)

**Total time:** 15-20 hours for all 2,087 questions

**Cost:** ~$38-54 depending on provider

**Result:** 75% of all exercises enhanced with high-quality Schema V2.0 feedback!

---

## 📞 Support

**Tool issues?**
- Check this guide
- Review error messages
- Test with small sample first

**Quality concerns?**
- Review first 20-30 questions manually
- Adjust approval criteria
- Use edit mode for refinements

**API questions?**
- Anthropic docs: https://docs.anthropic.com/
- OpenAI docs: https://platform.openai.com/docs

---

**Ready to enhance 2,087 questions in ~20 hours? Let's go! 🚀**
