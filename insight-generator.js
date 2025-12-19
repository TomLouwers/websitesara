/**
 * InsightGenerator - Generates ONE single learning insight from quiz data
 * Following the "ONE Insight" pedagogical principle:
 * - Merges all explanations into a single sentence
 * - Subject-aware formatting
 * - Growth mindset, jij-vorm
 * - Special handling for verhaaltjessommen (story problems)
 */

class InsightGenerator {
  /**
   * Detects subject type from extra_info content
   * @param {object|string} extraInfo - The extra_info field from quiz data
   * @returns {string} - 'math', 'spelling', 'vocabulary', 'verhaaltjessommen', 'general'
   */
  static detectSubject(extraInfo, question = {}) {
    // Check for verhaaltjessommen indicators
    const hasLova = question.lova && Object.keys(question.lova).length > 0;
    const hasFoutanalyse = question.options?.some(opt => opt.foutanalyse);

    if (hasLova || hasFoutanalyse) {
      return 'verhaaltjessommen';
    }

    if (!extraInfo) return 'general';

    // For objects, check specific keys first (more reliable than text search)
    if (typeof extraInfo === 'object') {
      // Vocabulary: has betekenis field
      if (extraInfo.betekenis) {
        return 'vocabulary';
      }

      // Spelling: has regel, voorbeelden/examples, or spelling-specific fields
      if (extraInfo.regel || extraInfo.voorbeelden || extraInfo.examples) {
        return 'spelling';
      }

      // Math/Getal & Bewerking: has steps, tips (plural), berekening
      if (extraInfo.steps || extraInfo.berekening || extraInfo.verhoudingstabel) {
        return 'math';
      }

      // Getal & Bewerking: specifically has tips array
      if (extraInfo.tips && Array.isArray(extraInfo.tips)) {
        return 'math';
      }
    }

    // Fallback to text-based detection
    const infoStr = typeof extraInfo === 'string'
      ? extraInfo
      : JSON.stringify(extraInfo).toLowerCase();

    // Math indicators (numbers, operators, calculations)
    if (infoStr.match(/\d+|bewerking|rekenen|delen|vermenigvuldig|optellen|aftrekken|breuk|procent|verhoudingstabel|berekening/)) {
      return 'math';
    }

    // Spelling indicators (but not "tips" - that's math)
    if (infoStr.match(/\bregel\b|medeklinker|klinker|werkwoord|voltooid|verleden tijd|lettergreep|spelling|voorbeelden/)) {
      return 'spelling';
    }

    // Vocabulary indicators
    if (infoStr.match(/betekenis|definitie|synoniem|antoniem/)) {
      return 'vocabulary';
    }

    return 'general';
  }

  /**
   * Extracts the first sentence from a text
   * @param {string} text - Input text
   * @returns {string} - First sentence
   */
  static extractFirstSentence(text) {
    if (!text) return '';

    // Remove markdown and formatting
    const clean = text.replace(/[*_#]/g, '').trim();

    // Find first sentence (ending with . ! ?)
    const match = clean.match(/^[^.!?]+[.!?]/);
    return match ? match[0].trim() : clean.split('\n')[0].trim();
  }

  /**
   * Converts explanation to jij-vorm (second person, growth mindset)
   * @param {string} text - Input text
   * @returns {string} - Converted text
   */
  static toJijVorm(text) {
    if (!text) return '';

    // Common conversions
    let converted = text
      // Remove labels like A/B/C/D
      .replace(/\b[A-D][:.)\]]/g, '')
      // Convert imperatives to "jij" form where needed
      .replace(/^Let op:/i, 'Let op:')
      .replace(/^Onthoud:/i, 'Onthoud:')
      .replace(/^Tip:/i, '')
      .replace(/^💡/g, '')
      .trim();

    return converted;
  }

