# Gamification System Documentation

Complete client-side gamification system for OefenPlatform using **localStorage only** - no database, no backend required.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Integration Guide](#integration-guide)
- [API Reference](#api-reference)
- [localStorage Structure](#localstorage-structure)
- [Best Practices](#best-practices)

---

## Overview

The gamification system provides persistent cross-session rewards and progression using **100% client-side storage**. Students earn XP, unlock achievements, maintain daily streaks, and complete challenges—all without requiring a server or database.

###Design Principles

✅ **Static-first**: No backend, no database, no API calls
✅ **Privacy**: All data stays on device (localStorage)
✅ **Positive-only**: No punishment, no loss framing
✅ **Age-appropriate**: Features gated by grade (3-8)
✅ **Complementary**: Works alongside existing `SessionRewardManager`

---

## Features

### 🎯 Core Features (All Grades)

| Feature | Description | Storage |
|---------|-------------|---------|
| **XP & Leveling** | Earn XP, level up, unlock rewards | `sara_player_profile` |
| **Achievement Badges** | 15+ badges for milestones | `sara_achievements` |
| **Daily Streaks** | Track consecutive days practicing | `sara_daily_streak` |
| **Daily Challenges** | 3-4 challenges reset each day | `sara_challenges` |
| **Stats Dashboard** | Performance by category/grade | `sara_stats` |

### 📊 Grade-Specific Features

| Grades | Additional Features |
|--------|---------------------|
| **3-5** | Basic XP, streaks, simple badges |
| **4-8** | Daily challenges, weekly goals, avatar customization |
| **6-8** | Advanced stats, leaderboard (per-device), prestige system |

---

## Quick Start

### 1. Include Required Files

```html
<!-- In your HTML <head> -->
<link rel="stylesheet" href="/static/css/gamification.css">

<!-- Before </body> -->
<script src="/static/src/gamification.js"></script>
<script src="/static/src/gamification-ui.js"></script>
```

### 2. Initialize

```javascript
// Initialize gamification manager
const gamification = new GamificationManager({
    grade: 4,                // Student's grade level (3-8)
    playerName: 'Leerling'   // Optional player name
});

// Initialize UI components
const gamificationUI = new GamificationUI(gamification);
```

### 3. Display UI Components

```javascript
// Render player profile in sidebar
gamificationUI.renderPlayerProfile('profile-container');

// Render daily challenges
gamificationUI.renderDailyChallenges('challenges-container');

// Render achievements gallery
gamificationUI.renderAchievements('achievements-container');

// Render stats dashboard
gamificationUI.renderStatsDashboard('stats-container');
```

### 4. Track Exercise Completion

```javascript
// When student completes an exercise
const results = {
    exerciseId: 'gb_groep4_m4_1',
    category: 'gb',
    grade: 4,
    correctCount: 8,
    totalCount: 10,
    timeSpentSeconds: 300,  // 5 minutes
    maxStreak: 6,
    hintsUsed: 2,
    perfectScore: false
};

const gamificationResults = gamification.completeExercise(results);

// Show notifications
if (gamificationResults.leveledUp) {
    gamificationUI.showLevelUp(gamificationResults.newLevel);
}

for (const achievement of gamificationResults.newAchievements) {
    gamificationUI.showAchievementUnlock(achievement);
}

for (const challenge of gamificationResults.completedChallenges) {
    gamificationUI.showChallengeComplete(challenge);
}

gamificationUI.showXPGain(gamificationResults.xpEarned, 'Oefening voltooid!');
```

---

## Architecture

### Data Flow

```
Student Action
    ↓
SessionRewardManager (session-only rewards)
    ↓
GamificationManager (persistent tracking)
    ↓
localStorage (5 keys, all JSON)
    ↓
GamificationUI (display components)
```

### Separation of Concerns

| Component | Responsibility | Persistence |
|-----------|---------------|-------------|
| `SessionRewardManager` | In-session streaks, shields, multipliers | Session-only |
| `GamificationManager` | Long-term progression, achievements, challenges | localStorage |
| `GamificationUI` | Display, animations, notifications | None |

**Why Both?**
- **Session rewards**: Encourage immediate engagement during a practice session
- **Gamification**: Build long-term habits and provide sense of progression

---

## Integration Guide

### Example: Quiz Page Integration

```html
<!-- quiz.html -->
<!DOCTYPE html>
<html>
<head>
    <!-- ... existing head content ... -->
    <link rel="stylesheet" href="/static/css/gamification.css">
</head>
<body>
    <!-- Existing quiz interface -->
    <div class="quiz-container">
        <!-- Quiz content -->
    </div>

    <!-- Add gamification sidebar -->
    <div class="gamification-sidebar">
        <div id="mini-profile"></div>
        <div id="daily-challenges"></div>
        <div id="quick-stats"></div>
    </div>

    <!-- Scripts -->
    <script src="/static/src/app.js"></script>
    <script src="/static/src/session-rewards.js"></script>
    <script src="/static/src/gamification.js"></script>
    <script src="/static/src/gamification-ui.js"></script>

    <script>
        // Initialize gamification
        const gamification = new GamificationManager({
            grade: getCurrentStudentGrade(), // Your function
            playerName: getPlayerName() // Optional
        });

        const gamificationUI = new GamificationUI(gamification);

        // Render UI components
        gamificationUI.renderMiniProfile('mini-profile');
        gamificationUI.renderDailyChallenges('daily-challenges');

        // Show daily streak update (first visit of the day)
        const summary = gamification.getPlayerSummary();
        if (summary.streak.current > 0) {
            gamificationUI.showStreakUpdate(summary.streak.current);
        }

        // When exercise completes
        function onExerciseComplete(exerciseResults) {
            // Existing session reward logic
            const sessionReward = sessionRewardManager.recordAnswer(correct);

            // Add gamification tracking
            const gamificationResult = gamification.completeExercise({
                exerciseId: currentExercise.id,
                category: currentExercise.category,
                grade: currentExercise.grade,
                correctCount: exerciseResults.correctCount,
                totalCount: exerciseResults.totalCount,
                timeSpentSeconds: exerciseResults.timeSpent,
                maxStreak: sessionReward.bestStreak,
                hintsUsed: exerciseResults.hintsUsed,
                perfectScore: exerciseResults.perfectScore
            });

            // Show gamification notifications
            if (gamificationResult.leveledUp) {
                gamificationUI.showLevelUp(gamificationResult.newLevel);
            }

            if (gamificationResult.newAchievements.length > 0) {
                for (const achievement of gamificationResult.newAchievements) {
                    gamificationUI.showAchievementUnlock(achievement);
                }
            }

            if (gamificationResult.completedChallenges.length > 0) {
                for (const challenge of gamificationResult.completedChallenges) {
                    gamificationUI.showChallengeComplete(challenge);
                }
            }

            // Refresh UI
            gamificationUI.renderMiniProfile('mini-profile');
            gamificationUI.renderDailyChallenges('daily-challenges');
        }
    </script>
</body>
</html>
```

### Example: Dashboard Page

```html
<!-- dashboard.html - Full stats and achievements view -->
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="/static/css/gamification.css">
</head>
<body>
    <div class="dashboard-container">
        <div id="player-profile"></div>
        <div id="achievements-gallery"></div>
        <div id="stats-dashboard"></div>
        <div id="challenges-overview"></div>
    </div>

    <script src="/static/src/gamification.js"></script>
    <script src="/static/src/gamification-ui.js"></script>
    <script>
        const gamification = new GamificationManager({ grade: 4 });
        const ui = new GamificationUI(gamification);

        // Render all components
        ui.renderPlayerProfile('player-profile');
        ui.renderAchievements('achievements-gallery');
        ui.renderStatsDashboard('stats-dashboard');
        ui.renderDailyChallenges('challenges-overview');
    </script>
</body>
</html>
```

---

## API Reference

### GamificationManager

#### Constructor

```javascript
const gm = new GamificationManager(options)
```

**Options:**
- `grade` (number): Student grade level (3-8). Determines feature gating.
- `playerName` (string, optional): Player display name. Default: "Leerling"

#### Methods

##### `completeExercise(results)`

Record completed exercise and update all tracking.

**Parameters:**
```javascript
{
    exerciseId: string,       // Exercise identifier
    category: string,         // Exercise category (gb, ws, etc.)
    grade: number,            // Exercise grade level
    correctCount: number,     // Number of correct answers
    totalCount: number,       // Total questions in exercise
    timeSpentSeconds: number, // Time spent on exercise
    maxStreak: number,        // Best streak during exercise
    hintsUsed: number,        // Number of hints used (optional)
    perfectScore: boolean     // Whether all answers were correct (optional)
}
```

**Returns:**
```javascript
{
    xpEarned: number,                    // XP earned from this exercise
    leveledUp: boolean,                  // Whether player leveled up
    newLevel: number|null,               // New level if leveled up
    completedChallenges: Array,          // Challenges completed
    newAchievements: Array,              // Achievements unlocked
    totalXP: number,                     // Player's total XP
    currentLevel: number,                // Current level
    dailyStreak: number                  // Current daily streak
}
```

##### `getPlayerSummary()`

Get complete player state for UI rendering.

**Returns:**
```javascript
{
    enabled: boolean,
    profile: {
        name: string,
        level: number,
        xp: number,
        xpToNextLevel: number,
        xpProgress: number  // Percentage 0-100
    },
    streak: {
        current: number,    // Current consecutive days
        longest: number,    // Best ever streak
        totalDays: number   // Total days practiced
    },
    achievements: {
        total: number,              // Total unlocked
        unlocked: Array<string>,    // Achievement IDs
        recentlyUnlocked: Array     // Last 5 achievements
    },
    challenges: {
        daily: Array,               // Daily challenges
        weekly: Array,              // Weekly challenges (grades 4+)
        completedToday: number      // Completed today
    },
    stats: {
        totalExercises: number,
        totalQuestions: number,
        totalCorrect: number,
        accuracy: number,           // Percentage
        timeSpent: number,          // Minutes
        perfectScores: number
    }
}
```

##### `resetAll()`

Clear all gamification data (shows confirmation dialog).

##### `exportData()`

Export all gamification data for backup.

**Returns:**
```javascript
{
    version: "2.0.0",
    exportedAt: string,  // ISO timestamp
    data: {
        profile: Object,
        achievements: Object,
        dailyStreak: Object,
        challenges: Object,
        stats: Object
    }
}
```

##### `importData(exportedData)`

Import previously exported data.

**Parameters:**
- `exportedData`: Object returned from `exportData()`

---

### GamificationUI

#### Constructor

```javascript
const ui = new GamificationUI(gamificationManager)
```

#### Rendering Methods

##### `renderPlayerProfile(containerId)`

Render full player profile with avatar, XP bar, and stats.

##### `renderMiniProfile(containerId)`

Render compact profile for header/navbar.

##### `renderDailyChallenges(containerId)`

Render daily challenges with progress bars.

##### `renderAchievements(containerId)`

Render achievements gallery (all achievements, locked/unlocked).

##### `renderStatsDashboard(containerId)`

Render comprehensive statistics dashboard.

#### Notification Methods

##### `showLevelUp(newLevel)`

Display level-up celebration modal.

##### `showAchievementUnlock(achievement)`

Display achievement unlock notification (toast).

##### `showChallengeComplete(challenge)`

Display challenge completion notification.

##### `showXPGain(xp, reason)`

Display XP gain notification.

##### `showStreakUpdate(currentStreak)`

Display daily streak update popup.

---

## localStorage Structure

All data stored in 5 localStorage keys:

### `sara_player_profile`

```json
{
    "playerName": "Leerling",
    "grade": 4,
    "createdAt": 1704460800000,
    "lastActiveAt": 1704547200000,
    "xp": 450,
    "level": 5,
    "xpToNextLevel": 249,
    "totalExercisesCompleted": 15,
    "totalQuestionsAnswered": 150,
    "totalCorrectAnswers": 120,
    "totalTimeSpentMinutes": 75,
    "unlockedThemes": ["default", "space"],
    "unlockedAvatars": ["student", "detective"],
    "currentTheme": "space",
    "currentAvatar": "detective",
    "prestigeLevel": 0,
    "prestigePoints": 0
}
```

### `sara_achievements`

```json
{
    "unlocked": [
        "first_exercise",
        "getting_started",
        "streak_3",
        "century_club"
    ],
    "progress": {},
    "lastUnlockedAt": 1704547200000
}
```

### `sara_daily_streak`

```json
{
    "currentStreak": 5,
    "longestStreak": 7,
    "lastActiveDate": "2026-01-05",
    "totalDaysActive": 12,
    "streakFrozen": false,
    "freezesAvailable": 0
}
```

### `sara_challenges`

```json
{
    "generatedDate": "2026-01-05",
    "daily": [
        {
            "id": "daily_2026-01-05_exercises",
            "type": "exercises",
            "title": "Oefen Meester",
            "description": "Voltooi 3 oefeningen vandaag",
            "target": 3,
            "progress": 2,
            "completed": false,
            "reward": { "xp": 50, "badge": null }
        }
    ],
    "weekly": []
}
```

### `sara_stats`

```json
{
    "byCategory": {
        "gb": { "correct": 80, "total": 100 },
        "ws": { "correct": 40, "total": 50 }
    },
    "byGrade": {
        "4": { "correct": 120, "total": 150 }
    },
    "byDate": {
        "2026-01-05": { "correct": 10, "total": 15, "exercises": 2 }
    },
    "fastestStreak": 10,
    "perfectScores": 3,
    "totalHintsUsed": 25
}
```

---

## Best Practices

### ✅ DO

1. **Initialize once per page**
   ```javascript
   const gamification = new GamificationManager({ grade: 4 });
   ```

2. **Call `completeExercise()` only once per exercise**
   ```javascript
   // When exercise finishes, not after every question
   gamification.completeExercise(results);
   ```

3. **Use grade-appropriate features**
   ```javascript
   // Check features availability
   if (gamification.features.dailyChallenges) {
       ui.renderDailyChallenges('container');
   }
   ```

4. **Handle localStorage unavailable**
   ```javascript
   const summary = gamification.getPlayerSummary();
   if (!summary.enabled) {
       // Show fallback UI or message
       console.warn('Gamification disabled (localStorage not available)');
   }
   ```

5. **Refresh UI after actions**
   ```javascript
   gamification.completeExercise(results);
   // Refresh displays
   ui.renderMiniProfile('header-profile');
   ui.renderDailyChallenges('challenges');
   ```

### ❌ DON'T

1. **Don't call completeExercise() multiple times**
   ```javascript
   // BAD: Duplicate tracking
   gamification.completeExercise(results);
   gamification.completeExercise(results); // ❌
   ```

2. **Don't rely on localStorage being available**
   ```javascript
   // BAD: Assumes storage works
   const level = gamification.profile.level; // ❌ Might fail

   // GOOD: Check first
   const summary = gamification.getPlayerSummary();
   if (summary.enabled) {
       const level = summary.profile.level;
   }
   ```

3. **Don't modify localStorage directly**
   ```javascript
   // BAD: Bypass manager
   localStorage.setItem('sara_player_profile', '...'); // ❌

   // GOOD: Use manager methods
   gamification.completeExercise(results); // ✅
   ```

4. **Don't show all notifications at once**
   ```javascript
   // BAD: Notification spam
   ui.showXPGain(10);
   ui.showXPGain(20);
   ui.showXPGain(30); // ❌

   // GOOD: Notifications queue automatically
   // Just call them - they'll show sequentially
   ```

---

## XP Calculation

Base XP formula per exercise:

```javascript
let xp = 0;

// Base: 10 XP per correct answer
xp += correctCount * 10;

// Accuracy bonus
if (accuracy >= 90%) xp += 50;  // Excellent
if (accuracy >= 75%) xp += 30;  // Good
if (accuracy >= 60%) xp += 15;  // Okay

// Speed bonus (< 30 sec/question)
if (avgTimePerQuestion < 30) xp += 20;

// Streak bonus
if (maxStreak >= 5) xp += 25;
if (maxStreak >= 10) xp += 50;

// Perfect score
if (perfectScore) xp += 100;
```

**Examples:**
- 10 questions, 8 correct, 80% accuracy, 25 sec/q, streak 6:
  - Base: 80 XP
  - Accuracy: 30 XP
  - Speed: 20 XP
  - Streak: 25 XP
  - **Total: 155 XP**

- 10 questions, 10 correct, 100%, 20 sec/q, streak 10:
  - Base: 100 XP
  - Accuracy: 50 XP
  - Speed: 20 XP
  - Streak: 75 XP (50 + 25)
  - Perfect: 100 XP
  - **Total: 345 XP**

---

## Leveling System

XP required for each level increases by 20%:

```
Level 1: 0 XP
Level 2: 100 XP
Level 3: 220 XP  (100 × 1.2)
Level 4: 364 XP  (220 × 1.2)
Level 5: 537 XP  (364 × 1.2)
...
Level 10: 1,031 XP
Level 20: 6,628 XP
```

**Level Unlocks:**
- Level 3: Detective avatar
- Level 5: Space theme
- Level 7: Scientist avatar
- Level 10: Underwater theme
- Level 12: Astronaut avatar
- Level 15: Forest theme

---

## Achievements List

| ID | Title | Description | Condition |
|----|-------|-------------|-----------|
| `first_exercise` | Eerste Stap | Voltooi je eerste oefening | 1 exercise |
| `getting_started` | Aan de Slag! | Voltooi 5 oefeningen | 5 exercises |
| `streak_3` | Op Dreef | Oefen 3 dagen op rij | 3-day streak |
| `streak_7` | Week Warrior | Oefen 7 dagen op rij | 7-day streak |
| `streak_14` | Twee Weken Kampioen | Oefen 14 dagen op rij | 14-day streak |
| `streak_30` | Maand Meester | Oefen 30 dagen op rij | 30-day streak |
| `century_club` | Honderd Club | 100 vragen goed | 100 correct |
| `five_hundred` | Vijfhonderd! | 500 vragen goed | 500 correct |
| `thousand` | Duizend! | 1000 vragen goed | 1000 correct |
| `perfectionist` | Perfectionist | 1 perfecte score | 1 perfect |
| `flawless_five` | Vijf Foutloos | 5 perfecte scores | 5 perfect |
| `level_5` | Level 5 Legende | Bereik level 5 | Level 5 |
| `level_10` | Level 10 Held | Bereik level 10 | Level 10 |
| `level_20` | Level 20 Kampioen | Bereik level 20 | Level 20 |
| `math_master` | Reken Meester | 90% bij Getallen | 90% in gb |
| `word_wizard` | Woorden Wizard | 90% bij Woordenschat | 90% in ws |

---

## Troubleshooting

### localStorage Not Available

**Symptom:** `summary.enabled` is `false`

**Causes:**
- Private/incognito mode
- Browser settings block storage
- Storage quota exceeded

**Solution:**
```javascript
const summary = gamification.getPlayerSummary();
if (!summary.enabled) {
    showMessage('Voortgang kan niet worden opgeslagen. Controleer je browserinstellingen.');
}
```

### Progress Lost After Browser Clear

**Issue:** Student clears browser data, loses progress

**Solutions:**
1. **Export/Import**:
   ```javascript
   // Provide export button
   const backup = gamification.exportData();
   downloadAsJSON(backup, 'sara-backup.json');

   // Import from backup
   gamification.importData(backupData);
   ```

2. **Educate users**: Add notice that clearing browser data will reset progress

---

## Future Enhancements

Possible additions (still static/localStorage):

- **Streak Freeze**: Power-up to protect 1-day missed streak
- **Friend Challenges**: Share challenge codes (no backend needed)
- **Custom Avatars**: Upload custom avatar images (stored as base64)
- **Theme Editor**: Create custom themes (color schemes in localStorage)
- **Progress Charts**: Visual charts using Chart.js (all client-side)

---

## Summary

✅ **100% client-side** - No server or database
✅ **5 localStorage keys** - All data in JSON
✅ **15+ achievements** - Unlockable badges
✅ **Daily challenges** - Fresh every day
✅ **XP & leveling** - Progressive rewards
✅ **Daily streaks** - Habit building
✅ **Age-appropriate** - Grade-specific features
✅ **Privacy-first** - Data never leaves device

**Perfect for a static educational platform!** 🎉
