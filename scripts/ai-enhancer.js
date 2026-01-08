#!/usr/bin/env node

/**
 * AI-Assisted Exercise Enhancement Tool
 *
 * Uses OpenAI or Anthropic Claude API to automatically generate Schema V2.0
 * feedback for exercises. Supports human review and editing before saving.
 *
 * Usage:
 *   node scripts/ai-enhancer.js <template-file> [options]
 *
 * Options:
 *   --provider=openai|anthropic  AI provider (default: anthropic)
 *   --model=<model-name>         Model to use
 *   --output=<file>              Output file (default: *_AI_ENHANCED.json)
 *   --batch-size=<n>             Questions per batch (default: 5)
 *   --review                     Interactive review mode (default: true)
 *   --auto-approve               Skip review, auto-approve all (use with caution!)
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// ANSI colors
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[36m',
  magenta: '\x1b[35m',
};

const log = {
  title: (msg) => console.log(`${colors.bright}${colors.blue}${msg}${colors.reset}\n`),
  info: (msg) => console.log(`${colors.blue}${msg}${colors.reset}`),
  success: (msg) => console.log(`${colors.green}✓${colors.reset} ${msg}`),
  warning: (msg) => console.log(`${colors.yellow}⚠${colors.reset} ${msg}`),
  error: (msg) => console.log(`${colors.red}✗${colors.reset} ${msg}`),
  step: (msg) => console.log(`${colors.yellow}⏳ ${msg}...${colors.reset}`),
  highlight: (msg) => console.log(`${colors.magenta}${msg}${colors.reset}`),
};

// Configuration
const CONFIG = {
  provider: 'anthropic', // 'openai' or 'anthropic'
  model: 'claude-sonnet-4-5-20250929', // or 'gpt-4o'
  batchSize: 5,
  review: true,
  autoApprove: false,
  apiKey: null,
};

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log(`
AI-Assisted Exercise Enhancement Tool

Usage:
  node scripts/ai-enhancer.js <template-file> [options]

Options:
  --provider=openai|anthropic   AI provider (default: anthropic)
  --model=<model-name>          Model to use
  --output=<file>               Output file (default: *_AI_ENHANCED.json)
  --batch-size=<n>              Questions per batch (default: 5)
  --review                      Interactive review mode (default: true)
  --auto-approve                Skip review, auto-approve all (use with caution!)
  --api-key=<key>               API key (or use env: ANTHROPIC_API_KEY / OPENAI_API_KEY)

Examples:
  # Basic usage (Anthropic Claude)
  node scripts/ai-enhancer.js data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json

  # Use OpenAI
  node scripts/ai-enhancer.js data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json --provider=openai

  # Auto-approve (skip review)
  node scripts/ai-enhancer.js data/exercises/bl/bl_groep4_e4_1_TEMPLATE.json --auto-approve

Environment Variables:
  ANTHROPIC_API_KEY   Anthropic API key
  OPENAI_API_KEY      OpenAI API key
    `);
    process.exit(0);
  }

  const inputFile = args.find(arg => !arg.startsWith('--'));
  const options = {};

  args.forEach(arg => {
    if (arg.startsWith('--')) {
      const [key, value] = arg.substring(2).split('=');
      options[key] = value || true;
    }
  });

  return { inputFile, options };
}

// Load API key from environment or arguments
function loadApiKey(provider, options) {
  if (options['api-key']) {
    return options['api-key'];
  }

  const envKey = provider === 'anthropic' ? 'ANTHROPIC_API_KEY' : 'OPENAI_API_KEY';
  const key = process.env[envKey];

  if (!key) {
    log.error(`API key not found. Please set ${envKey} environment variable or use --api-key=<key>`);
    log.info('\nTo set environment variable:');
    log.info(`  export ${envKey}="your-api-key-here"`);
    log.info('\nOr create a .env file in the project root:');
    log.info(`  ${envKey}=your-api-key-here`);
    process.exit(1);
  }

  return key;
}

// Generate enhancement prompts based on exercise type
function generatePrompt(exercise, question, category) {
  const isReading = category === 'bl';
  const isMath = category === 'gb';

  let context = '';
  if (isReading && exercise.text) {
    context = `TEXT:\n${exercise.text}\n\n`;
  }

  const questionText = question.question || question.item_id;
  const correctAnswer = question.options?.find(opt => opt.correct)?.text || 'Not specified';
  const allOptions = question.options?.map((opt, idx) =>
    `${String.fromCharCode(65 + idx)}. ${opt.text}${opt.correct ? ' (CORRECT)' : ''}`
  ).join('\n') || '';

  const ageGuide = {
    'groep4': '8-9 years old',
    'groep5': '9-10 years old',
    'groep6': '10-11 years old',
    'groep7': '11-12 years old',
    'groep8': '12-13 years old',
  };
  const gradeMatch = exercise.title?.match(/groep(\d)/i);
  const age = gradeMatch ? ageGuide[`groep${gradeMatch[1]}`] : '8-12 years old';

  const errorTypes = isReading
    ? 'letterlijk_gemist, inferentie_fout, vocabulaire, structuur, detail_vergeten'
    : 'rekenfout_basis, conceptfout, procedurele_fout, afleesfout, eenhedenfout';

  return `You are an expert Dutch primary education specialist creating Schema V2.0 feedback for exercises.

EXERCISE CONTEXT:
Title: ${exercise.title || 'Untitled'}
Category: ${isReading ? 'Reading Comprehension' : 'Mathematics'}
Target Age: ${age}
Skill: ${question.skill || 'Not specified'}

${context}QUESTION:
${questionText}

OPTIONS:
${allOptions}

CORRECT ANSWER: ${correctAnswer}

TASK:
Generate high-quality educational feedback following Schema V2.0 format. Return ONLY valid JSON (no markdown, no explanations).

REQUIRED OUTPUT STRUCTURE:
{
  "feedback": {
    "correct": {
      "explanation": "WHY is this answer correct? Reference specific details. Be encouraging and specific.",
      "skill_reinforcement": "What skill did the student demonstrate? Positive reinforcement."
    },
    "incorrect": {
      "by_option": {
        "A": {
          "explanation": "WHY is option A wrong? Be specific about the error.",
          "hint": "Directional hint to guide toward correct answer.",
          "misconception": "What did the student misunderstand?",
          "error_type": "One of: ${errorTypes}"
        },
        "B": { ... },
        ...
      },
      "workedExample": {
        "steps": [
          "Step 1: Clear action to take",
          "Step 2: Next specific step",
          "Step 3: How to arrive at answer",
          "Step 4: Conclusion with answer"
        ]
      }
    }
  },
  "hints": {
    "tier1_procedural": {
      "text": "${question.hint || 'WHERE to look or WHAT to do first'}",
      "reveal_percentage": 0.2,
      "type": "procedural"
    },
    "tier2_conceptual": {
      "text": "WHAT concept to think about or understand",
      "reveal_percentage": 0.5,
      "type": "conceptual"
    },
    "tier3_worked_example": {
      "text": "HOW to solve step-by-step (nearly complete solution)",
      "reveal_percentage": 0.9,
      "type": "worked_example"
    }
  }
}

CRITICAL GUIDELINES:
1. Use age-appropriate language (${age})
2. Be specific - reference the text/question directly
3. Explain WHY, not just confirm correctness
4. Positive, encouraging tone
5. For math: use KaTeX notation with $ signs: $2 + 3 = 5$
6. For reading: quote specific text passages
7. Worked example: 3-5 clear steps
8. All incorrect options must have feedback
9. Error types must match the specified list
10. Return ONLY the JSON object, nothing else

Generate the feedback now:`;
}

// Call Anthropic Claude API
async function callAnthropicAPI(prompt, apiKey, model) {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: model,
      max_tokens: 4096,
      messages: [
        {
          role: 'user',
          content: prompt,
        },
      ],
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Anthropic API error: ${response.status} ${error}`);
  }

  const data = await response.json();
  return data.content[0].text;
}

// Call OpenAI API
async function callOpenAIAPI(prompt, apiKey, model) {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: model,
      messages: [
        {
          role: 'system',
          content: 'You are an expert Dutch primary education specialist. Return only valid JSON.',
        },
        {
          role: 'user',
          content: prompt,
        },
      ],
      temperature: 0.7,
      response_format: { type: 'json_object' },
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`OpenAI API error: ${response.status} ${error}`);
  }

  const data = await response.json();
  return data.choices[0].message.content;
}

// Parse AI response and extract JSON
function parseAIResponse(response) {
  try {
    // Try direct JSON parse
    return JSON.parse(response);
  } catch (e) {
    // Try to extract JSON from markdown code blocks
    const jsonMatch = response.match(/```json\s*([\s\S]*?)\s*```/) ||
                      response.match(/```\s*([\s\S]*?)\s*```/);

    if (jsonMatch) {
      return JSON.parse(jsonMatch[1]);
    }

    // Try to find JSON object
    const objectMatch = response.match(/\{[\s\S]*\}/);
    if (objectMatch) {
      return JSON.parse(objectMatch[0]);
    }

    throw new Error('Could not parse JSON from AI response');
  }
}

// Enhance a single question
async function enhanceQuestion(exercise, question, category, config) {
  const prompt = generatePrompt(exercise, question, category);

  let response;
  if (config.provider === 'anthropic') {
    response = await callAnthropicAPI(prompt, config.apiKey, config.model);
  } else {
    response = await callOpenAIAPI(prompt, config.apiKey, config.model);
  }

  const enhancement = parseAIResponse(response);

  // Merge enhancement into question
  return {
    ...question,
    feedback: enhancement.feedback,
    hints: enhancement.hints,
  };
}

// Review interface
async function reviewQuestion(original, enhanced, exerciseTitle, questionId) {
  console.log(`\n${colors.bright}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
  console.log(`${colors.bright}Exercise: ${exerciseTitle}${colors.reset}`);
  console.log(`${colors.bright}Question: ${questionId}${colors.reset}`);
  console.log(`${colors.bright}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}\n`);

  console.log(`${colors.blue}Question:${colors.reset}`);
  console.log(original.question || original.item_id);
  console.log();

  if (enhanced.feedback?.correct) {
    console.log(`${colors.green}✓ Correct Feedback:${colors.reset}`);
    console.log(`  Explanation: ${enhanced.feedback.correct.explanation}`);
    console.log(`  Reinforcement: ${enhanced.feedback.correct.skill_reinforcement}`);
    console.log();
  }

  if (enhanced.feedback?.incorrect?.by_option) {
    console.log(`${colors.red}✗ Incorrect Feedback (sample - Option A):${colors.reset}`);
    const optionA = enhanced.feedback.incorrect.by_option.A ||
                    enhanced.feedback.incorrect.by_option['0'];
    if (optionA) {
      console.log(`  Explanation: ${optionA.explanation}`);
      console.log(`  Hint: ${optionA.hint}`);
      console.log(`  Error type: ${optionA.error_type}`);
    }
    console.log();
  }

  if (enhanced.feedback?.incorrect?.workedExample) {
    console.log(`${colors.magenta}📝 Worked Example:${colors.reset}`);
    enhanced.feedback.incorrect.workedExample.steps.forEach((step, idx) => {
      console.log(`  ${idx + 1}. ${step}`);
    });
    console.log();
  }

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise((resolve) => {
    rl.question(`${colors.yellow}Approve this enhancement? (y/n/edit/quit): ${colors.reset}`, (answer) => {
      rl.close();
      resolve(answer.trim().toLowerCase());
    });
  });
}

// Main enhancement function
async function enhanceExerciseFile(inputFile, options) {
  log.title('AI-Assisted Exercise Enhancer');

  // Update config from options
  CONFIG.provider = options.provider || CONFIG.provider;
  CONFIG.model = options.model || CONFIG.model;
  CONFIG.batchSize = parseInt(options['batch-size']) || CONFIG.batchSize;
  CONFIG.review = options['auto-approve'] ? false : (options.review !== 'false');
  CONFIG.autoApprove = options['auto-approve'] || false;
  CONFIG.apiKey = loadApiKey(CONFIG.provider, options);

  const outputFile = options.output || inputFile.replace('_TEMPLATE.json', '_AI_ENHANCED.json');

  log.info(`📂 Input:  ${inputFile}`);
  log.info(`📝 Output: ${outputFile}`);
  log.info(`🤖 Provider: ${CONFIG.provider} (${CONFIG.model})`);
  log.info(`📊 Batch size: ${CONFIG.batchSize} questions`);
  log.info(`👁️  Review mode: ${CONFIG.review ? 'enabled' : 'disabled (auto-approve)'}`);
  console.log();

  // Read input file
  log.step('Reading template file');
  const data = JSON.parse(fs.readFileSync(inputFile, 'utf-8'));
  const category = inputFile.includes('/bl/') ? 'bl' : 'gb';

  const totalQuestions = data.exercises.reduce((sum, ex) => sum + (ex.questions?.length || 0), 0);
  log.success(`Loaded ${data.exercises.length} exercises with ${totalQuestions} questions`);
  console.log();

  // Track progress
  let enhanced = 0;
  let approved = 0;
  let edited = 0;
  let skipped = 0;

  // Enhance exercises
  for (const exercise of data.exercises) {
    if (!exercise.questions || exercise.questions.length === 0) {
      continue;
    }

    log.highlight(`\nProcessing: ${exercise.title || 'Untitled Exercise'} (${exercise.questions.length} questions)`);

    for (let i = 0; i < exercise.questions.length; i++) {
      const question = exercise.questions[i];
      const questionId = question.item_id || question.question || `Q${i + 1}`;

      // Skip if already enhanced (no TODOs)
      const hasEnhancement = question.feedback &&
                            question.feedback.correct &&
                            !JSON.stringify(question.feedback).includes('TODO');

      if (hasEnhancement) {
        log.warning(`  Skipping ${questionId} - already enhanced`);
        skipped++;
        continue;
      }

      try {
        log.step(`  Enhancing ${questionId} (${enhanced + 1}/${totalQuestions})`);

        const enhancedQuestion = await enhanceQuestion(exercise, question, category, CONFIG);

        // Review if enabled
        if (CONFIG.review) {
          const decision = await reviewQuestion(
            question,
            enhancedQuestion,
            exercise.title,
            questionId
          );

          if (decision === 'y' || decision === 'yes') {
            exercise.questions[i] = enhancedQuestion;
            approved++;
            log.success(`  ✓ Approved ${questionId}`);
          } else if (decision === 'edit' || decision === 'e') {
            log.info(`  ✏️  Edit mode: Enhancement saved for manual editing`);
            exercise.questions[i] = enhancedQuestion;
            edited++;
          } else if (decision === 'quit' || decision === 'q') {
            log.warning('\nEnhancement interrupted by user. Saving progress...');
            break;
          } else {
            log.warning(`  ✗ Skipped ${questionId}`);
            skipped++;
          }
        } else {
          // Auto-approve
          exercise.questions[i] = enhancedQuestion;
          approved++;
          log.success(`  ✓ Auto-approved ${questionId}`);
        }

        enhanced++;

        // Rate limiting: small delay between requests
        await new Promise(resolve => setTimeout(resolve, 1000));

      } catch (error) {
        log.error(`  Failed to enhance ${questionId}: ${error.message}`);
        skipped++;
      }
    }
  }

  // Save output
  log.step('\nSaving enhanced file');

  // Update metadata
  if (!data.metadata) {
    data.metadata = {};
  }
  data.metadata.schema_version = '2.0.0';
  data.metadata.enhanced = true;
  data.metadata.ai_enhanced = true;
  data.metadata.ai_provider = CONFIG.provider;
  data.metadata.ai_model = CONFIG.model;
  data.metadata.enhanced_date = new Date().toISOString();

  fs.writeFileSync(outputFile, JSON.stringify(data, null, 2), 'utf-8');
  log.success(`Saved to: ${outputFile}`);

  // Summary
  console.log();
  log.title('Enhancement Summary');
  console.log(`  Total questions:     ${totalQuestions}`);
  console.log(`  Enhanced:            ${enhanced}`);
  console.log(`  Approved:            ${approved}`);
  console.log(`  Edited (review):     ${edited}`);
  console.log(`  Skipped:             ${skipped}`);
  console.log(`  Success rate:        ${((approved / enhanced) * 100).toFixed(1)}%`);
  console.log();

  log.success('✨ AI enhancement complete!');
  console.log();
  log.info('Next steps:');
  log.info(`  1. Review the enhanced file: ${outputFile}`);
  log.info(`  2. Test in the browser`);
  log.info(`  3. Run validator: node scripts/schema-validator-v2.js`);
  log.info(`  4. Replace template with enhanced version if satisfied`);
}

// Main
(async () => {
  try {
    const { inputFile, options } = parseArgs();

    if (!inputFile) {
      log.error('No input file specified. Use --help for usage information.');
      process.exit(1);
    }

    if (!fs.existsSync(inputFile)) {
      log.error(`File not found: ${inputFile}`);
      process.exit(1);
    }

    await enhanceExerciseFile(inputFile, options);
  } catch (error) {
    log.error(`Fatal error: ${error.message}`);
    console.error(error);
    process.exit(1);
  }
})();
