module.exports = {
  content: [
    './*.html',
    './modules/**/*.html',
    './*.js',
    './modules/**/*.js'
  ],
  css: ['./styles.css'],
  output: './styles.purged.css',

  // Safelist: Classes added dynamically by JavaScript or needed for states
  safelist: {
    // Standard safelisting
    standard: [
      // Quiz states
      'selected', 'correct', 'incorrect', 'disabled', 'hidden', 'show',
      // Animations
      'card-flip-out', 'card-flip-in', 'expanded', 'active',
      // Focus mode
      'focus-mode-active',
      // Dyslexia mode
      'dyslexia-mode',
      // Font sizes
      'font-size-groot', 'font-size-extra-groot',
      // High contrast
      'high-contrast-mode',
      // Level/theme cards
      'level-3', 'level-4', 'level-5', 'level-6', 'level-7', 'level-8',
      // Theme colors
      'color-teal', 'color-blue', 'color-purple', 'color-mint', 'color-coral', 'color-yellow',
      // Quiz components
      'visible', 'milestone-celebration', 'streak-bonus'
    ],

    // Deep: Keep all variants of these classes
    deep: [
      /^option/, // option, option-label, option-text, etc.
      /^quiz-/, // quiz-card, quiz-progress, etc.
      /^theme-/, // theme-card, theme-primary, etc.
      /^level-/, // level-card, level-badge, etc.
      /^subject-/, // subject-card, subject-icon, etc.
      /^feedback-/, // feedback-card, feedback-section, etc.
      /^lova-/, // lova-help, lova-panel, etc.
      /^modaal-/, // modaal-overlay, modaal-content, etc.
      /^btn-/, // btn-primary, btn-secondary, etc.
      /^card-/, // card-morph, card-body, etc.
      /^hero-/, // hero-section, hero-content, etc.
      /^nav-/, // nav-brand, nav-link, etc.
      /^reading-/, // reading-content, etc.
      /^story-/, // story-block, story-text, etc.
      /^answer-/, // answer-option, etc.
      /^skill-/, // skill-badge, etc.
      /^strategy-/, // strategy-badge, etc.
      /^error-/, // error-badge, etc.
      /^visual-/, // visual-aid, etc.
      /^remedial-/, // remedial-section, etc.
      /^hint-/, // hint-container, etc.
      /^accessibility-/, // accessibility-panel, etc.
      /^font-scale-/, // font-scale-standard, etc.
    ],

    // Greedy: Match patterns more aggressively
    greedy: [
      /data-/,
      /:hover/,
      /:focus/,
      /:active/,
      /:disabled/,
      /:checked/,
      /::before/,
      /::after/,
    ]
  },

  // Don't remove keyframes
  keyframes: true,

  // Don't remove font-face declarations
  fontFace: true,

  // Variables to keep
  variables: true
};
