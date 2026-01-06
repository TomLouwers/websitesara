# Gamification System Test Plan

## Test Environment
- **Server:** http://localhost:8080
- **Test Date:** 2026-01-06
- **Branch:** claude/improve-edtech-platform-zf8Zb

---

## Pre-Test Setup

### 1. Clear localStorage (Fresh Start)
Open browser console and run:
```javascript
localStorage.clear();
sessionStorage.clear();
console.log('✅ Storage cleared');
```

---

## Test Cases

### Test 1: Initial Load - No Gamification Data

**Steps:**
1. Navigate to `http://localhost:8080/index.html`
2. Select any quiz (e.g., "Basisvaardigheden Groep 3 - Midden niveau")
3. Click to start quiz

**Expected Results:**
- ✅ Quiz loads without errors
- ✅ No mini-profile visible yet (first visit)
- ✅ Console shows: `✅ Gamification system initialized`

**Verify in Console:**
```javascript
// Check localStorage keys
console.log('Profile:', JSON.parse(localStorage.getItem('sara_player_profile')));
console.log('Achievements:', JSON.parse(localStorage.getItem('sara_achievements')));
console.log('Streak:', JSON.parse(localStorage.getItem('sara_daily_streak')));
console.log('Challenges:', JSON.parse(localStorage.getItem('sara_challenges')));
console.log('Stats:', JSON.parse(localStorage.getItem('sara_stats')));
```

---

### Test 2: Complete First Quiz - Verify XP Gain

**Steps:**
1. Answer 5-10 questions in the quiz
2. Submit answers (mix of correct/incorrect)
3. Reach results page

**Expected Results:**
- ✅ Results page displays normally
- ✅ XP notification appears: "+XX XP" (after 500ms delay)
- ✅ Text: "X vragen goed!"
- ✅ Profile updated in localStorage

**Verify in Console:**
```javascript
const profile = JSON.parse(localStorage.getItem('sara_player_profile'));
console.log('Level:', profile.level);
console.log('XP:', profile.xp);
console.log('Total Exercises:', profile.totalExercisesCompleted);
```

**XP Calculation:**
- Base: 10 XP per correct answer
- Perfect bonus: +50 XP if all correct
- Expected for 8/10 correct: 80 XP

---

### Test 3: Achievement Unlock - First Exercise

**Steps:**
1. Complete first quiz (from Test 2)
2. Wait on results page

**Expected Results:**
- ✅ Achievement notification appears (after 2s delay)
- ✅ Shows: 🎯 Badge icon
- ✅ Text: "Badge Behaald!"
- ✅ Title: "Eerste Stappen" (first exercise completed)

**Verify in Console:**
```javascript
const achievements = JSON.parse(localStorage.getItem('sara_achievements'));
console.log('Unlocked:', achievements.unlocked);
// Should include: 'first_exercise'
```

---

### Test 4: Daily Streak Tracking

**Steps:**
1. Return to home page
2. Start another quiz
3. Check for streak notification

**Expected Results:**
- ✅ Streak notification appears (after 1s delay)
- ✅ Shows: ✨ emoji
- ✅ Text: "Welkom terug!"
- ✅ Shows: "Dag 1"

**Verify in Console:**
```javascript
const streak = JSON.parse(localStorage.getItem('sara_daily_streak'));
console.log('Current Streak:', streak.currentStreak);
console.log('Last Active:', streak.lastActiveDate);
// currentStreak should be 1
// lastActiveDate should be today: "2026-01-06"
```

---

### Test 5: Daily Challenges

**Steps:**
1. Complete 3 different quizzes

**Expected Results:**
- ✅ Challenge progress updates
- ✅ After 3rd quiz: Challenge completion notification
- ✅ Shows: 🎯 icon, "Uitdaging Voltooid!"
- ✅ Shows: "+50 XP" (challenge reward)

**Verify in Console:**
```javascript
const challenges = JSON.parse(localStorage.getItem('sara_challenges'));
console.log('Daily Challenges:', challenges.daily);
// Find challenge with type: 'exercises'
// progress should be 3, target should be 3, completed: true
```

---

### Test 6: Level Up Celebration

**Steps:**
1. Complete enough quizzes to reach 100 XP (Level 2)
2. Level 1 → 2 requires: 100 XP
3. Complete quizzes until XP > 100

**Expected Results:**
- ✅ Level-up modal appears (after 2s delay)
- ✅ Shows: 🎉 animation
- ✅ Text: "Level Omhoog!"
- ✅ Shows new level number: "2"
- ✅ Text: "Je bent nu level 2!"
- ✅ Auto-closes after 5 seconds

**Verify in Console:**
```javascript
const profile = JSON.parse(localStorage.getItem('sara_player_profile'));
console.log('Level:', profile.level);
console.log('XP:', profile.xp);
console.log('XP to Next Level:', profile.xpToNextLevel);
// level should be 2
// xpToNextLevel should be 149 (level 2→3 = 249 total, minus current XP)
```

---

### Test 7: Mini-Profile Display

**Steps:**
1. After completing first quiz, start a new quiz
2. Check header area

**Expected Results:**
- ✅ Mini-profile visible in header (right side)
- ✅ Shows avatar image
- ✅ Shows level badge
- ✅ Shows XP progress bar
- ✅ Shows streak: 🔥1

**Visual Check:**
- Profile should be compact (mini version)
- Should not overlap with other header elements

---

### Test 8: Category Statistics

**Steps:**
1. Complete quizzes from different categories (gb, mk, etc.)
2. Check stats in localStorage

