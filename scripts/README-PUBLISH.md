# Publishing Approved Exercises

Complete workflow for moving approved exercises from draft to production.

## Overview

The publish system safely moves exercises through the quality pipeline:

```
data-v2-draft/          →  Validation  →  Review  →  data-v2/
(AI generated)                                         (Production)
```

## Quick Start

### Complete Workflow

```bash
# 1. Generate exercises with AI
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --grade 4 \
  --count 20 \
  --output data-v2-draft/exercises

# 2. Review in browser
open tools/review-exercises.html
# → Load files from data-v2-draft/exercises/gb/
# → Approve good exercises
# → Export approved JSON

# 3. Publish approved exercises
python3 scripts/publish-approved.py \
  --from data-v2-draft/exercises/gb/ \
  --to data-v2/exercises/gb/ \
  --validate \
  --update-index

# 4. Done! Exercises are now live
```

## Publish Script Usage

### Basic Publishing

```bash
# Publish all files from directory
python3 scripts/publish-approved.py \
  --from data-v2-draft/exercises/gb/ \
  --to data-v2/exercises/gb/
```

### With Validation (Recommended)

```bash
# Validate before publishing (blocks low-quality exercises)
python3 scripts/publish-approved.py \
  --from data-v2-draft/exercises/gb/ \
  --to data-v2/exercises/gb/ \
  --validate
```

**Quality Requirements:**
- No critical errors
- No schema errors
- Quality score ≥ 60%
- Valid answer indices
- Proper JSON structure

### Dry Run (Preview)

```bash
# See what would be published without moving files
python3 scripts/publish-approved.py \
  --from data-v2-draft/exercises/gb/ \
  --to data-v2/exercises/gb/ \
  --dry-run
```

Output:
```
🔍 DRY RUN MODE - No files will be moved

📄 gb_groep4_m4_1_core.json
   ✅ Would publish to data-v2/exercises/gb/gb_groep4_m4_1_core.json
   ✅ Would publish support file
   📦 Would backup existing file
```

### Single File Publishing

```bash
# Publish one specific file
python3 scripts/publish-approved.py \
  --file data-v2-draft/exercises/gb/gb_groep4_m4_core.json \
  --to data-v2/exercises/gb/
```

### Update Index After Publishing

```bash
# Automatically rebuild index.json
python3 scripts/publish-approved.py \
  --from data-v2-draft/exercises/gb/ \
  --to data-v2/exercises/gb/ \
  --update-index
```

### Generate Report

```bash
# Save publish report for documentation
python3 scripts/publish-approved.py \
  --from data-v2-draft/exercises/gb/ \
  --to data-v2/exercises/gb/ \
  --report publish-report-$(date +%Y%m%d).txt
```

## Safety Features

### Automatic Backups

By default, existing files are backed up before overwriting:

```
data-v2/exercises/gb/
├── gb_groep4_m4_core.json          # Current (new)
└── .backups/
    └── gb_groep4_m4_core_20260105_143022.json  # Backup (old)
```

**Disable backups** (not recommended):
```bash
python3 scripts/publish-approved.py \
  --from data-v2-draft/ \
  --to data-v2/ \
  --no-backup
```

### Validation Gates

Exercises are rejected if:
- ❌ Critical validation errors
- ❌ Schema version mismatch
- ❌ Missing required fields
- ❌ Invalid answer index
- ❌ Quality score < 60%
- ❌ Invalid JSON syntax

**Skip validation** (use with caution):
```bash
python3 scripts/publish-approved.py \
  --from data-v2-draft/ \
  --to data-v2/ \
  --skip-validation
```

## Index Management

### Rebuild Index

After publishing, update the master index:

```bash
# Rebuild index for all exercises
python3 scripts/build-index.py

# Custom directory
python3 scripts/build-index.py --directory data-v2/exercises

# Custom output location
python3 scripts/build-index.py --output custom-index.json
```

