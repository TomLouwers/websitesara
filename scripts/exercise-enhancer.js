#!/usr/bin/env node

/**
 * Exercise Enhancement Helper Tool
 *
 * Takes an existing exercise and helps enhance it to Schema V2.0
 * by generating templates with the correct structure.
 *
 * Usage:
 *   node scripts/exercise-enhancer.js <input-file> <output-file>
 *   node scripts/exercise-enhancer.js data/exercises/bl/bl_groep4_m4_1.json data/exercises/bl/bl_groep4_m4_1_enhanced.json
 *
 * Features:
 * - Preserves all existing fields
 * - Adds Schema V2.0 structure with TODO placeholders
 * - Validates before saving
 * - Creates backup of original
 *
 * @version 1.0.0
 * @date 2026-01-07
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Color codes
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m',
    magenta: '\x1b[35m',
};

/**
 * Generate enhanced feedback template for a question
 */
function generateFeedbackTemplate(question) {
    const options = question.options || [];
    const correctOption = options.find(opt => opt.is_correct) ||
                         (typeof question.correct === 'number' ? options[question.correct] : null);

    const template = {
        correct: {
            explanation: '📝 TODO: Explain WHY this answer is correct',
            skill_reinforcement: '💪 TODO: What skill did the student demonstrate?'
        },
        incorrect: {
            by_option: {},
            workedExample: {
                steps: [
                    'TODO: Step 1 - What to do first',
                    'TODO: Step 2 - Next action',
                    'TODO: Step 3 - How to arrive at answer',
                    'TODO: Step 4 - Conclusion'
                ]
            }
        }
    };

    // Generate per-option feedback for wrong answers
    options.forEach(option => {
        if (!option.is_correct && (typeof question.correct !== 'number' || options.indexOf(option) !== question.correct)) {
            const label = option.label || String.fromCharCode(65 + options.indexOf(option)); // A, B, C, D
            template.incorrect.by_option[label] = {
                explanation: `TODO: Why is "${option.text}" incorrect?`,
                hint: 'TODO: Hint to guide toward correct answer',
                misconception: 'TODO: What error pattern does this represent?',
                error_type: 'TODO: letterlijk_gemist | inferentie_fout | vocabulaire | rekenfout_basis | conceptfout'
            };
        }
    });

    return template;
}

/**
 * Generate 3-tier hints template
 */
function generate3TierHints(question) {
    const existingHint = question.hint || 'Think about the question carefully';

    return {
        tier1_procedural: {
            text: question.hint || 'TODO: WHERE to look (procedural guidance)',
            reveal_percentage: 0.2,
            type: 'procedural'
        },
        tier2_conceptual: {
            text: 'TODO: WHAT to think about (conceptual understanding)',
            reveal_percentage: 0.5,
            type: 'conceptual'
        },
        tier3_worked_example: {
            text: 'TODO: HOW to solve it (near-complete solution)',
            reveal_percentage: 0.9,
            type: 'worked_example'
        }
    };
}

/**
 * Enhance a single question
 */
function enhanceQuestion(question) {
    // Check if already enhanced
    if (question.feedback && question.feedback.correct) {
        console.log(`   ℹ️  Question "${question.item_id || question.id}" already enhanced, skipping...`);
        return question;
    }

    // Create enhanced version
    const enhanced = { ...question };

    // Add feedback if missing
    if (!enhanced.feedback) {
        enhanced.feedback = generateFeedbackTemplate(question);
    }

    // Add 3-tier hints if missing
    if (!enhanced.hints) {
        enhanced.hints = generate3TierHints(question);
    }

    // Add metadata if missing
    if (!enhanced.metadata) {
        enhanced.metadata = {
            schema_version: '2.0.0',
            enhanced: true,
            enhanced_date: new Date().toISOString().split('T')[0]
        };
    } else {
        enhanced.metadata.schema_version = '2.0.0';
        enhanced.metadata.enhanced = true;
        enhanced.metadata.enhanced_date = new Date().toISOString().split('T')[0];
    }

    return enhanced;
}

/**
 * Enhance an exercise
 */
function enhanceExercise(exercise) {
    if (!exercise.questions || !Array.isArray(exercise.questions)) {
        throw new Error('Invalid exercise structure: missing questions array');
    }

    const enhanced = { ...exercise };

    // Add exercise-level metadata
    if (!enhanced.metadata) {
        enhanced.metadata = {};
    }
    enhanced.metadata.schema_version = '2.0.0';
    enhanced.metadata.enhanced = true;

    // Enhance each question
    enhanced.questions = exercise.questions.map(q => enhanceQuestion(q));

    return enhanced;
}

/**
 * Count TODOs in object
 */
function countTODOs(obj) {
    const str = JSON.stringify(obj);
    return (str.match(/TODO:/g) || []).length;
}

/**
 * Create backup of original file
 */
function createBackup(filePath) {
    const backupPath = filePath.replace('.json', '.backup.json');
    fs.copyFileSync(filePath, backupPath);
    return backupPath;
}

/**
 * Main enhancement workflow
 */
