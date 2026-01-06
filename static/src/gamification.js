/**
 * GamificationManager - Persistent cross-session gamification system
 *
 * ARCHITECTURE:
 * - 100% client-side (localStorage only)
 * - No database, no backend, no API calls
 * - Works alongside SessionRewardManager
 * - Persists achievements, XP, streaks, challenges across sessions
 * - Age-appropriate feature gating (grades 3-8)
 *
 * STORAGE KEYS:
 * - sara_player_profile: XP, level, unlocks
 * - sara_achievements: Badge collection
 * - sara_daily_streak: Daily login/practice tracking
 * - sara_challenges: Daily/weekly challenges
 * - sara_stats: Performance analytics
 *
 * @version 2.0.0
 */

class GamificationManager {
    constructor(options = {}) {
        this.options = {
            grade: options.grade || 4,
            playerName: options.playerName || 'Leerling',
            ...options
        };

        // Check localStorage availability
        this.storageAvailable = this._testLocalStorage();

        if (!this.storageAvailable) {
            console.warn('[Gamification] localStorage niet beschikbaar. Gamification uitgeschakeld.');
            return;
        }

        // Initialize or load persistent data
        this.profile = this._loadProfile();
        this.achievements = this._loadAchievements();
        this.dailyStreak = this._loadDailyStreak();
        this.challenges = this._loadChallenges();
        this.stats = this._loadStats();

        // Check for new day and update
        this._checkNewDay();

        // Age-gated features
        this.features = this._initializeFeatures();

        // Save initial state
        this._saveAll();
    }

    /**
     * Initialize age-appropriate features
     */
    _initializeFeatures() {
        const grade = this.options.grade;

        return {
            // Grades 3-5: Basic gamification
            xpSystem: grade >= 3,
            basicBadges: grade >= 3,
            dailyStreaks: grade >= 3,
            simpleUnlocks: grade >= 3,

            // Grades 4-8: Intermediate
            dailyChallenges: grade >= 4,
            weeklyGoals: grade >= 4,
            avatarCustomization: grade >= 4,

            // Grades 6-8: Advanced
            leaderboard: grade >= 6,
            advancedStats: grade >= 6,
            prestigeSystem: grade >= 6
        };
    }

    /**
     * Test localStorage availability
     */
    _testLocalStorage() {
        try {
            const test = '__storage_test__';
            localStorage.setItem(test, test);
            localStorage.removeItem(test);
            return true;
        } catch (e) {
            return false;
        }
    }

    /**
     * Load or initialize player profile
     */
    _loadProfile() {
        try {
            const data = localStorage.getItem('sara_player_profile');
            if (data) {
                return JSON.parse(data);
            }
        } catch (e) {
            console.error('[Gamification] Error loading profile:', e);
        }

        // Initialize new profile
        return {
            playerName: this.options.playerName,
            grade: this.options.grade,
            createdAt: Date.now(),
            lastActiveAt: Date.now(),

            // XP and leveling
            xp: 0,
            level: 1,
            xpToNextLevel: 100,

            // Total stats
            totalExercisesCompleted: 0,
            totalQuestionsAnswered: 0,
            totalCorrectAnswers: 0,
            totalTimeSpentMinutes: 0,

            // Unlocks
            unlockedThemes: ['default'],
            unlockedAvatars: ['student'],
            currentTheme: 'default',
            currentAvatar: 'student',

            // Prestige (grades 6-8)
            prestigeLevel: 0,
            prestigePoints: 0
        };
    }

    /**
     * Load or initialize achievements
     */
    _loadAchievements() {
        try {
            const data = localStorage.getItem('sara_achievements');
            if (data) {
                return JSON.parse(data);
            }
        } catch (e) {
            console.error('[Gamification] Error loading achievements:', e);
        }

        // Initialize achievement tracking
        return {
            unlocked: [], // Array of achievement IDs
            progress: {}, // Track progress towards achievements
            lastUnlockedAt: null
        };
    }

    /**
     * Load or initialize daily streak
     */
    _loadDailyStreak() {
        try {
            const data = localStorage.getItem('sara_daily_streak');
            if (data) {
                const streak = JSON.parse(data);

                // Validate streak is still valid
                const today = this._getToday();
                const yesterday = this._getYesterday();

                if (streak.lastActiveDate === today) {
                    return streak; // Already logged in today
                } else if (streak.lastActiveDate === yesterday) {
                    // Visited yesterday, can continue streak
                    return streak;
                } else {
                    // Streak broken, reset
                    return this._resetStreak();
                }
            }
        } catch (e) {
            console.error('[Gamification] Error loading daily streak:', e);
        }

        return this._resetStreak();
    }