  /**
   * Builds ONE insight for verhaaltjessommen (story problems)
   * Weaves foutanalyse + max 1 LOVA focus into one sentence
   *
   * @param {object} selectedOption - The incorrect option that was selected
   * @param {object} question - Full question object with lova data
   * @returns {string} - ONE sentence insight
   */
  static buildVerhaaltjesomInsight(selectedOption, question) {
    // Extract foutanalyse (leading part)
    let foutanalyse = selectedOption?.foutanalyse || '';

    // Remove reflection question (🤔 Reflectievraag)
    foutanalyse = foutanalyse.split('🤔')[0].trim();

    // Extract ONE LOVA focus based on error type
    let lovaFocus = '';
    const lova = question.lova || {};

    // Priority: stap1_lezen (reading) > stap2_ordenen (organizing) > stap3_vormen (calculating)
    if (lova.stap1_lezen?.focus) {
      lovaFocus = lova.stap1_lezen.focus;
    } else if (lova.stap1_lezen?.hoofdvraag) {
      lovaFocus = `let op wat er gevraagd wordt: ${lova.stap1_lezen.hoofdvraag.toLowerCase()}`;
    } else if (lova.stap2_ordenen?.conversies && lova.stap2_ordenen.conversies.length > 0) {
      const conversie = lova.stap2_ordenen.conversies[0];
      lovaFocus = `denk aan de omrekening: ${conversie}`;
    } else if (lova.stap3_vormen?.bewerkingen && lova.stap3_vormen.bewerkingen.length > 0) {
      const bewerking = lova.stap3_vormen.bewerkingen[0];
      if (bewerking.uitleg) {
        lovaFocus = bewerking.uitleg.toLowerCase();
      }
    }

    // If we have foutanalyse, build the woven sentence
    if (foutanalyse) {
      // Clean foutanalyse
      foutanalyse = this.extractFirstSentence(foutanalyse);
      foutanalyse = this.toJijVorm(foutanalyse);

      // If we have LOVA focus, weave them together
      if (lovaFocus) {
        lovaFocus = this.toJijVorm(lovaFocus);

        // Choose connector based on context
        let connector = 'omdat';
        if (foutanalyse.toLowerCase().includes('vergat') || foutanalyse.toLowerCase().includes('vergeet')) {
          connector = 'want';
        } else if (foutanalyse.toLowerCase().includes('dan')) {
          connector = 'daardoor';
        }

        // Build woven sentence
        return `${foutanalyse} ${connector} ${lovaFocus}`;
      }

      // Only foutanalyse available
      return foutanalyse;
    }

    // Fallback: use LOVA focus alone or default
    if (lovaFocus) {
      return `Let op: ${lovaFocus}`;
    }

    return 'Let goed op wat er gevraagd wordt.';
  }

  /**
   * Builds ONE insight for general subjects (math, spelling, vocabulary, general)
   *
   * @param {object|string} extraInfo - The extra_info field
   * @param {string} subject - Subject type
   * @returns {string} - ONE sentence insight
   */
  static buildGeneralInsight(extraInfo, subject) {
    if (!extraInfo) {
      return 'Let goed op wat er gevraagd wordt.';
    }

    let insight = '';

    // Handle object vs string
    if (typeof extraInfo === 'object') {
      // Priority order based on subject type and common fields
      // 1. concept (general learning concept)
      // 2. regel (spelling rule)
      // 3. betekenis (vocabulary definition)
      // 4. tips/tip (general tips)
      // 5. voorbeelden/examples (examples)
      // 6. uitleg (explanation)
      // 7. first string value

      if (extraInfo.concept) {
        insight = extraInfo.concept;
      } else if (extraInfo.regel) {
        insight = extraInfo.regel;
      } else if (extraInfo.betekenis) {
        insight = `Betekent: ${extraInfo.betekenis}`;
      } else if (extraInfo.tips && Array.isArray(extraInfo.tips) && extraInfo.tips.length > 0) {
        insight = extraInfo.tips[0];
      } else if (extraInfo.tip) {
        insight = Array.isArray(extraInfo.tip) ? extraInfo.tip[0] : extraInfo.tip;
      } else if (extraInfo.voorbeelden && Array.isArray(extraInfo.voorbeelden) && extraInfo.voorbeelden.length > 0) {
        // For examples, take first one
        insight = extraInfo.voorbeelden[0];
      } else if (extraInfo.examples && Array.isArray(extraInfo.examples) && extraInfo.examples.length > 0) {
        insight = extraInfo.examples[0];
      } else if (extraInfo.uitleg) {
        insight = extraInfo.uitleg;
      } else if (extraInfo.steps && Array.isArray(extraInfo.steps) && extraInfo.steps.length > 0) {
        // For steps, extract learning point from first step
        const firstStep = extraInfo.steps[0];
        insight = typeof firstStep === 'string' ? firstStep : (firstStep.uitleg || firstStep.text || '');
      } else {
        // Get first string value from any field
        const firstValue = Object.values(extraInfo).find(v => typeof v === 'string' && v.length > 0);
        insight = firstValue || '';
      }
    } else {
      insight = extraInfo;
    }

    // Extract first sentence
    insight = this.extractFirstSentence(insight);

    // Convert to jij-vorm
    insight = this.toJijVorm(insight);

    // Add subject-specific prefix if needed
    if (insight && !insight.match(/^(Onthoud|Let op|Betekent|Tip):/i)) {
      switch (subject) {
        case 'math':
          insight = `Onthoud: ${insight.charAt(0).toLowerCase()}${insight.slice(1)}`;
          break;
        case 'spelling':
          insight = `Onthoud: ${insight.charAt(0).toLowerCase()}${insight.slice(1)}`;
          break;
        case 'vocabulary':
          if (!insight.toLowerCase().startsWith('betekent')) {
            insight = `Betekent: ${insight.charAt(0).toLowerCase()}${insight.slice(1)}`;
          }
          break;
        case 'general':
          insight = `Let op: ${insight.charAt(0).toLowerCase()}${insight.slice(1)}`;
          break;
      }
    }

    // Ensure it ends with a period
    if (insight && !insight.match(/[.!?]$/)) {
      insight += '.';
    }

    return insight || 'Let goed op wat er gevraagd wordt.';
  }

