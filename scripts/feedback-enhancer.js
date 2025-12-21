#!/usr/bin/env node

/**
 * Feedback Enhancement Script
 *
 * Analyzes existing support files and enriches them with better feedback
 *
 * Usage:
 *   node scripts/feedback-enhancer.js --analyze               # Analyze all support files
 *   node scripts/feedback-enhancer.js --enhance --category=bl # Enhance BL support files
 *   node scripts/feedback-enhancer.js --enhance --dry-run     # Preview enhancements
 *   node scripts/feedback-enhancer.js --report                # Generate quality report
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  supportDir: path.join(__dirname, '..', 'data-v2', 'exercises'),
  outputDir: path.join(__dirname, '..', 'data-v2-enhanced', 'exercises'),
  reportsDir: path.join(__dirname, '..', 'reports'),
  dryRun: process.argv.includes('--dry-run'),
  category: process.argv.find(arg => arg.startsWith('--category='))?.split('=')[1],
  mode: process.argv.includes('--analyze') ? 'analyze' :
        process.argv.includes('--enhance') ? 'enhance' :
        process.argv.includes('--report') ? 'report' : 'help',
};

// Feedback quality metrics
const QUALITY_CHECKS = {
  hasHints: (item) => !!item.hint || (item.hints && item.hints.length > 0),
  hasProgressiveHints: (item) => item.hints && item.hints.length >= 2,
  hasExplanation: (item) => !!item.feedback?.explanation,
  hasPerOptionFeedback: (item) => item.feedback?.per_option && item.feedback.per_option.length > 0,
  hasLearningObjectives: (item) => item.learning?.learning_objectives && item.learning.learning_objectives.length > 0,
  hasCommonErrors: (item) => item.learning?.common_errors && item.learning.common_errors.length > 0,
  hasReadingStrategies: (item) => item.learning?.reading_strategies && item.learning.reading_strategies.length > 0,
  hasAdaptiveLogic: (item) => !!item.adaptive,
  hasContextualFeedback: (item) => {
    const fb = item.feedback;
    return fb && (fb.correct?.on_first_try || fb.incorrect?.first_attempt);
  },
};

// Statistics
const stats = {
  total_files: 0,
  total_items: 0,
  quality_scores: [],
  issues: [],
  enhancements_applied: 0,
};

/**
 * Main function
 */
async function main() {
  console.log('🎯 Feedback Enhancement Tool\n');

  switch (CONFIG.mode) {
    case 'analyze':
      await analyzeAllFiles();
      break;
    case 'enhance':
      await enhanceAllFiles();
      break;
    case 'report':
      await generateReport();
      break;
    default:
      showHelp();
  }
}

/**
 * Analyze all support files for quality
 */
async function analyzeAllFiles() {
  console.log('📊 Analyzing feedback quality...\n');

  const categories = CONFIG.category ? [CONFIG.category] : ['bl', 'gb', 'wo', 'ws', 'sp', 'tl'];

  for (const category of categories) {
    const files = findSupportFiles(category);

    for (const file of files) {
      analyzeFile(file);
    }
  }

  printAnalysisResults();
}

/**
 * Analyze a single support file
 */
function analyzeFile(filePath) {
  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    stats.total_files++;

    const items = extractItems(data);

    items.forEach((item, index) => {
      stats.total_items++;

      const quality = calculateQualityScore(item);
      stats.quality_scores.push(quality.score);

      if (quality.score < 50) {
        stats.issues.push({
          file: path.basename(filePath),
          item_id: item.item_id,
          score: quality.score,
          missing: quality.missing,
        });
      }
    });

  } catch (error) {
    console.error(`Error analyzing ${filePath}:`, error.message);
  }
}

/**
 * Calculate quality score for an item
 */
function calculateQualityScore(item) {
  const checks = Object.entries(QUALITY_CHECKS);
  const passed = checks.filter(([name, fn]) => fn(item));
  const score = Math.round((passed.length / checks.length) * 100);

  const missing = checks
    .filter(([name, fn]) => !fn(item))
    .map(([name]) => name);

  return { score, missing, passed: passed.length, total: checks.length };
}

/**
 * Extract items from support data (handles both structures)
 */