    /**
     * Reset daily streak
     */
    _resetStreak() {
        return {
            currentStreak: 0,
            longestStreak: 0,
            lastActiveDate: null,
            totalDaysActive: 0,
            streakFrozen: false, // Future feature: freeze streak with power-up
            freezesAvailable: 0
        };
    }

    /**
     * Load or initialize challenges
     */
    _loadChallenges() {
        try {
            const data = localStorage.getItem('sara_challenges');
            if (data) {
                const challenges = JSON.parse(data);

                // Check if challenges are still valid (daily/weekly)
                const today = this._getToday();
                if (challenges.generatedDate !== today) {
                    // Generate new daily challenges
                    return this._generateDailyChallenges();
                }

                return challenges;
            }
        } catch (e) {
            console.error('[Gamification] Error loading challenges:', e);
        }

        return this._generateDailyChallenges();
    }

    /**
     * Generate daily challenges
     */
    _generateDailyChallenges() {
        const today = this._getToday();
        const challenges = [];

        // Challenge 1: Complete X exercises
        challenges.push({
            id: `daily_${today}_exercises`,
            type: 'exercises',
            title: 'Oefen Meester',
            description: 'Voltooi 3 oefeningen vandaag',
            target: 3,
            progress: 0,
            completed: false,
            reward: { xp: 50, badge: null }
        });

        // Challenge 2: Get X correct in a row
        challenges.push({
            id: `daily_${today}_streak`,
            type: 'streak',
            title: 'Superspeurder',
            description: 'Beantwoord 5 vragen op rij goed',
            target: 5,
            progress: 0,
            completed: false,
            reward: { xp: 30, badge: null }
        });

        // Challenge 3: Practice X minutes
        challenges.push({
            id: `daily_${today}_time`,
            type: 'time',
            title: 'Doorzetter',
            description: 'Oefen 10 minuten vandaag',
            target: 10, // minutes
            progress: 0,
            completed: false,
            reward: { xp: 40, badge: null }
        });

        // Grade-specific challenge (grades 5+)
        if (this.options.grade >= 5) {
            challenges.push({
                id: `daily_${today}_accuracy`,
                type: 'accuracy',
                title: 'Precisie Expert',
                description: 'Behaal 80% goed vandaag',
                target: 80, // percentage
                progress: 0,
                completed: false,
                reward: { xp: 60, badge: null }
            });
        }

        return {
            generatedDate: today,
            daily: challenges,
            weekly: this._generateWeeklyChallenges()
        };
    }

    /**
     * Generate weekly challenges (grades 4+)
     */
    _generateWeeklyChallenges() {
        if (this.options.grade < 4) {
            return [];
        }

        const weekNumber = this._getWeekNumber();

        return [
            {
                id: `weekly_${weekNumber}_exercises`,
                type: 'exercises',
                title: 'Week Kampioen',
                description: 'Voltooi 15 oefeningen deze week',
                target: 15,
                progress: 0,
                completed: false,
                reward: { xp: 200, badge: 'week_champion' }
            },
            {
                id: `weekly_${weekNumber}_streak`,
                type: 'daily_streak',
                title: 'Dagelijkse Discipline',
                description: 'Oefen 5 dagen deze week',
                target: 5,
                progress: 0,
                completed: false,
                reward: { xp: 150, badge: 'consistent_learner' }
            }
        ];
    }

    /**
     * Load or initialize statistics
     */
    _loadStats() {
        try {
            const data = localStorage.getItem('sara_stats');
            if (data) {
                return JSON.parse(data);
            }
        } catch (e) {
            console.error('[Gamification] Error loading stats:', e);
        }

        return {
            byCategory: {}, // { gb: { correct: 50, total: 100 }, ... }
            byGrade: {},    // { 4: { correct: 80, total: 120 }, ... }
            byDate: {},     // { '2026-01-05': { correct: 10, total: 15 }, ... }
            fastestStreak: 0,
            perfectScores: 0,
            totalHintsUsed: 0
        };
    }