  /**
   * Main entry point: Generates ONE Insight for correct answers
   *
   * @param {object} question - Full question object
   * @returns {string} - ONE sentence insight
   */
  static generateCorrectInsight(question) {
    const subject = this.detectSubject(question.extra_info, question);
    const extraInfo = question.extra_info;

    if (subject === 'verhaaltjessommen') {
      // For correct verhaaltjessommen, use extra_info concept if available
      if (typeof extraInfo === 'object' && extraInfo.concept) {
        return this.buildGeneralInsight(extraInfo.concept, 'general');
      }
      return this.buildGeneralInsight(extraInfo, 'general');
    }

    return this.buildGeneralInsight(extraInfo, subject);
  }

  /**
   * Main entry point: Generates ONE Insight for incorrect answers
   *
   * @param {object} question - Full question object
   * @param {object} selectedOption - The incorrect option that was selected
   * @returns {string} - ONE sentence insight starting with "Let op: ..."
   */
  static generateIncorrectInsight(question, selectedOption) {
    const subject = this.detectSubject(question.extra_info, question);

    if (subject === 'verhaaltjessommen') {
      const insight = this.buildVerhaaltjesomInsight(selectedOption, question);

      // Check if insight already starts with an imperative verb
      const startsWithImperative = insight.match(/^(let|lees|kijk|denk|probeer|controleer|check|tel|reken)\s/i);

      // Ensure it starts with "Let op:" for incorrect answers (unless already imperative)
      if (!insight.match(/^Let op:/i) && !startsWithImperative) {
        return `Let op: ${insight.charAt(0).toLowerCase()}${insight.slice(1)}`;
      }
      return insight;
    }

    // For other subjects, build from extra_info and prefix with "Let op:"
    let insight = this.buildGeneralInsight(question.extra_info, subject);

    // Remove existing prefixes and add "Let op:"
    insight = insight.replace(/^(Onthoud|Betekent|Tip):\s*/i, '');

    // Check if insight already starts with an imperative verb (let, lees, kijk, denk, etc.)
    const startsWithImperative = insight.match(/^(let|lees|kijk|denk|probeer|controleer|check)\s/i);

    if (!insight.match(/^Let op:/i) && !startsWithImperative) {
      insight = `Let op: ${insight.charAt(0).toLowerCase()}${insight.slice(1)}`;
    }

    return insight;
  }

  /**
   * Builds the confirmation text for feedback
   *
   * @param {object} question - Full question object
   * @param {number} correctIndex - Index of correct answer
   * @param {boolean} isCorrect - Whether user answered correctly
   * @returns {string} - Confirmation text
   */
  static buildConfirmation(question, correctIndex, isCorrect) {
    const correctOption = question.options[correctIndex];
    // Handle both string format (old) and object format (new) options
    const correctText = typeof correctOption === 'string'
      ? correctOption
      : (correctOption?.text || '');

    if (isCorrect) {
      return `Dit klopt: ${correctText}`;
    }

    // For incorrect answers on verhaaltjessommen, add calculation if available
    const subject = this.detectSubject(question.extra_info, question);

    if (subject === 'verhaaltjessommen') {
      // Try to extract ONE bare calculation from lova.stap3_vormen
      const lova = question.lova || {};
      if (lova.stap3_vormen?.bewerkingen && lova.stap3_vormen.bewerkingen.length > 0) {
        const bewerkingen = lova.stap3_vormen.bewerkingen;

        // Build bare calculation (e.g., "5.345 + 2.875 + 1.000")
        const berekeningSom = bewerkingen
          .map(b => b.berekening)
          .filter(Boolean)
          .join(' → ');

        if (berekeningSom && berekeningSom.length < 60) {
          return `Het juiste antwoord is: ${correctText} (${berekeningSom})`;
        }
      }
    }

    return `Het juiste antwoord is: ${correctText}`;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = InsightGenerator;
}
