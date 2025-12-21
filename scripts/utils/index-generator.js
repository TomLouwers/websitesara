/**
 * Generate exercise index from migrated files
 */

const fs = require('fs');
const path = require('path');

/**
 * Generate index.json from all core files
 */
async function generateIndex(exercisesDir) {
  const categories = ['bl', 'gb', 'wo', 'ws', 'sp', 'tl'];
  const exercises = [];

  for (const category of categories) {
    const categoryDir = path.join(exercisesDir, category);

    if (!fs.existsSync(categoryDir)) {
      continue;
    }

    const files = fs.readdirSync(categoryDir)
      .filter(file => file.endsWith('_core.json'));

    for (const file of files) {
      const filePath = path.join(categoryDir, file);
      const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

      const baseName = file.replace('_core.json', '');
      const supportPath = path.join(categoryDir, `${baseName}_support.json`);
      const hasSupport = fs.existsSync(supportPath);

      exercises.push({
        id: data.metadata.id,
        category: data.metadata.category,
        type: data.metadata.type,
        title: data.display.title,
        theme: data.display.theme || "",
        grade: data.metadata.grade,
        level: data.metadata.level || "",
        difficulty: data.display.difficulty || "medium",
        tags: data.display.tags || [],
        stats: {
          item_count: data.items?.length || 0,
          estimated_duration_seconds: estimateDuration(data),
        },
        features: {
          has_audio: hasAudio(data),
          has_hints: hasSupport,
          has_reading_text: !!(data.content?.text),
        },
        paths: {
          core: `${category}/${baseName}_core.json`,
          support: hasSupport ? `${category}/${baseName}_support.json` : undefined,
        },
      });
    }
  }

  return {
    schema_version: "2.0.0",
    generated_at: new Date().toISOString(),
    total_exercises: exercises.length,
    exercises,
    filters: {
      grades: [3, 4, 5, 6, 7, 8],
      categories: [
        { id: "bl", name: "Begrijpend Lezen" },
        { id: "gb", name: "Basisvaardigheden" },
        { id: "wo", name: "Wereldoriëntatie" },
        { id: "ws", name: "Woordenschat" },
        { id: "sp", name: "Spelling" },
        { id: "tl", name: "Technisch Lezen" },
      ],
    },
  };
}

/**
 * Estimate exercise duration based on type and item count
 */
function estimateDuration(data) {
  const itemCount = data.items?.length || 0;
  const type = data.metadata.type;

  const secondsPerItem = {
    reading_comprehension: 45, // BL takes longer
    audio_dictation: 30,        // SP has audio playback
    word_list: 1,               // TL is timed reading
    multiple_choice: 20,        // Standard questions
  };

  const baseTime = secondsPerItem[type] || 20;

  // Add reading time for BL
  if (type === 'reading_comprehension' && data.content?.word_count) {
    const readingTime = Math.ceil(data.content.word_count / 3); // ~180 words/min
    return readingTime + (itemCount * baseTime);
  }

  return itemCount * baseTime;
}

/**
 * Check if exercise has audio
 */
function hasAudio(data) {
  return data.items?.some(item => item.audio) || false;
}

module.exports = {
  generateIndex,
};
