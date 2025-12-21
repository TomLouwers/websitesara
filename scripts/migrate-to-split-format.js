#!/usr/bin/env node

/**
 * Migration Script: Convert existing exercise JSONs to split format (core + support)
 *
 * Usage:
 *   node scripts/migrate-to-split-format.js [--dry-run] [--category=bl]
 *
 * Options:
 *   --dry-run        Preview changes without writing files
 *   --category=XX    Only migrate specific category (bl, gb, wo, ws, sp, tl)
 *   --backup         Create backup before migration (default: true)
 *   --no-backup      Skip backup creation
 */

const fs = require('fs');
const path = require('path');

// Import transformers
const transformBL = require('./transformers/bl-transformer');
const transformGB = require('./transformers/gb-transformer');
const transformWO = require('./transformers/wo-transformer');
const transformWS = require('./transformers/ws-transformer');
const transformSP = require('./transformers/sp-transformer');
const transformTL = require('./transformers/tl-transformer');

const { validateCore, validateSupport } = require('./validators/schema-validator');
const { createBackup } = require('./utils/backup');
const { generateIndex } = require('./utils/index-generator');
const { compareData } = require('./utils/compare');

// Configuration
const CONFIG = {
  sourceDir: path.join(__dirname, '..', 'data', 'exercises'),
  outputDir: path.join(__dirname, '..', 'data-v2', 'exercises'),
  sharedDir: path.join(__dirname, '..', 'data-v2', 'shared'),
  backupDir: path.join(__dirname, '..', 'backups'),
  dryRun: process.argv.includes('--dry-run'),
  category: process.argv.find(arg => arg.startsWith('--category='))?.split('=')[1],
  createBackup: !process.argv.includes('--no-backup'),
};

// Category to transformer mapping
const TRANSFORMERS = {
  bl: transformBL,
  gb: transformGB,
  wo: transformWO,
  ws: transformWS,
  sp: transformSP,
  tl: transformTL,
};

// Statistics
const stats = {
  processed: 0,
  succeeded: 0,
  failed: 0,
  skipped: 0,
  errors: [],
};

/**
 * Main migration function
 */
