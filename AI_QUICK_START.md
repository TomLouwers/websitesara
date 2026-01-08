# AI Enhancement - Quick Start Card

**⏱️ Save 150+ hours with AI-assisted enhancement!**

---

## 🚀 3-Step Quick Start

### 1️⃣ Get API Key (5 min)

**Anthropic Claude (Recommended):**
→ https://console.anthropic.com/ → API Keys → Create Key

**Copy key** (starts with `sk-ant-...`)

### 2️⃣ Set Environment Variable (1 min)

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### 3️⃣ Run Enhancement (3-20 hours total)

```bash
# Single file (with review)
node scripts/ai-enhancer.js data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json

# All files (batch processing)
./scripts/batch-ai-enhance.sh

# Fast mode (auto-approve, no review)
./scripts/batch-ai-enhance.sh --auto-approve
```

---

## 📊 Time & Cost

| Mode | Time | Cost | Quality |
|------|------|------|---------|
| **With Review** (Recommended) | 15-20 hours | ~$38-54 | ⭐⭐⭐⭐⭐ High |
| **Auto-Approve** | 3-4 hours | ~$38-54 | ⭐⭐⭐⭐ Good |
| **Manual** (no AI) | 174 hours | $0 | ⭐⭐⭐⭐⭐ High |

**Time savings: 150+ hours!**

---

## 💡 Recommended Workflow

### Day 1: Test & Groep 4 (4 hours)
```bash
# Test on small sample
node scripts/ai-enhancer.js data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json

# Review first 20 questions carefully
# If quality is good, continue

# Process Groep 4 math
node scripts/ai-enhancer.js data/exercises/gb/gb_groep4_m4_TEMPLATE.json
```

### Day 2-3: Groep 5-6 (5 hours)
```bash
./scripts/batch-ai-enhance.sh --grade=5
./scripts/batch-ai-enhance.sh --grade=6
```

### Day 4-5: Groep 7-8 (5 hours)
```bash
./scripts/batch-ai-enhance.sh --grade=7
./scripts/batch-ai-enhance.sh --grade=8
```

### Day 6: Quality Control (3 hours)
```bash
# Validate all files
node scripts/schema-validator-v2.js

# Test in browser
# Manual spot-check refinements
```

**Total: 1 week, 17-20 hours**

---

## ✅ Quality Checklist

For each file, the AI generates:

✅ **Correct Feedback**
- Specific explanation (references text/question)
- Skill reinforcement (positive encouragement)

✅ **Incorrect Feedback** (per option)
- Why option is wrong
- Directional hint
- Misconception identified
- Error type classified

✅ **Worked Example**
- 3-5 clear steps
- Age-appropriate language
- Leads to correct answer

✅ **3-Tier Hints**
- Tier 1: WHERE to look (procedural)
- Tier 2: WHAT to think about (conceptual)
- Tier 3: HOW to solve (worked example)

---

## 🎯 Review Tips

When reviewing AI output:

**Approve (y) if:**
- Feedback is specific and accurate
- Language is age-appropriate
- Tone is positive and encouraging
- References actual content

**Skip (n) if:**
- Too generic ("Good job!")
- Incorrect information
- Wrong grade level language
- Missing key explanations

**Edit (e) if:**
- Mostly good, needs minor tweaks
- Save for manual refinement later

---

## 📈 Progress Tracking

```bash
# Before
Enhanced (V2.0): 4 (0.1%)

# After Groep 4
Enhanced (V2.0): 417 (15%)

# After all templates
Enhanced (V2.0): 2,091 (75%)

# Final goal
Enhanced (V2.0): 2,784 (100%) 🎉
```

---

## 🆘 Troubleshooting

**API key not found?**
```bash
echo $ANTHROPIC_API_KEY  # Check if set
export ANTHROPIC_API_KEY="sk-ant-..."  # Set it
```

**Rate limiting?**
```bash
# Reduce batch size
node scripts/ai-enhancer.js <file> --batch-size=3
```

**JSON parse errors?**
- Usually self-corrects
- Retry same file (progress saved)

---

## 📚 Full Documentation

- **AI_ENHANCEMENT_GUIDE.md** - Complete guide with all options
- **TEMPLATES_OVERVIEW.md** - All templates reference
- **ENHANCEMENT_WORKFLOW.md** - Manual enhancement guide

---

## 🎉 You're Ready!

1. Get API key
2. Set environment variable
3. Run: `node scripts/ai-enhancer.js <file>`
4. Review and approve
5. Celebrate 150+ hours saved! 🎊

**Questions? Check AI_ENHANCEMENT_GUIDE.md**
