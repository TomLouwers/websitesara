# EdTech Platform Product Roadmap
**Version:** 1.0
**Date:** January 2026
**Platform:** OefenPlatform (Sara's Learning Platform)

---

## Executive Summary

This roadmap outlines strategic improvements across five key areas:
1. **Exercise Quality** - Enhance pedagogical value and learning outcomes
2. **Content Generation** - Scale exercise library with AI-assisted authoring
3. **Feedback System** - Implement adaptive, personalized learning feedback
4. **UI/UX Enhancement** - Modernize interface for better engagement
5. **Gamification & Bonus System** - Expand motivational mechanics

---

## Current State Analysis

### Platform Architecture
- **Frontend:** Pure JavaScript (no framework), localStorage-based
- **Exercise Types:**
  - Begrijpend Lezen (Reading Comprehension) - `bl_groep*_*.json`
  - Getal & Bewerking (Math) - `gb_groep*_*.json`
  - Woordenschat (Vocabulary) - `ws_groep*_*.json`
  - Werkwoordspelling (Spelling) - `sp_groep*_*.json`
- **Grade Levels:** Groep 3-8 (ages 6-12)
- **Current Exercise Count:** ~1,500+ exercises across subjects
- **Gamification:**
  - Session-based rewards (`SessionRewardManager`)
  - Cross-session progression (`GamificationManager`)
  - Streak mechanics, XP, achievements, daily challenges

### Key Strengths
✅ Age-appropriate feature gating (grades 3-5 vs 6-8)
✅ Neuroscience-safe feedback (no red X, no punishment)
✅ Rich metadata structure (skills, strategies, hints)
✅ Math rendering with KaTeX
✅ Accessibility features (dyslexia mode, font sizes)

### Pain Points
❌ Exercise quality varies (inconsistent hints, incomplete feedback)
❌ No content authoring tools (manual JSON editing)
❌ Feedback can be generic ("Goed gedaan!" vs. concept-specific)
❌ Limited adaptive difficulty
❌ Gamification mostly passive (badges awarded, not earned through choices)

---

## EPIC 1: Exercise Quality Enhancement

### Theme
**"Every exercise should teach, not just test"**

---

### US-1.1: Enhanced Feedback Schema
**As a** student
**I want** detailed explanations when I make mistakes
**So that** I understand WHY my answer was wrong and HOW to solve it correctly

**Acceptance Criteria:**
- [ ] Every exercise includes `feedback.correct.explanation` (why answer is right)
- [ ] Every exercise includes `feedback.incorrect.explanation` (what misconception led to error)
- [ ] Every exercise includes `feedback.incorrect.workedExample` (step-by-step solution)
- [ ] Feedback references the specific skill/strategy being tested

**Technical Implementation:**
```json
// New schema extension for existing exercises
{
  "question": "Waarom noemt Sofie de hamster Nibbel?",
  "skill": "letterlijk",
  "strategy": "informatie_zoeken",
  "feedback": {
    "correct": {
      "explanation": "Goed gevonden! In de tekst staat: 'omdat hij graag op zonnebloempitten kauwt'. Je hebt de belangrijke informatie goed gelezen.",
      "skill_reinforcement": "Je kunt letterlijke informatie goed vinden in de tekst!"
    },
    "incorrect": {
      "by_option": {
        "A": {
          "explanation": "Nibbel slaapt wel in het huisje, maar dat is niet de reden voor zijn naam.",
          "hint": "Zoek in de tekst naar het woord 'omdat' na de naam Nibbel.",
          "misconception": "Verwarring tussen gebeurtenissen in het verhaal"
        }
      },
      "workedExample": {
        "steps": [
          "1. Lees de zin: 'Ze noemt hem Nibbel, omdat...'",
          "2. Het woord 'omdat' geeft de reden",
          "3. Wat staat er na 'omdat'? → 'hij graag op zonnebloempitten kauwt'",
          "4. Knabbelen = nibbelen → daarom Nibbel!"
        ]
      }
    }
  }
}
```

**File Changes:**
- Update all JSON files in `data/exercises/bl/`, `data/exercises/gb/`, etc.
- Modify `static/src/app.js` to render new feedback structure
- Update `card-morph-feedback.js` to display worked examples

**Effort:** 40 story points (8 sprints)
**Priority:** HIGH
**Dependencies:** None

---

### US-1.2: Skill Taxonomy & Progression
**As an** educator
**I want** exercises organized by cognitive skill level
**So that** students progress from simple to complex within each topic

**Acceptance Criteria:**
- [ ] All exercises tagged with Bloom's taxonomy level (Remember, Understand, Apply, Analyze)
- [ ] Reading comprehension uses official Dutch framework: Letterlijk, Interpreterend, Reflecterend
- [ ] Math exercises tagged with strategy: Procedureel, Conceptueel, Probleemoplossend
- [ ] UI shows skill badges on quiz.html (already exists, needs expansion)

**Technical Implementation:**
```json
// Enhanced metadata structure
{
  "metadata": {
    "grade": 4,
    "category": "bl",
    "cognitive_level": "understand", // Bloom's taxonomy
    "skill_framework": {
      "primary": "letterlijk",
      "secondary": ["informatie_zoeken", "detail_herkennen"]
    },
    "difficulty": {
      "lexile_level": "450L", // Reading level
      "complexity_score": 2.5, // 1-5 scale
      "prerequisite_skills": ["basiswoordenschat_groep3"]
    }
  }
}
```

**Effort:** 20 story points (4 sprints)
**Priority:** MEDIUM
**Dependencies:** US-1.1

---

### US-1.3: Adaptive Hint System
**As a** struggling student
**I want** progressive hints that don't give away the answer
**So that** I can learn to solve problems independently

**Acceptance Criteria:**
- [ ] 3-tier hint system: Procedural → Conceptual → Worked Example
- [ ] Hints appear only after 12s of inactivity (already implemented)
- [ ] Gamification: Using hints reduces XP by 10% (grades 6-8 only)
- [ ] Track hint usage in `GamificationManager.stats.totalHintsUsed`

**Technical Implementation:**
```json
{
  "hints": {
    "tier1_procedural": {
      "text": "Kijk naar de zin waar Nibbel voor het eerst genoemd wordt.",
      "reveal_percentage": 0.2
    },
    "tier2_conceptual": {
      "text": "Let op het woord 'omdat' - dat geeft altijd een reden.",
      "reveal_percentage": 0.5
    },
    "tier3_worked_example": {
      "text": "De zin is: 'Ze noemt hem Nibbel, omdat hij graag op zonnebloempitten kauwt.' Het antwoord staat direct na 'omdat'.",
      "reveal_percentage": 0.9
    }
  }
}
```

**File Changes:**
- Update quiz.html hint display logic
- Modify `SessionRewardManager` to track hint tier usage
- Add hint penalty to XP calculation in `GamificationManager._calculateXP()`

**Effort:** 13 story points (2.5 sprints)
**Priority:** HIGH
**Dependencies:** US-1.1

---

### US-1.4: Question Validation Pipeline
**As a** content creator
**I want** automated validation of exercise quality
**So that** all exercises meet pedagogical standards before deployment

**Acceptance Criteria:**
- [ ] Validate JSON schema compliance (already exists in `scripts/validators/schema-validator.js`)
- [ ] Check for required fields: hint, explanation, workedExample
- [ ] Validate reading level matches grade (Flesch-Douma readability)
- [ ] Flag exercises missing diversity (e.g., all characters Dutch names)
- [ ] Generate quality score report per exercise file

**Technical Implementation:**
```javascript
// Extend scripts/validators/schema-validator.js
class ExerciseQualityValidator {
  validatePedagogy(exercise) {
    const issues = [];

    // Check feedback completeness
    if (!exercise.feedback?.correct?.explanation) {
      issues.push({ severity: 'error', message: 'Missing correct explanation' });
    }

    // Check reading level
    const readability = this.calculateFleschDouma(exercise.text);
    const expectedLevel = this.getReadabilityForGrade(exercise.metadata.grade);
    if (Math.abs(readability - expectedLevel) > 10) {
      issues.push({
        severity: 'warning',
        message: `Reading level ${readability} doesn't match grade ${exercise.metadata.grade}`
      });
    }

    return issues;
  }
}
```

**Effort:** 8 story points (1.5 sprints)
**Priority:** MEDIUM
**Dependencies:** US-1.1

---

## EPIC 2: Content Generation & Scaling

### Theme
**"From 1,500 to 15,000 exercises with AI assistance"**

---

### US-2.1: Exercise Template System
**As a** content creator
**I want** reusable templates for common exercise patterns
**So that** I can generate variations quickly without starting from scratch

**Acceptance Criteria:**
- [ ] Template library in `data/templates/` (already exists, needs expansion)
- [ ] Templates support variable substitution: `{{character_name}}`, `{{number_1}}`, etc.
- [ ] Web-based template editor (new tool in `tools/exercise-generator.html`)
- [ ] Generate 10 variations from 1 template with randomization

**Technical Implementation:**
```json
// Template example: data/templates/bl_inferentieel_emotie.json
{
  "template_id": "bl_inferentieel_emotie_v1",
  "schema_version": "2.0.0",
  "variables": {
    "character_name": ["Sofie", "Jamal", "Li", "Emma", "Yusuf"],
    "emotion": ["blij", "verdrietig", "boos", "bang"],
    "event": ["huisdier krijgen", "verjaardag vieren", "iets verliezen"]
  },
  "text_template": "{{character_name}} is {{emotion}} omdat {{pronoun}} {{event}}. {{character_name}} {{action_matching_emotion}}.",
  "question_template": "Hoe voelt {{character_name}} zich?",
  "correct_answer": "{{emotion}}",
  "distractors_template": ["{{other_emotion_1}}", "{{other_emotion_2}}", "{{other_emotion_3}}"]
}
```

**New Tool:**
- Create `tools/exercise-generator.html` - Web UI for template creation
- Supports preview, variable testing, bulk generation
- Exports to standard JSON format

**Effort:** 21 story points (4 sprints)
**Priority:** HIGH
**Dependencies:** None

---

### US-2.2: AI-Assisted Content Generation (LLM Integration)
**As a** content creator
**I want** AI to generate exercise variations
**So that** I can scale content 10x faster while maintaining quality

**Acceptance Criteria:**
- [ ] Integration with OpenAI API or Claude API for text generation
- [ ] Generate reading comprehension passages at target grade level
- [ ] Generate math word problems with controlled difficulty
- [ ] Human review workflow before exercises go live
- [ ] Track AI-generated vs human-created exercises

**Technical Implementation:**
```javascript
// New file: scripts/ai-content-generator.js
class AIExerciseGenerator {
  async generateReadingPassage(params) {
    const prompt = `
Generate a Dutch reading comprehension passage for grade ${params.grade}.

Requirements:
- Theme: ${params.theme}
- Text type: ${params.textType} (verhalend/informatief/betogend)
- Word count: ${params.wordCount}
- Reading level: ${params.readingLevel} (Flesch-Douma score)
- Include diverse character names (Dutch, international)
- Age-appropriate vocabulary

Output format: JSON with text, metadata, and 3 questions (letterlijk, inferentieel, reflecterend)
    `;

    const response = await this.callLLM(prompt);
    const exercise = this.parseAndValidate(response);
    return exercise;
  }

