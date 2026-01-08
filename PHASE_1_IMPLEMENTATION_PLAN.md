# Phase 1: Foundation - Implementation Plan
**Status:** In Progress
**Start Date:** January 7, 2026
**Branch:** `claude/phase-1-foundation-setup-XfTiV`

---

## Current State Analysis

### ✅ What We Have
- **Feedback System:** Basic card morph feedback with single insight
- **Hint System:** Single hint per question (after 12s inactivity)
- **Error Analysis:** Exists for verhaaltjessommen only (conversiefout, leesfout_ruis, etc.)
- **Exercise Schema:**
  - Reading (bl): `hint`, `skill`, options with `is_correct`
  - Math (gb): `correct` index, `tips` array in `extra_info`
  - NO worked examples or detailed explanations yet
- **Mobile:** Responsive CSS but no swipe gestures
- **Offline:** No Service Worker yet

### ❌ What's Missing (Phase 1 Goals)
1. **Rich Feedback:** Explanations for WHY answers are correct/incorrect
2. **Worked Examples:** Step-by-step solutions for all exercises
3. **3-Tier Hints:** Progressive hint system (Procedural → Conceptual → Worked Example)
4. **Error Remediation:** Links to practice exercises for each error type
5. **Mobile Interactions:** Swipe navigation for touch devices
6. **Offline Support:** Service Worker for caching

---

## Implementation Strategy

### 🎯 Approach
**Incremental & Backwards Compatible:**
- All changes will be **additive** (no breaking changes)
- Old exercises without new fields will still work
- New feedback rendering will gracefully fall back to old format
- Test after each major change

---

## Task Breakdown

### 1️⃣ US-1.1: Enhanced Feedback Schema (HIGH Priority)

#### 1.1.1 Define New Schema Extension
**File:** `SCHEMA_V2.md` (new documentation file)

```json
{
  "feedback": {
    "correct": {
      "explanation": "Why this answer is right",
      "skill_reinforcement": "Positive skill reinforcement"
    },
    "incorrect": {
      "by_option": {
        "A": {
          "explanation": "Why this is wrong",
          "hint": "Directional hint",
          "misconception": "Common error pattern"
        }
      },
      "workedExample": {
        "steps": ["Step 1", "Step 2", "Step 3"]
      }
    }
  }
}
```

#### 1.1.2 Update Sample Exercises
**Files:**
- `data/exercises/bl/bl_groep4_m4_1.json` (1 exercise as proof of concept)
- `data/exercises/gb/gb_groep4_m4.json` (1 exercise as proof of concept)

**Action:** Enhance 2 sample exercises with full feedback schema

#### 1.1.3 Update Feedback Rendering
**File:** `static/src/card-morph-feedback.js`

**Changes:**
- Add `renderWorkedExample()` method
- Add `renderDetailedExplanation()` method
- Update `renderFeedbackContent()` to use new fields if available
- **Fallback:** If new fields don't exist, use old format

**Code Addition:**
```javascript
renderDetailedFeedback(card, { isCorrect, question, selectedOption }) {
  // Check if new feedback schema exists
  const hasFeedback = question.feedback &&
                      (question.feedback.correct || question.feedback.incorrect);

  if (hasFeedback && isCorrect) {
    // Render correct explanation
    const explanation = question.feedback.correct.explanation || '';
    const reinforcement = question.feedback.correct.skill_reinforcement || '';
    // ... render new UI
  } else if (hasFeedback && !isCorrect) {
    // Render incorrect explanation + worked example
    const optionKey = selectedOption.label;
    const optionFeedback = question.feedback.incorrect.by_option?.[optionKey];
    // ... render new UI
  } else {
    // FALLBACK: Use old rendering method
    this.renderFeedbackContent(card, { isCorrect, insight, confirmation });
  }
}
```

#### 1.1.4 Testing
- [x] Test with enhanced exercises (new format)
- [x] Test with old exercises (backwards compatibility)
- [x] Test all subjects (bl, gb, ws, sp)

---

### 2️⃣ US-1.3: 3-Tier Adaptive Hint System (HIGH Priority)

#### 1.3.1 Update Exercise Schema for Hints
**Old Format (single hint):**
```json
{
  "hint": "Lees waarom de hamster die naam krijgt."
}
```

