/**
 * Transformer for SP (Spelling) exercises
 *
 * Input: Object with set config and items array
 * Output: { core, support }
 */

function transformSP(data, filename) {
  const baseId = filename.replace('.json', '');

  const core = {
    schema_version: "2.0.0",
    metadata: {
      id: baseId,
      type: "audio_dictation",
      category: "sp",
      grade: data.set?.grade || extractGrade(filename),
      level: data.set?.level || extractLevel(filename),
      language: "nl-NL",
    },
    display: {
      title: `Spelling Dictee Groep ${data.set?.grade || extractGrade(filename)}`,
    },
    items: [],
    settings: {
      allow_skip: false,
    },
  };

  const support = {
    schema_version: "2.0.0",
    exercise_id: baseId,
    feedback: {},
    items: [],
  };

  // Add global feedback templates if available
  if (data.set?.feedback_templates) {
    support.feedback.templates = {
      correct: data.set.feedback_templates.correct,
      incorrect: data.set.feedback_templates.incorrect,
    };
  }

  // Process items
  const items = data.items || [];

  items.forEach(item => {
    // Add to core
    const coreItem = {
      id: item.id,
      type: "text_input",
      theme: item.tags?.[0] || "",
      question: {
        text: item.prompt?.instruction || "Luister en schrijf op:",
      },
      answer: {
        type: "text",
        correct_value: item.target?.answer || "",
        accepted_values: item.target?.accept || [item.target?.answer],
        case_sensitive: data.set?.flags?.case_sensitive ?? false,
        trim_whitespace: data.set?.flags?.trim ?? true,
      },
    };

    // Add audio paths
    if (item.audio) {
      coreItem.audio = {
        sentence: item.audio.sentence,
        instruction: item.audio.instruction,
      };
    }

    core.items.push(coreItem);

    // Add to support
    const supportItem = {
      item_id: item.id,
    };

    // Add tips if available
    if (item.feedback?.tips) {
      supportItem.learning = {
        tips: item.feedback.tips,
      };
    }

    support.items.push(supportItem);
  });

  return { core, support };
}

function extractGrade(filename) {
  const match = filename.match(/groep(\d)/);
  return match ? parseInt(match[1], 10) : 4;
}

function extractLevel(filename) {
  const match = filename.match(/([em])(\d)/i);
  return match ? match[1].toUpperCase() + match[2] : "";
}

module.exports = transformSP;
