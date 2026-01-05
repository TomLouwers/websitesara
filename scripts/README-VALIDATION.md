# Exercise Validation System

Comprehensive quality control system for OefenPlatform exercises.

## Quick Start

```bash
# Install dependencies (optional, for readability checks)
pip install -r scripts/requirements-validation.txt

# Validate a single exercise
python3 scripts/comprehensive_validation.py --file data-v2/exercises/bl/bl_groep4_e4_1_core.json

# Validate all exercises in a category
python3 scripts/comprehensive_validation.py --category gb

# Validate all exercises
python3 scripts/comprehensive_validation.py --all

# Generate HTML report
python3 scripts/comprehensive_validation.py --all --report validation-report.html
```

## What It Checks

### 1. Schema Compliance ✅
- Valid JSON syntax
- Schema version 2.0.0
- Required fields present (metadata, items/exercises/problems)
- Correct data types

### 2. Metadata Quality 📋
- Required fields: id, type, category, language, grade
- SLO alignment (recommended)
- Grade range validation (3-8)
- Referentieniveau presence

### 3. Content Quality 📝
- Question text present and non-empty
- No placeholder text (TODO, XXX, FIXME, ???)
- Minimum text length
- Age-appropriate readability (if textstat installed)

### 4. Multiple Choice Validation ✔️
- At least 2 options
- Maximum 6 options (pedagogical best practice)
- All options have text
- No duplicate options
- Correct answer index in valid range

### 5. Answer Correctness ✓
- Correct_index is valid integer
- Points to existing option
- Within range of available options

### 6. Hint Quality 💡
- Presence of hints (recommended)
- Progressive hints (3 levels ideal)
- Hint length validation
- No duplicate hints

### 7. Feedback Quality 💬
- Feedback messages present
- Per-option feedback (recommended for 100% quality)
- Contextual feedback (correct/incorrect variations)

### 8. Learning Metadata 🎓
- Learning strategies (reading/math)
- Common errors documented
- Remediation guidance

## Quality Score

Each exercise receives a quality score from 0-100% based on:

**Deductions:**
- Critical issues: -20% each
- Errors: -10% each
- Warnings: -2% each

**Bonuses:**
- Progressive hints (3+ levels): +20%
- Per-option feedback: +20%
- Learning strategies: +10%
- SLO alignment: +10%

**Score Interpretation:**
- **90-100%**: Excellent quality, publish-ready
- **70-89%**: Good quality, minor improvements needed
- **40-69%**: Acceptable, significant improvements recommended
- **0-39%**: Poor quality, major revision required

## Severity Levels

### 🔴 CRITICAL
Blocks publishing. Must be fixed.
- Invalid JSON
- Missing required schema fields
- Invalid answer index
- No items/exercises

### 🟠 ERROR
Should be fixed before publishing.
- Missing metadata fields
- Empty question text
- Duplicate options
- Invalid data types

### 🟡 WARNING
Review recommended.
- Missing SLO alignment
- Text readability issues
- Too many/too few options
- Short hints

### 🔵 INFO
Nice to have, improves quality.
- No per-option feedback
- No learning strategies
- Single hint (recommend 3)
- No support data

## Usage Examples

### Validate Before Committing

```bash
# Check all changed exercises
python3 scripts/comprehensive_validation.py --all

# Must have 0 critical, 0 errors
echo $?  # Exit code 0 = passed, 1 = failed
```

### Quality Report for Content Team

```bash
# Generate HTML report
python3 scripts/comprehensive_validation.py --all --report reports/quality-$(date +%Y%m%d).html

# Open in browser
open reports/quality-20260105.html
```

### Validate New AI-Generated Exercises

```bash
# Validate draft exercises
python3 scripts/comprehensive_validation.py --directory data-v2-draft/exercises/gb/

# Strict mode (warnings become errors)
python3 scripts/comprehensive_validation.py --directory data-v2-draft/ --strict
```

### Check Single Exercise During Development

```bash
# Quick check
python3 scripts/comprehensive_validation.py --file data-v2/exercises/gb/gb_groep4_m4_core.json
```

## Integration with CI/CD

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Validate only changed exercise files
changed_files=$(git diff --cached --name-only --diff-filter=ACM | grep "_core.json$")

if [ -n "$changed_files" ]; then
    echo "Validating changed exercises..."
    for file in $changed_files; do
        python3 scripts/comprehensive_validation.py --file "$file"
        if [ $? -ne 0 ]; then
            echo "❌ Validation failed for $file"
            exit 1
        fi
    done
    echo "✅ All exercises passed validation"
