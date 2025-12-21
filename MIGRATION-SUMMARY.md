# Migration Script - Complete Summary

## ✅ What Has Been Created

### Migration Scripts

```
scripts/
├── migrate-to-split-format.js       # Main migration orchestrator
├── test-single-file.js              # Test single file migration
├── README-MIGRATION.md              # Detailed documentation
├── transformers/                    # Category-specific transformers
│   ├── bl-transformer.js           # Begrijpend Lezen
│   ├── gb-transformer.js           # Basisvaardigheden
│   ├── wo-transformer.js           # Wereldoriëntatie
│   ├── ws-transformer.js           # Woordenschat
│   ├── sp-transformer.js           # Spelling
│   └── tl-transformer.js           # Technisch Lezen
├── validators/
│   └── schema-validator.js         # JSON schema validation
└── utils/
    ├── backup.js                    # Backup creation
    ├── index-generator.js           # Generate exercise index
    └── compare.js                   # Data integrity checks
```

### Documentation

- `MIGRATION-GUIDE.md` - Step-by-step migration guide
- `scripts/README-MIGRATION.md` - Technical documentation

### NPM Scripts

Added to `package.json`:
- `npm run migrate:dry-run` - Preview changes
- `npm run migrate:test <file>` - Test single file
- `npm run migrate:bl` - Migrate BL category
- `npm run migrate:gb` - Migrate GB category
- `npm run migrate:wo` - Migrate WO category
- `npm run migrate:ws` - Migrate WS category
- `npm run migrate:sp` - Migrate SP category
- `npm run migrate:tl` - Migrate TL category
- `npm run migrate:all` - Migrate all categories

---

## 🎯 New JSON Structure

### Core Exercise (`*_core.json`)
```json
{
  "schema_version": "2.0.0",
  "metadata": {
    "id": "bl_groep4_m4_1",
    "type": "reading_comprehension",
    "category": "bl",
    "grade": 4,
    "level": "M4"
  },
  "display": {
    "title": "De nieuwe hamster",
    "theme": "Dieren / gezin"
  },
  "content": {
    "text": "Sofie krijgt...",
    "text_type": "verhalend"
  },
  "items": [
    {
      "id": "1a",
      "type": "multiple_choice",
      "question": { "text": "Waarom..." },
      "options": [...],
      "answer": { "correct_index": 1 }
    }
  ]
}
```

### Support Data (`*_support.json`)
```json
{
  "schema_version": "2.0.0",
  "exercise_id": "bl_groep4_m4_1",
  "items": [
    {
      "item_id": "1a",
      "hint": "Lees waarom...",
      "feedback": {
        "correct": "Goed gedaan!",
        "explanation": "In de tekst staat..."
      },
      "learning": {
        "skill": "letterlijk",
        "tips": [...]
      }
    }
  ]
}
```

### Exercise Index (`index.json`)
```json
{
  "schema_version": "2.0.0",
  "total_exercises": 70,
  "exercises": [
    {
      "id": "bl_groep4_m4_1",
      "category": "bl",
      "title": "De nieuwe hamster",
      "grade": 4,
      "stats": { "item_count": 4 },
      "features": { "has_audio": false, "has_hints": true },
      "paths": {
        "core": "bl/bl_groep4_m4_1_core.json",
        "support": "bl/bl_groep4_m4_1_support.json"
      }
    }
  ]
}
```

---

## 📂 Output Structure

```
data-v2/
├── exercises/
│   ├── bl/                          # Begrijpend Lezen
│   │   ├── bl_groep4_m4_1_core.json
│   │   ├── bl_groep4_m4_1_support.json
│   │   └── ...
│   ├── gb/                          # Basisvaardigheden
│   │   ├── gb_groep4_m4_core.json
│   │   ├── gb_groep4_m4_support.json
│   │   └── ...
│   ├── wo/                          # Wereldoriëntatie
│   ├── ws/                          # Woordenschat
│   ├── sp/                          # Spelling
│   ├── tl/                          # Technisch Lezen
│   └── index.json                   # Master exercise index
└── shared/
    ├── feedback-templates.json      # Global feedback messages
    ├── ui-strings.json              # UI text (buttons, labels)
    └── audio-config.json            # Audio settings
```

---

## 🚀 How to Use

### Quick Start (Recommended)

1. **Test first:**
   ```bash
   npm run migrate:dry-run
   ```

2. **Migrate all:**
   ```bash
   npm run migrate:all
   ```

3. **Review output:**
   ```bash
   tree data-v2/
   ```

### Safe Approach (Category by Category)

1. **Test one file:**
   ```bash
   npm run migrate:test data/exercises/wo/groep4_wo_150.json
   ```

2. **Migrate one category:**
   ```bash
   npm run migrate:wo
   ```