    /**
     * Check if it's a new day and update streak
     */
    _checkNewDay() {
        const today = this._getToday();
        const yesterday = this._getYesterday();

        if (this.dailyStreak.lastActiveDate === today) {
            // Already logged in today
            return;
        }

        if (this.dailyStreak.lastActiveDate === yesterday) {
            // Visited yesterday, increment streak
            this.dailyStreak.currentStreak++;
            this.dailyStreak.lastActiveDate = today;
            this.dailyStreak.totalDaysActive++;

            // Update longest streak
            if (this.dailyStreak.currentStreak > this.dailyStreak.longestStreak) {
                this.dailyStreak.longestStreak = this.dailyStreak.currentStreak;
            }

            // Check for streak achievements
            this._checkStreakAchievements();

        } else {
            // Streak broken (unless frozen)
            if (!this.dailyStreak.streakFrozen) {
                this.dailyStreak.currentStreak = 1; // Start new streak
            }
            this.dailyStreak.lastActiveDate = today;
            this.dailyStreak.totalDaysActive++;
        }

        // Update profile last active
        this.profile.lastActiveAt = Date.now();

        this._saveAll();
    }

    /**
     * Process completed exercise
     */
    completeExercise(results) {
        if (!this.storageAvailable) return null;

        const {
            exerciseId,
            category,
            grade,
            correctCount,
            totalCount,
            timeSpentSeconds,
            maxStreak,
            hintsUsed = 0,
            perfectScore = false
        } = results;

        // Update profile stats
        this.profile.totalExercisesCompleted++;
        this.profile.totalQuestionsAnswered += totalCount;
        this.profile.totalCorrectAnswers += correctCount;
        this.profile.totalTimeSpentMinutes += Math.round(timeSpentSeconds / 60);

        // Calculate XP earned
        const xpEarned = this._calculateXP(results);
        const leveledUp = this._addXP(xpEarned);

        // Update stats
        this._updateStats(category, grade, correctCount, totalCount, perfectScore, hintsUsed);

        // Update challenges
        const completedChallenges = this._updateChallenges(results);

        // Check for achievements
        const newAchievements = this._checkAchievements(results);

        // Save everything
        this._saveAll();

        return {
            xpEarned,
            leveledUp,
            newLevel: leveledUp ? this.profile.level : null,
            completedChallenges,
            newAchievements,
            totalXP: this.profile.xp,
            currentLevel: this.profile.level,
            dailyStreak: this.dailyStreak.currentStreak
        };
    }

    /**
     * Calculate XP earned from exercise
     */
    _calculateXP(results) {
        const { correctCount, totalCount, timeSpentSeconds, maxStreak, perfectScore } = results;

        let xp = 0;

        // Base XP: 10 per correct answer
        xp += correctCount * 10;

        // Accuracy bonus
        const accuracy = (correctCount / totalCount) * 100;
        if (accuracy >= 90) xp += 50; // Excellent
        else if (accuracy >= 75) xp += 30; // Good
        else if (accuracy >= 60) xp += 15; // Okay

        // Speed bonus (< 30 seconds per question)
        const avgTime = timeSpentSeconds / totalCount;
        if (avgTime < 30) xp += 20;

        // Streak bonus
        if (maxStreak >= 5) xp += 25;
        if (maxStreak >= 10) xp += 50;

        // Perfect score bonus
        if (perfectScore) xp += 100;

        return Math.floor(xp);
    }

    /**
     * Add XP and check for level up
     */
    _addXP(xp) {
        this.profile.xp += xp;

        // Check for level up
        while (this.profile.xp >= this.profile.xpToNextLevel) {
            this.profile.xp -= this.profile.xpToNextLevel;
            this.profile.level++;

            // Calculate XP for next level (increases by 20% each level)
            this.profile.xpToNextLevel = Math.floor(100 * Math.pow(1.2, this.profile.level - 1));

            // Unlock rewards at certain levels
            this._checkLevelUnlocks();

            return true; // Leveled up
        }

        return false; // No level up
    }

    /**
     * Check for level-based unlocks
     */
    _checkLevelUnlocks() {
        const level = this.profile.level;

        // Unlock themes
        if (level === 5 && !this.profile.unlockedThemes.includes('space')) {
            this.profile.unlockedThemes.push('space');
        }
        if (level === 10 && !this.profile.unlockedThemes.includes('underwater')) {
            this.profile.unlockedThemes.push('underwater');
        }
        if (level === 15 && !this.profile.unlockedThemes.includes('forest')) {
            this.profile.unlockedThemes.push('forest');
        }

        // Unlock avatars
        if (level === 3 && !this.profile.unlockedAvatars.includes('detective')) {
            this.profile.unlockedAvatars.push('detective');
        }
        if (level === 7 && !this.profile.unlockedAvatars.includes('scientist')) {
            this.profile.unlockedAvatars.push('scientist');
        }
        if (level === 12 && !this.profile.unlockedAvatars.includes('astronaut')) {
            this.profile.unlockedAvatars.push('astronaut');
        }
    }