function extractItems(data) {
  const items = [];

  if (data.exercises && Array.isArray(data.exercises)) {
    // BL structure
    data.exercises.forEach(exercise => {
      if (exercise.items) {
        items.push(...exercise.items);
      }
    });
  } else if (data.items && Array.isArray(data.items)) {
    // Simple structure
    items.push(...data.items);
  }

  return items;
}

/**
 * Find all support files for a category
 */
function findSupportFiles(category) {
  const categoryDir = path.join(CONFIG.supportDir, category);

  if (!fs.existsSync(categoryDir)) {
    return [];
  }

  return fs.readdirSync(categoryDir)
    .filter(file => file.endsWith('_support.json'))
    .map(file => path.join(categoryDir, file));
}

/**
 * Enhance all support files
 */
async function enhanceAllFiles() {
  console.log('✨ Enhancing feedback quality...\n');
  console.log(`Mode: ${CONFIG.dryRun ? 'DRY RUN' : 'PRODUCTION'}\n`);

  const categories = CONFIG.category ? [CONFIG.category] : ['bl', 'gb', 'wo', 'ws', 'sp', 'tl'];

  for (const category of categories) {
    const files = findSupportFiles(category);

    for (const file of files) {
      await enhanceFile(file, category);
    }
  }

  printEnhancementResults();
}

/**
 * Enhance a single support file
 */
async function enhanceFile(filePath, category) {
  try {
    console.log(`Enhancing: ${path.basename(filePath)}`);

    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const enhanced = enhanceData(data);

    if (!CONFIG.dryRun) {
      const outputPath = filePath.replace('data-v2', 'data-v2-enhanced');
      const outputDir = path.dirname(outputPath);

      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
      }

      fs.writeFileSync(outputPath, JSON.stringify(enhanced, null, 2));
      console.log(`  ✅ Enhanced and saved to: ${outputPath}`);
    } else {
      console.log(`  ✅ Would enhance (dry-run)`);
    }

    stats.enhancements_applied++;

  } catch (error) {
    console.error(`  ❌ Error: ${error.message}`);
  }
}

/**
 * Enhance support data
 */
function enhanceData(data) {
  const enhanced = { ...data };

  // Add global feedback if missing
  if (!enhanced.global_feedback) {
    enhanced.global_feedback = {
      on_start: "Lees de tekst aandachtig voordat je de vragen beantwoordt.",
      on_complete: "Goed gedaan! Je hebt alle vragen beantwoord.",
      on_perfect_score: "Perfect! Je hebt alles goed! 🌟",
      on_pass: "Goed gedaan! Je hebt {score} van de {total} vragen goed.",
    };
  }

  // Enhance items
  if (enhanced.exercises && Array.isArray(enhanced.exercises)) {
    // BL structure
    enhanced.exercises = enhanced.exercises.map(exercise => ({
      ...exercise,
      items: exercise.items.map(item => enhanceItem(item)),
    }));
  } else if (enhanced.items && Array.isArray(enhanced.items)) {
    // Simple structure
    enhanced.items = enhanced.items.map(item => enhanceItem(item));
  }

  return enhanced;
}

/**
 * Enhance a single item
 */