**What the index includes:**
```json
{
  "schema_version": "2.0.0",
  "generated_at": "2026-01-05T14:30:22",
  "total_exercises": 85,
  "categories": ["bl", "gb", "sp", "tl", "wo", "ws"],
  "exercises": [
    {
      "id": "gb_groep4_m4_1",
      "category": "gb",
      "type": "multiple_choice",
      "title": "Tafels 1-10",
      "grade": 4,
      "level": "M4",
      "difficulty": "medium",
      "item_count": 25,
      "has_support": true,
      "paths": {
        "core": "gb/gb_groep4_m4_1_core.json",
        "support": "gb/gb_groep4_m4_1_support.json"
      }
    }
  ],
  "statistics": {
    "by_category": {"gb": 30, "bl": 25, ...},
    "by_grade": {3: 10, 4: 20, ...},
    "with_support": 82,
    "total_items": 2450
  }
}
```

## Complete Workflow Examples

### Example 1: Publish New Math Exercises

```bash
# 1. Generate 50 math exercises
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --grade 4 \
  --level M \
  --output data-v2-draft/exercises

# Generated files:
#   data-v2-draft/exercises/gb/gb_groep4_m_4g1_core.json
#   data-v2-draft/exercises/gb/gb_groep4_m_4g1_support.json
#   ... (more files)

# 2. Review in browser
open tools/review-exercises.html
# → Drag & drop all files from data-v2-draft/exercises/gb/
# → Review each exercise (use A/R/F shortcuts)
# → Approved: 45, Rejected: 5
# → Export approved exercises

# 3. Check what would be published
python3 scripts/publish-approved.py \
  --from data-v2-draft/exercises/gb/ \
  --to data-v2/exercises/gb/ \
  --validate \
  --dry-run

# Review output, looks good!

# 4. Publish for real
python3 scripts/publish-approved.py \
  --from data-v2-draft/exercises/gb/ \
  --to data-v2/exercises/gb/ \
  --validate \
  --update-index \
  --report publish-math-groep4.txt

# 5. Clean up draft folder
rm -rf data-v2-draft/exercises/gb/

# Done! 45 new math exercises are now live
```

### Example 2: Replace Existing Low-Quality Exercise

```bash
# 1. Identify low-quality exercise
python3 scripts/comprehensive_validation.py \
  --file data-v2/exercises/gb/gb_groep3_e3_core.json

# Output: Quality score: 42% (needs improvement)

# 2. Generate improved version with AI
python3 scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --row 8 \
  --count 10 \
  --output data-v2-draft/exercises

# 3. Review and approve best one
open tools/review-exercises.html

# 4. Publish (will backup old version)
python3 scripts/publish-approved.py \
  --file data-v2-draft/exercises/gb/gb_groep3_e3_core.json \
  --to data-v2/exercises/gb/ \
  --validate

# Output:
#   📦 Backed up to: .backups/gb_groep3_e3_core_20260105_143022.json
#   ✅ Published to data-v2/exercises/gb/gb_groep3_e3_core.json

# 5. Rebuild index
python3 scripts/build-index.py

# Improved exercise is now live, old version safely backed up
```

### Example 3: Batch Publish Multiple Categories

```bash
# Publish all categories at once
for category in bl gb sp wo ws; do
  echo "Publishing ${category}..."
  python3 scripts/publish-approved.py \
    --from data-v2-draft/exercises/${category}/ \
    --to data-v2/exercises/${category}/ \
    --validate \
    --report publish-${category}.txt
done

# Rebuild master index
python3 scripts/build-index.py
```

## Directory Structure

```
data-v2-draft/                  # Staging area
└── exercises/
    ├── gb/                     # Math exercises (draft)
    │   ├── gb_groep4_m4_1_core.json
    │   └── gb_groep4_m4_1_support.json
    ├── bl/                     # Reading exercises (draft)
    └── ...

data-v2/                        # Production
└── exercises/
    ├── gb/                     # Math exercises (live)
    │   ├── gb_groep4_m4_1_core.json
    │   ├── gb_groep4_m4_1_support.json
    │   └── .backups/           # Auto-created backups
    │       └── gb_groep4_m4_1_core_20260105_143022.json
    ├── bl/                     # Reading exercises (live)
    ├── index.json              # Master index (auto-generated)
    └── ...
```

## Best Practices

### 1. Always Validate Before Publishing

```bash
# ✅ Good
--validate

# ❌ Bad (unless you have a good reason)
--skip-validation
```

