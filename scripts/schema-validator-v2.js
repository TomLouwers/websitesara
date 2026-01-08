#!/usr/bin/env node

/**
 * Schema Validator & Exercise Quality Scanner
 *
 * Scans all exercise files and checks:
 * - Schema V2.0 compliance (feedback fields)
 * - Required fields presence
 * - Quality issues
 * - Enhancement status
 *
 * Usage: node scripts/schema-validator-v2.js
 * Output: Console report + quality-report.json
 *
 * @version 2.0.0
 * @date 2026-01-07
 */

const fs = require('fs');
const path = require('path');

// Configuration
const EXERCISE_DIRS = [
    'data/exercises/bl',  // Reading comprehension
    'data/exercises/gb',  // Math
    'data/exercises/ws',  // Vocabulary
    'data/exercises/wo',  // Word spelling
    'data/exercises/sp',  // Spelling dictation
    'data/exercises/tl',  // DMT lists
];

// Color codes for terminal output
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m',
};

// Statistics
const stats = {
    totalFiles: 0,
    totalExercises: 0,
    totalQuestions: 0,
    enhanced: 0,
    legacy: 0,
    issues: [],
    byCategory: {}
};

/**
 * Check if a question has Schema V2.0 enhanced feedback
 */
function hasEnhancedFeedback(question) {
    return !!(question.feedback &&
             (question.feedback.correct || question.feedback.incorrect));
}

/**
 * Check if a question has 3-tier hints
 */
function has3TierHints(question) {
    return !!(question.hints &&
             question.hints.tier1_procedural);
}

/**
 * Validate a single question
 */
function validateQuestion(question, exerciseFile, exerciseId) {
    const issues = [];
    const status = {
        hasEnhancedFeedback: hasEnhancedFeedback(question),
        has3TierHints: has3TierHints(question),
        hasHint: !!question.hint || !!question.hints,
        hasSkill: !!question.skill,
        hasStrategy: !!question.strategy
    };

    // Check for missing essential fields
    if (!question.question && !question.text) {
        issues.push({
            severity: 'error',
            field: 'question',
            message: 'Missing question text',
            file: exerciseFile,
            exerciseId: exerciseId,
            questionId: question.item_id || question.id
        });
    }

    if (!question.options && question.correct === undefined) {
        issues.push({
            severity: 'error',
            field: 'answer',
            message: 'Missing answer options or correct field',
            file: exerciseFile,
            exerciseId: exerciseId,
            questionId: question.item_id || question.id
        });
    }

    // Check for hint (basic requirement)
    if (!status.hasHint) {
        issues.push({
            severity: 'warning',
            field: 'hint',
            message: 'Missing hint',
            file: exerciseFile,
            exerciseId: exerciseId,
            questionId: question.item_id || question.id
        });
    }

    // Check Schema V2.0 fields
    if (!status.hasEnhancedFeedback) {
        issues.push({
            severity: 'info',
            field: 'feedback',
            message: 'Not enhanced - missing Schema V2.0 feedback',
            file: exerciseFile,
            exerciseId: exerciseId,
            questionId: question.item_id || question.id
        });
    } else {
        // If has feedback, check completeness
        if (question.feedback.correct && !question.feedback.correct.explanation) {
            issues.push({
                severity: 'warning',
                field: 'feedback.correct.explanation',
                message: 'Enhanced but missing correct explanation',
                file: exerciseFile,
                exerciseId: exerciseId,
                questionId: question.item_id || question.id
            });
        }

        if (question.feedback.incorrect && !question.feedback.incorrect.workedExample) {
            issues.push({
                severity: 'warning',
                field: 'feedback.incorrect.workedExample',
                message: 'Enhanced but missing worked example',
                file: exerciseFile,
                exerciseId: exerciseId,
                questionId: question.item_id || question.id
            });
        }
    }

    return { issues, status };
}

/**
 * Validate a single exercise
 */