function enhanceItem(item) {
  const enhanced = { ...item };

  // Convert simple hint to progressive hints
  if (enhanced.hint && !enhanced.hints) {
    enhanced.hints = [
      {
        level: 1,
        text: enhanced.hint,
        cost_points: 0,
      },
      {
        level: 2,
        text: generateHint(enhanced.hint, 2),
        cost_points: 1,
      },
    ];
    delete enhanced.hint; // Remove old format
  }

  // Add feedback structure if missing
  if (!enhanced.feedback) {
    enhanced.feedback = {};
  }

  // Add correct feedback variations
  if (!enhanced.feedback.correct) {
    enhanced.feedback.correct = {
      default: "Goed gedaan!",
      on_first_try: "Uitstekend! Je hebt het meteen goed! 🎯",
      after_hint: "Mooi! De hint heeft je geholpen.",
    };
  }

  // Add incorrect feedback variations
  if (!enhanced.feedback.incorrect) {
    enhanced.feedback.incorrect = {
      first_attempt: "Nog niet helemaal. Probeer het nog eens.",
      second_attempt: "Denk goed na. Wil je een hint?",
      third_attempt: "Laten we samen kijken naar de vraag.",
    };
  }

  // Add explanation if missing
  if (!enhanced.feedback.explanation) {
    enhanced.feedback.explanation = {
      text: "Het juiste antwoord is...",
    };
  }

  // Enhance learning metadata
  if (enhanced.learning) {
    if (!enhanced.learning.skill_description) {
      enhanced.learning.skill_description = getSkillDescription(enhanced.learning.skill);
    }

    if (!enhanced.learning.reading_strategies) {
      enhanced.learning.reading_strategies = getReadingStrategies(enhanced.learning.skill);
    }

    if (!enhanced.learning.common_errors) {
      enhanced.learning.common_errors = getCommonErrors(enhanced.learning.skill);
    }
  }

  // Add adaptive logic template
  if (!enhanced.adaptive) {
    enhanced.adaptive = {
      if_correct_quickly: {
        action: "increase_difficulty",
        message: "Je bent hier goed in! Laten we het wat uitdagender maken.",
      },
      if_wrong_multiple: {
        action: "decrease_difficulty",
        message: "Laten we eerst wat makkelijkere vragen doen.",
      },
    };
  }

  return enhanced;
}

/**
 * Generate a more specific hint based on the original
 */
function generateHint(originalHint, level) {
  const hints = {
    2: `${originalHint} Kijk extra goed naar de details.`,
  };
  return hints[level] || originalHint;
}

/**
 * Get skill description
 */
function getSkillDescription(skill) {
  const descriptions = {
    letterlijk: "Letterlijke informatie terughalen uit de tekst",
    inferentieel: "Tussen de regels lezen en conclusies trekken",
    verbanden: "Verbanden leggen tussen verschillende delen van de tekst",
    hoofdzaken: "Onderscheid maken tussen hoofd- en bijzaken",
    woordenschat: "Woordbetekenis begrijpen uit context",
    conclusies: "Conclusies trekken op basis van de tekst",
  };
  return descriptions[skill] || "Leesvaardigheid";
}

/**
 * Get reading strategies for a skill
 */
function getReadingStrategies(skill) {
  const strategies = {
    letterlijk: [
      "Zoek naar signaalwoorden zoals 'omdat', 'want', 'daarom'",
      "Lees de vraag eerst, dan weet je waar je op moet letten",
      "Onderstreep belangrijke informatie in de tekst",
    ],
    inferentieel: [
      "Denk na over wat er niet letterlijk staat maar wel bedoeld wordt",
      "Gebruik je eigen kennis en ervaring",
      "Let op aanwijzingen in de tekst",
    ],
    verbanden: [
      "Let op verbindingswoorden zoals 'maar', 'dus', 'omdat'",
      "Denk aan oorzaak en gevolg",
      "Kijk naar de volgorde van gebeurtenissen",
    ],
    hoofdzaken: [
      "Vraag je af: waar gaat de tekst vooral over?",
      "De eerste en laatste zin zijn vaak belangrijk",
      "Details zijn leuk, maar niet altijd belangrijk",
    ],
    woordenschat: [
      "Kijk naar de context: welke woorden staan eromheen?",
      "Probeer het woord te vervangen door een ander woord",
      "Lees de hele zin, niet alleen het moeilijke woord",
    ],
  };
  return strategies[skill] || ["Lees de tekst aandachtig"];
}

/**
 * Get common errors for a skill
 */
function getCommonErrors(skill) {
  return [
    {
      type: "niet_zorgvuldig_lezen",
      description: "Snel lezen zonder op details te letten",
      remedy: "Neem de tijd om elke zin goed te lezen",
    },
    {
      type: "raden",
      description: "Antwoord geven zonder de tekst te raadplegen",
      remedy: "Zoek het antwoord altijd in de tekst",
    },
  ];
}

/**
 * Generate quality report
 */
