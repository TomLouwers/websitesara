/**
 * Verhaaltjessommen (Word Problems) Transformer
 * Transforms story-based math problems to v2.0 split format
 */

function transformVerhaaltjessommen(data, filePath) {
  const filename = filePath.split('/').pop();
  const baseId = 'verhaaltjessommen_cito';

  // Core file - questions and structure
  const core = {
    schema_version: "2.0.0",
    metadata: {
      id: baseId,
      type: "word_problems",
      category: "vs",
      grade_levels: [6, 7, 8],
      language: "nl",
      subjects: ["rekenen", "wiskunde"],
      difficulty: "cito_preparation",
      created_date: new Date().toISOString().split('T')[0],
      last_updated: new Date().toISOString().split('T')[0],
      version: "1.0.0",
      author: "Sara Platform",
      source: filename
    },
    display: {
      title: "Verhaaltjessommen - CITO Voorbereiding",
      description: "Realistische rekenproblemen voor CITO-toets voorbereiding",
      instructions: "Lees elke verhaaltjessom zorgvuldig en volg de LOVA-methode: Lezen, Ordenen, Vormen, Antwoorden.",
      icon: "📊",
      estimated_time_minutes: 60,
      total_items: data.length
    },
    problems: [], // Array of story problems
    settings: {
      allow_review: true,
      show_feedback_immediately: false,
      allow_hints: true,
      randomize_options: false
    }
  };

  // Support file - feedback, hints, methodology
  const support = {
    schema_version: "2.0.0",
    exercise_id: baseId,
    problems: [] // Matching structure
  };

  // Group by theme for better organization
  const themes = {};
  data.forEach(problem => {
    if (!themes[problem.theme]) {
      themes[problem.theme] = [];
    }
    themes[problem.theme].push(problem);
  });

  // Transform each problem
  data.forEach((problem, problemIndex) => {
    const coreProblem = {
      id: problem.id,
      title: problem.title,
      theme: problem.theme,
      content: {
        story: problem.content,
        context: problem.context || null,
        data_table: problem.data_table || null,
        image_url: problem.image_url || null
      },
      items: [] // Questions for this problem
    };

    const supportProblem = {
      id: problem.id,
      items: []
    };

    // Transform each question in the problem
    problem.questions.forEach((q, qIndex) => {
      const itemId = `${problem.id}_${String.fromCharCode(97 + qIndex)}`; // 1_a, 1_b, etc.

      // Find correct answer index
      const correctIndex = q.options.findIndex(opt => opt.is_correct === true);

      // Core item
      const coreItem = {
        id: itemId,
        type: "multiple_choice",
        question: {
          text: q.question
        },
        options: q.options.map((opt, optIndex) => ({
          label: String.fromCharCode(65 + optIndex), // A, B, C, D
          text: opt.text
        })),
        answer: {
          type: "single",
          correct_index: correctIndex
        }
      };

      // Support item - rich feedback
      const supportItem = {
        item_id: itemId,

        // Main hint
        hint: q.hint || null,

        // Per-option feedback
        feedback: {
          per_option: q.options.map((opt, optIndex) => {
            if (opt.is_correct) {
              return null; // No feedback for correct answer
            }
            return {
              option_index: optIndex,
              text: opt.foutanalyse || "Probeer het opnieuw.",
              error_type: opt.error_type || "unknown",
              visual_aid_query: opt.visual_aid_query || null,
              remedial_basis_id: opt.remedial_basis_id || null
            };
          }).filter(f => f !== null)
        },

        // Extra information - solution steps
        explanation: q.extra_info ? {
          concept: q.extra_info.concept || null,
          steps: q.extra_info.berekening || [],
          calculation_table: q.extra_info.berekening_tabel || null
        } : null,

        // LOVA methodology
        lova: q.lova ? {
          step1_reading: {
            noise_information: q.lova.stap1_lezen?.ruis || [],
            main_question: q.lova.stap1_lezen?.hoofdvraag || null,
            sub_steps: q.lova.stap1_lezen?.tussenstappen || []
          },
          step2_organizing: {
            relevant_numbers: q.lova.stap2_ordenen?.relevante_getallen || {},
            tool: q.lova.stap2_ordenen?.tool || null,
            conversions: q.lova.stap2_ordenen?.conversies || []
          },
          step3_forming: {
            operations: q.lova.stap3_vormen?.bewerkingen || []
          },
          step4_answering: {
            expected_unit: q.lova.stap4_antwoorden?.verwachte_eenheid || null,
            logic_check: q.lova.stap4_antwoorden?.logica_check || null,
            answer: q.lova.stap4_antwoorden?.antwoord || null
          }
        } : null,

        // Learning metadata
        learning: {
          skill: "word_problems",
          theme: problem.theme,
          error_types: q.options
            .filter(opt => !opt.is_correct && opt.error_type)
            .map(opt => opt.error_type),
          requires_multi_step: q.hint?.includes('TWEE stappen') || q.hint?.includes('meerdere stappen') || false
        }
      };

      coreProblem.items.push(coreItem);
      supportProblem.items.push(supportItem);
    });

    core.problems.push(coreProblem);
    support.problems.push(supportProblem);
  });

  // Add theme summary to metadata
  core.metadata.themes = Object.keys(themes).map(theme => ({
    name: theme,
    count: themes[theme].length
  }));

  return { core, support };
}

module.exports = { transformVerhaaltjessommen };