    /**
     * Update performance statistics
     */
    _updateStats(category, grade, correctCount, totalCount, perfectScore, hintsUsed) {
        // By category
        if (!this.stats.byCategory[category]) {
            this.stats.byCategory[category] = { correct: 0, total: 0 };
        }
        this.stats.byCategory[category].correct += correctCount;
        this.stats.byCategory[category].total += totalCount;

        // By grade
        if (!this.stats.byGrade[grade]) {
            this.stats.byGrade[grade] = { correct: 0, total: 0 };
        }
        this.stats.byGrade[grade].correct += correctCount;
        this.stats.byGrade[grade].total += totalCount;

        // By date
        const today = this._getToday();
        if (!this.stats.byDate[today]) {
            this.stats.byDate[today] = { correct: 0, total: 0, exercises: 0 };
        }
        this.stats.byDate[today].correct += correctCount;
        this.stats.byDate[today].total += totalCount;
        this.stats.byDate[today].exercises++;

        // Special stats
        if (perfectScore) {
            this.stats.perfectScores++;
        }
        this.stats.totalHintsUsed += hintsUsed;
    }

    /**
     * Update challenge progress
     */
    _updateChallenges(results) {
        const { correctCount, totalCount, timeSpentSeconds, maxStreak } = results;
        const completed = [];

        // Update daily challenges
        for (const challenge of this.challenges.daily) {
            if (challenge.completed) continue;

            switch (challenge.type) {
                case 'exercises':
                    challenge.progress++;
                    break;
                case 'streak':
                    challenge.progress = Math.max(challenge.progress, maxStreak);
                    break;
                case 'time':
                    challenge.progress += Math.round(timeSpentSeconds / 60);
                    break;
                case 'accuracy':
                    const accuracy = (correctCount / totalCount) * 100;
                    challenge.progress = Math.round(accuracy);
                    break;
            }

            // Check if completed
            if (challenge.progress >= challenge.target) {
                challenge.completed = true;
                challenge.completedAt = Date.now();

                // Award rewards
                this._addXP(challenge.reward.xp);
                if (challenge.reward.badge) {
                    this._unlockAchievement(challenge.reward.badge);
                }

                completed.push(challenge);
            }
        }

        // Update weekly challenges
        for (const challenge of this.challenges.weekly) {
            if (challenge.completed) continue;

            switch (challenge.type) {
                case 'exercises':
                    challenge.progress++;
                    break;
                case 'daily_streak':
                    challenge.progress = this.dailyStreak.currentStreak;
                    break;
            }

            // Check if completed
            if (challenge.progress >= challenge.target) {
                challenge.completed = true;
                challenge.completedAt = Date.now();

                // Award rewards
                this._addXP(challenge.reward.xp);
                if (challenge.reward.badge) {
                    this._unlockAchievement(challenge.reward.badge);
                }

                completed.push(challenge);
            }
        }

        return completed;
    }

    /**
     * Check for achievements
     */
    _checkAchievements(results) {
        const newAchievements = [];

        // Define all achievements
        const achievements = this._getAchievementDefinitions();

        for (const achievement of achievements) {
            // Skip if already unlocked
            if (this.achievements.unlocked.includes(achievement.id)) {
                continue;
            }

            // Check if condition is met
            if (this._checkAchievementCondition(achievement)) {
                this._unlockAchievement(achievement.id);
                newAchievements.push(achievement);
            }
        }

        return newAchievements;
    }

    /**
     * Check if achievement condition is met
     */
    _checkAchievementCondition(achievement) {
        switch (achievement.condition.type) {
            case 'total_exercises':
                return this.profile.totalExercisesCompleted >= achievement.condition.value;

            case 'total_correct':
                return this.profile.totalCorrectAnswers >= achievement.condition.value;

            case 'daily_streak':
                return this.dailyStreak.currentStreak >= achievement.condition.value;

            case 'level':
                return this.profile.level >= achievement.condition.value;

            case 'perfect_scores':
                return this.stats.perfectScores >= achievement.condition.value;

            case 'category_mastery':
                const cat = this.stats.byCategory[achievement.condition.category];
                if (!cat || cat.total < 100) return false;
                const accuracy = (cat.correct / cat.total) * 100;
                return accuracy >= achievement.condition.accuracy;

            default:
                return false;
        }
    }

