/**
 * SessionRewardManager - Session-based reward and streak system
 *
 * DESIGN PRINCIPLES:
 * - No negative points
 * - No punishment
 * - No loss framing
 * - Session-only persistence (resets on page reload)
 * - Age-appropriate feature gating
 * - Positive reinforcement only
 *
 * @version 1.0.0
 */

class SessionRewardManager {
    constructor(options = {}) {
        this.options = {
            grade: options.grade || 4, // groep 3-8
            enableLocalStorage: options.enableLocalStorage || false,
            enableAudio: options.enableAudio !== false,
            ...options
        };

        // Session-only state (resets on refresh)
        this.state = {
            // Core scoring
            score: 0,
            bonusPoints: 0,

            // Streak tracking
            currentStreak: 0,
            bestStreak: 0,
            correctAnswers: 0,
            totalAnswers: 0,

            // Streak milestones reached this session
            milestonesReached: {
                3: false,
                5: false,
                10: false
            },

            // Shield mechanic (session-only, max 1)
            shieldAvailable: false,
            shieldUsed: false,
            shieldEarnedAt: null,

            // Multiplier state (grades 6-8 only)
            multiplierActive: false,
            multiplierValue: 1,

            // Near-miss tracking
            lastStreakBeforeMiss: 0,

            // Meta rewards (session-based)
            stickersUnlocked: [],
            starLevel: 'empty', // empty, bronze, silver, gold

            // Session metadata
            sessionStartTime: Date.now(),
            sessionId: this._generateSessionId()
        };

        // Streak thresholds and rewards
        this.STREAK_THRESHOLDS = {
            3: { bonus: 2, emoji: '🔥', title: 'Op dreef!', tier: 'encouraging' },
            5: { bonus: 3, emoji: '🔍', title: 'Super-speurder!', tier: 'skill' },
            10: { bonus: 5, emoji: '🚀', title: 'Onverslaanbaar vandaag!', tier: 'celebration' }
        };

        // Age-gated features
        this.features = this._initializeFeatures();

        // Optional local storage (never relied upon)
        this.storage = this.options.enableLocalStorage ? new SessionStorage() : null;
    }

    /**
     * Initialize age-appropriate features
     */
    _initializeFeatures() {
        const grade = this.options.grade;

        return {
            // Grades 3-5: Basic features
            streakCards: grade >= 3,
            starAnimations: grade >= 3,
            simpleCelebrations: grade >= 3,

            // Grades 6-8: Advanced features
            comboMultipliers: grade >= 6,
            shieldMechanic: grade >= 6,
            complexAnimations: grade >= 6
        };
    }

