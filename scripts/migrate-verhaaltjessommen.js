#!/usr/bin/env node

/**
 * Migration Script: Convert verhaaltjessommen (word problems) to v2.0 split format
 *
 * Usage:
 *   node scripts/migrate-verhaaltjessommen.js [--dry-run]
 */

const fs = require('fs');
const path = require('path');
const { transformVerhaaltjessommen } = require('./transformers/vs-transformer');
const { validateCore, validateSupport } = require('./validators/schema-validator');

// Configuration
const CONFIG = {
  sourceFile: path.join(__dirname, '..', 'data', 'templates', 'verhaaltjessommen - Template.json'),
  outputDir: path.join(__dirname, '..', 'data-v2', 'exercises', 'vs'),
  dryRun: process.argv.includes('--dry-run'),
};

/**
 * Main migration function
 */
async function migrate() {
  console.log('🚀 Migrating Verhaaltjessommen (Word Problems)...\n');
  console.log(`Mode: ${CONFIG.dryRun ? 'DRY RUN' : 'PRODUCTION'}\n`);

  try {
    // Step 1: Read source file
    console.log('📖 Reading source file...');
    if (!fs.existsSync(CONFIG.sourceFile)) {
      throw new Error(`Source file not found: ${CONFIG.sourceFile}`);
    }

    const rawData = fs.readFileSync(CONFIG.sourceFile, 'utf-8');
    const data = JSON.parse(rawData);
    console.log(`✅ Loaded ${data.length} word problems\n`);

    // Step 2: Analyze themes
    const themes = {};
    data.forEach(problem => {
      if (!themes[problem.theme]) {
        themes[problem.theme] = 0;
      }
      themes[problem.theme]++;
    });

    console.log('📊 Problems by theme:');
    Object.entries(themes).sort((a, b) => b[1] - a[1]).forEach(([theme, count]) => {
      console.log(`  - ${theme}: ${count} problems`);
    });
    console.log('');

    // Step 3: Transform data
    console.log('🔄 Transforming to v2.0 split format...');
    const { core, support } = transformVerhaaltjessommen(data, CONFIG.sourceFile);
    console.log(`✅ Transformed ${core.problems.length} problems\n`);

    // Step 4: Validate
    console.log('✔️  Validating schema...');
    const coreValidation = validateCore(core);
    const supportValidation = validateSupport(support);

    if (!coreValidation.valid) {
      console.log('❌ Core validation failed:');
      coreValidation.errors.forEach(err => console.log(`  - ${err}`));
      process.exit(1);
    }

    if (!supportValidation.valid) {
      console.log('❌ Support validation failed:');
      supportValidation.errors.forEach(err => console.log(`  - ${err}`));
      process.exit(1);
    }

    console.log('✅ Validation passed\n');

    // Step 5: Write files
    if (!CONFIG.dryRun) {
      console.log('💾 Writing output files...');

      // Create output directory
      if (!fs.existsSync(CONFIG.outputDir)) {
        fs.mkdirSync(CONFIG.outputDir, { recursive: true });
      }

      const coreFile = path.join(CONFIG.outputDir, 'verhaaltjessommen_cito_core.json');
      const supportFile = path.join(CONFIG.outputDir, 'verhaaltjessommen_cito_support.json');

      fs.writeFileSync(coreFile, JSON.stringify(core, null, 2));
      fs.writeFileSync(supportFile, JSON.stringify(support, null, 2));

      console.log(`✅ Core file written: ${coreFile}`);
      console.log(`✅ Support file written: ${supportFile}\n`);

      // File size stats
      const coreSize = (fs.statSync(coreFile).size / 1024).toFixed(2);
      const supportSize = (fs.statSync(supportFile).size / 1024).toFixed(2);
      console.log('📊 File sizes:');
      console.log(`  - Core: ${coreSize} KB`);
      console.log(`  - Support: ${supportSize} KB\n`);
    } else {
      console.log('⚠️  DRY RUN MODE - No files written\n');
    }

    // Step 6: Summary
    console.log('==================================================');
    console.log('✅ MIGRATION COMPLETE');
    console.log('==================================================');
    console.log(`Total problems: ${core.problems.length}`);
    console.log(`Total questions: ${core.problems.reduce((sum, p) => sum + p.items.length, 0)}`);
    console.log(`Themes: ${core.metadata.themes.length}`);
    console.log(`Output directory: ${CONFIG.outputDir}`);
    console.log('==================================================\n');

  } catch (error) {
    console.error('❌ Migration failed:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// Run migration
migrate();
