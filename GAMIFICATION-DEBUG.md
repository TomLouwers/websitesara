## 🔍 Gamification Debug Checklist

You're not seeing gamification features during your GB quiz. Let's troubleshoot:

---

## Step 1: Check Which Page You're On

**Press F12 to open Developer Tools, then check the URL bar:**

### If you see: `index.html` or just `/`
**This is the problem!** The old index.html has quizzes embedded but NO gamification.

**Solution:** We need to check if the quizzes are launching through quiz.html or staying on index.html.

### If you see: `quiz.html`
Good! You're on the right page. Continue to Step 2.

---

## Step 2: Check Browser Console (F12)

**Look for these messages:**

### ✅ GOOD - You should see:
```
✅ Gamification system initialized
   Storage available: true
```

### ❌ BAD - If you see:
```
❌ ReferenceError: GamificationManager is not defined
❌ Failed to load resource: gamification.js
❌ localStorage is not available
```

**Action:** Tell me which error you see.

---

## Step 3: Check Network Tab (F12 → Network)

**Filter by "gamification" and reload the page.**

### Should see these files load with status 200:
- `gamification.css` → 200 OK
- `gamification.js` → 200 OK
- `gamification-ui.js` → 200 OK

### If you see 404 errors:
Files are missing or not loading correctly.

---

## Step 4: Check localStorage

**In Console (F12), run:**
```javascript
console.log('Storage available:', typeof(Storage) !== 'undefined');
console.log('Keys:', Object.keys(localStorage).filter(k => k.startsWith('sara_')));
```

### Before your first quiz:
```
Storage available: true
Keys: []  // Empty is normal
```

### After completing a quiz:
```
Storage available: true
Keys: ['sara_player_profile', 'sara_achievements', 'sara_daily_streak', 'sara_challenges', 'sara_stats']
```

---

## Step 5: Where to Look for Gamification

### During Quiz (on quiz.html):

**Look in TOP RIGHT of header:**
```
┌─────────────────────────────────┐
│  [Avatar]  Level 2  🔥 3 days   │
│  [=======-----] 150/249 XP      │
└─────────────────────────────────┘
```

**NOTE:** On your VERY FIRST quiz, this won't appear yet. It shows starting from quiz #2.

### After Completing Quiz (results page):

**Look for notifications appearing on screen:**

1. **XP Notification** (500ms after results load):
   ```
   ┌──────────────────┐
   │   +80 XP         │
   │ 8 vragen goed!   │
   └──────────────────┘
   ```

2. **Achievement** (2 seconds after results):
   ```
   ┌────────────────────────┐
   │   🏆 Badge Behaald!    │
   │   Eerste Stappen       │
   │ Voltooi je eerste quiz │
   └────────────────────────┘
   ```

---

## Quick Test Script

**Paste this in Console (F12) while on quiz.html:**

```javascript
// Check if gamification loaded
console.log('=== GAMIFICATION DEBUG ===');
console.log('GamificationManager exists:', typeof GamificationManager !== 'undefined');
console.log('GamificationUI exists:', typeof GamificationUI !== 'undefined');
console.log('gamificationManager initialized:', typeof gamificationManager !== 'undefined' && gamificationManager !== null);
console.log('gamificationUI initialized:', typeof gamificationUI !== 'undefined' && gamificationUI !== null);

// Check localStorage
const keys = ['sara_player_profile', 'sara_achievements', 'sara_daily_streak', 'sara_challenges', 'sara_stats'];
keys.forEach(key => {
    const data = localStorage.getItem(key);
    console.log(key + ':', data ? 'EXISTS ✓' : 'NOT FOUND');
});

// If initialized, show current state
if (typeof gamificationManager !== 'undefined' && gamificationManager !== null) {
    const summary = gamificationManager.getPlayerSummary();
    console.log('Current Level:', summary.profile.level);
    console.log('Current XP:', summary.profile.xp);
    console.log('Exercises Completed:', summary.stats.totalExercises);
}
```

---

## Common Issues & Solutions

### Issue 1: "I'm on index.html, not quiz.html"
**Problem:** The quiz is embedded in index.html (old flow)
**Solution:** We need to update index.html to redirect to quiz.html

### Issue 2: "Console shows GamificationManager is not defined"
**Problem:** Scripts not loading
**Solution:** Check Network tab - files might be 404ing

### Issue 3: "Console shows 'Storage available: false'"
**Problem:** localStorage disabled in browser
**Solution:** Enable localStorage in browser settings

### Issue 4: "I completed a quiz but see no notifications"
**Problem:** Check if you're on the results page or if there are console errors
**Solution:** Run the debug script above and share results

---

## What to Tell Me

Please run the debug script above and tell me:

1. **What URL are you on?** (index.html or quiz.html)
2. **Any console errors?** (red text in console)
3. **Output of the debug script?**
4. **Did you complete the quiz and reach the results page?**

This will help me identify the exact issue!