fi
```

### GitHub Actions

```yaml
name: Validate Exercises

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r scripts/requirements-validation.txt
      - name: Validate exercises
        run: python3 scripts/comprehensive_validation.py --all --strict
      - name: Upload report
        if: failure()
        uses: actions/upload-artifact@v2
        with:
          name: validation-report
          path: validation-report.html
```

## Readability Checking

### Installing textstat

```bash
pip install textstat
```

### Dutch Readability Scores

The validator uses Flesch Reading Ease for Dutch:

| Grade | Target Score | Interpretation |
|-------|--------------|----------------|
| 3     | 80+          | Very easy      |
| 4     | 75+          | Easy           |
| 5     | 70+          | Fairly easy    |
| 6     | 65+          | Standard       |
| 7     | 60+          | Fairly difficult |
| 8     | 55+          | Difficult      |

**Warning threshold:** 15 points below target
- Example: Grade 4 text scoring < 60 triggers warning

### Example Readability Issues

**Too difficult for Grade 4:**
```
❌ "De gespecialiseerde terminologie vereist substantiële cognitieve capaciteit."
Score: 25 (target: 75+)

✅ "Deze woorden zijn moeilijk. Je moet goed nadenken."
Score: 78 (target: 75+)
```

## Future Enhancements

### Grammar & Spelling (Planned)

```python
# Will be added in next version
try:
    import language_tool_python
    tool = language_tool_python.LanguageTool('nl')
    matches = tool.check(text)
    # Report spelling/grammar errors
except ImportError:
    pass
```

### Math Answer Verification (Planned)

```python
# Use sympy to verify math problems
from sympy import sympify, Eq
# Check if correct answer actually solves the equation
```

### Bias Detection (Planned)

- Name diversity check
- Gender balance in examples
- Cultural representation
- Accessibility considerations

## Troubleshooting

### "textstat not installed"

```bash
pip install textstat
```

Readability checks are optional. The validator works without it.

### "AttributeError: 'dict' object..."

Your JSON structure might be non-standard. Check that:
- `options[].text` is a string, not object
- `question.text` is a string
- No nested dicts where strings expected

### Low Quality Score Despite No Errors

Quality score rewards presence of features:
- Add 3-level progressive hints: +20%
- Add per-option feedback: +20%
- Add learning strategies: +10%
- Add SLO alignment: +10%

Even without errors, missing these features lowers the score.

### Validation Passes But Exercise Has Issues

The validator checks structure and presence, not semantic correctness:
- ✅ Detects: Missing answer, invalid index, duplicate options
- ❌ Doesn't detect: Incorrect answer key, misleading distractors, poor question wording

Always combine automated validation with human review.

## Output Formats

### Console Output

```
bl_groep4_e4_1 (85.5% quality):
  🟡 [WARNING] metadata: Missing SLO alignment (at metadata)
   💡 Suggestion: Add slo_alignment with kerndoelen, rekendomeinen
  🔵 [INFO] feedback: No per-option feedback (at item 1)
  🔵 [INFO] hint: Only 1 hint provided. Consider adding 2-3 progressive hints
```

### HTML Report

- Summary dashboard with metrics
- Exercise-by-exercise breakdown
- Color-coded severity
- Clickable issue details
- Exportable/shareable

## Best Practices

### For Content Creators

1. **Run validation early and often**
   - Before committing
   - After AI generation
   - Before publishing

2. **Aim for 80%+ quality score**
   - Add progressive hints
   - Write per-option feedback
   - Include learning strategies

3. **Fix critical/errors first**
   - Warnings can wait
   - Info issues improve quality but aren't blocking

### For Developers

1. **Keep validation fast**
   - Current: ~1 second per exercise
   - Target: < 100ms per exercise

2. **Extend carefully**
   - Add new checks as ValidationIssue
   - Maintain severity hierarchy
   - Document new checks

3. **Test on real data**
   - Validate against all existing exercises
   - Check for regressions

## Related Scripts

- `scripts/feedback-enhancer.js` - Automatically improves feedback quality
- `scripts/validators/schema-validator.js` - JavaScript schema validation
- `tools/check_missing_tips.py` - Finds exercises without hints
- `tools/verify_answers.py` - Manual answer verification

## Support

For issues or questions:
1. Check this README
2. Review validation output carefully
3. Examine similar passing exercises
4. Create GitHub issue with example

---

**Version:** 1.0.0
**Last Updated:** 2026-01-05
**Maintainer:** Product Team
