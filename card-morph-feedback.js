/**
 * CardMorphFeedback - Morphs question card into feedback state
 *
 * Design Principles:
 * - Card stays in place (spatial continuity)
 * - 3D flip animation (max 250ms)
 * - ONE Insight as visual center
 * - Anti-skip gate for incorrect answers (1500ms)
 */

class CardMorphFeedback {
  constructor() {
    this.feedbackState = null; // 'correct' or 'incorrect'
    this.antiSkipTimer = null;
    this.canProceed = false;
    this.originalCardHTML = null; // Store original HTML to restore later
  }

  /**
   * Morphs the question card into feedback state
   *
   * @param {object} params - Configuration object
   * @param {boolean} params.isCorrect - Whether answer was correct
   * @param {string} params.insight - The ONE Insight sentence
   * @param {string} params.confirmation - Answer confirmation text
   * @param {HTMLElement} params.questionCard - The question card element to morph
   * @param {HTMLElement} params.nextButton - The "Volgende" button
   * @param {Function} params.onProceed - Callback when user can proceed
   */
  morph({ isCorrect, insight, confirmation, questionCard, nextButton, onProceed }) {
    this.feedbackState = isCorrect ? 'correct' : 'incorrect';
    this.canProceed = isCorrect; // Correct answers can proceed immediately

    // Store original HTML if not already stored
    if (!this.originalCardHTML) {
      this.originalCardHTML = questionCard.innerHTML;
    }

    // Step 1: Add flip-out animation class
    questionCard.classList.add('card-flip-out');

    // Step 2: After 125ms (half of 250ms), swap content
    setTimeout(() => {
      this.renderFeedbackContent(questionCard, {
        isCorrect,
        insight,
        confirmation
      });

      // Add flip-in animation
      questionCard.classList.remove('card-flip-out');
      questionCard.classList.add('card-flip-in');

      // Step 3: Clean up animation classes after completion
      setTimeout(() => {
        questionCard.classList.remove('card-flip-in');
      }, 125);

    }, 125);

    // Step 4: Handle next button
    this.setupNextButton(nextButton, isCorrect, onProceed);
  }

  /**
   * Renders feedback content inside the card
   *
   * @param {HTMLElement} card - The card element
   * @param {object} content - Feedback content
   */
  renderFeedbackContent(card, { isCorrect, insight, confirmation }) {
    const stateClass = isCorrect ? 'feedback-correct' : 'feedback-incorrect';
    const emoji = isCorrect ? '✓' : '👀';
    const header = isCorrect ? 'Top gedaan!' : 'Kijk even mee 👇';
    const bgColor = isCorrect ? '#E8F5E9' : '#FFF3E0';

    card.innerHTML = `
      <div class="feedback-morph-container ${stateClass}" style="background-color: ${bgColor};">
        <!-- Header -->
        <div class="feedback-morph-header">
          <span class="feedback-morph-emoji">${emoji}</span>
          <h3 class="feedback-morph-title">${header}</h3>
        </div>

        <!-- ONE Insight (Visual Center) -->
        <div class="feedback-morph-insight">
          <p class="feedback-morph-insight-text">${insight}</p>
        </div>

        <!-- Confirmation -->
        <div class="feedback-morph-confirmation">
          <p class="feedback-morph-confirmation-text">${confirmation}</p>
        </div>
      </div>
    `;
  }

  /**
   * Sets up the next button with anti-skip logic
   *
   * @param {HTMLElement} button - The next button element
   * @param {boolean} isCorrect - Whether answer was correct
   * @param {Function} onProceed - Callback when user can proceed
   */
  setupNextButton(button, isCorrect, onProceed) {
    if (!button) return;

    if (isCorrect) {
      // Correct: enable immediately
      this.enableNextButton(button, onProceed);
    } else {
      // Incorrect: disable for 1500ms
      this.disableNextButton(button);

      // Add helper text
      const helperText = document.createElement('p');
      helperText.className = 'feedback-anti-skip-helper';
      helperText.textContent = 'Lees dit even…';
      helperText.style.cssText = `
        font-size: 0.875rem;
        color: #666;
        text-align: center;
        margin-top: 0.5rem;
        opacity: 1;
        transition: opacity 0.3s ease;
      `;

      // Insert helper text after button
      button.parentNode.insertBefore(helperText, button.nextSibling);

      // Set timer
      this.antiSkipTimer = setTimeout(() => {
        this.canProceed = true;

        // Fade out helper text
        helperText.style.opacity = '0';
        setTimeout(() => {
          if (helperText.parentNode) {
            helperText.parentNode.removeChild(helperText);
          }
        }, 300);

        // Enable button with fade-in
        this.enableNextButton(button, onProceed);
      }, 1500);
    }
  }