**Expected Results:**
- ✅ Stats tracked per category
- ✅ Stats tracked per grade
- ✅ Stats tracked per date

**Verify in Console:**
```javascript
const stats = JSON.parse(localStorage.getItem('sara_stats'));
console.log('By Category:', stats.byCategory);
console.log('By Grade:', stats.byGrade);
console.log('By Date:', stats.byDate);
// Each should have correct/total counts
```

---

### Test 9: Perfect Score Achievement

**Steps:**
1. Complete a quiz with 100% correct answers

**Expected Results:**
- ✅ Perfect score bonus: +50 XP
- ✅ Achievement unlock notification (if first perfect)
- ✅ Achievement: "perfectionist" unlocked

**Verify in Console:**
```javascript
const achievements = JSON.parse(localStorage.getItem('sara_achievements'));
console.log('Unlocked:', achievements.unlocked);
// Should include: 'perfectionist' (if first perfect score)
```

---

### Test 10: Persistence Across Sessions

**Steps:**
1. Complete several quizzes (gain XP, unlock achievements)
2. Close browser tab
3. Reopen: http://localhost:8080/index.html
4. Start new quiz

**Expected Results:**
- ✅ Progress persists (level, XP, achievements)
- ✅ Mini-profile shows correct data
- ✅ Streak maintained (same day)
- ✅ Challenges progress maintained

**Verify in Console:**
```javascript
// All localStorage data should still exist
const profile = JSON.parse(localStorage.getItem('sara_player_profile'));
console.log('Persisted Profile:', profile);
```

---

## Edge Cases

### Edge Case 1: localStorage Disabled

**Steps:**
1. Disable localStorage in browser settings
2. Start quiz

**Expected Results:**
- ✅ Quiz works normally (gamification disabled)
- ✅ Console shows warning (optional)
- ✅ No errors or crashes

---

### Edge Case 2: Invalid localStorage Data

**Steps:**
```javascript
localStorage.setItem('sara_player_profile', 'invalid json');
```
2. Reload page and start quiz

**Expected Results:**
- ✅ Gamification resets to defaults
- ✅ No errors or crashes

---

## Console Checks

### No JavaScript Errors
```javascript
// Console should show:
✅ Gamification system initialized
📊 Updating gamification with results: {...}
🎮 Gamification feedback: {...}

// Should NOT show:
❌ Any error messages
❌ Undefined variables
❌ Failed to load resources
```

---

## Performance Checks

### Resource Loading
- ✅ gamification.css loads (< 100ms)
- ✅ gamification.js loads (< 200ms)
- ✅ gamification-ui.js loads (< 200ms)

### Notification Timing
- ✅ XP notification: 500ms delay
- ✅ Level-up: 2s delay (after XP notification)
- ✅ Achievements: 2s delay (staggered 3.5s apart)
- ✅ Challenges: 3s delay (staggered 3.5s apart)

---

## Success Criteria

All tests pass if:
1. ✅ No JavaScript errors in console
2. ✅ All localStorage keys created correctly
3. ✅ XP calculated and awarded correctly
4. ✅ Achievements unlock at right milestones
5. ✅ Notifications display at correct times
6. ✅ Mini-profile renders correctly
7. ✅ Data persists across sessions
8. ✅ Daily streak tracking works
9. ✅ Challenges progress correctly
10. ✅ Level-up celebrations trigger

---

## Quick Test Script

Run this in browser console for automated checks:

```javascript
// Quick Gamification Test
(function() {
    console.log('🧪 Running Gamification Tests...\n');

    // Test 1: Check localStorage keys
    const keys = ['sara_player_profile', 'sara_achievements', 'sara_daily_streak', 'sara_challenges', 'sara_stats'];
    const results = {
        pass: 0,
        fail: 0
    };

    keys.forEach(key => {
        const data = localStorage.getItem(key);
        if (data) {
            try {
                const parsed = JSON.parse(data);
                console.log(`✅ ${key}:`, parsed);
                results.pass++;
            } catch (e) {
                console.error(`❌ ${key}: Invalid JSON`);
                results.fail++;
            }
        } else {
            console.warn(`⚠️  ${key}: Not found (might be first visit)`);
        }
    });

    // Test 2: Verify profile structure
    const profile = JSON.parse(localStorage.getItem('sara_player_profile'));
    if (profile) {
        const requiredFields = ['xp', 'level', 'totalExercisesCompleted'];
        requiredFields.forEach(field => {
            if (profile[field] !== undefined) {
                console.log(`✅ Profile has ${field}:`, profile[field]);
                results.pass++;
            } else {
                console.error(`❌ Profile missing ${field}`);
                results.fail++;
            }
        });
    }

    // Test 3: Verify managers exist
    if (typeof gamificationManager !== 'undefined') {
        console.log('✅ gamificationManager initialized');
        results.pass++;
    } else {
        console.error('❌ gamificationManager not found');
        results.fail++;
    }

    if (typeof gamificationUI !== 'undefined') {
        console.log('✅ gamificationUI initialized');
        results.pass++;
    } else {
        console.error('❌ gamificationUI not found');
        results.fail++;
    }

    // Summary
    console.log('\n📊 Test Results:');
    console.log(`   Passed: ${results.pass}`);
    console.log(`   Failed: ${results.fail}`);
    console.log(`   Total:  ${results.pass + results.fail}`);

    if (results.fail === 0) {
        console.log('\n✅ ALL TESTS PASSED!');
    } else {
        console.log('\n❌ Some tests failed. Check output above.');
    }
})();
```
