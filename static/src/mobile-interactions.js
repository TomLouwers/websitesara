/**
 * MobileInteractions - Touch gestures and mobile-specific interactions
 *
 * Features:
 * - Swipe left/right navigation for quiz questions
 * - Touch-optimized feedback
 * - Visual indicators for swipe actions
 *
 * @version 1.0.0
 * @date 2026-01-07
 */

class MobileInteractions {
  constructor(options = {}) {
    this.onSwipeNext = options.onSwipeNext || (() => {});
    this.onSwipePrevious = options.onSwipePrevious || (() => {});
    this.swipeThreshold = options.swipeThreshold || 100; // pixels
    this.enabled = this._isTouchDevice();

    // State tracking
    this.touchStartX = 0;
    this.touchEndX = 0;
    this.touchStartY = 0;
    this.touchEndY = 0;
    this.isSwipeActive = false;

    if (this.enabled) {
      this.init();
      console.log('[MobileInteractions] Initialized - swipe gestures enabled');
    }
  }

  /**
   * Initialize touch event listeners
   */
  init() {
    // Use passive listeners for better scroll performance
    document.addEventListener('touchstart', (e) => this.handleTouchStart(e), { passive: true });
    document.addEventListener('touchmove', (e) => this.handleTouchMove(e), { passive: false });
    document.addEventListener('touchend', (e) => this.handleTouchEnd(e), { passive: true });
  }

  /**
   * Handle touch start event
   */
  handleTouchStart(e) {
    this.touchStartX = e.changedTouches[0].screenX;
    this.touchStartY = e.changedTouches[0].screenY;
    this.isSwipeActive = false;
  }

  /**
   * Handle touch move event
   * Shows visual feedback during swipe
   */
  handleTouchMove(e) {
    // Only prevent default if horizontal swipe is detected
    const touchX = e.changedTouches[0].screenX;
    const touchY = e.changedTouches[0].screenY;

    const diffX = Math.abs(touchX - this.touchStartX);
    const diffY = Math.abs(touchY - this.touchStartY);

    // If horizontal swipe is more dominant than vertical, prevent scroll
    if (diffX > diffY && diffX > 30) {
      e.preventDefault();
      this.isSwipeActive = true;

      // Show visual indicator
      this.showSwipeIndicator(touchX - this.touchStartX);
    }
  }

  /**
   * Handle touch end event
   * Triggers navigation if swipe threshold is met
   */
  handleTouchEnd(e) {
    this.touchEndX = e.changedTouches[0].screenX;
    this.touchEndY = e.changedTouches[0].screenY;

    // Clear visual indicator
    this.clearSwipeIndicator();

    if (this.isSwipeActive) {
      this.handleSwipe();
    }

    this.isSwipeActive = false;
  }

  /**
   * Process swipe gesture and trigger appropriate action
   */
  handleSwipe() {
    const diffX = this.touchStartX - this.touchEndX;
    const diffY = Math.abs(this.touchStartY - this.touchEndY);

    // Ensure horizontal swipe (not vertical scroll)
    if (diffY > 50) {
      return; // Too much vertical movement, probably a scroll
    }

    // Swipe left - next question
    if (diffX > this.swipeThreshold) {
      console.log('[MobileInteractions] Swipe left detected - next');
      this.onSwipeNext();
      this.showSwipeFeedback('next');
    }

    // Swipe right - previous question (if enabled)
    if (diffX < -this.swipeThreshold) {
      console.log('[MobileInteractions] Swipe right detected - previous');
      this.onSwipePrevious();
      this.showSwipeFeedback('previous');
    }
  }

  /**
   * Show visual indicator during swipe
   * @param {number} offset - Horizontal offset in pixels
   */
  showSwipeIndicator(offset) {
    let indicator = document.getElementById('swipe-indicator');

    if (!indicator) {
      indicator = document.createElement('div');
      indicator.id = 'swipe-indicator';
      indicator.style.cssText = `
        position: fixed;
        top: 50%;
        transform: translateY(-50%);
        font-size: 3rem;
        opacity: 0;
        transition: opacity 0.2s ease;
        pointer-events: none;
        z-index: 9999;
      `;
      document.body.appendChild(indicator);
    }

    // Show arrow based on direction
    if (offset < -50) {
      indicator.textContent = '⬅️';
      indicator.style.left = '20px';
      indicator.style.right = 'auto';
    } else if (offset > 50) {
      indicator.textContent = '➡️';
      indicator.style.right = '20px';
      indicator.style.left = 'auto';
    }

    // Fade in
    requestAnimationFrame(() => {
      indicator.style.opacity = '0.7';
    });
  }

  /**
   * Clear swipe indicator
   */
  clearSwipeIndicator() {
    const indicator = document.getElementById('swipe-indicator');
    if (indicator) {
      indicator.style.opacity = '0';
    }
  }

  /**
   * Show brief feedback after successful swipe
   * @param {string} direction - 'next' or 'previous'
   */
  showSwipeFeedback(direction) {
    const feedback = document.createElement('div');
    feedback.className = 'swipe-feedback';
    feedback.textContent = direction === 'next' ? 'Volgende →' : '← Vorige';
    feedback.style.cssText = `
      position: fixed;
      top: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(50, 196, 160, 0.9);
      color: white;
      padding: 0.5rem 1rem;
      border-radius: 20px;
      font-size: 0.9rem;
      font-weight: 600;
      z-index: 10000;
      opacity: 0;
      transition: opacity 0.3s ease;
      pointer-events: none;
    `;

    document.body.appendChild(feedback);

    // Animate in
    requestAnimationFrame(() => {
      feedback.style.opacity = '1';
    });

    // Animate out and remove
    setTimeout(() => {
      feedback.style.opacity = '0';
      setTimeout(() => {
        if (feedback.parentNode) {
          feedback.parentNode.removeChild(feedback);
        }
      }, 300);
    }, 1000);
  }

  /**
   * Check if device supports touch
   * @returns {boolean}
   */
  _isTouchDevice() {
    return ('ontouchstart' in window) ||
           (navigator.maxTouchPoints > 0) ||
           (navigator.msMaxTouchPoints > 0);
  }

  /**
   * Enable swipe gestures
   */
  enable() {
    this.enabled = true;
  }

  /**
   * Disable swipe gestures (e.g., during animations)
   */
  disable() {
    this.enabled = false;
  }

  /**
   * Destroy and clean up
   */
  destroy() {
    document.removeEventListener('touchstart', this.handleTouchStart);
    document.removeEventListener('touchmove', this.handleTouchMove);
    document.removeEventListener('touchend', this.handleTouchEnd);

    const indicator = document.getElementById('swipe-indicator');
    if (indicator && indicator.parentNode) {
      indicator.parentNode.removeChild(indicator);
    }
  }
}

/**
 * Utility: Add haptic feedback on supported devices
 */
function triggerHapticFeedback(type = 'light') {
  if (navigator.vibrate) {
    const patterns = {
      light: 10,
      medium: 20,
      heavy: 50
    };
    navigator.vibrate(patterns[type] || patterns.light);
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { MobileInteractions, triggerHapticFeedback };
}