  async generateMathProblem(params) {
    // Similar approach for math word problems
  }
}
```

**API Requirements:**
- OpenAI GPT-4 or Anthropic Claude
- Budget: ~€0.10 per exercise generated
- Quality threshold: 90% pass rate on validation

**Effort:** 34 story points (7 sprints)
**Priority:** MEDIUM
**Dependencies:** US-2.1, US-1.4 (validation pipeline)

---

### US-2.3: Crowdsourced Content Review
**As an** educator
**I want** to submit my own exercises for review
**So that** the platform grows with community contributions

**Acceptance Criteria:**
- [ ] Submission form at `tools/submit-exercise.html`
- [ ] Exercises stored in `data/exercises/community/pending/`
- [ ] Admin review dashboard at `tools/review-exercises.html` (already exists!)
- [ ] Approved exercises moved to main library
- [ ] Contributors credited in exercise metadata

**Technical Implementation:**
- Extend existing `tools/review-exercises.html`
- Add submission form with schema validation
- Email notification to admin on new submissions
- Version control: Git branch per submission for review

**Effort:** 13 story points (2.5 sprints)
**Priority:** LOW
**Dependencies:** US-1.4

---

### US-2.4: Exercise Remixing & Variation Engine
**As a** student
**I want** different versions of exercises I struggled with
**So that** I can practice the same skill with fresh content

**Acceptance Criteria:**
- [ ] Identify exercises where student scored <50%
- [ ] Generate 2-3 variations with same skill, different content
- [ ] Variations use template system (US-2.1)
- [ ] Store in sessionStorage for immediate retry
- [ ] Track improvement across variations

**Technical Implementation:**
```javascript
// Extend static/src/app.js
class ExerciseVariationEngine {
  generateVariation(originalExercise, performance) {
    const template = this.findMatchingTemplate(originalExercise);
    const variation = this.applyTemplate(template, {
      difficulty: performance.score < 0.3 ? 'easier' : 'same',
      preserveSkill: true,
      newContext: true
    });
    return variation;
  }
}
```

**Effort:** 21 story points (4 sprints)
**Priority:** MEDIUM
**Dependencies:** US-2.1

---

## EPIC 3: Adaptive Feedback System

### Theme
**"Feedback that teaches, not just tells"**

---

### US-3.1: Real-Time Error Analysis
**As a** student
**I want** immediate diagnosis of my mistake type
**So that** I understand my misconception and avoid it next time

**Acceptance Criteria:**
- [ ] Classify errors into categories (already exists in `foutanalyse-modaal.js`)
- [ ] Math errors: Conversiefout, Rekenfout Basis, Rekenfout Complex, Begrip, Strategie
- [ ] Reading errors: Letterlijk Gemist, Inferentie Fout, Vocabulaire
- [ ] Show error badge with emoji (already implemented)
- [ ] Link to targeted remediation exercises

**Enhancement to Existing System:**
```javascript
// Extend static/src/foutanalyse-modaal.js
class ErrorAnalyzer {
  diagnoseError(question, userAnswer, correctAnswer) {
    const errorType = this.classifyError(question, userAnswer, correctAnswer);
    const remediation = this.getRemediation(errorType, question.skill);

    return {
      type: errorType,
      emoji: CONFIG.errorEmojis[errorType],
      explanation: this.generateExplanation(errorType, question),
      remediation: remediation, // Links to practice exercises
      reflectionQuestion: this.generateReflectionPrompt(errorType)
    };
  }

