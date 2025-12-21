/**
 * Transformer for TL (Technisch Lezen) exercises
 *
 * Input: Object with word list configuration
 * Output: { core, support }
 */

function transformTL(data, filename) {
  const baseId = filename.replace('.json', '');

  const core = {
    schema_version: "2.0.0",
    metadata: {
      id: baseId,
      type: "word_list",
      category: "tl",
      grade: extractGrade(filename),
      language: data.language || "nl-NL",
    },
    display: {
      title: data.list?.list_id ? `DMT Lijst ${data.list.list_id.toUpperCase()}` : "Technisch Lezen",
      difficulty: data.list?.difficulty || "medium",
    },
    content: {
      instruction: "Lees de woorden zo snel en goed mogelijk.",
    },
    items: [],
    settings: {
      time_limit_seconds: data.list?.time_limit_seconds || 60,
      show_timer: true,
    },
  };

  const support = {
    schema_version: "2.0.0",
    exercise_id: baseId,
    items: [],
  };

  // Process words
  const words = data.list?.words || [];

  words.forEach(wordItem => {
    // Add to core
    const coreItem = {
      id: wordItem.id,
      type: "text_input",
      question: {
        text: wordItem.word,
      },
      answer: {
        type: "text",
        correct_value: wordItem.word,
      },
    };

    core.items.push(coreItem);

    // Support items are minimal for TL
    support.items.push({
      item_id: wordItem.id,
    });
  });

  return { core, support };
}

function extractGrade(filename) {
  const match = filename.match(/groep(\d)/);
  return match ? parseInt(match[1], 10) : 4;
}

module.exports = transformTL;