function validateExercise(exercise, filePath) {
    const fileName = path.basename(filePath);
    const issues = [];
    let enhancedCount = 0;
    let legacyCount = 0;

    // Check exercise structure
    if (!exercise.questions || !Array.isArray(exercise.questions)) {
        issues.push({
            severity: 'error',
            field: 'questions',
            message: 'Missing or invalid questions array',
            file: fileName,
            exerciseId: exercise.id || exercise.title
        });
        return { issues, enhancedCount, legacyCount };
    }

    // Validate each question
    exercise.questions.forEach((question, index) => {
        const result = validateQuestion(question, fileName, exercise.id || exercise.title);
        issues.push(...result.issues);

        if (result.status.hasEnhancedFeedback) {
            enhancedCount++;
        } else {
            legacyCount++;
        }
    });

    return { issues, enhancedCount, legacyCount };
}

/**
 * Scan a single file
 */
function scanFile(filePath) {
    const fileName = path.basename(filePath);

    try {
        const content = fs.readFileSync(filePath, 'utf8');
        const data = JSON.parse(content);

        // Handle both single exercise and array of exercises
        const exercises = Array.isArray(data) ? data : [data];

        exercises.forEach(exercise => {
            stats.totalExercises++;

            const category = path.basename(path.dirname(filePath));
            if (!stats.byCategory[category]) {
                stats.byCategory[category] = {
                    files: 0,
                    exercises: 0,
                    questions: 0,
                    enhanced: 0,
                    legacy: 0
                };
            }
            stats.byCategory[category].exercises++;

            // Validate exercise
            const result = validateExercise(exercise, filePath);

            // Update stats
            if (exercise.questions) {
                const questionCount = exercise.questions.length;
                stats.totalQuestions += questionCount;
                stats.byCategory[category].questions += questionCount;
                stats.enhanced += result.enhancedCount;
                stats.legacy += result.legacyCount;
                stats.byCategory[category].enhanced += result.enhancedCount;
                stats.byCategory[category].legacy += result.legacyCount;
            }

            // Store issues
            stats.issues.push(...result.issues);
        });

    } catch (error) {
        console.error(`${colors.red}Error reading ${fileName}: ${error.message}${colors.reset}`);
        stats.issues.push({
            severity: 'error',
            field: 'file',
            message: `Failed to parse file: ${error.message}`,
            file: fileName
        });
    }
}

/**
 * Scan a directory recursively
 */
function scanDirectory(dirPath) {
    if (!fs.existsSync(dirPath)) {
        console.log(`${colors.yellow}⚠️  Directory not found: ${dirPath}${colors.reset}`);
        return;
    }

    const files = fs.readdirSync(dirPath);

    files.forEach(file => {
        const filePath = path.join(dirPath, file);
        const stat = fs.statSync(filePath);

        if (stat.isDirectory()) {
            scanDirectory(filePath);
        } else if (file.endsWith('.json')) {
            stats.totalFiles++;
            const category = path.basename(dirPath);
            if (!stats.byCategory[category]) {
                stats.byCategory[category] = {
                    files: 0,
                    exercises: 0,
                    questions: 0,
                    enhanced: 0,
                    legacy: 0
                };
            }
            stats.byCategory[category].files++;
            scanFile(filePath);
        }
    });
}

/**
 * Generate console report
 */
