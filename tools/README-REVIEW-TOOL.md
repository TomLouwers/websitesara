# Exercise Review Tool

Web-based interface for reviewing and approving AI-generated exercises before publishing.

## Features

✨ **Visual Review Interface**
- Side-by-side JSON editor and live preview
- Real-time syntax validation
- Quality score calculation
- Math notation rendering (KaTeX)

🎯 **Quick Actions**
- Approve (A) - Mark exercise as ready to publish
- Reject (R) - Discard low-quality exercise
- Flag (F) - Mark for further review with notes
- Skip - Move to next without decision

📊 **Dashboard**
- Track pending, approved, rejected, flagged counts
- Quality score display (0-100%)
- Validation error highlighting

⚡ **Keyboard Shortcuts**
- `A` - Approve current exercise
- `R` - Reject current exercise
- `F` - Flag for review
- `←` `→` - Navigate between exercises

## Quick Start

### 1. Open the Tool

```bash
# From project root
open tools/review-exercises.html

# Or use your browser
firefox tools/review-exercises.html
```

### 2. Load Exercise Files

**Drag & drop** or **click to browse**:
- Core files: `*_core.json`
- Support files: `*_support.json`

The tool automatically pairs core and support files by name.

### 3. Review Exercises

For each exercise:
1. **Preview** the question and options
2. **Check** quality score and validation errors
3. **Edit** JSON if needed (auto-updates preview)
4. **Approve**, **Reject**, **Flag**, or **Skip**

### 4. Export Results

- **Download Approved JSON** - Get all approved exercise files
- **Download Review Report** - Get summary of review session

## Screenshots

**Upload Screen:**
```
┌─────────────────────────────────────┐
│  Exercise Review Tool               │
├─────────────────────────────────────┤
│                                     │
│  ☁️  Upload Exercise Files          │
│                                     │
│  Drag & drop JSON files here        │
│  or click to browse                 │
│                                     │
└─────────────────────────────────────┘
```

**Review Interface:**
```
┌─────────────────────────┬─────────────────────────┐
│  JSON Editor            │  Live Preview           │
│  ─────────────          │  ─────────────          │
│  {                      │  Quality: 78%           │
│    "schema_version":... │                         │
│    "metadata": {        │  ✅ No validation issues│
│      "id": "gb_...",    │                         │
│      ...                │  Vraag: Bereken: ¾ + ½ │
│    },                   │  □ ¼                    │
│    "items": [...]       │  □ ½                    │
│  }                      │  ☑ 1¼ (correct)         │
│                         │  □ 1½                   │
├─────────────────────────┴─────────────────────────┤
│  ✅ Approve  ❌ Reject  🚩 Flag  ⏭️ Skip         │
└─────────────────────────────────────────────────┘
```

## Workflow Integration

### Typical Workflow

```bash
# 1. Generate exercises with AI
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --grade 4 \
  --output data-v2-draft/exercises

# 2. Review in browser
open tools/review-exercises.html
# → Load files from data-v2-draft/exercises/gb/
# → Review each exercise
# → Approve good ones, reject bad ones

# 3. Export approved
# → Click "Download Approved JSON"
# → Files saved to Downloads/

# 4. Move to production
cp ~/Downloads/*_core.json data-v2/exercises/gb/
cp ~/Downloads/*_support.json data-v2/exercises/gb/

# 5. Rebuild index
python3 scripts/build-index.py
```

## Quality Scoring

The tool calculates quality scores based on:

| Feature | Weight | Description |
|---------|--------|-------------|
| **Progressive Hints (3+)** | 20% | Has 3 levels of hints |
| **Per-Option Feedback** | 20% | Specific feedback for each wrong answer |
| **Learning Strategies** | 10% | Reading/math strategies documented |
| **SLO Alignment** | 10% | Has curriculum alignment metadata |
| **Base Quality** | 40% | No critical errors, valid schema |

**Score Interpretation:**
- **90-100%** 🟢 Excellent - Publish immediately
- **70-89%** 🟡 Good - Minor improvements recommended
- **40-69%** 🟠 Acceptable - Significant improvements needed
- **0-39%** 🔴 Poor - Major revision or reject

## Validation Checks

Automatically validates:

**Critical Issues** 🔴
- Invalid JSON syntax
- Missing required fields
- Invalid answer index
- No items/questions

**Errors** 🟠
- Missing metadata fields
- Empty question text
- Duplicate options
- Wrong data types