    /**
     * Unlock achievement
     */
    _unlockAchievement(achievementId) {
        if (!this.achievements.unlocked.includes(achievementId)) {
            this.achievements.unlocked.push(achievementId);
            this.achievements.lastUnlockedAt = Date.now();
        }
    }

    /**
     * Check for streak-based achievements
     */
    _checkStreakAchievements() {
        const streak = this.dailyStreak.currentStreak;

        if (streak === 3) this._unlockAchievement('streak_3');
        if (streak === 7) this._unlockAchievement('streak_7');
        if (streak === 14) this._unlockAchievement('streak_14');
        if (streak === 30) this._unlockAchievement('streak_30');
    }

    /**
     * Get player summary
     */
    getPlayerSummary() {
        if (!this.storageAvailable) {
            return { enabled: false };
        }

        return {
            enabled: true,
            profile: {
                name: this.profile.playerName,
                level: this.profile.level,
                xp: this.profile.xp,
                xpToNextLevel: this.profile.xpToNextLevel,
                xpProgress: Math.round((this.profile.xp / this.profile.xpToNextLevel) * 100)
            },
            streak: {
                current: this.dailyStreak.currentStreak,
                longest: this.dailyStreak.longestStreak,
                totalDays: this.dailyStreak.totalDaysActive
            },
            achievements: {
                total: this.achievements.unlocked.length,
                unlocked: this.achievements.unlocked,
                recentlyUnlocked: this._getRecentAchievements(5)
            },
            challenges: {
                daily: this.challenges.daily,
                weekly: this.challenges.weekly,
                completedToday: this.challenges.daily.filter(c => c.completed).length
            },
            stats: {
                totalExercises: this.profile.totalExercisesCompleted,
                totalQuestions: this.profile.totalQuestionsAnswered,
                totalCorrect: this.profile.totalCorrectAnswers,
                accuracy: Math.round((this.profile.totalCorrectAnswers / this.profile.totalQuestionsAnswered) * 100) || 0,
                timeSpent: this.profile.totalTimeSpentMinutes,
                perfectScores: this.stats.perfectScores
            }
        };
    }

    /**
     * Get recent achievements
     */
    _getRecentAchievements(count) {
        const allAchievements = this._getAchievementDefinitions();
        const unlocked = allAchievements.filter(a => this.achievements.unlocked.includes(a.id));
        return unlocked.slice(-count);
    }

    /**
     * Get today's date string (YYYY-MM-DD)
     */
    _getToday() {
        const now = new Date();
        return now.toISOString().split('T')[0];
    }

    /**
     * Get yesterday's date string (YYYY-MM-DD)
     */
    _getYesterday() {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        return yesterday.toISOString().split('T')[0];
    }

    /**
     * Get week number
     */
    _getWeekNumber() {
        const now = new Date();
        const start = new Date(now.getFullYear(), 0, 1);
        const diff = now - start;
        const oneWeek = 1000 * 60 * 60 * 24 * 7;
        return Math.floor(diff / oneWeek);
    }

    /**
     * Save all data to localStorage
     */
    _saveAll() {
        if (!this.storageAvailable) return;

        try {
            localStorage.setItem('sara_player_profile', JSON.stringify(this.profile));
            localStorage.setItem('sara_achievements', JSON.stringify(this.achievements));
            localStorage.setItem('sara_daily_streak', JSON.stringify(this.dailyStreak));
            localStorage.setItem('sara_challenges', JSON.stringify(this.challenges));
            localStorage.setItem('sara_stats', JSON.stringify(this.stats));
        } catch (e) {
            console.error('[Gamification] Error saving data:', e);
        }
    }

