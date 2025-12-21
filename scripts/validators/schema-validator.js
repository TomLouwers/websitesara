/**
 * Schema validation for core and support JSON files
 */

/**
 * Validate core exercise schema
 */
function validateCore(data) {
  const errors = [];

  // Required fields
  if (!data.schema_version) {
    errors.push('Missing schema_version');
  }

  if (!data.metadata) {
    errors.push('Missing metadata');
  } else {
    if (!data.metadata.id) errors.push('Missing metadata.id');
    if (!data.metadata.type) errors.push('Missing metadata.type');
    if (!data.metadata.category) errors.push('Missing metadata.category');
    // Grade can be a single value or array (grade_levels)
    if (data.metadata.grade === undefined && !data.metadata.grade_levels) {
      errors.push('Missing metadata.grade or metadata.grade_levels');
    }
  }

  // Check for items array (simple structure) OR exercises array (BL structure)
  if (data.exercises && Array.isArray(data.exercises)) {
    // BL structure: exercises[].items[]
    if (data.exercises.length === 0) {
      errors.push('Exercises array is empty');
    } else {
      data.exercises.forEach((exercise, exIndex) => {
        if (!exercise.items || !Array.isArray(exercise.items)) {
          errors.push(`Exercise ${exIndex}: missing or invalid items array`);
        } else {
          exercise.items.forEach((item, itemIndex) => {
            if (!item.id) {
              errors.push(`Exercise ${exIndex}, Item ${itemIndex}: missing id`);
            }
            if (!item.question?.text) {
              errors.push(`Exercise ${exIndex}, Item ${itemIndex}: missing question.text`);
            }
            if (!item.answer) {
              errors.push(`Exercise ${exIndex}, Item ${itemIndex}: missing answer`);
            }
            // Multiple choice items need options
            if (item.type === 'multiple_choice' || !item.type) {
              if (!item.options || !Array.isArray(item.options)) {
                errors.push(`Exercise ${exIndex}, Item ${itemIndex}: missing or invalid options`);
              } else if (item.options.length < 2) {
                errors.push(`Exercise ${exIndex}, Item ${itemIndex}: need at least 2 options`);
              }
            }
          });
        }
      });
    }
  } else if (data.items && Array.isArray(data.items)) {
    // Simple structure: items[]
    if (data.items.length === 0) {
      errors.push('Items array is empty');
    } else {
      // Validate each item
      data.items.forEach((item, index) => {
        if (!item.id) {
          errors.push(`Item ${index}: missing id`);
        }
        if (!item.question?.text) {
          errors.push(`Item ${index}: missing question.text`);
        }
        if (!item.answer) {
          errors.push(`Item ${index}: missing answer`);
        }
        // Multiple choice items need options
        if (item.type === 'multiple_choice' || !item.type) {
          if (!item.options || !Array.isArray(item.options)) {
            errors.push(`Item ${index}: missing or invalid options`);
          } else if (item.options.length < 2) {
            errors.push(`Item ${index}: need at least 2 options`);
          }
        }
      });
    }
  } else if (data.problems && Array.isArray(data.problems)) {
    // VS structure: problems[].items[]
    if (data.problems.length === 0) {
      errors.push('Problems array is empty');
    } else {
      data.problems.forEach((problem, probIndex) => {
        if (!problem.items || !Array.isArray(problem.items)) {
          errors.push(`Problem ${probIndex}: missing or invalid items array`);
        } else {
          problem.items.forEach((item, itemIndex) => {
            if (!item.id) {
              errors.push(`Problem ${probIndex}, Item ${itemIndex}: missing id`);
            }
            if (!item.question?.text) {
              errors.push(`Problem ${probIndex}, Item ${itemIndex}: missing question.text`);
            }
            if (!item.answer) {
              errors.push(`Problem ${probIndex}, Item ${itemIndex}: missing answer`);
            }
            if (item.type === 'multiple_choice' || !item.type) {
              if (!item.options || !Array.isArray(item.options)) {
                errors.push(`Problem ${probIndex}, Item ${itemIndex}: missing or invalid options`);
              } else if (item.options.length < 2) {
                errors.push(`Problem ${probIndex}, Item ${itemIndex}: need at least 2 options`);
              }
            }
          });
        }
      });
    }
  } else {
    errors.push('Missing items, exercises, or problems array');
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Validate support exercise schema
 */
function validateSupport(data) {
  const errors = [];

  if (!data) {
    return { valid: true, errors: [] }; // Support is optional
  }

  // Required fields
  if (!data.schema_version) {
    errors.push('Missing schema_version');
  }

  if (!data.exercise_id) {
    errors.push('Missing exercise_id');
  }

  // Check for items array (simple structure) OR exercises array (BL structure)
  if (data.exercises && Array.isArray(data.exercises)) {
    // BL structure: exercises[].items[]
    data.exercises.forEach((exercise, exIndex) => {
      if (!exercise.items || !Array.isArray(exercise.items)) {
        errors.push(`Support exercise ${exIndex}: missing or invalid items array`);
      } else {
        exercise.items.forEach((item, itemIndex) => {
          if (!item.item_id) {
            errors.push(`Support exercise ${exIndex}, item ${itemIndex}: missing item_id`);
          }
        });
      }
    });
  } else if (data.items && Array.isArray(data.items)) {
    // Simple structure: items[]
    data.items.forEach((item, index) => {
      if (!item.item_id) {
        errors.push(`Support item ${index}: missing item_id`);
      }
    });
  } else if (data.problems && Array.isArray(data.problems)) {
    // VS structure: problems[].items[]
    data.problems.forEach((problem, probIndex) => {
      if (!problem.items || !Array.isArray(problem.items)) {
        errors.push(`Support problem ${probIndex}: missing or invalid items array`);
      } else {
        problem.items.forEach((item, itemIndex) => {
          if (!item.item_id) {
            errors.push(`Support problem ${probIndex}, item ${itemIndex}: missing item_id`);
          }
        });
      }
    });
  } else {
    errors.push('Missing items, exercises, or problems array');
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

module.exports = {
  validateCore,
  validateSupport,
};