async function generateReport() {
  console.log('📋 Generating feedback quality report...\n');

  await analyzeAllFiles();

  const report = {
    generated_at: new Date().toISOString(),
    summary: {
      total_files: stats.total_files,
      total_items: stats.total_items,
      average_quality_score: Math.round(
        stats.quality_scores.reduce((a, b) => a + b, 0) / stats.quality_scores.length
      ),
      items_below_50: stats.issues.length,
      items_above_80: stats.quality_scores.filter(s => s >= 80).length,
    },
    quality_distribution: {
      excellent: stats.quality_scores.filter(s => s >= 80).length,
      good: stats.quality_scores.filter(s => s >= 60 && s < 80).length,
      fair: stats.quality_scores.filter(s => s >= 40 && s < 60).length,
      poor: stats.quality_scores.filter(s => s < 40).length,
    },
    top_issues: stats.issues
      .sort((a, b) => a.score - b.score)
      .slice(0, 20),
  };

  // Save report
  if (!fs.existsSync(CONFIG.reportsDir)) {
    fs.mkdirSync(CONFIG.reportsDir, { recursive: true });
  }

  const reportPath = path.join(
    CONFIG.reportsDir,
    `feedback-quality-${new Date().toISOString().split('T')[0]}.json`
  );

  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));

  console.log('📊 Report Summary:');
  console.log(`  Total items analyzed: ${report.summary.total_items}`);
  console.log(`  Average quality score: ${report.summary.average_quality_score}%`);
  console.log(`  Excellent (80%+): ${report.quality_distribution.excellent}`);
  console.log(`  Good (60-79%): ${report.quality_distribution.good}`);
  console.log(`  Fair (40-59%): ${report.quality_distribution.fair}`);
  console.log(`  Poor (<40%): ${report.quality_distribution.poor}`);
  console.log(`\n  Report saved: ${reportPath}`);
}

/**
 * Print analysis results
 */
function printAnalysisResults() {
  const avgScore = Math.round(
    stats.quality_scores.reduce((a, b) => a + b, 0) / stats.quality_scores.length
  );

  console.log('\n' + '='.repeat(50));
  console.log('📊 ANALYSIS RESULTS');
  console.log('='.repeat(50));
  console.log(`Files analyzed: ${stats.total_files}`);
  console.log(`Items analyzed: ${stats.total_items}`);
  console.log(`Average quality score: ${avgScore}%`);
  console.log(`Items needing improvement (<50%): ${stats.issues.length}`);

  if (stats.issues.length > 0) {
    console.log('\n📋 Top items needing improvement:');
    stats.issues.slice(0, 10).forEach(issue => {
      console.log(`  ${issue.file} - ${issue.item_id} (${issue.score}%)`);
      console.log(`    Missing: ${issue.missing.join(', ')}`);
    });
  }

  console.log('='.repeat(50) + '\n');
}

/**
 * Print enhancement results
 */
function printEnhancementResults() {
  console.log('\n' + '='.repeat(50));
  console.log('✨ ENHANCEMENT RESULTS');
  console.log('='.repeat(50));
  console.log(`Files enhanced: ${stats.enhancements_applied}`);

  if (CONFIG.dryRun) {
    console.log('\n⚠️  DRY RUN MODE - No files were written');
    console.log('Run without --dry-run to apply enhancements');
  } else {
    console.log(`\nEnhanced files saved to: ${CONFIG.outputDir}`);
  }

  console.log('='.repeat(50) + '\n');
}

/**
 * Show help message
 */
function showHelp() {
  console.log(`
Feedback Enhancement Tool

Usage:
  node scripts/feedback-enhancer.js [options]

Options:
  --analyze               Analyze all support files for quality
  --enhance               Enhance support files with better feedback
  --report                Generate detailed quality report
  --category=XX           Process specific category only (bl, gb, wo, ws, sp, tl)
  --dry-run               Preview changes without writing files

Examples:
  # Analyze all support files
  node scripts/feedback-enhancer.js --analyze

  # Enhance BL files (dry run)
  node scripts/feedback-enhancer.js --enhance --category=bl --dry-run

  # Enhance all files
  node scripts/feedback-enhancer.js --enhance

  # Generate quality report
  node scripts/feedback-enhancer.js --report

Quality Metrics:
  - Progressive hints (multiple levels)
  - Detailed explanations
  - Per-option feedback
  - Learning objectives
  - Common errors and remediation
  - Reading strategies
  - Adaptive logic
  - Contextual feedback
`);
}

// Run
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
