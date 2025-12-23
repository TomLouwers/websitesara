# Session-Based Reward System Documentation

## Overview

A comprehensive, psychologically-safe reward system designed for Dutch primary school children (grades 3-8) in a no-login, session-based educational web app.

**Core Philosophy**: No negative points, no punishment, no loss framing. Pure positive reinforcement within a single session.

## Architecture

### Core Components

1. **SessionRewardManager** (`session-rewards.js`)
   - State machine for tracking rewards, streaks, shields, multipliers
   - Session-only persistence (resets on page refresh)
   - Age-appropriate feature gating
   - Optional localStorage (never relied upon)

2. **StreakAnimationController** (`streak-animations.js`)
   - Visual feedback and animations
   - Non-blocking animations (≤ 600ms)
   - Respects `prefers-reduced-motion`
   - Graduated reward ladder

3. **CSS Animations** (`rewards.css`)
   - All visual styles for reward UI
   - Mobile-responsive
   - Dark mode support
   - Print-friendly

### Integration Points

- **app.js**: Main quiz logic integration
- **quiz.html**: UI elements for reward display
- **config.js**: Configuration (optional, mostly embedded in modules)

## Scoring Rules

### Base Points

- **Correct answer**: +1 point
- **Incorrect answer**: 0 points (never subtract)

### Streak Bonuses

| Streak | Bonus Points | Emoji | Title | Tier |
|--------|-------------|-------|-------|------|
| 3 | +2 | 🔥 | Op dreef! | Encouraging |
| 5 | +3 | 🔍 | Super-speurder! | Skill-based |
| 10 | +5 | 🚀 | Onverslaanbaar vandaag! | Celebration |

### Multipliers (Grades 6-8 Only)

- Activates at 3-streak
- Applies **x2** to bonus points only (not base points)
- Visual indicator shows during active multiplier
- Silently deactivates on incorrect answer (no negative animation)

### Shield Mechanic (Grades 6-8 Only)

- **Unlock condition**: 5 total correct answers
- **Max per session**: 1 shield
- **Function**: Protects streak once when incorrect answer given
- **Consumption**: Immediate, single-use
- **Visual feedback**: "🛡️ Bonus gered!" animation

## Age-Appropriate Feature Gating

### Grades 3-5 (Ages 6-10)

✅ Enabled:
- Streak cards (3, 5, 10)
- Star animations
- Simple celebrations
- Point burst effects

❌ Disabled:
- Combo multipliers
- Shield mechanic
- Complex animations

### Grades 6-8 (Ages 10-12)

✅ All of grades 3-5, plus:
- Visual combo multiplier (x2)
- Shield mechanic
- More sophisticated animations

## Animation System

### Graduated Reward Ladder

| Event | Visual | Audio | Duration |
|-------|--------|-------|----------|
| Correct answer | ⭐ subtle ping | Soft "ding" | 300ms |
| 3-streak | 🔥 Card + glow | Warm chord | 600ms |
| 5-streak | 🔍 Card + pulse | Success tone | 600ms |
| 10-streak | 🚀 Card + confetti | Celebration | 600ms |

### Point Burst Animation

1. **Burst phase** (200ms): Particles spread from answer area
2. **Fly phase** (400ms): Particles fly to star in navigation
3. **Arrival** (300ms): Star pulses on point collection

Total duration: **600ms** (non-blocking, skippable)

### Near-Miss Feedback

Triggered when streak = 4 and incorrect answer:

```
💪 Bijna! Nog één goede en je zit weer in de bonus.
```

**Design rules**:
- No sad sounds
- No red visuals
- No "streak verloren" messaging
- Encouraging tone only

## Meta Rewards (Session-Based)

### Stickers

Unlocked during session, shown on end-of-quiz screen:

| Sticker ID | Emoji | Title | Unlock Condition |
|------------|-------|-------|------------------|
| streak_3 | 🔥 | Op dreef! | 3-streak reached |
| streak_5 | 🔍 | Super-speurder! | 5-streak reached |
| streak_10 | 🚀 | Onverslaanbaar! | 10-streak reached |
| perfect_start | ⭐ | Perfect begin | First 5 all correct |
| shield_hero | 🛡️ | Schild-held | Shield used successfully |

**Copy for stickers**:
```
Wat je deze ronde hebt ontdekt:
[Sticker grid]
Blijft bewaard op dit apparaat.
```

### Progressive Star

Visual indicator of session performance (in top navigation):

| Level | Accuracy | Visual |
|-------|----------|--------|
| Empty | < 50% or < 5 answers | Gray, dim |
| Bronze | 50-74% | Bronze glow |
| Silver | 75-89% | Silver glow |
| Gold | 90%+ | Gold glow + sparkle |

## State Machine

### State Variables

```javascript
{
  // Core scoring
  score: 0,
  bonusPoints: 0,

  // Streak tracking
  currentStreak: 0,
  bestStreak: 0,
  correctAnswers: 0,
  totalAnswers: 0,

  // Milestones
  milestonesReached: { 3: false, 5: false, 10: false },

  // Shield (session-only)
  shieldAvailable: false,
  shieldUsed: false,
  shieldEarnedAt: null,

  // Multiplier (grades 6-8)
  multiplierActive: false,
  multiplierValue: 1,

  // Near-miss tracking
  lastStreakBeforeMiss: 0,

  // Meta rewards
  stickersUnlocked: [],
  starLevel: 'empty',

  // Session metadata
  sessionStartTime: Date.now(),
  sessionId: 'session_...'
}
```

### State Transitions

#### Correct Answer

```
1. Increment correctAnswers, currentStreak
2. Award +1 base point
3. Check streak milestones (3, 5, 10)
4. If milestone reached:
   - Calculate bonus points
   - Apply multiplier if active (grades 6-8)
   - Show streak card animation
5. Check shield unlock (at 5 correct)
6. Update meta rewards (stickers, star level)
7. Play point burst animation
```

#### Incorrect Answer

```
1. Check if shield available and streak >= 3
2. If shield available:
   - Consume shield
   - Protect streak
   - Show "Bonus gered!" animation
3. Else:
   - Check near-miss (streak == 4)
   - If near-miss: show encouragement
   - Reset streak to 0
   - Silently deactivate multiplier (no animation)
```

## Copy Guidelines

### Session Framing

Always use copy that indicates session-only scope:

✅ **Good**:
- "in deze oefening"
- "deze ronde"
- "vandaag"
- "Blijft bewaard op dit apparaat"

❌ **Avoid**:
- "permanent"
- "altijd"
- "je hebt verdiend" (implies ownership)
- "je collectie"

### Emotional Safety

✅ **Good**:
- "Je bent goed bezig!"
- "Bijna!"
- "Blijf oefenen en je wordt nóg beter!"
- "Elke vraag maakt je sterker!"

❌ **Avoid**:
- "Fout!"
- "Streak verloren"
- "Probeer het beter te doen"
- Any comparison language

## Implementation Details

### Initialization

```javascript
// Initialize reward system (in app.js DOMContentLoaded)
sessionRewardManager = new SessionRewardManager({
    grade: 4, // extracted from URL or quiz data
    enableLocalStorage: false, // never relied upon
    enableAudio: true
});

streakAnimationController = new StreakAnimationController({
    grade: 4,
    enableAudio: true
});

// Link audio manager
streakAnimationController.setAudioManager(audioManager);
```

### Processing Answers

```javascript
// On correct answer
const feedback = sessionRewardManager.processAnswer(true);
await streakAnimationController.playCorrectFeedback(feedback);

// On incorrect answer
const feedback = sessionRewardManager.processAnswer(false);
await streakAnimationController.playIncorrectFeedback(feedback);
```

### End of Quiz

```javascript
// Get session summary
const summary = sessionRewardManager.getSessionSummary();

// Render stickers
streakAnimationController.renderStickers(
    summary.stickers,
    (id) => sessionRewardManager.getStickerMetadata(id)
);
```