**Warnings** 🟡
- Missing SLO alignment
- Only 1-2 hints (recommend 3)
- No per-option feedback

## Tips for Efficient Review

### 1. Use Keyboard Shortcuts

Review 10x faster:
- Keep hands on keyboard
- `A` to approve good exercises
- `→` to move to next
- No mouse needed!

### 2. Focus on Critical Issues First

**Must Fix:**
- Wrong answer key
- Invalid JSON
- Missing question text

**Can Ignore (for now):**
- Missing SLO tags (can add later)
- Only 2 hints instead of 3
- Generic feedback (can enrich later)

### 3. Batch Similar Exercises

Review similar topics together:
- All "breuken" exercises
- All "tafels" exercises
- Easier to spot inconsistencies

### 4. Edit In-Place

Don't reject unless really bad:
- Fix typos directly in editor
- Adjust question wording
- Improve hint clarity
- Then approve

### 5. Use Flags for Edge Cases

Flag when you're unsure:
- Questionable difficulty level
- Ambiguous wording
- Need subject expert review
- Cultural sensitivity concerns

## Customization

### Modify Quality Thresholds

Edit the `calculateQualityScore()` function:

```javascript
// In review-exercises.html
function calculateQualityScore(core, support) {
    let score = 0;

    // Customize these weights
    score += (hasMultipleHints / itemCount) * 20;  // Change to 15 or 25
    score += (hasPerOptionFeedback / itemCount) * 20;
    score += (hasStrategies / itemCount) * 10;

    if (core.metadata?.slo_alignment) score += 10;

    return Math.round(score);
}
```

### Add Custom Validation Rules

Edit the `validateExercise()` function:

```javascript
function validateExercise(core, support) {
    const errors = [];

    // Add your custom checks
    if (core.metadata?.grade < 3 || core.metadata?.grade > 8) {
        errors.push({
            severity: 'warning',
            message: 'Grade outside normal range (3-8)'
        });
    }

    return errors;
}
```

## Troubleshooting

### "No preview showing"

**Problem:** Preview area is blank

**Solutions:**
1. Check JSON is valid (look for syntax errors)
2. Ensure `items` array exists in core file
3. Check browser console for errors (F12)

### "Math notation not rendering"

**Problem:** Shows `$\frac{3}{4}$` instead of ¾

**Solutions:**
1. Check KaTeX is loaded (see browser console)
2. Verify LaTeX syntax is correct
3. Remember to use `\\frac` in JSON (double backslash)

### "Can't load files"

**Problem:** Upload doesn't work

**Solutions:**
1. Use .json files only
2. Check file names end with `_core.json` or `_support.json`
3. Try drag & drop instead of file picker
4. Check browser allows file access (some browsers block local files)

### "Keyboard shortcuts don't work"

**Problem:** Pressing A/R/F does nothing

**Solutions:**
1. Click outside the text editor first
2. Make sure you're not typing in the JSON editor
3. Check caps lock is off

## Advanced Usage

### Review Multiple Batches

```bash
# Review batch 1
open tools/review-exercises.html
# Load data-v2-draft/exercises/gb/*.json
# Review and export

# Review batch 2
# Refresh page
# Load data-v2-draft/exercises/bl/*.json
# Review and export
```

### Combine with Validation Script

```bash
# 1. Validate first
python3 scripts/comprehensive_validation.py \
  --directory data-v2-draft/exercises/gb/ \
  --report validation-report.html

# 2. Review validation report
open validation-report.html

# 3. Load same files in review tool
open tools/review-exercises.html
# Load files with issues
```

### Export for Different Environments

The review tool can be used offline:
- Copy `tools/review-exercises.html` to USB drive
- Use on any computer with browser
- No internet needed (KaTeX loads from CDN but has fallback)

## Future Enhancements

Planned features:
- [ ] Bulk approve/reject by quality score
- [ ] Comment threads on exercises
- [ ] Side-by-side diff for edits
- [ ] AI-powered suggestion for improvements
- [ ] Direct publish to production (with git integration)
- [ ] Multi-user review (track who approved what)

## Related Tools

- `scripts/ai-bulk-generator.py` - Generate exercises with AI
- `scripts/comprehensive_validation.py` - Validate exercise quality
- `docs/KATEX-GUIDE.md` - Math notation reference

---

**Version:** 1.0.0
**Last Updated:** 2026-01-05
**Browser Compatibility:** Chrome 90+, Firefox 88+, Safari 14+