  generateReflectionPrompt(errorType) {
    const prompts = {
      'conversiefout': 'Heb je de eenheden goed omgezet? Welke stap vergat je?',
      'rekenfout_basis': 'Welke rekenbewerking heb je gebruikt? Klopt dat bij deze vraag?',
      'begrip': 'Wat vroeg de vraag precies? Lees hem nog eens langzaam.'
    };
    return prompts[errorType];
  }
}
```

**Effort:** 13 story points (2.5 sprints)
**Priority:** HIGH
**Dependencies:** US-1.1

---

### US-3.2: Personalized Learning Insights
**As a** student
**I want** to see my learning patterns over time
**So that** I know which skills to focus on

**Acceptance Criteria:**
- [ ] Dashboard showing performance by skill (letterlijk: 85%, inferentieel: 62%)
- [ ] Identify weakest skills across sessions (uses `GamificationManager.stats.byCategory`)
- [ ] Recommend next exercise based on weaknesses
- [ ] Visualize progress over time (line chart)
- [ ] Age-appropriate language (grades 3-5 vs 6-8)

**Technical Implementation:**
```javascript
// New file: static/src/learning-insights.js
class LearningInsights {
  constructor(gamificationManager) {
    this.stats = gamificationManager.stats;
    this.profile = gamificationManager.profile;
  }