    /**
     * Generate unique session ID
     */
    _generateSessionId() {
        return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Process answer and update state
     * @param {boolean} isCorrect - Whether the answer was correct
     * @returns {Object} - Feedback object with all reward information
     */
    processAnswer(isCorrect) {
        this.state.totalAnswers++;

        if (isCorrect) {
            return this._handleCorrectAnswer();
        } else {
            return this._handleIncorrectAnswer();
        }
    }

    /**
     * Handle correct answer
     */
    _handleCorrectAnswer() {
        this.state.correctAnswers++;
        this.state.currentStreak++;

        // Update best streak
        if (this.state.currentStreak > this.state.bestStreak) {
            this.state.bestStreak = this.state.currentStreak;
        }

        // Base points
        const basePoints = 1;
        this.state.score += basePoints;

        // Check for streak bonuses
        const streakReward = this._checkStreakMilestone();

        // Check for shield unlock (at 5 correct, if not already earned)
        const shieldUnlocked = this._checkShieldUnlock();

        // Build feedback object
        const feedback = {
            type: 'correct',
            basePoints: basePoints,
            bonusPoints: 0,
            totalPointsEarned: basePoints,
            currentStreak: this.state.currentStreak,

            // Streak milestone info
            streakMilestone: null,

            // Shield info
            shieldUnlocked: shieldUnlocked,
            shieldAvailable: this.state.shieldAvailable,

            // Multiplier info (grades 6-8)
            multiplierActive: this.state.multiplierActive,
            multiplierValue: this.state.multiplierValue,

            // Session stats
            score: this.state.score,
            correctAnswers: this.state.correctAnswers,
            totalAnswers: this.state.totalAnswers
        };

        // Add streak milestone details if reached
        if (streakReward) {
            const threshold = this.STREAK_THRESHOLDS[streakReward.threshold];
            let bonusPoints = threshold.bonus;

            // Apply multiplier to bonus points only (grades 6-8)
            if (this.features.comboMultipliers && this.state.multiplierActive) {
                bonusPoints *= this.state.multiplierValue;
            }

            this.state.bonusPoints += bonusPoints;
            this.state.score += bonusPoints;

            feedback.bonusPoints = bonusPoints;
            feedback.totalPointsEarned = basePoints + bonusPoints;
            feedback.streakMilestone = {
                threshold: streakReward.threshold,
                emoji: threshold.emoji,
                title: threshold.title,
                tier: threshold.tier,
                bonusPoints: bonusPoints,
                multiplierApplied: this.state.multiplierActive
            };

            // Activate multiplier for next milestone (grades 6-8)
            if (this.features.comboMultipliers && streakReward.threshold === 3) {
                this.state.multiplierActive = true;
                this.state.multiplierValue = 2;
            }
        }

        // Update meta rewards
        this._updateMetaRewards();

        // Optional: save to local storage
        this._saveToStorage();

        return feedback;
    }

    /**
     * Handle incorrect answer
     */
    _handleIncorrectAnswer() {
        // Check for near-miss (had 4 correct, now missing)
        const nearMiss = this.state.currentStreak === 4;

        // Check if shield can protect the streak
        const shieldProtected = this._tryUseShield();

        const feedback = {
            type: 'incorrect',
            basePoints: 0,
            bonusPoints: 0,
            totalPointsEarned: 0,

            // Streak info
            streakBeforeMiss: this.state.currentStreak,
            currentStreak: shieldProtected ? this.state.currentStreak : 0,
            streakProtected: shieldProtected,

            // Near-miss feedback
            nearMiss: nearMiss,
            nearMissMessage: nearMiss ? 'Bijna! Nog één goede en je zit weer in de bonus.' : null,

            // Shield info
            shieldUsed: shieldProtected,
            shieldAvailable: this.state.shieldAvailable,

            // Session stats
            score: this.state.score,
            correctAnswers: this.state.correctAnswers,
            totalAnswers: this.state.totalAnswers
        };

        // Only break streak if shield didn't protect
        if (!shieldProtected) {
            this.state.lastStreakBeforeMiss = this.state.currentStreak;
            this.state.currentStreak = 0;

            // Deactivate multiplier (no negative animation, just silent reset)
            if (this.state.multiplierActive) {
                this.state.multiplierActive = false;
                this.state.multiplierValue = 1;
            }
        }

        // Optional: save to local storage
        this._saveToStorage();

        return feedback;
    }

    /**
     * Check if a streak milestone was reached
     */
    _checkStreakMilestone() {
        const streak = this.state.currentStreak;

        // Check each threshold
        for (const threshold of [10, 5, 3]) {
            if (streak === threshold && !this.state.milestonesReached[threshold]) {
                this.state.milestonesReached[threshold] = true;
                return { threshold };
            }
        }

        return null;
    }

    /**
     * Check if shield should be unlocked
     * Shield unlocks at 5 correct answers (not streak, just total correct)
     */
    _checkShieldUnlock() {
        if (!this.features.shieldMechanic) {
            return false;
        }

        // Unlock shield at 5 correct answers, if not already earned
        if (this.state.correctAnswers === 5 && !this.state.shieldEarnedAt && !this.state.shieldUsed) {
            this.state.shieldAvailable = true;
            this.state.shieldEarnedAt = Date.now();
            return true;
        }

        return false;
    }

    /**
     * Try to use shield to protect streak
     */
    _tryUseShield() {
        if (!this.features.shieldMechanic) {
            return false;
        }

        // Only use shield if:
        // 1. Shield is available
        // 2. Current streak >= 3 (worth protecting)
        // 3. Shield hasn't been used yet
        if (this.state.shieldAvailable && this.state.currentStreak >= 3 && !this.state.shieldUsed) {
            this.state.shieldAvailable = false;
            this.state.shieldUsed = true;
            return true;
        }

        return false;
    }

    /**
     * Update meta rewards (stickers, star level)
     */
    _updateMetaRewards() {
        // Unlock stickers at milestones
        this._updateStickers();

        // Update star level based on performance
        this._updateStarLevel();
    }

    /**
     * Update stickers based on achievements
     */
    _updateStickers() {
        const stickers = this.state.stickersUnlocked;

        // 3-streak sticker
        if (this.state.currentStreak >= 3 && !stickers.includes('streak_3')) {
            stickers.push('streak_3');
        }

        // 5-streak sticker
        if (this.state.currentStreak >= 5 && !stickers.includes('streak_5')) {
            stickers.push('streak_5');
        }

        // 10-streak sticker
        if (this.state.currentStreak >= 10 && !stickers.includes('streak_10')) {
            stickers.push('streak_10');
        }

        // Perfect start (first 5 all correct)
        if (this.state.totalAnswers === 5 && this.state.correctAnswers === 5 && !stickers.includes('perfect_start')) {
            stickers.push('perfect_start');
        }

        // Shield hero (used shield successfully)
        if (this.state.shieldUsed && !stickers.includes('shield_hero')) {
            stickers.push('shield_hero');
        }
    }

    /**
     * Update star level based on accuracy
     */
    _updateStarLevel() {
        if (this.state.totalAnswers < 5) {
            this.state.starLevel = 'empty';
            return;
        }

        const accuracy = this.state.correctAnswers / this.state.totalAnswers;

        if (accuracy >= 0.9) {
            this.state.starLevel = 'gold';
        } else if (accuracy >= 0.75) {
            this.state.starLevel = 'silver';
        } else if (accuracy >= 0.5) {
            this.state.starLevel = 'bronze';
        } else {
            this.state.starLevel = 'empty';
        }
    }

    /**
     * Get current session summary
     */
    getSessionSummary() {
        const accuracy = this.state.totalAnswers > 0
            ? (this.state.correctAnswers / this.state.totalAnswers)
            : 0;

        return {
            // Score
            totalScore: this.state.score,
            basePoints: this.state.correctAnswers,
            bonusPoints: this.state.bonusPoints,

            // Streaks
            bestStreak: this.state.bestStreak,
            milestonesReached: Object.keys(this.state.milestonesReached)
                .filter(k => this.state.milestonesReached[k])
                .map(k => parseInt(k)),

            // Accuracy
            correctAnswers: this.state.correctAnswers,
            totalAnswers: this.state.totalAnswers,
            accuracy: accuracy,

            // Meta rewards
            stickers: this.state.stickersUnlocked,
            starLevel: this.state.starLevel,

            // Shield usage
            shieldUsed: this.state.shieldUsed,

            // Session metadata
            sessionDuration: Date.now() - this.state.sessionStartTime,
            sessionId: this.state.sessionId
        };
    }

    /**
     * Get sticker metadata for display
     */
    getStickerMetadata(stickerId) {
        const metadata = {
            'streak_3': {
                emoji: '🔥',
                title: 'Op dreef!',
                description: '3 goede antwoorden op rij'
            },
            'streak_5': {
                emoji: '🔍',
                title: 'Super-speurder!',
                description: '5 goede antwoorden op rij'
            },
            'streak_10': {
                emoji: '🚀',
                title: 'Onverslaanbaar!',
                description: '10 goede antwoorden op rij'
            },
            'perfect_start': {
                emoji: '⭐',
                title: 'Perfect begin',
                description: 'Eerste 5 vragen allemaal goed'
            },
            'shield_hero': {
                emoji: '🛡️',
                title: 'Schild-held',
                description: 'Je bonus gered met het schild'
            }
        };

        return metadata[stickerId] || null;
    }

    /**
     * Reset session (for new quiz)
     */
    reset() {
        const grade = this.options.grade;
        this.state = {
            score: 0,
            bonusPoints: 0,
            currentStreak: 0,
            bestStreak: 0,
            correctAnswers: 0,
            totalAnswers: 0,
            milestonesReached: { 3: false, 5: false, 10: false },
            shieldAvailable: false,
            shieldUsed: false,
            shieldEarnedAt: null,
            multiplierActive: false,
            multiplierValue: 1,
            lastStreakBeforeMiss: 0,
            stickersUnlocked: [],
            starLevel: 'empty',
            sessionStartTime: Date.now(),
            sessionId: this._generateSessionId()
        };

        this._saveToStorage();
    }

    /**
     * Save state to local storage (optional, never relied upon)
     */
    _saveToStorage() {
        if (!this.storage) {
            return;
        }

        try {
            this.storage.saveSession(this.state);
        } catch (e) {
            // Silent fail - local storage is optional
            console.warn('Local storage save failed (this is OK):', e);
        }
    }

    /**
     * Load state from local storage (optional)
     */
    loadFromStorage() {
        if (!this.storage) {
            return false;
        }

        try {
            const saved = this.storage.loadSession();
            if (saved) {
                this.state = { ...this.state, ...saved };
                return true;
            }
        } catch (e) {
            // Silent fail - local storage is optional
            console.warn('Local storage load failed (this is OK):', e);
        }

        return false;
    }
}

/**
 * Optional session storage helper
 * IMPORTANT: Never relied upon, never promised to user
 */
class SessionStorage {
    constructor() {
        this.key = 'sara_session_rewards';
    }