## HTML Elements Required

### Quiz Page

```html
<!-- Progress star (existing element updated) -->
<span id="progressStar">⭐</span>
<span id="totalCorrectNew">0</span>

<!-- Reward UI elements -->
<div id="streakCard"></div>
<div id="pointBurstContainer"></div>
<div id="shieldBadge"></div>
<div id="multiplierBadge"></div>
<div id="nearMissCard"></div>
```

### Results Page

```html
<div id="stickerCollection" style="display: none;">
    <!-- Dynamically populated -->
</div>
```

## Accessibility

### Reduced Motion

System respects `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
    .point-particle {
        display: none !important;
    }
}
```

### Audio Control

- Audio can be muted via settings
- TTS fallback for missing audio files
- Volume levels: soft (0.3), medium (0.6), loud (0.9)

### Screen Readers

All visual feedback includes semantic HTML and ARIA labels:

```html
<div role="status" aria-live="polite" id="streakCard">
    <!-- Announced by screen readers -->
</div>
```

## Performance

### Animation Budget

- **Single animation**: ≤ 600ms
- **Non-blocking**: Never prevents user interaction
- **Skippable**: User can click through
- **Hardware-accelerated**: Uses `transform` and `opacity`

### Memory Management

- Particles cleaned up after animation
- Event listeners properly removed
- No memory leaks in long sessions

## Testing Checklist

### Unit Tests

- [ ] SessionRewardManager state transitions
- [ ] Correct point calculations
- [ ] Multiplier logic (grades 6-8)
- [ ] Shield consumption
- [ ] Near-miss detection
- [ ] Sticker unlocking
- [ ] Star level progression

### Integration Tests

- [ ] Answer processing flow
- [ ] Animation sequencing
- [ ] Audio playback with fallback
- [ ] Grade-based feature gating
- [ ] localStorage optional persistence

### Visual Tests

- [ ] All animations render correctly
- [ ] Mobile responsive layout
- [ ] Dark mode compatibility
- [ ] Reduced motion respected
- [ ] Print styles work

### UX Tests

- [ ] Animations feel joyful, not overwhelming
- [ ] Timing feels natural
- [ ] No animation blocking interaction
- [ ] Copy is age-appropriate
- [ ] No negative framing anywhere

## Edge Cases Handled

1. **Page refresh**: Session resets cleanly
2. **Shared device**: No cross-user contamination
3. **Multiple tabs**: Each session independent
4. **Network failure**: System works offline
5. **Missing audio files**: TTS fallback
6. **Reduced motion**: Simplified feedback
7. **Ancient browsers**: Graceful degradation
8. **Quick answers**: Animations don't stack
9. **Zero answers**: No division by zero errors
10. **Shield at streak 0**: Not triggered

## Future Enhancements (Optional)

Potential additions that maintain safety principles:

- [ ] More sticker varieties (seasonal, subject-specific)
- [ ] Sound pack options (animal sounds, space sounds, etc.)
- [ ] Star constellations (multi-session stars, optional)
- [ ] Print-friendly "achievement certificate"
- [ ] Share-friendly summary card (no personal data)

## Troubleshooting

### Animations not appearing

1. Check CSS file loaded: `rewards.css`
2. Check JS modules loaded: `session-rewards.js`, `streak-animations.js`
3. Check `initializeRewardSystem()` called
4. Check DOM elements exist

### Points not calculating correctly

1. Check `processAnswerWithRewards()` is called
2. Verify grade detection logic
3. Check multiplier only applies to bonus points
4. Verify streak reset logic

### Shield not working

1. Check grade >= 6
2. Verify 5 correct answers reached
3. Check shield hasn't been used already
4. Verify streak >= 3 when triggered

## Credits

Designed with love for Dutch primary school children.
Built with safety, joy, and learning at the core.

---

**Version**: 1.0.0
**Last Updated**: 2024-01-20
**Maintainer**: Educational Platform Team