3. **Verify:**
   ```bash
   ls data-v2/exercises/wo/
   cat data-v2/exercises/wo/groep4_wo_150_core.json
   ```

4. **Repeat for other categories:**
   ```bash
   npm run migrate:bl
   npm run migrate:gb
   npm run migrate:ws
   npm run migrate:sp
   npm run migrate:tl
   ```

---

## 🔍 What the Script Does

1. ✅ **Backup** - Creates git commit + manual backup
2. ✅ **Transform** - Splits each JSON into core + support
3. ✅ **Validate** - Checks schema compliance
4. ✅ **Compare** - Verifies no data loss
5. ✅ **Index** - Generates master exercise list
6. ✅ **Shared** - Creates global resource files

---

## 📊 Expected Results

### Files
- **Input:** ~70 JSON files in `data/exercises/`
- **Output:** ~140 JSON files (70 core + 70 support) in `data-v2/exercises/`
- **Plus:** 1 index.json + 3 shared resource files

### Performance Improvement
- **Before:** 1 request × 150KB = 150KB
- **After:** 1 request × 60KB (core) + lazy 40KB (support when needed)
- **Savings:** 60% faster initial load

---

## ⚠️ Important Notes

### Backup Safety
- ✅ Automatic git commit before migration
- ✅ Manual backup to `backups/` folder
- ✅ Original files never modified (writes to `data-v2/`)

### What Gets Split

**Core (loaded immediately):**
- Exercise metadata
- Questions and options
- Answer keys
- Audio paths

**Support (loaded on-demand):**
- Hints
- Feedback messages
- Tips and explanations
- Learning objectives

### Categories Handled

| Code | Name | Files | Transformer |
|------|------|-------|-------------|
| bl | Begrijpend Lezen | ~10 | bl-transformer.js |
| gb | Basisvaardigheden | ~10 | gb-transformer.js |
| wo | Wereldoriëntatie | ~6 | wo-transformer.js |
| ws | Woordenschat | ~9 | ws-transformer.js |
| sp | Spelling | ~10 | sp-transformer.js |
| tl | Technisch Lezen | ~4 | tl-transformer.js |

---

## 🛠️ Customization

### Modify a Transformer

Edit category-specific logic:
```bash
# Example: Customize BL transformer
nano scripts/transformers/bl-transformer.js
```

### Change Output Directory

Edit `scripts/migrate-to-split-format.js`:
```javascript
const CONFIG = {
  outputDir: path.join(__dirname, '..', 'data-v2', 'exercises'),
  // Change to your preferred location
};
```

### Add Custom Validation

Edit `scripts/validators/schema-validator.js`:
```javascript
function validateCore(data) {
  // Add your custom validation rules
}
```

---

## 🔄 Integration with Your App

### Old Way
```javascript
const exercise = await fetch('/data/exercises/bl/bl_groep4_m4_1.json');
```

### New Way
```javascript
// 1. Load index (once, cache it)
const index = await fetch('/data-v2/exercises/index.json');

// 2. Load core when user selects exercise
const core = await fetch('/data-v2/exercises/bl/bl_groep4_m4_1_core.json');

// 3. Load support only when needed (hint button clicked)
const support = await fetch('/data-v2/exercises/bl/bl_groep4_m4_1_support.json');
```

### Benefits
- Faster page loads
- Less bandwidth usage
- Better UX (progressive loading)
- Easier to cache

---

## ✅ Checklist

Before migration:
- [ ] Read `MIGRATION-GUIDE.md`
- [ ] Test with `npm run migrate:dry-run`
- [ ] Test single file with `npm run migrate:test`

During migration:
- [ ] Run `npm run migrate:all`
- [ ] Check for errors in console
- [ ] Verify file counts match

After migration:
- [ ] Review `data-v2/exercises/index.json`
- [ ] Spot-check core files (questions visible)
- [ ] Spot-check support files (feedback visible)
- [ ] Check shared resources created
- [ ] Commit to git

Integration:
- [ ] Update app code to load from `data-v2/`
- [ ] Test each exercise type in UI
- [ ] Verify audio works (SP exercises)
- [ ] Test lazy-loading of support data
- [ ] Move `data-v2/` to `data/` once verified

---

## 📚 Further Reading

- `MIGRATION-GUIDE.md` - Step-by-step walkthrough
- `scripts/README-MIGRATION.md` - Technical details
- Generic JSON template proposals in earlier conversation

---

## 🎉 Next Steps

1. **Read** `MIGRATION-GUIDE.md` (5 min)
2. **Test** with dry-run (2 min)
3. **Migrate** all exercises (5 min)
4. **Verify** output files (3 min)
5. **Update** application code (30 min)
6. **Deploy** and test (15 min)

**Total time:** ~1 hour for complete migration and integration

Good luck! 🚀