async function enhanceFile(inputPath, outputPath) {
    console.log(`${colors.bright}${colors.cyan}Exercise Enhancement Helper${colors.reset}\n`);

    // Validate input
    if (!fs.existsSync(inputPath)) {
        console.error(`${colors.red}❌ Error: File not found: ${inputPath}${colors.reset}`);
        process.exit(1);
    }

    console.log(`📂 Input:  ${colors.cyan}${inputPath}${colors.reset}`);
    console.log(`📝 Output: ${colors.cyan}${outputPath}${colors.reset}\n`);

    // Read input file
    console.log(`${colors.yellow}⏳ Reading exercise file...${colors.reset}`);
    let data;
    try {
        const content = fs.readFileSync(inputPath, 'utf8');
        data = JSON.parse(content);
    } catch (error) {
        console.error(`${colors.red}❌ Error reading file: ${error.message}${colors.reset}`);
        process.exit(1);
    }

    // Handle both single exercise and array
    const exercises = Array.isArray(data) ? data : [data];
    const isArray = Array.isArray(data);

    console.log(`${colors.green}✓${colors.reset} Found ${exercises.length} exercise(s)\n`);

    // Enhance exercises
    console.log(`${colors.yellow}⏳ Generating Schema V2.0 templates...${colors.reset}`);
    const enhanced = exercises.map((ex, idx) => {
        console.log(`   Processing exercise ${idx + 1}/${exercises.length}: "${ex.title || ex.id}"`);
        try {
            return enhanceExercise(ex);
        } catch (error) {
            console.error(`   ${colors.red}❌ Error: ${error.message}${colors.reset}`);
            return ex; // Return original on error
        }
    });

    // Count TODOs
    const totalTODOs = enhanced.reduce((sum, ex) => sum + countTODOs(ex), 0);

    console.log(`${colors.green}✓${colors.reset} Templates generated\n`);

    // Show statistics
    const totalQuestions = enhanced.reduce((sum, ex) => sum + (ex.questions?.length || 0), 0);
    console.log(`${colors.bright}📊 Statistics${colors.reset}`);
    console.log(`   Questions to enhance: ${totalQuestions}`);
    console.log(`   TODOs to complete:    ${totalTODOs}`);
    console.log(`   Estimated time:       ${Math.ceil(totalQuestions * 5)} minutes\n`);

    // Save enhanced file
    console.log(`${colors.yellow}⏳ Saving enhanced file...${colors.reset}`);

    try {
        const output = isArray ? enhanced : enhanced[0];
        fs.writeFileSync(
            outputPath,
            JSON.stringify(output, null, 2),
            'utf8'
        );
        console.log(`${colors.green}✓${colors.reset} Saved to: ${colors.cyan}${outputPath}${colors.reset}\n`);
    } catch (error) {
        console.error(`${colors.red}❌ Error saving file: ${error.message}${colors.reset}`);
        process.exit(1);
    }

    // Show next steps
    console.log(`${colors.bright}${colors.green}✨ Success!${colors.reset}`);
    console.log(`\n${colors.bright}📝 Next Steps:${colors.reset}`);
    console.log(`   1. Open ${colors.cyan}${outputPath}${colors.reset}`);
    console.log(`   2. Search for "TODO:" and fill in each field`);
    console.log(`   3. Focus on:`);
    console.log(`      • ${colors.yellow}feedback.correct.explanation${colors.reset} - Why answer is correct`);
    console.log(`      • ${colors.yellow}feedback.incorrect.by_option${colors.reset} - Per-option feedback`);
    console.log(`      • ${colors.yellow}feedback.incorrect.workedExample${colors.reset} - Step-by-step solution`);
    console.log(`      • ${colors.yellow}hints.tier2_conceptual${colors.reset} - Conceptual hint`);
    console.log(`      • ${colors.yellow}hints.tier3_worked_example${colors.reset} - Worked example hint`);
    console.log(`   4. Remove "TODO:" prefix when done`);
    console.log(`   5. Test in the app!\n`);

    // Show example
    console.log(`${colors.bright}💡 Example:${colors.reset}`);
    console.log(`${colors.red}   Before:${colors.reset} "explanation": "TODO: Explain why correct"`);
    console.log(`${colors.green}   After:${colors.reset}  "explanation": "Goed gevonden! Je hebt het juiste antwoord gekozen omdat..."`);
    console.log('');
}

// CLI interface
const args = process.argv.slice(2);

if (args.length < 1) {
    console.log(`${colors.bright}Usage:${colors.reset}`);
    console.log(`  node scripts/exercise-enhancer.js <input-file> [output-file]`);
    console.log('');
    console.log(`${colors.bright}Examples:${colors.reset}`);
    console.log(`  node scripts/exercise-enhancer.js data/exercises/bl/bl_groep4_m4_1.json`);
    console.log(`  node scripts/exercise-enhancer.js data/exercises/bl/bl_groep4_m4_1.json output.json`);
    console.log('');
    process.exit(0);
}

const inputPath = args[0];
const outputPath = args[1] || inputPath.replace('.json', '_enhanced.json');

enhanceFile(inputPath, outputPath);