    /**
     * Get all achievement definitions
     */
    _getAchievementDefinitions() {
        return [
            // Beginner achievements
            { id: 'first_exercise', title: 'Eerste Stap', description: 'Voltooi je eerste oefening', emoji: '🎯', condition: { type: 'total_exercises', value: 1 } },
            { id: 'getting_started', title: 'Aan de Slag!', description: 'Voltooi 5 oefeningen', emoji: '🚀', condition: { type: 'total_exercises', value: 5 } },

            // Streak achievements
            { id: 'streak_3', title: 'Op Dreef', description: 'Oefen 3 dagen op rij', emoji: '🔥', condition: { type: 'daily_streak', value: 3 } },
            { id: 'streak_7', title: 'Week Warrior', description: 'Oefen 7 dagen op rij', emoji: '⭐', condition: { type: 'daily_streak', value: 7 } },
            { id: 'streak_14', title: 'Twee Weken Kampioen', description: 'Oefen 14 dagen op rij', emoji: '🏆', condition: { type: 'daily_streak', value: 14 } },
            { id: 'streak_30', title: 'Maand Meester', description: 'Oefen 30 dagen op rij', emoji: '👑', condition: { type: 'daily_streak', value: 30 } },

            // Volume achievements
            { id: 'century_club', title: 'Honderd Club', description: 'Beantwoord 100 vragen goed', emoji: '💯', condition: { type: 'total_correct', value: 100 } },
            { id: 'five_hundred', title: 'Vijfhonderd!', description: 'Beantwoord 500 vragen goed', emoji: '🎊', condition: { type: 'total_correct', value: 500 } },
            { id: 'thousand', title: 'Duizend!', description: 'Beantwoord 1000 vragen goed', emoji: '🌟', condition: { type: 'total_correct', value: 1000 } },

            // Perfectionist achievements
            { id: 'perfectionist', title: 'Perfectionist', description: 'Behaal 1 perfecte score', emoji: '✨', condition: { type: 'perfect_scores', value: 1 } },
            { id: 'flawless_five', title: 'Vijf Foutloos', description: 'Behaal 5 perfecte scores', emoji: '💎', condition: { type: 'perfect_scores', value: 5 } },

            // Level achievements
            { id: 'level_5', title: 'Level 5 Legende', description: 'Bereik level 5', emoji: '🎖️', condition: { type: 'level', value: 5 } },
            { id: 'level_10', title: 'Level 10 Held', description: 'Bereik level 10', emoji: '🦸', condition: { type: 'level', value: 10 } },
            { id: 'level_20', title: 'Level 20 Kampioen', description: 'Bereik level 20', emoji: '👑', condition: { type: 'level', value: 20 } },

            // Category mastery (grades 5+)
            { id: 'math_master', title: 'Reken Meester', description: '90% goed bij Getallen & Bewerkingen', emoji: '🧮', condition: { type: 'category_mastery', category: 'gb', accuracy: 90 } },
            { id: 'word_wizard', title: 'Woorden Wizard', description: '90% goed bij Woordenschat', emoji: '📚', condition: { type: 'category_mastery', category: 'ws', accuracy: 90 } }
        ];
    }

    /**
     * Reset all data (for testing or new player)
     */
    resetAll() {
        if (!this.storageAvailable) return;

        if (confirm('Weet je zeker dat je al je voortgang wilt verwijderen? Dit kan niet ongedaan gemaakt worden.')) {
            localStorage.removeItem('sara_player_profile');
            localStorage.removeItem('sara_achievements');
            localStorage.removeItem('sara_daily_streak');
            localStorage.removeItem('sara_challenges');
            localStorage.removeItem('sara_stats');

            // Reload page to reinitialize
            window.location.reload();
        }
    }

    /**
     * Export data (for backup or migration)
     */
    exportData() {
        if (!this.storageAvailable) return null;

        return {
            version: '2.0.0',
            exportedAt: new Date().toISOString(),
            data: {
                profile: this.profile,
                achievements: this.achievements,
                dailyStreak: this.dailyStreak,
                challenges: this.challenges,
                stats: this.stats
            }
        };
    }

    /**
     * Import data (from backup)
     */
    importData(exportedData) {
        if (!this.storageAvailable) return false;

        if (!exportedData || !exportedData.data) {
            alert('Ongeldige backup data');
            return false;
        }

        if (confirm('Weet je zeker dat je je huidige voortgang wilt vervangen met deze backup?')) {
            this.profile = exportedData.data.profile;
            this.achievements = exportedData.data.achievements;
            this.dailyStreak = exportedData.data.dailyStreak;
            this.challenges = exportedData.data.challenges;
            this.stats = exportedData.data.stats;

            this._saveAll();

            alert('Backup succesvol geïmporteerd!');
            window.location.reload();
            return true;
        }

        return false;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GamificationManager;
}