  getSkillBreakdown() {
    const breakdown = {};
    Object.entries(this.stats.byCategory).forEach(([category, data]) => {
      breakdown[category] = {
        accuracy: (data.correct / data.total) * 100,
        total: data.total,
        status: this.getStatusLabel((data.correct / data.total) * 100)
      };
    });
    return breakdown;
  }

  getStatusLabel(accuracy) {
    if (accuracy >= 85) return { emoji: '🌟', text: 'Expert!' };
    if (accuracy >= 70) return { emoji: '👍', text: 'Goed bezig!' };
    if (accuracy >= 50) return { emoji: '📈', text: 'Blijf oefenen!' };
    return { emoji: '💪', text: 'Focus hierop!' };
  }

  recommendNextExercise() {
    // Find weakest skill with >10 attempts (statistically significant)
    const weakestSkill = Object.entries(this.stats.byCategory)
      .filter(([_, data]) => data.total >= 10)
      .sort((a, b) => (a[1].correct/a[1].total) - (b[1].correct/b[1].total))[0];

    return {
      category: weakestSkill[0],
      reason: `Je score voor ${CONFIG.subjectTitles[weakestSkill[0]]} is ${Math.round((weakestSkill[1].correct/weakestSkill[1].total)*100)}%. Nog even oefenen!`
    };
  }
}
```

**New UI Page:**
- Create `insights.html` - Personal learning dashboard
- Show skill radar chart, progress timeline, recommended exercises
- Link from main menu and results page

**Effort:** 21 story points (4 sprints)
**Priority:** MEDIUM
**Dependencies:** Gamification system already in place

---

### US-3.3: Contextual Feedback Timing
**As a** student
**I want** feedback delivered at the optimal moment
**So that** I stay in flow state and don't get frustrated

**Acceptance Criteria:**
- [ ] Correct answers: Immediate positive reinforcement (already done)
- [ ] Incorrect answers on first try: Gentle hint, allow retry
- [ ] Incorrect answers on second try: Full explanation + worked example
- [ ] Streak broken: Encouraging message ("Je had er al 4 goed!")
- [ ] No interruption for minor typos (fuzzy matching for open-ended questions)

**Technical Implementation:**
```javascript
// Extend static/src/app.js
class AdaptiveFeedbackEngine {
  determineFeedbackStrategy(attempt, history) {
    if (attempt === 1 && !history.correct) {
      return {
        type: 'gentle_hint',
        delay: 500, // ms
        allowRetry: true,
        message: 'Bijna! Probeer het nog eens.',
        showPartialFeedback: true
      };
    } else if (attempt === 2 && !history.correct) {
      return {
        type: 'full_explanation',
        delay: 0,
        allowRetry: false,
        showWorkedExample: true,
        showReflectionPrompt: true
      };
    }
    // ... more strategies
  }
}
```

**Effort:** 8 story points (1.5 sprints)
**Priority:** MEDIUM
**Dependencies:** US-3.1

---

### US-3.4: Metacognitive Prompts
**As a** student (grades 6-8)
**I want** reflection questions after mistakes
**So that** I develop self-awareness about my thinking process

**Acceptance Criteria:**
- [ ] After incorrect answer, show reflection prompt (already exists in `foutanalyse-modaal.js`)
- [ ] Prompts are open-ended: "Wat dacht je toen je dit antwoord koos?"
- [ ] Encourage self-explanation before showing solution
- [ ] Track engagement with reflection (did student read it?)
- [ ] Age-gated: Only grades 6-8

**Enhancement:**
```javascript
// Extend foutanalyse-modaal.js reflection prompts
const METACOGNITIVE_PROMPTS = {
  'conversiefout': [
    'Welke eenheid stond er in de vraag? Welke eenheid heb jij gebruikt?',
    'Hoe zou je dit anders aanpakken als je het opnieuw deed?'
  ],
  'begrip': [
    'Wat vroeg de vraag precies? Schrijf het in je eigen woorden op.',
    'Welk woord in de vraag was moeilijk? Wat betekent het?'
  ]
};
```

**Effort:** 5 story points (1 sprint)
**Priority:** LOW
**Dependencies:** US-3.1

---

## EPIC 4: UI/UX Enhancement

### Theme
**"Delightful experiences that make learning fun"**

---

### US-4.1: Mobile-First Responsive Redesign
**As a** student on a tablet
**I want** touch-optimized UI with large tap targets
**So that** I can use the platform comfortably on any device

**Acceptance Criteria:**
- [ ] Minimum touch target: 44x44px (already mostly implemented)
- [ ] Quiz page responsive: quiz.html already has mobile breakpoints
- [ ] Swipe gestures: Swipe to next question (new feature)
- [ ] Fullscreen mode on tablets (hide browser chrome)
- [ ] Offline mode: Service Worker for caching exercises

**Technical Implementation:**
```javascript
// New file: static/src/mobile-interactions.js
class MobileInteractions {
  enableSwipeNavigation() {
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', e => {
      touchStartX = e.changedTouches[0].screenX;
    });

    document.addEventListener('touchend', e => {
      touchEndX = e.changedTouches[0].screenX;
      this.handleSwipe();
    });
  }

  handleSwipe() {
    const swipeThreshold = 100;
    if (touchEndX < touchStartX - swipeThreshold) {
      // Swipe left - next question (if answer submitted)
      if (currentQuestionAnswered) {
        nextQuestion();
      }
    }
  }
}

