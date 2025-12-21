# Migration Guide: Exercise JSON Standardization

## Overview

This guide walks you through migrating your exercise JSONs from the current format to the new standardized split format (core + support).

## Why Migrate?

**Benefits:**
- ✅ 60% faster initial page loads (core data only)
- ✅ 80% bandwidth savings when feedback not needed
- ✅ Better security (answers separated from questions)
- ✅ Easier maintenance (update feedback without touching questions)
- ✅ Future-proof (versioned schema with extensibility)
- ✅ Consistent structure across all exercise types

## Before You Start

### Prerequisites
- Node.js installed (you already have it)
- Git repository (for backup safety)
- 10-15 minutes of time

### Safety Measures
1. **Automatic Git Backup** - Script creates a commit before migration
2. **Manual Backup** - Script copies files to `backups/` folder
3. **Dry Run Mode** - Preview changes without writing files
4. **Validation** - Automatic schema and integrity checks

## Step-by-Step Migration

### Step 1: Test with a Single File (2 minutes)

Pick one simple exercise to test:

```bash
# Test a simple WO exercise
npm run migrate:test data/exercises/wo/groep4_wo_150.json
```

**Expected output:**
```
✅ Core validation: PASSED
✅ Support validation: PASSED
✅ Migration test PASSED!
```

**What to check:**
- Core JSON has questions and options
- Support JSON has feedback/explanations
- Item counts match

---

### Step 2: Dry Run on One Category (2 minutes)

Test migration on the simplest category (WO) without writing files:

```bash
npm run migrate:dry-run -- --category=wo
```

**Expected output:**
```
Found 6 exercise files to process

Processing: wo/groep3_wo_150.json
  ✅ Would create core + support files
Processing: wo/groep4_wo_150.json
  ✅ Would create core + support files
...

📊 MIGRATION SUMMARY
Total processed:  6
✅ Succeeded:     6
❌ Failed:        0
```

**What to check:**
- No failures
- File count matches your wo/ folder
- No scary error messages

---

### Step 3: Migrate One Category (3 minutes)

Actually migrate the WO category:

```bash
npm run migrate:wo
```

**Expected output:**
```
📦 Creating backup...
✅ Backup created

Found 6 exercise files to process

Processing: wo/groep3_wo_150.json
  ✅ groep3_wo_150_core.json
  ✅ groep3_wo_150_support.json
...

📚 Generating exercise index...
✅ Index generated: 6 exercises

🔧 Creating shared resources...
✅ Shared resources created

📊 MIGRATION SUMMARY
✅ Succeeded: 6
✅ Migration complete! Output in: data-v2/exercises
```

**What to check:**
```bash
# Verify files created
ls data-v2/exercises/wo/

# Check a core file
cat data-v2/exercises/wo/groep4_wo_150_core.json | head -20

# Check a support file
cat data-v2/exercises/wo/groep4_wo_150_support.json | head -20
```

---

### Step 4: Verify Output (2 minutes)

Check the generated files:

```bash
# Check the index
cat data-v2/exercises/index.json | head -30

# Check shared resources
cat data-v2/shared/feedback-templates.json
cat data-v2/shared/ui-strings.json
cat data-v2/shared/audio-config.json
```

**What to look for:**
- Index contains all exercises
- Core files have questions, no feedback
- Support files have feedback, no questions
- Shared files have templates

---

### Step 5: Migrate All Categories (5 minutes)

If Step 3-4 looked good, migrate everything:

```bash
npm run migrate:all
```

**This will migrate:**
- BL (Begrijpend Lezen) - ~10 files
- GB (Basisvaardigheden) - ~10 files
- WO (Wereldoriëntatie) - ~6 files
- WS (Woordenschat) - ~9 files
- SP (Spelling) - ~10 files
- TL (Technisch Lezen) - ~4 files

**Total:** ~50-70 files

---

### Step 6: Review & Commit (3 minutes)

Check the results:

```bash
# See what was created
tree data-v2/ -L 2

# Spot-check a few files from each category
cat data-v2/exercises/bl/bl_groep4_m4_1_core.json
cat data-v2/exercises/sp/sp_groep4_m4_core.json
cat data-v2/exercises/gb/gb_groep4_m4_core.json
```