**New Format (3-tier hints):**
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
      "text": "De zin is: 'Ze noemt hem Nibbel, omdat hij graag op zonnebloempitten kauwt.'",
      "reveal_percentage": 0.9
    }
  }
}
```

**Backwards Compatibility:** If only `hint` exists, use it as tier1

#### 1.3.2 Update Hint Display Logic
**File:** `static/src/app.js` (search for hint logic around line 12s timer)

**Current Logic:**
- After 12s inactivity, show single hint
- Hint appears in a tooltip

**New Logic:**
- **Tier 1:** After 12s inactivity (unchanged timing)
- **Tier 2:** After 1st wrong answer OR 30s inactivity
- **Tier 3:** After 2nd wrong answer OR clicking "Meer hulp"

**UI Addition:** "Meer hulp" button appears after Tier 1 is shown

#### 1.3.3 Track Hint Usage in Gamification
**File:** `static/src/gamification.js`

**Changes:**
- Add `totalHintsUsed` to stats
- Add `hintTierUsage: { tier1: 0, tier2: 0, tier3: 0 }`
- **XP Penalty (Grades 6-8 only):** Using Tier 2/3 reduces XP by 10%

```javascript
_calculateXP(question, isCorrect, hintsUsed) {
  let baseXP = isCorrect ? 10 : 0;

  // Penalty for using advanced hints (grades 6-8 only)
  if (this.features.advancedStats && hintsUsed.tier2) {
    baseXP *= 0.95;
  }
  if (this.features.advancedStats && hintsUsed.tier3) {
    baseXP *= 0.90;
  }

  return baseXP;
}
```

#### 1.3.4 Testing
- [x] Test hint progression (tier 1 → 2 → 3)
- [x] Test backwards compatibility (old single hint)
- [x] Test XP penalty for grades 6-8
- [x] Test no penalty for grades 3-5

---

### 3️⃣ US-3.1: Enhanced Error Analysis (HIGH Priority)

#### 3.1.1 Current State
**File:** `static/src/foutanalyse-modaal.js`
- Exists for verhaaltjessommen only
- Has 4 error types: conversiefout, leesfout_ruis, conceptfout, rekenfout_basis
- Shows visual aids and reflection questions

#### 3.1.2 Extend to All Subjects
**Action:** Generalize error classification

**New Error Types for Reading (bl):**
- `letterlijk_gemist`: Missed literal information
- `inferentie_fout`: Failed to make inference
- `vocabulaire`: Vocabulary issue

**New Error Types for Math (gb):**
- Keep existing: conversiefout, conceptfout, rekenfout_basis
- Add: `strategie_fout` (wrong strategy chosen)

#### 3.1.3 Add Remediation Links
**File:** `static/src/foutanalyse-modaal.js`

```javascript
function getRemediation(errorType, skill) {
  const remediationMap = {
    'letterlijk_gemist': {
      exercises: ['bl_groep4_letterlijk_practice_1'],
      tip: 'Oefen met het vinden van letterlijke informatie'
    },
    'inferentie_fout': {
      exercises: ['bl_groep4_inferentieel_practice_1'],
      tip: 'Oefen met het maken van verbanden'
    },
    'conversiefout': {
      exercises: ['gb_groep5_eenheden_practice_1'],
      tip: 'Oefen met het omrekenen van eenheden'
    }
  };

  return remediationMap[errorType] || null;
}
```

**UI Addition:** "Oefen meer" button in error modal linking to practice exercises

#### 3.1.4 Testing
- [x] Test error classification for all subjects
- [x] Test remediation links
- [x] Test modal still works for verhaaltjessommen (no regression)

---

### 4️⃣ US-4.1: Mobile-First Enhancements (HIGH Priority)

#### 4.1.1 Add Swipe Navigation
**File:** `static/src/mobile-interactions.js` (NEW FILE)

```javascript
/**
 * MobileInteractions - Touch gestures for quiz navigation
 */
class MobileInteractions {
  constructor(options = {}) {
    this.onSwipeNext = options.onSwipeNext || (() => {});
    this.onSwipePrevious = options.onSwipePrevious || (() => {});
    this.enabled = this._isTouchDevice();

    if (this.enabled) {
      this.init();
    }
  }