function printReport() {
    console.log('\n' + '='.repeat(80));
    console.log(`${colors.bright}${colors.cyan}Exercise Quality Report - Schema V2.0 Validator${colors.reset}`);
    console.log('='.repeat(80) + '\n');

    // Overall statistics
    console.log(`${colors.bright}📊 Overall Statistics${colors.reset}`);
    console.log(`   Files scanned:      ${stats.totalFiles}`);
    console.log(`   Total exercises:    ${stats.totalExercises}`);
    console.log(`   Total questions:    ${stats.totalQuestions}`);
    console.log('');

    // Enhancement status
    const enhancedPercent = ((stats.enhanced / stats.totalQuestions) * 100).toFixed(1);
    const legacyPercent = ((stats.legacy / stats.totalQuestions) * 100).toFixed(1);

    console.log(`${colors.bright}✨ Enhancement Status${colors.reset}`);
    console.log(`   ${colors.green}Enhanced (V2.0):${colors.reset}    ${stats.enhanced} (${enhancedPercent}%)`);
    console.log(`   ${colors.yellow}Legacy:${colors.reset}             ${stats.legacy} (${legacyPercent}%)`);
    console.log('');

    // By category
    console.log(`${colors.bright}📚 By Category${colors.reset}`);
    Object.entries(stats.byCategory).forEach(([category, data]) => {
        const catEnhanced = ((data.enhanced / data.questions) * 100).toFixed(1);
        console.log(`   ${category.toUpperCase().padEnd(4)} → ${data.questions} questions, ${data.enhanced} enhanced (${catEnhanced}%)`);
    });
    console.log('');

    // Issues summary
    const errors = stats.issues.filter(i => i.severity === 'error').length;
    const warnings = stats.issues.filter(i => i.severity === 'warning').length;
    const info = stats.issues.filter(i => i.severity === 'info').length;

    console.log(`${colors.bright}⚠️  Issues Found${colors.reset}`);
    console.log(`   ${colors.red}Errors:${colors.reset}     ${errors}`);
    console.log(`   ${colors.yellow}Warnings:${colors.reset}   ${warnings}`);
    console.log(`   ${colors.blue}Info:${colors.reset}       ${info}`);
    console.log('');

    // Show sample issues
    if (errors > 0) {
        console.log(`${colors.red}❌ Sample Errors (first 5):${colors.reset}`);
        stats.issues
            .filter(i => i.severity === 'error')
            .slice(0, 5)
            .forEach(issue => {
                console.log(`   → ${issue.file}: ${issue.message}`);
            });
        console.log('');
    }

    // Enhancement opportunities
    console.log(`${colors.bright}🚀 Enhancement Opportunities${colors.reset}`);
    console.log(`   Questions to enhance: ${stats.legacy}`);
    console.log(`   Estimated time (5 min/question): ${Math.ceil(stats.legacy * 5 / 60)} hours`);
    console.log(`   With helper tool (2 min/question): ${Math.ceil(stats.legacy * 2 / 60)} hours`);
    console.log('');

    console.log('='.repeat(80));
    console.log(`${colors.green}✅ Scan complete!${colors.reset}`);
    console.log(`   Full report saved to: ${colors.cyan}quality-report.json${colors.reset}`);
    console.log('='.repeat(80) + '\n');
}

/**
 * Save JSON report
 */
function saveReport() {
    const report = {
        timestamp: new Date().toISOString(),
        summary: {
            totalFiles: stats.totalFiles,
            totalExercises: stats.totalExercises,
            totalQuestions: stats.totalQuestions,
            enhanced: stats.enhanced,
            legacy: stats.legacy,
            enhancementPercentage: ((stats.enhanced / stats.totalQuestions) * 100).toFixed(2)
        },
        byCategory: stats.byCategory,
        issues: stats.issues,
        recommendations: {
            priorityFiles: findPriorityFiles(),
            quickWins: findQuickWins()
        }
    };

    fs.writeFileSync(
        'quality-report.json',
        JSON.stringify(report, null, 2),
        'utf8'
    );
}

/**
 * Find files that should be prioritized for enhancement
 */
function findPriorityFiles() {
    // Files with most legacy questions
    const fileStats = {};

    stats.issues
        .filter(i => i.severity === 'info' && i.message.includes('Not enhanced'))
        .forEach(issue => {
            if (!fileStats[issue.file]) {
                fileStats[issue.file] = 0;
            }
            fileStats[issue.file]++;
        });

    return Object.entries(fileStats)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([file, count]) => ({ file, legacyQuestions: count }));
}

/**
 * Find exercises that are partially enhanced (quick wins)
 */
function findQuickWins() {
    // Files with at least one enhanced question (templates available)
    return ['Check quality-report.json for detailed analysis'];
}

// Main execution
console.log(`${colors.bright}Starting exercise scan...${colors.reset}\n`);

EXERCISE_DIRS.forEach(dir => {
    console.log(`Scanning: ${dir}...`);
    scanDirectory(dir);
});

printReport();
saveReport();
