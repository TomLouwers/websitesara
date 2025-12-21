/**
 * Transformer for BL (Begrijpend Lezen) exercises
 *
 * Input: Array of exercises with nested questions
 * Output: { core, support }
 */

function transformBL(data, filename) {
  // BL files are arrays of exercises
  if (!Array.isArray(data)) {
    data = [data];
  }

  // Extract ID from filename: bl_groep4_m4_1.json -> bl_groep4_m4_1
  const baseId = filename.replace('.json', '');

  // For simplicity, we'll process the first exercise
  // In production, you might want to split multi-exercise files
  const exercise = data[0];

  if (!exercise) {
    throw new Error('No exercise data found');
  }

  // Build core data
  const core = {
    schema_version: "2.0.0",
    metadata: {
      id: baseId,
      type: "reading_comprehension",
      category: "bl",
      grade: extractGrade(filename),
      level: extractLevel(filename),
      language: "nl-NL",
    },
    display: {
      title: exercise.title || "Begrijpend Lezen",
      theme: exercise.theme || "",
    },
    content: {
      text: exercise.text || "",
      text_type: exercise.text_type || "verhalend",
    },
    items: [],
    settings: {
      allow_review: true,
    },
  };

  // Add word/sentence count if available
  if (exercise.metadata) {
    core.content.word_count = exercise.metadata.word_count;
    core.content.sentence_count = exercise.metadata.sentence_count;
  }

  // Build support data
  const support = {
    schema_version: "2.0.0",
    exercise_id: baseId,
    items: [],
  };

  // Process questions
  const questions = exercise.questions || [];

  questions.forEach((q, index) => {
    // Add to core
    const coreItem = {
      id: q.item_id || `${index + 1}`,
      type: "multiple_choice",
      question: {
        text: q.question || "",
      },
      options: (q.options || []).map(opt => ({
        label: opt.label || "",
        text: opt.text || "",
      })),
      answer: {
        type: "single",
        correct_index: findCorrectIndex(q.options || []),
      },
    };

    core.items.push(coreItem);

    // Add to support
    const supportItem = {
      item_id: q.item_id || `${index + 1}`,
    };

    if (q.hint) {
      supportItem.hint = q.hint;
    }

    if (q.skill) {
      supportItem.learning = { skill: q.skill };
    }

    support.items.push(supportItem);
  });

  return { core, support };
}

/**
 * Find the index of the correct answer
 */
function findCorrectIndex(options) {
  const index = options.findIndex(opt => opt.is_correct === true);
  return index >= 0 ? index : 0;
}

/**
 * Extract grade from filename (e.g., bl_groep4_m4_1.json -> 4)
 */
function extractGrade(filename) {
  const match = filename.match(/groep(\d)/);
  return match ? parseInt(match[1], 10) : 4;
}

/**
 * Extract level from filename (e.g., bl_groep4_m4_1.json -> M4)
 */
function extractLevel(filename) {
  const match = filename.match(/([em])(\d)/i);
  return match ? match[1].toUpperCase() + match[2] : "";
}

module.exports = transformBL;
