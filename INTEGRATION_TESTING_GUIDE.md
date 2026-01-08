# Phase 1 Integration - Testing Guide

**Status:** ✅ Integration Complete - Ready for Testing
**Date:** January 7, 2026
**Branch:** `claude/phase-1-foundation-setup-XfTiV`

---

## 🎯 What Was Integrated

### Core Integration Changes
1. ✅ Service Worker registered in app.js
2. ✅ Mobile Interactions initialized for swipe navigation
3. ✅ Enhanced feedback rendering integrated (Schema V2.0)
4. ✅ quiz.html updated with new scripts

---

## 🧪 Testing Checklist

### 1. Basic Functionality (Backwards Compatibility)

#### Test Old Exercises
**File:** Any existing exercise (e.g., `bl_groep4_m4_1.json`)

**Steps:**
1. Navigate to index.html
2. Select any subject (e.g., Begrijpend Lezen, Groep 4)
3. Start quiz
4. Answer a question correctly ✓
5. Answer a question incorrectly ✗

**Expected:**
- ✅ Quiz loads normally
- ✅ Questions display correctly
- ✅ Feedback shows (legacy format: "Top gedaan!" / "Kijk nog eens goed")
- ✅ Next button works
- ✅ Progress bar updates
- ✅ Score calculation correct
- ✅ No console errors

---

### 2. Enhanced Feedback (Schema V2.0)

#### Test Enhanced Reading Exercise
**File:** `data/exercises/bl/bl_groep4_enhanced_sample.json`

**How to Load:**
You'll need to temporarily modify index.html or create a direct link:

**Option A: Modify index.html temporarily**
1. Find the "Begrijpend Lezen Groep 4" button
2. Update `data-json` attribute to: `data/exercises/bl/bl_groep4_enhanced_sample.json`
3. Start quiz

**Option B: Use browser console**
```javascript
// On index.html, open browser console
sessionStorage.setItem('quizState', JSON.stringify({
    currentSubject: 'bl',
    currentQuiz: { metadata: { grade: 4, category: 'bl' } },
    currentQuestionIndex: 0,
    score: 0,
    wrongAnswers: [],
    totalQuestions: 2,
    lovaClickCount: 0,
    categoryProgress: {},
    useTextGrouping: false
}));

// Then fetch and set the quiz
fetch('data/exercises/bl/bl_groep4_enhanced_sample.json')
    .then(r => r.json())
    .then(data => {
        const state = JSON.parse(sessionStorage.getItem('quizState'));
        state.currentQuiz = data[0];  // First exercise
        state.randomizedQuestions = data[0].questions;
        state.totalQuestions = data[0].questions.length;
        sessionStorage.setItem('quizState', JSON.stringify(state));
        window.location.href = 'quiz.html';
    });
```

**Test Correct Answer:**
1. Question 1: "Waarom noemt Sofie de hamster Nibbel?"
2. Select: **B - Hij knabbelt graag aan pitten**
3. Click Submit

**Expected:**
- ✨ Header: "Helemaal goed!"
- 📝 Explanation: "Goed gevonden! In de tekst staat: 'omdat hij graag op zonnebloempitten kauwt'. Je hebt de belangrijke informatie goed gelezen."
- 💪 Skill Reinforcement: "Je kunt letterlijke informatie goed vinden in de tekst! Deze vaardigheid is heel belangrijk bij het begrijpen van wat je leest."
- ✅ Green background
- ✅ Next button enabled immediately

**Test Incorrect Answer:**
1. Question 1: "Waarom noemt Sofie de hamster Nibbel?"
2. Select: **A - Hij slaapt veel** (wrong)
3. Click Submit

**Expected:**
- 🤔 Header: "Laten we het samen bekijken"
- 📝 Explanation: "Nibbel slaapt wel in het huisje, maar dat is niet de reden voor zijn naam."
- 💡 Tip: "Zoek in de tekst naar het woord 'omdat' na de naam Nibbel."
- 📝 Worked Example (numbered steps):
  1. Lees de zin: 'Ze noemt hem Nibbel, omdat...'
  2. Het woord 'omdat' geeft de reden voor iets
  3. Wat staat er na 'omdat'? → 'hij graag op zonnebloempitten kauwt'
  4. Knabbelen = nibbelen → daarom heet hij Nibbel!
  5. Antwoord: B - Hij knabbelt graag aan pitten.
- ⏱️ Next button disabled for 1500ms ("Lees dit even…")
- ✅ Orange/yellow background

#### Test Enhanced Math Exercise
**File:** `data/exercises/gb/gb_groep4_enhanced_sample.json`

**Test Math Rendering:**
1. Load the enhanced math exercise
2. Question should display: "$47 + 28 = ?$" (rendered with KaTeX)
3. Answer incorrectly to see worked example with math notation

**Expected:**
- ✅ Math notation renders beautifully (KaTeX)
- ✅ Worked example shows steps with math: $40 + 20 = 60$, $7 + 8 = 15$
- ✅ Step-by-step breakdown is clear
- ✅ Per-option feedback explains the specific mistake

---

### 3. Mobile Interactions

#### Test Swipe Navigation
**Device:** Tablet, phone, or Chrome DevTools mobile emulation

**Steps:**
1. Open quiz.html on mobile device
2. Answer a question (submit answer)
3. Swipe left on the screen

**Expected:**
- ✅ Visual indicator shows "➡️" during swipe
- ✅ Swipe feedback appears: "Volgende →"
- ✅ Moves to next question
- ✅ Swipe only works after answering (not before)
- ✅ No accidental vertical scroll blocking

**Test Swipe Before Answering:**
1. Start quiz
2. Try to swipe left (before submitting answer)