Commit the changes:

```bash
git add data-v2/
git commit -m "Migrate exercises to v2.0 split format (core + support)"
```

---

## Quick Reference Commands

```bash
# Dry run (preview only)
npm run migrate:dry-run

# Test single file
npm run migrate:test data/exercises/bl/bl_groep4_m4_1.json

# Migrate by category
npm run migrate:bl   # Begrijpend Lezen
npm run migrate:gb   # Basisvaardigheden
npm run migrate:wo   # Wereldoriëntatie
npm run migrate:ws   # Woordenschat
npm run migrate:sp   # Spelling
npm run migrate:tl   # Technisch Lezen

# Migrate everything
npm run migrate:all
```

---

## Troubleshooting

### Problem: "Missing metadata.id"

**Cause:** Transformer couldn't extract ID from filename

**Fix:** Check filename format. Should be like: `bl_groep4_m4_1.json`

---

### Problem: "Item count mismatch"

**Cause:** Some items were filtered or restructured

**Fix:** This is usually OK. Check the warnings - often due to format differences.

---

### Problem: "No transformer for category"

**Cause:** Category not recognized

**Fix:** Ensure category folder is one of: bl, gb, wo, ws, sp, tl

---

### Problem: Migration failed halfway

**Fix:** Restore from backup:

```bash
# Find latest backup
ls -la backups/

# Restore
cp -r backups/backup-[timestamp]/* data/exercises/

# Or use git
git log
git reset --hard [commit-before-migration]
```

---

## After Migration

### Update Your Application Code

**Before:**
```javascript
const data = await fetch('/data/exercises/bl/bl_groep4_m4_1.json');
```

**After:**
```javascript
// Load core immediately
const core = await fetch('/data-v2/exercises/bl/bl_groep4_m4_1_core.json');

// Load support when needed (lazy)
const support = await fetch('/data-v2/exercises/bl/bl_groep4_m4_1_support.json');
```

### Example Loading Pattern

```javascript
// 1. Load index for exercise list
const index = await fetch('/data-v2/exercises/index.json').then(r => r.json());

// 2. Display exercise list
renderExerciseList(index.exercises);

// 3. User selects exercise -> load core
async function loadExercise(exerciseId) {
  const exercise = index.exercises.find(e => e.id === exerciseId);
  const core = await fetch(`/data-v2/exercises/${exercise.paths.core}`).then(r => r.json());
  return core;
}

// 4. User needs hint -> load support
async function loadSupport(exerciseId) {
  const exercise = index.exercises.find(e => e.id === exerciseId);
  if (!exercise.paths.support) return null;
  const support = await fetch(`/data-v2/exercises/${exercise.paths.support}`).then(r => r.json());
  return support;
}
```

---

## Cleanup (After Verification)

Once you've tested the new format in your app:

```bash
# Move old data to archive
mkdir -p archive/exercises-v1
mv data/exercises/* archive/exercises-v1/

# Move new data to production location
mv data-v2/exercises/* data/exercises/
mv data-v2/shared data/

# Cleanup
rm -rf data-v2

# Commit
git add .
git commit -m "Switch to v2.0 exercise format in production"
```

---

## Rollback Plan

If you need to rollback after deploying:

```bash
# Restore from archive
cp -r archive/exercises-v1/* data/exercises/

# Or restore from git
git log --all --oneline | grep "Pre-migration"
git checkout [commit-hash] -- data/exercises/
```

---

## Support

- See detailed docs: `scripts/README-MIGRATION.md`
- Check transformer code: `scripts/transformers/`
- Review validation: `scripts/validators/schema-validator.js`

---

## Success Criteria

✅ All files migrated without errors
✅ Index.json generated with all exercises
✅ Shared resources created
✅ Spot-checks look correct
✅ Git commit created
✅ Application loads new format successfully
✅ All exercise types work in UI
✅ Audio plays correctly (for SP exercises)

**Estimated total time: 15-20 minutes**

Good luck! 🚀