async function migrate() {
  console.log('🚀 Starting migration to split format...\n');
  console.log(`Mode: ${CONFIG.dryRun ? 'DRY RUN' : 'PRODUCTION'}`);
  console.log(`Category filter: ${CONFIG.category || 'ALL'}\n`);

  try {
    // Step 1: Create backup
    if (CONFIG.createBackup && !CONFIG.dryRun) {
      console.log('📦 Creating backup...');
      await createBackup(CONFIG.sourceDir, CONFIG.backupDir);
      console.log('✅ Backup created\n');
    }

    // Step 2: Ensure output directories exist
    if (!CONFIG.dryRun) {
      ensureDirectories();
    }

    // Step 3: Find all exercise files
    const files = findExerciseFiles();
    console.log(`Found ${files.length} exercise files to process\n`);

    // Step 4: Process each file
    for (const file of files) {
      await processFile(file);
    }

    // Step 5: Generate index
    console.log('\n📚 Generating exercise index...');
    const exercises = await generateIndex(CONFIG.outputDir);

    if (!CONFIG.dryRun) {
      const indexPath = path.join(CONFIG.outputDir, 'index.json');
      fs.writeFileSync(indexPath, JSON.stringify(exercises, null, 2));
      console.log(`✅ Index generated: ${exercises.exercises.length} exercises`);
    } else {
      console.log(`✅ Index would contain: ${exercises.exercises.length} exercises`);
    }

    // Step 6: Create shared resources
    console.log('\n🔧 Creating shared resources...');
    if (!CONFIG.dryRun) {
      await createSharedResources();
      console.log('✅ Shared resources created');
    } else {
      console.log('✅ Shared resources would be created');
    }

    // Step 7: Print summary
    printSummary();

  } catch (error) {
    console.error('\n❌ Migration failed:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

/**
 * Find all exercise JSON files
 */
function findExerciseFiles() {
  const categories = CONFIG.category ? [CONFIG.category] : ['bl', 'gb', 'wo', 'ws', 'sp', 'tl'];
  const files = [];

  for (const category of categories) {
    const categoryDir = path.join(CONFIG.sourceDir, category);

    if (!fs.existsSync(categoryDir)) {
      console.warn(`⚠️  Category directory not found: ${category}`);
      continue;
    }

    const categoryFiles = fs.readdirSync(categoryDir)
      .filter(file => file.endsWith('.json'))
      .map(file => ({
        category,
        filename: file,
        fullPath: path.join(categoryDir, file),
      }));

    files.push(...categoryFiles);
  }

  return files;
}

/**
 * Process a single exercise file
 */
async function processFile(file) {
  stats.processed++;

  const { category, filename, fullPath } = file;
  const transformer = TRANSFORMERS[category];

  if (!transformer) {
    console.warn(`⚠️  No transformer for category: ${category}`);
    stats.skipped++;
    return;
  }

  try {
    console.log(`Processing: ${category}/${filename}`);

    // Read source file
    const sourceData = JSON.parse(fs.readFileSync(fullPath, 'utf8'));

    // Transform to core + support
    const { core, support } = transformer(sourceData, filename);

    // Validate
    const coreValidation = validateCore(core);
    const supportValidation = validateSupport(support);

    if (!coreValidation.valid) {
      throw new Error(`Core validation failed: ${JSON.stringify(coreValidation.errors)}`);
    }

    if (support && !supportValidation.valid) {
      throw new Error(`Support validation failed: ${JSON.stringify(supportValidation.errors)}`);
    }

    // Compare data integrity
    const comparison = compareData(sourceData, core, support, category);
    if (!comparison.valid) {
      console.warn(`  ⚠️  Data integrity warning: ${comparison.warnings.join(', ')}`);
    }

    // Write files
    if (!CONFIG.dryRun) {
      const outputDir = path.join(CONFIG.outputDir, category);
      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
      }

      const baseName = filename.replace('.json', '');
      const corePath = path.join(outputDir, `${baseName}_core.json`);
      const supportPath = path.join(outputDir, `${baseName}_support.json`);

      fs.writeFileSync(corePath, JSON.stringify(core, null, 2));

      // Check if support has content (items OR exercises)
      const hasSupport = support && ((support.items && support.items.length > 0) || (support.exercises && support.exercises.length > 0));

      if (hasSupport) {
        fs.writeFileSync(supportPath, JSON.stringify(support, null, 2));
      }

      console.log(`  ✅ ${baseName}_core.json`);
      if (hasSupport) {
        console.log(`  ✅ ${baseName}_support.json`);
      }
    } else {
      console.log(`  ✅ Would create core + support files`);
    }

    stats.succeeded++;

  } catch (error) {
    console.error(`  ❌ Error: ${error.message}`);
    stats.failed++;
    stats.errors.push({
      file: `${category}/${filename}`,
      error: error.message,
    });
  }
}

/**
 * Ensure output directories exist
 */
function ensureDirectories() {
  const dirs = [
    CONFIG.outputDir,
    CONFIG.sharedDir,
    ...['bl', 'gb', 'wo', 'ws', 'sp', 'tl'].map(cat => path.join(CONFIG.outputDir, cat)),
  ];

  for (const dir of dirs) {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }
}

/**
 * Create shared resource files
 */
async function createSharedResources() {
  const feedbackTemplates = {
    schema_version: "2.0.0",
    correct: [
      "Goed gedaan!",
      "Prima!",
      "Uitstekend!",
      "Dat klopt!"
    ],
    incorrect: [
      "Nog niet helemaal. Probeer het nog eens.",
      "Niet helemaal. Lees de vraag nog eens goed."
    ],
    completion: {
      perfect: "Perfect! Je hebt alles goed!",
      pass: "Goed gedaan! Je hebt {percentage}% gehaald.",
      fail: "Je hebt {percentage}% gehaald. Probeer het nog eens."
    },
    instructions: {
      bl: "Lees de tekst aandachtig en beantwoord de vragen.",
      gb: "Bereken en kies het juiste antwoord.",
      wo: "Kies het juiste antwoord.",
      ws: "Kies de betekenis die het beste past.",
      sp: "Luister naar de audio en schrijf op wat je hoort.",
      tl: "Lees de woorden zo snel en goed mogelijk."
    }
  };

  const uiStrings = {
    schema_version: "2.0.0",
    language: "nl-NL",
    navigation: {
      next: "Volgende",
      previous: "Vorige",
      finish: "Afronden",
      retry: "Opnieuw proberen"
    },
    actions: {
      submit: "Verzenden",
      check: "Controleer",
      hint: "Hint",
      play: "Afspelen",
      replay: "Opnieuw"
    },
    labels: {
      score: "Score",
      progress: "Voortgang",
      question: "Vraag",
      of: "van",
      time: "Tijd"
    }
  };

  const audioConfig = {
    schema_version: "2.0.0",
    settings: {
      autoplay: false,
      volume: 0.8,
      preload: "metadata"
    },
    formats: {
      preferred: "mp3",
      fallback: ["ogg", "wav"]
    },
    paths: {
      base: "/audio",
      patterns: {
        sp: "sp_gr{grade}_{level}_{id:02d}_{part}.mp3"
      }
    }
  };

  fs.writeFileSync(
    path.join(CONFIG.sharedDir, 'feedback-templates.json'),
    JSON.stringify(feedbackTemplates, null, 2)
  );

  fs.writeFileSync(
    path.join(CONFIG.sharedDir, 'ui-strings.json'),
    JSON.stringify(uiStrings, null, 2)
  );

  fs.writeFileSync(
    path.join(CONFIG.sharedDir, 'audio-config.json'),
    JSON.stringify(audioConfig, null, 2)
  );
}

/**
 * Print migration summary
 */
function printSummary() {
  console.log('\n' + '='.repeat(50));
  console.log('📊 MIGRATION SUMMARY');
  console.log('='.repeat(50));
  console.log(`Total processed:  ${stats.processed}`);
  console.log(`✅ Succeeded:     ${stats.succeeded}`);
  console.log(`❌ Failed:        ${stats.failed}`);
  console.log(`⏭️  Skipped:       ${stats.skipped}`);

  if (stats.errors.length > 0) {
    console.log('\n❌ ERRORS:');
    stats.errors.forEach(({ file, error }) => {
      console.log(`  - ${file}: ${error}`);
    });
  }

  if (CONFIG.dryRun) {
    console.log('\n⚠️  DRY RUN MODE - No files were written');
    console.log('Run without --dry-run to apply changes');
  } else {
    console.log(`\n✅ Migration complete! Output in: ${CONFIG.outputDir}`);
  }

  console.log('='.repeat(50) + '\n');
}

// Run migration
migrate().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