  /**
   * Disables the next button
   *
   * @param {HTMLElement} button - The next button element
   */
  disableNextButton(button) {
    button.disabled = true;
    button.style.opacity = '0.4';
    button.style.cursor = 'not-allowed';
    button.style.transition = 'opacity 0.3s ease';
  }

  /**
   * Enables the next button with fade-in
   *
   * @param {HTMLElement} button - The next button element
   * @param {Function} onProceed - Callback when clicked
   */
  enableNextButton(button, onProceed) {
    button.disabled = false;
    button.style.opacity = '1';
    button.style.cursor = 'pointer';

    // Set up click handler
    button.onclick = () => {
      if (this.canProceed) {
        this.reset();
        if (onProceed) onProceed();
      }
    };
  }

  /**
   * Resets the feedback state and restores original card HTML
   * @param {HTMLElement} questionCard - The question card element to restore
   */
  reset(questionCard) {
    if (this.antiSkipTimer) {
      clearTimeout(this.antiSkipTimer);
      this.antiSkipTimer = null;
    }

    // Remove any helper text elements
    const helperTexts = document.querySelectorAll('.feedback-anti-skip-helper');
    helperTexts.forEach(helper => {
      if (helper.parentNode) {
        helper.parentNode.removeChild(helper);
      }
    });

    // Restore original HTML if we have it and a card element
    if (this.originalCardHTML && questionCard) {
      // Restore original question HTML immediately (no animation on reset)
      questionCard.innerHTML = this.originalCardHTML;

      // Remove any animation classes
      questionCard.classList.remove('card-flip-out', 'card-flip-in');

      // Clear stored HTML so next question's structure can be captured
      this.originalCardHTML = null;
    }

    this.canProceed = false;
    this.feedbackState = null;
  }

  /**
   * Cancels any active anti-skip timer (e.g., when user navigates away)
   */
  cancel() {
    this.reset();
  }
}

/**
 * CardMorphFeedback CSS Styles
 * To be added to quiz.html or loaded separately
 */
const CARD_MORPH_STYLES = `
/* Card flip animation */
.card-flip-out {
  animation: flipOut 125ms ease-in forwards;
}

.card-flip-in {
  animation: flipIn 125ms ease-out forwards;
}

@keyframes flipOut {
  from {
    transform: rotateY(0deg);
    opacity: 1;
  }
  to {
    transform: rotateY(90deg);
    opacity: 0;
  }
}

@keyframes flipIn {
  from {
    transform: rotateY(-90deg);
    opacity: 0;
  }
  to {
    transform: rotateY(0deg);
    opacity: 1;
  }
}

/* Feedback morph container */
.feedback-morph-container {
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
}

.feedback-morph-container.feedback-correct {
  border: 2px solid #81C784;
}

.feedback-morph-container.feedback-incorrect {
  border: 2px solid #FFB74D;
}

/* Header */
.feedback-morph-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.feedback-morph-emoji {
  font-size: 2rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  background: white;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.feedback-morph-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
}

/* ONE Insight (Visual Center) */
.feedback-morph-insight {
  margin: 2rem 0;
  padding: 1.5rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  border-left: 4px solid #3498db;
}

.feedback-morph-insight-text {
  margin: 0;
  font-size: 1.125rem;
  line-height: 1.6;
  color: #2c3e50;
  font-weight: 500;
}

/* Confirmation */
.feedback-morph-confirmation {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 6px;
}

.feedback-morph-confirmation-text {
  margin: 0;
  font-size: 1rem;
  line-height: 1.5;
  color: #555;
}

/* Anti-skip helper text */
.feedback-anti-skip-helper {
  font-size: 0.875rem;
  color: #666;
  text-align: center;
  margin-top: 0.5rem;
  font-style: italic;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .feedback-morph-container {
    padding: 1.5rem;
  }

  .feedback-morph-title {
    font-size: 1.25rem;
  }

  .feedback-morph-insight-text {
    font-size: 1rem;
  }

  .feedback-morph-emoji {
    font-size: 1.5rem;
    width: 2rem;
    height: 2rem;
  }
}
`;

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { CardMorphFeedback, CARD_MORPH_STYLES };
}
