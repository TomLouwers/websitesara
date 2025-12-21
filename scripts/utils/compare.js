/**
 * Compare source and transformed data to ensure no data loss
 */

/**
 * Compare original and transformed data
 */
function compareData(source, core, support, category) {
  const warnings = [];

  // Convert source to array if needed
  const sourceArray = Array.isArray(source) ? source : [source];

  // Category-specific comparisons
  switch (category) {
    case 'bl':
      return compareBL(sourceArray, core, support, warnings);
    case 'gb':
      return compareGB(sourceArray, core, support, warnings);
    case 'wo':
    case 'ws':
      return compareWOWS(sourceArray, core, support, warnings);
    case 'sp':
      return compareSP(source, core, support, warnings);
    case 'tl':
      return compareTL(source, core, support, warnings);
    default:
      warnings.push('Unknown category, skipping comparison');
  }

  return {
    valid: warnings.length === 0,
    warnings,
  };
}

/**
 * Compare BL data
 */
function compareBL(source, core, support, warnings) {
  const sourceExercise = source[0];

  if (!sourceExercise) {
    warnings.push('No source exercise found');
    return { valid: false, warnings };
  }

  const sourceQuestions = sourceExercise.questions || [];
  const coreItems = core.items || [];

  if (sourceQuestions.length !== coreItems.length) {
    warnings.push(`Question count mismatch: ${sourceQuestions.length} -> ${coreItems.length}`);
  }

  // Check each question
  sourceQuestions.forEach((sourceQ, index) => {
    const coreItem = coreItems[index];
    if (!coreItem) {
      warnings.push(`Missing core item ${index}`);
      return;
    }

    const sourceOptions = sourceQ.options || [];
    const coreOptions = coreItem.options || [];

    if (sourceOptions.length !== coreOptions.length) {
      warnings.push(`Item ${index}: option count mismatch`);
    }
  });

  return { valid: warnings.length === 0, warnings };
}

/**
 * Compare GB data
 */
function compareGB(source, core, support, warnings) {
  if (source.length !== core.items.length) {
    warnings.push(`Item count mismatch: ${source.length} -> ${core.items.length}`);
  }

  return { valid: warnings.length === 0, warnings };
}

/**
 * Compare WO/WS data
 */
function compareWOWS(source, core, support, warnings) {
  if (source.length !== core.items.length) {
    warnings.push(`Item count mismatch: ${source.length} -> ${core.items.length}`);
  }

  return { valid: warnings.length === 0, warnings };
}

/**
 * Compare SP data
 */
function compareSP(source, core, support, warnings) {
  const sourceItems = source.items || [];
  const coreItems = core.items || [];

  if (sourceItems.length !== coreItems.length) {
    warnings.push(`Item count mismatch: ${sourceItems.length} -> ${coreItems.length}`);
  }

  return { valid: warnings.length === 0, warnings };
}

/**
 * Compare TL data
 */
function compareTL(source, core, support, warnings) {
  const sourceWords = source.list?.words || [];
  const coreItems = core.items || [];

  if (sourceWords.length !== coreItems.length) {
    warnings.push(`Word count mismatch: ${sourceWords.length} -> ${coreItems.length}`);
  }

  return { valid: warnings.length === 0, warnings };
}

module.exports = {
  compareData,
};