// Service Worker for offline
// New file: sw.js
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('sara-exercises-v1').then(cache => {
      return cache.addAll([
        '/quiz.html',
        '/static/js/app.min.js',
        '/data/exercises/bl/bl_groep4_m4_1.json'
        // ... cache frequently used exercises
      ]);
    })
  );
});
```

**Effort:** 13 story points (2.5 sprints)
**Priority:** HIGH
**Dependencies:** None

---

### US-4.2: Interactive Animations & Microinteractions
**As a** young student (grades 3-5)
**I want** playful animations when I get answers right
**So that** I feel excited and motivated to continue

**Acceptance Criteria:**
- [ ] Correct answer: Confetti animation (already exists in rewards.css)
- [ ] Streak milestone: Full-screen celebration (already implemented)
- [ ] Level up: Character animation or badge reveal
- [ ] Answer selection: Smooth morphing transition (card-morph-feedback.js already does this)
- [ ] Loading states: Skeleton screens instead of spinners

**Enhancement:**
```css
/* Extend static/css/rewards.css */
@keyframes confetti-burst {
  0% {
    opacity: 1;
    transform: translateY(0) rotate(0deg);
  }
  100% {
    opacity: 0;
    transform: translateY(-200px) rotate(720deg);
  }
}

.confetti-piece {
  position: absolute;
  width: 10px;
  height: 10px;
  background: var(--primary-color);
  animation: confetti-burst 1.5s ease-out forwards;
}
```

**New Library:**
- Add Canvas Confetti library for celebration effects
- Lottie animations for character reveals

**Effort:** 8 story points (1.5 sprints)
**Priority:** LOW
**Dependencies:** None

---

### US-4.3: Accessibility Audit & WCAG 2.1 AA Compliance
**As a** student with visual impairment
**I want** screen reader support and keyboard navigation
**So that** I can use the platform independently

**Acceptance Criteria:**
- [ ] All images have alt text
- [ ] Keyboard navigation: Tab through all interactive elements
- [ ] ARIA labels on custom components (quiz options, progress bar)
- [ ] Color contrast ratio ≥ 4.5:1 (already high contrast mode exists)
- [ ] Skip to content link
- [ ] Tested with NVDA/JAWS screen readers

**Technical Implementation:**
```html
<!-- Enhance quiz.html with ARIA -->
<div class="quiz-answers-wrapper" role="radiogroup" aria-labelledby="questionTextNew">
  <div class="option"
       role="radio"
       aria-checked="false"
       tabindex="0"
       aria-label="Optie B: Hij knabbelt graag aan pitten">
    Hij knabbelt graag aan pitten.
  </div>
</div>

<div class="quiz-progress-track" role="progressbar"
     aria-valuenow="3"
     aria-valuemin="1"
     aria-valuemax="10"
     aria-label="Vraag 3 van 10">