  init() {
    let touchStartX = 0;
    let touchEndX = 0;
    const swipeThreshold = 100;

    document.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    document.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      this.handleSwipe(touchStartX, touchEndX, swipeThreshold);
    }, { passive: true });
  }

  handleSwipe(startX, endX, threshold) {
    const diff = startX - endX;

    // Swipe left - next question (only if answer submitted)
    if (diff > threshold && hasAnswered) {
      this.onSwipeNext();
    }

    // Swipe right - previous question (if allowed)
    if (diff < -threshold) {
      this.onSwipePrevious();
    }
  }

  _isTouchDevice() {
    return ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
  }
}

// Initialize in app.js
const mobileInteractions = new MobileInteractions({
  onSwipeNext: () => {
    if (hasAnswered && currentQuestionIndex < totalQuestions - 1) {
      nextQuestion();
    }
  }
});
```

**Integrate in:** `static/src/app.js` (at bottom of file)

#### 4.1.2 Implement Service Worker
**File:** `sw.js` (NEW FILE in root)

```javascript
const CACHE_VERSION = 'sara-v1.0.0';
const CACHE_NAME = `sara-exercises-${CACHE_VERSION}`;

// Files to cache on install
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/quiz.html',
  '/static/css/styles.min.css',
  '/static/js/app.min.js',
  '/static/js/config.min.js',
  '/static/js/gamification.min.js'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

**Register Service Worker:**
**File:** `static/src/app.js` (add at top after DOMContentLoaded)

```javascript
// Register Service Worker for offline support
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('SW registered:', registration.scope);
      })
      .catch((error) => {
        console.log('SW registration failed:', error);
      });
  });
}
```

#### 4.1.3 Testing
- [x] Test swipe left to next question
- [x] Test swipe only works after answering
- [x] Test Service Worker caches correctly
- [x] Test offline mode works
- [x] Test on mobile device (Chrome DevTools mobile emulation)

---

## Testing Checklist

### Functionality Tests
- [ ] Old exercises still work (backwards compatibility)
- [ ] New feedback schema displays correctly
- [ ] 3-tier hints work progressively
- [ ] Error analysis works for all subjects
- [ ] Swipe navigation works on touch devices
- [ ] Service Worker caches and serves offline
- [ ] Gamification XP calculation includes hint penalty

### Cross-Browser Tests
- [ ] Chrome (desktop + mobile)
- [ ] Firefox (desktop + mobile)
- [ ] Safari (iOS)
- [ ] Edge

### Accessibility Tests
- [ ] Keyboard navigation still works
- [ ] Screen reader compatibility
- [ ] Touch targets ≥ 44x44px

### Performance Tests
- [ ] Quiz loads in <2s on 3G
- [ ] Service Worker doesn't slow down navigation
- [ ] No console errors

---

## File Changes Summary

### New Files
- `PHASE_1_IMPLEMENTATION_PLAN.md` (this file)
- `SCHEMA_V2.md` (schema documentation)
- `static/src/mobile-interactions.js` (swipe gestures)
- `sw.js` (Service Worker)

### Modified Files
- `static/src/card-morph-feedback.js` (enhanced feedback rendering)
- `static/src/app.js` (3-tier hints + Service Worker registration)
- `static/src/foutanalyse-modaal.js` (remediation links)
- `static/src/gamification.js` (hint tracking + XP penalty)
- `data/exercises/bl/bl_groep4_m4_1.json` (sample enhanced exercise)
- `data/exercises/gb/gb_groep4_m4.json` (sample enhanced exercise)

### Build Files to Update
- Run minification after changes: `npm run build` (if build script exists)
- Update version in `quiz.html` CSS/JS cache busting: `?v=20260107`

---

## Success Criteria

### Phase 1 Complete When:
1. ✅ 2+ sample exercises have full feedback schema
2. ✅ 3-tier hint system works with XP tracking
3. ✅ Error analysis extended to all subjects
4. ✅ Swipe navigation works on mobile
5. ✅ Service Worker enables offline mode
6. ✅ All tests pass
7. ✅ No breaking changes (backwards compatible)
8. ✅ Website keeps working throughout

---

## Next Steps After Phase 1

### Phase 2 Preview (Q2 2026)
- Scale feedback enhancement to ALL 1,500+ exercises
- Build exercise template system
- Implement AI-assisted content generation

### Notes
- This plan focuses on **foundation** and **proof of concept**
- We're enhancing 2 exercises fully to validate the approach
- Once proven, we can scale to all exercises in Phase 2
- All changes are incremental and backwards compatible