Validation prevents:
- Broken exercises reaching students
- Invalid JSON causing app crashes
- Low-quality content degrading platform reputation

### 2. Use Dry Run First

For large batches, preview before publishing:

```bash
# 1. Dry run to preview
--dry-run

# 2. Review output carefully
# 3. Remove --dry-run to publish
```

### 3. Keep Backups Enabled

Backups saved you when:
- New version has unexpected bug
- Need to revert to previous version
- Compare old vs new to see changes

**Disk space concern?**
Old backups can be deleted after verification:
```bash
# Clean backups older than 30 days
find data-v2/exercises -type f -path "*/.backups/*" -mtime +30 -delete
```

### 4. Update Index After Publishing

Always rebuild index so app sees new exercises:

```bash
--update-index
```

Or manually:
```bash
python3 scripts/build-index.py
```

### 5. Generate Reports for Auditing

Keep track of what was published when:

```bash
--report publish-report-$(date +%Y%m%d).txt
```

Save reports in `docs/publish-reports/` for reference.

### 6. Clean Draft Folder After Publishing

```bash
# After successful publish
rm -rf data-v2-draft/exercises/gb/

# Or archive for reference
mv data-v2-draft/exercises/gb/ archive/2026-01-05-math-groep4/
```

## Troubleshooting

### "Validation failed"

**Problem:** Exercise rejected during publish

**Solutions:**
1. Check validation output for specific errors
2. Run comprehensive validation for details:
   ```bash
   python3 scripts/comprehensive_validation.py --file <file>
   ```
3. Fix issues in draft file
4. Retry publish

### "Quality score too low"

**Problem:** Score < 60%, blocked

**Solutions:**
1. Add 3-level progressive hints
2. Add per-option feedback
3. Add learning strategies
4. Add SLO alignment
5. Or use `--skip-validation` if quality check not needed (not recommended)

### "File not found"

**Problem:** Source file missing

**Solutions:**
1. Check file path is correct
2. Ensure file name ends with `_core.json`
3. Check current directory: `pwd`
4. Use absolute paths if needed

### "Permission denied"

**Problem:** Can't write to destination

**Solutions:**
```bash
# Check permissions
ls -la data-v2/exercises/gb/

# Fix permissions if needed
chmod 755 data-v2/exercises/gb/
```

### "Index not updating"

**Problem:** New exercises don't appear in app

**Solutions:**
1. Manually rebuild index:
   ```bash
   python3 scripts/build-index.py
   ```
2. Check index.json was created
3. Verify path is correct
4. Clear browser cache if testing locally

## Integration with Git

### Commit Published Exercises

```bash
# After publishing
git add data-v2/exercises/
git commit -m "Add 45 new Groep 4 math exercises

Generated with AI (Claude Sonnet)
Reviewed and approved via review tool
Quality score: 78% average
Topic: Tafels 1-10, multiplication/division"

git push
```

### Track Publish Reports

```bash
git add docs/publish-reports/
git commit -m "Add publish report for 2026-01-05 batch"
```

## Automation Ideas

### CI/CD Pipeline

```yaml
# .github/workflows/publish.yml
name: Publish Exercises

on:
  push:
    paths:
      - 'data-v2-draft/exercises/**'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate
        run: |
          python3 scripts/comprehensive_validation.py \
            --directory data-v2-draft/exercises \
            --report validation.html
      - name: Publish
        run: |
          python3 scripts/publish-approved.py \
            --from data-v2-draft/exercises \
            --to data-v2/exercises \
            --validate \
            --update-index
      - name: Commit
        run: |
          git add data-v2/exercises/
          git commit -m "Auto-publish approved exercises"
          git push
```

### Scheduled Rebuilds

```bash
# Cron job to rebuild index nightly
0 2 * * * cd /path/to/websitesara && python3 scripts/build-index.py
```

## Related Scripts

- `scripts/ai-bulk-generator.py` - Generate exercises with AI
- `scripts/comprehensive_validation.py` - Validate exercise quality
- `tools/review-exercises.html` - Review interface
- `scripts/build-index.py` - Rebuild master index

---

**Version:** 1.0.0
**Last Updated:** 2026-01-05
