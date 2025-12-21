/**
 * Transformer for GB (Basisvaardigheden) exercises
 *
 * Input: Array of math/basic skills questions
 * Output: { core, support }
 */

function transformGB(data, filename) {
  if (!Array.isArray(data)) {
    data = [data];
  }

  const baseId = filename.replace('.json', '');

  const core = {
    schema_version: "2.0.0",
    metadata: {
      id: baseId,
      type: "multiple_choice",
      category: "gb",
      grade: extractGrade(filename),
      level: extractLevel(filename),
      language: "nl-NL",
    },
    display: {
      title: `Basisvaardigheden Groep ${extractGrade(filename)}`,
    },
    content: {
      instruction: "Bereken:",
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
        text: item.questions?.[0]?.question || item.title || "",
      },
      options: (item.questions?.[0]?.options || []).map(opt => ({
        text: opt,
      })),
      answer: {
        type: "single",
        correct_index: item.questions?.[0]?.correct ?? 0,
      },
    };

    core.items.push(coreItem);

    // Add to support
    const supportItem = {
      item_id: item.id,
    };

    const extraInfo = item.questions?.[0]?.extra_info;
    if (extraInfo) {
      if (typeof extraInfo === 'string') {
        supportItem.feedback = { explanation: extraInfo };
      } else if (extraInfo.tips) {
        supportItem.learning = { tips: extraInfo.tips };
      }
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

module.exports = transformGB;
