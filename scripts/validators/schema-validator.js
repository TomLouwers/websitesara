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
    if (data.metadata.grade === undefined) errors.push('Missing metadata.grade');
  }

  if (!data.items || !Array.isArray(data.items)) {
    errors.push('Missing or invalid items array');
  } else if (data.items.length === 0) {
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

  if (!data.items || !Array.isArray(data.items)) {
    errors.push('Missing or invalid items array');
  } else {
    // Validate each item has item_id
    data.items.forEach((item, index) => {
      if (!item.item_id) {
        errors.push(`Support item ${index}: missing item_id`);
      }
    });
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
