/**
 * Transformer for WS (Woordenschat) exercises
 *
 * Input: Array of vocabulary questions
 * Output: { core, support }
 */

function transformWS(data, filename) {
  if (!Array.isArray(data)) {
    data = [data];
  }

  const baseId = filename.replace('.json', '');

  const core = {
    schema_version: "2.0.0",
    metadata: {
      id: baseId,
      type: "multiple_choice",
      category: "ws",
      grade: extractGrade(filename),
      level: extractLevel(filename),
      language: "nl-NL",
    },
    display: {
      title: `Woordenschat Groep ${extractGrade(filename)}`,
    },
    items: [],
    settings: {
      allow_review: true,
    },
  };

  const support = {
    schema_version: "2.0.0",
    exercise_id: baseId,
    items: [],
  };

  // Process items
  data.forEach(item => {
    // Add to core
    const coreItem = {
      id: item.id,
      type: "multiple_choice",
      theme: item.theme || "",
      question: {
        text: item.question || "",
      },
      options: (item.options || []).map(opt => ({
        text: opt,
      })),
      answer: {
        type: "single",
        correct_index: item.correct ?? 0,
      },
    };

    core.items.push(coreItem);

    // Add to support
    const supportItem = {
      item_id: item.id,
    };

    if (item.extra_info) {
      supportItem.feedback = {
        explanation: item.extra_info,
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

module.exports = transformWS;
