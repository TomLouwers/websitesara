# 🧪 Gamification Testing Instructions

## Quick Start

### 1. Server is Running
The test server is already running at:
```
http://localhost:8080
```

### 2. Two Ways to Test

#### Option A: Interactive Test Harness (Recommended)
Open in your browser:
```
http://localhost:8080/test-gamification.html
```

**Features:**
- ✅ One-click test buttons
- ✅ Simulate quiz completions
- ✅ View real-time stats
- ✅ See mini-profile preview
- ✅ Test achievements, challenges, level-ups
- ✅ Console output shows all events

**Quick Test Flow:**
1. Click "Initialize Gamification"
2. Click "Simulate Quiz (8/10 correct)" a few times
3. Watch notifications appear
4. Check stats update in real-time
5. Click "Force Level Up" to see celebration

---

#### Option B: Real Quiz Flow
Open in your browser:
```
http://localhost:8080/index.html
```

**Manual Test Flow:**
1. Clear localStorage (F12 → Console → `localStorage.clear()`)
2. Select "Basisvaardigheden Groep 3 - Midden niveau"
3. Complete the quiz (answer 5-10 questions)
4. Check results page for:
   - XP notification (+XX XP)
   - Achievement unlock (first exercise badge)
   - Profile display in header
5. Start another quiz:
   - Mini-profile should appear in header
   - Streak notification should show

---

## 📊 What to Verify

### ✅ Core Features
- [ ] XP awarded after completing quiz
- [ ] Level displayed correctly
- [ ] Mini-profile shows in header
- [ ] Notifications appear at correct times
- [ ] Data persists in localStorage

### ✅ Notifications
- [ ] XP gain notification (500ms after quiz)
- [ ] Achievement unlock notification (2s delay)
- [ ] Challenge complete notification (3s delay)
- [ ] Level-up celebration modal (2s delay)
- [ ] Streak update popup (1s after quiz start)

### ✅ localStorage Keys
Check browser console (F12):
```javascript
localStorage.getItem('sara_player_profile')
localStorage.getItem('sara_achievements')
localStorage.getItem('sara_daily_streak')
localStorage.getItem('sara_challenges')
localStorage.getItem('sara_stats')
```

All should return valid JSON.

---

## 🎯 Key Test Cases

### Test 1: First Quiz Ever
**Expected:**
- Profile created with Level 1, 0 XP
- First achievement unlocked: "Eerste Stappen"
- Streak set to 1 day
- Daily challenges generated

### Test 2: Perfect Score
**Expected:**
- Base XP: 10 per correct answer
- Perfect bonus: +50 XP
- Achievement: "Perfectionist" (if first perfect)

### Test 3: Level Up
**Expected:**
- Modal appears with celebration
- Shows new level number
- Lists new unlocks (themes/avatars at levels 3, 5, 7, etc.)
- Auto-closes after 5 seconds

### Test 4: Daily Challenges
**Expected:**
- Complete 3 exercises → "Oefen Meester" challenge done (+50 XP)
- Get 80% accuracy → "Nauwkeurigheid Pro" challenge done (+30 XP)

### Test 5: Persistence
**Expected:**
- Close browser tab
- Reopen quiz
- All progress maintained (level, XP, achievements, streak)

---

## 🔍 Debugging

### Check Console for Errors
Browser console should show:
```
✅ Gamification system initialized
📊 Updating gamification with results: {...}
🎮 Gamification feedback: {...}
```

**Should NOT show:**
- ❌ Undefined variables
- ❌ Failed to parse JSON
- ❌ Cannot read property of undefined

### Inspect localStorage
```javascript
// View all gamification data
Object.keys(localStorage)
  .filter(k => k.startsWith('sara_'))
  .forEach(k => {
    console.log(k, JSON.parse(localStorage.getItem(k)));
  });
```

### Check Network Tab
Verify files load successfully:
- `static/css/gamification.css` → 200 OK
- `static/src/gamification.js` → 200 OK
- `static/src/gamification-ui.js` → 200 OK

---

## 📝 Quick Test Script

Paste in browser console:
```javascript
// Quick Gamification Test
(function() {
    console.log('🧪 Running Gamification Tests...\n');

    const keys = ['sara_player_profile', 'sara_achievements',
                  'sara_daily_streak', 'sara_challenges', 'sara_stats'];
    let pass = 0, fail = 0;

    keys.forEach(key => {
        const data = localStorage.getItem(key);
        if (data) {
            try {
                JSON.parse(data);
                console.log(`✅ ${key}`);
                pass++;
            } catch (e) {
                console.error(`❌ ${key}: Invalid JSON`);
                fail++;
            }
        } else {
            console.warn(`⚠️  ${key}: Not found`);
        }
    });

    console.log(`\n📊 Results: ${pass} passed, ${fail} failed`);
})();
```

---

## 🎮 Expected Behavior Summary

### After Completing 1 Quiz:
- XP: ~80-100 (depending on score)
- Level: 1
- Achievements: 1 (First Steps)
- Streak: 1 day

### After Completing 5 Quizzes:
- XP: ~400-500
- Level: 3-4
- Achievements: 3-5 (First Steps, Century Club, Streak badges, etc.)
- Challenges: 1-2 completed

### After Reaching Level 5:
- Unlocks: Space theme
- Total XP: ~749+
- Achievements: 5-8

---

## 📞 Troubleshooting

### Issue: Notifications Not Appearing
**Solution:**
- Check browser console for errors
- Verify `gamificationManager` and `gamificationUI` are defined
- Check if quiz is completing successfully

### Issue: Mini-Profile Not Showing
**Solution:**
- Verify quiz.html includes the container: `<div id="gamification-mini-profile"></div>`
- Check CSS is loading: `static/css/gamification.css`
- Verify initialization code runs in DOMContentLoaded

### Issue: Data Not Persisting
**Solution:**
- Check localStorage is enabled in browser
- Verify localStorage keys exist
- Check for JSON parse errors

---

## ✅ Success Criteria

Test is successful if:
1. ✅ No JavaScript errors in console
2. ✅ All 5 localStorage keys created
3. ✅ XP awarded correctly (10 per correct + bonuses)
4. ✅ Notifications appear at correct times
5. ✅ Level-up celebration shows
6. ✅ Mini-profile renders in header
7. ✅ Data persists after browser refresh

---

**Ready to test!** 🚀

Start with: http://localhost:8080/test-gamification.html
