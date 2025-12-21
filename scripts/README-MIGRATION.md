# JSON Migration Script

This script migrates your existing exercise JSON files to the new split format (core + support).

## Quick Start

### 1. Test with Dry Run (Recommended First Step)

```bash
# Preview what will happen without making changes
node scripts/migrate-to-split-format.js --dry-run

# Test a specific category only
node scripts/migrate-to-split-format.js --dry-run --category=wo
```

### 2. Run Migration

```bash
# Migrate all exercises (creates backup automatically)
node scripts/migrate-to-split-format.js

# Migrate specific category
node scripts/migrate-to-split-format.js --category=bl

# Skip backup (not recommended)
node scripts/migrate-to-split-format.js --no-backup
```

## What It Does

1. **Creates Backup** - Saves original files to `backups/` directory
2. **Transforms Data** - Converts each JSON to core + support format
3. **Validates Output** - Checks schema compliance
4. **Generates Index** - Creates `index.json` for exercise browsing
5. **Creates Shared Resources** - Generates feedback templates, UI strings, audio config

## Output Structure

```
data-v2/
├── exercises/
│   ├── bl/
│   │   ├── bl_groep4_m4_1_core.json
│   │   ├── bl_groep4_m4_1_support.json
│   │   └── ...
│   ├── gb/
│   ├── wo/
│   ├── ws/
│   ├── sp/
│   ├── tl/
│   └── index.json
└── shared/
    ├── feedback-templates.json
    ├── ui-strings.json
    └── audio-config.json
```

## Categories

- `bl` - Begrijpend Lezen (Reading Comprehension)
- `gb` - Basisvaardigheden (Math/Basic Skills)
- `wo` - Wereldoriëntatie (General Knowledge)
- `ws` - Woordenschat (Vocabulary)
- `sp` - Spelling (Spelling/Dictation)
- `tl` - Technisch Lezen (Technical Reading/Word Lists)

## Transformers

Each category has a dedicated transformer:

- `transformers/bl-transformer.js` - Handles nested questions, reading passages
- `transformers/gb-transformer.js` - Handles math problems with tips
- `transformers/wo-transformer.js` - Simple Q&A format
- `transformers/ws-transformer.js` - Vocabulary questions
- `transformers/sp-transformer.js` - Audio dictation with special config
- `transformers/tl-transformer.js` - Word lists with timing

## Validation

The script validates:
- Required fields present
- Correct data types
- No data loss during transformation
- Schema compliance

## Rollback

If something goes wrong:

1. **Restore from backup:**
   ```bash
   # Backups are in backups/ directory
   cp -r backups/backup-[timestamp]/* data/exercises/
   ```

2. **Or use git:**
   ```bash
   git log  # Find backup commit
   git reset --hard [commit-hash]
   ```

## Testing Migration Output

After migration, test a few exercises:

```bash
# Check a core file
cat data-v2/exercises/bl/bl_groep4_m4_1_core.json | jq

# Check a support file
cat data-v2/exercises/bl/bl_groep4_m4_1_support.json | jq

# Check the index
cat data-v2/exercises/index.json | jq '.exercises | length'
```

## Common Issues

### Issue: "No transformer for category"
**Solution:** Check that the category folder name matches one of: bl, gb, wo, ws, sp, tl

### Issue: "Core validation failed"
**Solution:** Check the error message. Usually missing required fields. Check transformer logic.

### Issue: "Data integrity warning"
**Solution:** Review warnings. Some are informational (e.g., item count changed due to restructuring).

## Migration Checklist

- [ ] Run dry-run first
- [ ] Review dry-run output
- [ ] Backup created (automatic unless --no-backup)
- [ ] All categories migrated successfully
- [ ] Index.json generated
- [ ] Shared resources created
- [ ] Spot-check sample files
- [ ] Test in application
- [ ] Update application code to use new format
- [ ] Commit changes to git

## Next Steps

After successful migration:

1. Update your application code to load from `data-v2/`
2. Test each exercise type in the UI
3. Verify audio paths work (especially for SP)
4. Update any hard-coded paths
5. Remove old `data/exercises/` once verified

## Support

If you encounter issues:
1. Check the error messages in the console
2. Review the specific transformer for that category
3. Validate the source JSON is in expected format
4. Check the comparison warnings for data integrity issues