</div>
```

**Effort:** 13 story points (2.5 sprints)
**Priority:** MEDIUM
**Dependencies:** None

---

### US-4.4: Dark Mode & Theme Customization
**As a** student
**I want** to choose my own color theme
**So that** the platform feels personal and comfortable

**Acceptance Criteria:**
- [ ] Light mode (current default)
- [ ] Dark mode (OLED-friendly)
- [ ] Theme picker on index.html
- [ ] Themes saved in localStorage (already exists: `sara_player_profile.currentTheme`)
- [ ] Unlockable themes via gamification (space, underwater, forest - already defined!)

**Technical Implementation:**
```css
/* New file: static/css/themes.css */
:root[data-theme="dark"] {
  --background: #1a1a1a;
  --surface: #2d2d2d;
  --text-primary: #e0e0e0;
  --text-secondary: #b0b0b0;
  --primary-color: #64B5F6;
  --success-color: #81C784;
}

:root[data-theme="space"] {
  --background: linear-gradient(180deg, #0B0B1F 0%, #1a1a3e 100%);
  --primary-color: #9D4EDD;
  --accent-color: #FFC107;
  /* Stars background pattern */
}
```

**Effort:** 8 story points (1.5 sprints)
**Priority:** LOW
**Dependencies:** Gamification system

---

## EPIC 5: Gamification & Bonus System Expansion

### Theme
**"Intrinsic motivation through meaningful progression"**

---

### US-5.1: Achievement System Expansion
**As a** student
**I want** to unlock rare achievements through skillful play
**So that** I feel proud of my learning accomplishments

**Acceptance Criteria:**
- [ ] 50+ achievements across categories (currently ~15 defined in gamification.js)
- [ ] Achievement categories: Streaks, Volume, Perfectionist, Skill Mastery, Explorer
- [ ] Rare achievements: <5% unlock rate (e.g., "Maand Meester" - 30 day streak)
- [ ] Achievement showcase on profile page
- [ ] Social sharing: "I earned [badge]!"

**New Achievements:**
```javascript
// Extend GamificationManager._getAchievementDefinitions()
const NEW_ACHIEVEMENTS = [
  // Skill-based
  {
    id: 'reading_detective',
    title: 'Lees Detective',
    description: '95% goed bij Begrijpend Lezen',
    emoji: '🔍',
    condition: { type: 'category_mastery', category: 'bl', accuracy: 95 },
    rarity: 'rare'
  },

  // Speed-based
  {
    id: 'speed_demon',
    title: 'Snelheidsduivel',
    description: 'Voltooi 10 vragen in <15 seconden per vraag',
    emoji: '⚡',
    condition: { type: 'speed', avgTime: 15, minQuestions: 10 },
    rarity: 'epic'
  },

  // Exploration
  {
    id: 'explorer',
    title: 'Ontdekkingsreiziger',
    description: 'Probeer alle 6 vakken',
    emoji: '🗺️',
    condition: { type: 'categories_tried', count: 6 },
    rarity: 'common'
  },

  // Mastery
  {
    id: 'renaissance_learner',
    title: 'Renaissance Leerling',
    description: '80% goed bij alle vakken',
    emoji: '🎨',
    condition: { type: 'multi_category_mastery', accuracy: 80, categories: 'all' },
    rarity: 'legendary'
  }
];
```

**Effort:** 13 story points (2.5 sprints)
**Priority:** MEDIUM
**Dependencies:** Gamification system already in place

---

### US-5.2: Daily & Weekly Challenges
**As a** student
**I want** fresh challenges every day
**So that** I have clear goals and stay engaged

**Acceptance Criteria:**
- [ ] 3 daily challenges generated at midnight (already implemented in gamification.js)
- [ ] 2 weekly challenges (already implemented)
- [ ] Challenges tailored to student's grade level
- [ ] Bonus XP for completing all daily challenges (streak bonus)
- [ ] Challenge notification on login ("Je hebt 2 nieuwe uitdagingen!")

**Enhancement:**
```javascript
// Extend GamificationManager._generateDailyChallenges()
_generatePersonalizedChallenges() {
  const challenges = [];

  // Adaptive challenge: Focus on weakest skill
  const weakestSkill = this.getWeakestSkill();
  if (weakestSkill) {
    challenges.push({
      id: `daily_${this._getToday()}_improvement`,
      type: 'skill_improvement',
      title: 'Verbeter je zwakste punt',
      description: `Behaal 70% goed bij ${CONFIG.subjectTitles[weakestSkill]}`,
      target: 0.7,
      category: weakestSkill,
      reward: { xp: 75, badge: null }
    });
  }

  // Exploration challenge: Try new subject
  const unexploredSubjects = this.getUnexploredSubjects();
  if (unexploredSubjects.length > 0) {
    challenges.push({
      id: `daily_${this._getToday()}_explore`,
      type: 'exploration',
      title: 'Ontdek iets nieuws',
      description: `Probeer ${CONFIG.subjectTitles[unexploredSubjects[0]]}`,
      target: 1,
      category: unexploredSubjects[0],
      reward: { xp: 50, badge: null }
    });
  }

  return challenges;
}
```

**Effort:** 8 story points (1.5 sprints)
**Priority:** MEDIUM
**Dependencies:** None

---

### US-5.3: Leaderboards & Social Features
**As a** competitive student (grades 6-8)
**I want** to compare my progress with peers
**So that** I feel motivated to improve

**Acceptance Criteria:**
- [ ] Class leaderboard (requires teacher setup)
- [ ] Anonymous global leaderboard (opt-in only)
- [ ] Leaderboard categories: Daily XP, Weekly Streak, Total Achievements
- [ ] Privacy: No last names, only first name + emoji
- [ ] Age-gated: Only grades 6-8 (feature flag already exists)

**Technical Implementation:**
```javascript
// New file: static/src/leaderboard.js
class Leaderboard {
  constructor() {
    this.enabled = this.checkFeatureGate(); // Only grades 6-8
  }

  async submitScore(score) {
    if (!this.enabled) return;

    // Anonymous identifier (hashed device ID)
    const playerId = this.getAnonymousId();

    await fetch('/api/leaderboard', {
      method: 'POST',
      body: JSON.stringify({
        playerId: playerId,
        displayName: this.getDisplayName(), // "Emma 🦊"
        score: score.totalXP,
        category: 'weekly_xp'
      })
    });
  }

  getDisplayName() {
    const firstName = localStorage.getItem('playerName').split(' ')[0];
    const emoji = this.profile.currentAvatar === 'astronaut' ? '🚀' : '🌟';
    return `${firstName} ${emoji}`;
  }
}
```

**Backend Requirement:**
- Simple API endpoint for leaderboard (Firebase, Supabase, or static JSON)
- GDPR compliant: No PII stored

**Effort:** 21 story points (4 sprints)
**Priority:** LOW (requires backend)
**Dependencies:** Backend infrastructure

---

### US-5.4: Progression System: Levels & Unlocks
**As a** student
**I want** to level up and unlock rewards
**So that** I have long-term goals to work towards

**Acceptance Criteria:**
- [ ] Level system 1-50 (currently unlimited in gamification.js)
- [ ] XP requirements scale smoothly (already implemented: 20% increase per level)
- [ ] Unlocks at key levels (already defined: themes at 5/10/15, avatars at 3/7/12)
- [ ] Visual level-up animation
- [ ] Profile page shows current level, XP progress bar

**Enhancement:**
```javascript
// Extend GamificationManager._checkLevelUnlocks()
_checkLevelUnlocks() {
  const level = this.profile.level;
  const unlocks = [];

  // Themes
  const THEME_UNLOCKS = {
    5: 'space',
    10: 'underwater',
    15: 'forest',
    20: 'sunset',
    25: 'neon'
  };

  // Avatars
  const AVATAR_UNLOCKS = {
    3: 'detective',
    7: 'scientist',
    12: 'astronaut',
    18: 'artist',
    25: 'superhero'
  };

  // Power-ups (grades 6-8)
  const POWERUP_UNLOCKS = {
    10: 'streak_freeze', // Prevent streak break once
    20: 'hint_free', // Get 3 free hints
    30: 'xp_boost' // 2x XP for next session
  };

  // Check and unlock
  if (THEME_UNLOCKS[level]) {
    this.profile.unlockedThemes.push(THEME_UNLOCKS[level]);
    unlocks.push({ type: 'theme', name: THEME_UNLOCKS[level] });
  }

  return unlocks;
}
```

**Effort:** 8 story points (1.5 sprints)
**Priority:** MEDIUM
**Dependencies:** None

---

### US-5.5: Power-Ups & Consumables (Grades 6-8)
**As an** advanced student
**I want** strategic choices about when to use power-ups
**So that** I feel agency and make meaningful decisions

**Acceptance Criteria:**
- [ ] 3 power-up types: Streak Freeze, Hint Free, XP Boost
- [ ] Power-ups earned through achievements or purchased with XP
- [ ] Clear UI to activate power-up before quiz
- [ ] Track power-up usage in stats
- [ ] Age-gated: Grades 6-8 only

**Technical Implementation:**
```javascript
// Extend GamificationManager
class PowerUpManager {
  activatePowerUp(type) {
    const powerUp = this.profile.powerUps[type];

    if (!powerUp || powerUp.quantity <= 0) {
      return { success: false, message: 'Je hebt deze power-up niet.' };
    }

    // Consume power-up
    powerUp.quantity--;
    powerUp.activeUntil = this.calculateExpiry(type);

    this._saveAll();

    return {
      success: true,
      message: `${powerUp.name} geactiveerd!`,
      effect: powerUp.description
    };
  }

  calculateExpiry(type) {
    const DURATIONS = {
      'streak_freeze': null, // One-time use
      'hint_free': Date.now() + (24 * 60 * 60 * 1000), // 24 hours
      'xp_boost': null // One session
    };
    return DURATIONS[type];
  }
}
```

**Effort:** 13 story points (2.5 sprints)
**Priority:** LOW
**Dependencies:** US-5.4

---

## Implementation Roadmap

### Phase 1: Foundation (Q1 2026) - 3 months
**Focus:** Exercise quality + feedback fundamentals

| Epic | User Story | Priority | Effort | Sprint |
|------|-----------|----------|--------|--------|
| 1 | US-1.1 Enhanced Feedback Schema | HIGH | 40 | 1-8 |
| 1 | US-1.3 Adaptive Hint System | HIGH | 13 | 3-4 |
| 3 | US-3.1 Real-Time Error Analysis | HIGH | 13 | 5-7 |
| 4 | US-4.1 Mobile-First Redesign | HIGH | 13 | 6-8 |

**Deliverable:** All exercises have rich feedback, mobile experience improved

---

### Phase 2: Scaling Content (Q2 2026) - 3 months
**Focus:** Content generation + AI tools

| Epic | User Story | Priority | Effort | Sprint |
|------|-----------|----------|--------|--------|
| 2 | US-2.1 Exercise Template System | HIGH | 21 | 9-12 |
| 2 | US-2.2 AI-Assisted Generation | MEDIUM | 34 | 10-16 |
| 1 | US-1.4 Question Validation | MEDIUM | 8 | 12-13 |
| 2 | US-2.4 Exercise Remixing | MEDIUM | 21 | 14-17 |

**Deliverable:** Exercise library scales to 5,000+ with AI assistance

---

### Phase 3: Personalization (Q3 2026) - 3 months
**Focus:** Adaptive learning + insights

| Epic | User Story | Priority | Effort | Sprint |
|------|-----------|----------|--------|--------|
| 3 | US-3.2 Learning Insights Dashboard | MEDIUM | 21 | 18-21 |
| 1 | US-1.2 Skill Taxonomy | MEDIUM | 20 | 19-22 |
| 3 | US-3.3 Contextual Feedback Timing | MEDIUM | 8 | 22-23 |
| 5 | US-5.2 Daily/Weekly Challenges | MEDIUM | 8 | 23-24 |

**Deliverable:** Personalized learning paths, adaptive difficulty

---

### Phase 4: Engagement & Polish (Q4 2026) - 3 months
**Focus:** Gamification expansion + UX refinement

| Epic | User Story | Priority | Effort | Sprint |
|------|-----------|----------|--------|--------|
| 5 | US-5.1 Achievement System Expansion | MEDIUM | 13 | 25-27 |
| 5 | US-5.4 Levels & Unlocks Enhancement | MEDIUM | 8 | 27-28 |
| 4 | US-4.3 Accessibility Audit | MEDIUM | 13 | 28-30 |
| 5 | US-5.5 Power-Ups (Grades 6-8) | LOW | 13 | 30-32 |

**Deliverable:** Polished, accessible, deeply engaging platform

---

## Success Metrics

### Learning Outcomes
- **Accuracy Improvement:** Students improve 15% after using enhanced feedback (US-1.1)
- **Skill Mastery:** 70% of students achieve 80%+ accuracy in 3+ skills after 4 weeks
- **Engagement:** Average session length increases 25% (from ~8min to 10min)

### Content Metrics
- **Library Growth:** 1,500 → 15,000 exercises (10x growth)
- **Quality Score:** 90%+ of exercises pass validation (US-1.4)
- **Variety:** 50+ unique templates covering all skill types

### Engagement Metrics
- **Daily Active Users (DAU):** Increase 40% through daily challenges
- **Streak Retention:** 30% of users maintain 7+ day streak (vs 12% baseline)
- **Feature Adoption:** 60% of users unlock at least 1 achievement per week

### Technical Metrics
- **Load Time:** Quiz page loads in <2s on 3G (via Service Worker)
- **Accessibility:** WCAG 2.1 AA compliance score 95%+
- **Mobile Usage:** 70% of sessions on tablet/mobile

---

## Risk Analysis

### High Risk
| Risk | Mitigation |
|------|------------|
| **AI-generated exercises low quality** | Mandatory human review (US-2.3), validation pipeline (US-1.4), A/B testing |
| **Gamification too complex for young kids** | Age-gating (already implemented), user testing with grades 3-5 |
| **Backend cost for leaderboards** | Use Firebase free tier, cache aggressively, limit to grades 6-8 |

### Medium Risk
| Risk | Mitigation |
|------|------------|
| **Content generation too slow** | Start with templates (US-2.1) before AI (US-2.2), batch processing |
| **Teacher adoption for class leaderboards** | Make optional, provide onboarding guide, pilot with 5 schools |

---

## Appendix: Technical Architecture

### Current Stack
- **Frontend:** Vanilla JavaScript (ES6+), HTML5, CSS3
- **Storage:** localStorage (100% client-side)
- **Styling:** Custom CSS with utility classes
- **Math Rendering:** KaTeX
- **Icons:** Material Icons + Emoji

### Proposed Additions
- **Build Tool:** Vite (faster than current minification)
- **AI Integration:** OpenAI API or Claude API (serverless functions)
- **Backend (optional):** Firebase or Supabase (for leaderboards only)
- **Service Worker:** Workbox for offline caching
- **Animation:** Lottie for complex animations
- **Charts:** Chart.js for learning insights dashboard

---

**Document End**

*This roadmap is a living document. Update quarterly based on user feedback and learning analytics.*