    saveSession(state) {
        if (!this._isAvailable()) {
            return false;
        }

        try {
            const data = {
                state: state,
                savedAt: Date.now(),
                disclaimer: 'Blijft bewaard op dit apparaat. Kan verloren gaan bij refresh of op gedeelde apparaten.'
            };
            localStorage.setItem(this.key, JSON.stringify(data));
            return true;
        } catch (e) {
            return false;
        }
    }

    loadSession() {
        if (!this._isAvailable()) {
            return null;
        }

        try {
            const data = localStorage.getItem(this.key);
            if (!data) {
                return null;
            }

            const parsed = JSON.parse(data);

            // Only load if saved within last hour (prevent stale data)
            const hourAgo = Date.now() - (60 * 60 * 1000);
            if (parsed.savedAt < hourAgo) {
                this.clearSession();
                return null;
            }

            return parsed.state;
        } catch (e) {
            return null;
        }
    }

    clearSession() {
        if (!this._isAvailable()) {
            return;
        }

        try {
            localStorage.removeItem(this.key);
        } catch (e) {
            // Silent fail
        }
    }

    _isAvailable() {
        try {
            const test = '__localStorage_test__';
            localStorage.setItem(test, test);
            localStorage.removeItem(test);
            return true;
        } catch (e) {
            return false;
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SessionRewardManager, SessionStorage };
}