**Expected:**
- ❌ Swipe does NOT move to next question
- ✅ Normal page scroll still works

---

### 4. Service Worker & Offline Support

#### Test Cache Registration
**Steps:**
1. Open quiz.html
2. Open Chrome DevTools (F12)
3. Go to Console tab
4. Look for message: `[App] Service Worker registered: ...`

**Expected:**
- ✅ Service Worker registered successfully
- ✅ No console errors

#### Test Offline Mode
**Steps:**
1. Load website once while online (to populate cache)
2. Navigate through quiz once
3. Open Chrome DevTools → Application → Service Workers
4. Check "Offline" checkbox
5. Refresh page (F5)

**Expected:**
- ✅ Page loads from cache
- ✅ Static assets (CSS, JS) load
- ✅ Previously viewed exercises still work
- ✅ No "Unable to connect" errors

**Test Cache Contents:**
1. Chrome DevTools → Application → Cache Storage
2. Expand "sara-exercises-v1.0.0-phase1"

**Expected:**
- ✅ HTML files cached (index.html, quiz.html)
- ✅ CSS files cached
- ✅ JS files cached
- ✅ Sample exercises cached:
  - bl_groep4_enhanced_sample.json
  - gb_groep4_enhanced_sample.json

---

## 🔍 What to Check in Browser Console

### On Page Load
```
[App] Service Worker registered: http://localhost/
[App] Mobile interactions initialized
✅ Gamification system initialized
```

### On Swipe Gesture
```
[MobileInteractions] Swipe left detected - next
[App] Swipe next detected
```

### On Enhanced Exercise Load
```
(No errors about missing feedback fields)
```

---

## ⚠️ Troubleshooting

### Issue: Service Worker not registering
**Solution:** Make sure you're using:
- HTTPS in production, OR
- localhost for development
- Service Workers don't work on file:// protocol

### Issue: Swipe navigation not working
**Check:**
- Mobile interactions script loaded? `static/src/mobile-interactions.js`
- Console shows initialization? Look for "[App] Mobile interactions initialized"
- Are you on a touch device? Check console for "[MobileInteractions] Initialized"

### Issue: Enhanced feedback not showing
**Check:**
- Are you testing with enhanced exercise files?
- Does the question have `feedback` field in JSON?
- Console errors? Open DevTools → Console
- card-morph-feedback.js loaded? Check Network tab

### Issue: "MobileInteractions is not defined"
**Solution:**
- Ensure `mobile-interactions.js` is loaded BEFORE `app.js` in quiz.html
- Check script order in quiz.html

### Issue: Math notation not rendering
**Check:**
- KaTeX loaded? Look for `<link>` tag with katex.min.css
- renderMathInText function defined? Check if app.js loaded

---

## 🎨 Visual Differences

### Old Feedback (Legacy)
```
✓ Top gedaan!
"Goed gedaan!"
"Je antwoord: B"
```

### New Feedback (Schema V2.0)
```
✨ Helemaal goed!

[Highlighted box]
Goed gevonden! In de tekst staat: 'omdat hij graag
op zonnebloempitten kauwt'. Je hebt de belangrijke
informatie goed gelezen.

[Green box with border]
💪 Wat je goed doet: Je kunt letterlijke informatie goed
vinden in de tekst! Deze vaardigheid is heel belangrijk
bij het begrijpen van wat je leest.
```

---

## 📊 Test Results Template

Copy this to your notes:

```
## Phase 1 Integration Test Results

Date: ___________
Tester: ___________
Browser: ___________
Device: ___________

### ✅ Pass / ❌ Fail

[ ] Old exercises load correctly
[ ] Old feedback displays (legacy)
[ ] Enhanced reading exercise loads
[ ] Enhanced feedback displays
[ ] Worked examples render
[ ] Math notation renders (KaTeX)
[ ] Swipe left works on mobile
[ ] Swipe blocked before answering
[ ] Service Worker registered
[ ] Offline mode works
[ ] No console errors

### Notes:
_______________________________________________
_______________________________________________
_______________________________________________
```

---

## 🐛 Known Limitations

### Current Limitations:
1. Only 2 enhanced sample exercises (1 reading, 1 math)
2. Hint tracking not yet implemented in gamification
3. 3-tier hints not yet fully implemented (Schema V2.0 ready, UI pending)
4. No minified versions yet (using source files)

### To Be Completed:
- [ ] 3-tier hint display UI
- [ ] Hint usage tracking in gamification
- [ ] Build/minify updated files
- [ ] Scale enhanced feedback to all 1,500+ exercises (Phase 2)

---

## 📈 Success Criteria

### Phase 1 Complete When:
- ✅ All existing exercises work (backwards compatibility)
- ✅ 2 enhanced exercises demonstrate new schema
- ✅ Mobile swipe navigation works
- ✅ Service Worker caches assets
- ✅ Offline mode functional
- ✅ No console errors
- ✅ Enhanced feedback displays correctly
- ✅ Math rendering works

---

## 🚀 Next Steps After Testing

1. **If tests pass:**
   - Create pull request
   - Deploy to staging
   - User acceptance testing
   - Production deployment

2. **If issues found:**
   - Document issues
   - Fix critical bugs
   - Re-test
   - Iterate

3. **Phase 2 planning:**
   - Scale to all exercises
   - AI content generation
   - 3-tier hints full implementation
   - Build validation pipeline

---

**Testing Support:**
- Documentation: PHASE_1_SUMMARY.md
- Schema: SCHEMA_V2.md
- Implementation: PHASE_1_IMPLEMENTATION_PLAN.md

Happy testing! 🎉
