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

  // BL files contain arrays of multiple reading comprehension exercises
  // We'll keep all exercises together in one core/support file pair

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
      title: `Begrijpend Lezen Groep ${extractGrade(filename)} ${extractLevel(filename)}`,
      theme: "Diverse thema's",
    },
    exercises: [],
    settings: {
      allow_review: true,
    },
  };

  // Build support data
  const support = {
    schema_version: "2.0.0",
    exercise_id: baseId,
    exercises: [],
  };

  // Process all exercises in the array
  data.forEach((exercise, exerciseIndex) => {
    // Build core exercise
    const coreExercise = {
      id: exercise.id || (exerciseIndex + 1),
      title: exercise.title || "",
      theme: exercise.theme || "",
      content: {
        text: exercise.text || "",
        text_type: exercise.text_type || "verhalend",
      },
      items: [],
    };

    // Add word/sentence count if available
    if (exercise.metadata) {
      coreExercise.content.word_count = exercise.metadata.word_count;
      coreExercise.content.sentence_count = exercise.metadata.sentence_count;
    }

    // Build support exercise
    const supportExercise = {
      id: exercise.id || (exerciseIndex + 1),
      items: [],
    };

    // Process questions for this exercise
    const questions = exercise.questions || [];

    questions.forEach((q, index) => {
      // Add to core
      const coreItem = {
        id: q.item_id || `${exercise.id || (exerciseIndex + 1)}${String.fromCharCode(97 + index)}`,
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

      coreExercise.items.push(coreItem);

      // Add to support
      const supportItem = {
        item_id: q.item_id || `${exercise.id || (exerciseIndex + 1)}${String.fromCharCode(97 + index)}`,
      };

      if (q.hint) {
        supportItem.hint = q.hint;
      }

      if (q.skill) {
        supportItem.learning = { skill: q.skill };
      }

      supportExercise.items.push(supportItem);
    });

    core.exercises.push(coreExercise);
    support.exercises.push(supportExercise);
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
