/**
 * GamificationUI - UI components for displaying gamification features
 *
 * Displays:
 * - Player profile (level, XP, avatar)
 * - Daily streak counter
 * - Achievement notifications
 * - Challenge progress
 * - Level-up celebrations
 * - Stats dashboard
 *
 * @version 2.0.0
 */

class GamificationUI {
    constructor(gamificationManager) {
        this.gm = gamificationManager;

        // UI state
        this.notificationQueue = [];
        this.isShowingNotification = false;
    }

    /**
     * Render player profile widget
     */
    renderPlayerProfile(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const summary = this.gm.getPlayerSummary();
        if (!summary.enabled) {
            container.innerHTML = '<p class="gamification-disabled">Voortgang opslaan is uitgeschakeld</p>';
            return;
        }

        const { profile, streak, achievements } = summary;

        container.innerHTML = `
            <div class="player-profile">
                <div class="profile-header">
                    <div class="avatar-container">
                        <img src="/static/assets/avatars/${this.gm.profile.currentAvatar}.svg"
                             alt="Avatar"
                             class="player-avatar"
                             onerror="this.src='/static/assets/avatars/student.svg'">
                        <div class="level-badge">${profile.level}</div>
                    </div>
                    <div class="profile-info">
                        <h3 class="player-name">${profile.name}</h3>
                        <div class="xp-bar-container">
                            <div class="xp-bar-fill" style="width: ${profile.xpProgress}%"></div>
                            <span class="xp-text">${profile.xp} / ${profile.xpToNextLevel} XP</span>
                        </div>
                    </div>
                </div>

                <div class="profile-stats">
                    <div class="stat-item">
                        <span class="stat-icon">🔥</span>
                        <span class="stat-value">${streak.current}</span>
                        <span class="stat-label">Dag Streak</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-icon">🏆</span>
                        <span class="stat-value">${achievements.total}</span>
                        <span class="stat-label">Badges</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-icon">⭐</span>
                        <span class="stat-value">${summary.stats.perfectScores}</span>
                        <span class="stat-label">Perfect</span>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Render daily challenges
     */
    renderDailyChallenges(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const summary = this.gm.getPlayerSummary();
        if (!summary.enabled) return;

        const { daily } = summary.challenges;

        let html = '<div class="daily-challenges">';
        html += '<h3 class="challenges-title">Dagelijkse Uitdagingen</h3>';
        html += '<div class="challenges-list">';

        for (const challenge of daily) {
            const progress = Math.min(100, (challenge.progress / challenge.target) * 100);
            const isComplete = challenge.completed;

            html += `
                <div class="challenge-card ${isComplete ? 'completed' : ''}">
                    <div class="challenge-header">
                        <span class="challenge-title">${challenge.title}</span>
                        ${isComplete ? '<span class="challenge-badge">✓</span>' : ''}
                    </div>
                    <p class="challenge-description">${challenge.description}</p>
                    <div class="challenge-progress">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${progress}%"></div>
                        </div>
                        <span class="progress-text">${challenge.progress} / ${challenge.target}</span>
                    </div>
                    <div class="challenge-reward">
                        <span class="reward-icon">⭐</span>
                        <span class="reward-text">+${challenge.reward.xp} XP</span>
                    </div>
                </div>
            `;
        }

        html += '</div></div>';
        container.innerHTML = html;
    }

    /**
     * Render achievements gallery
     */
    renderAchievements(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const summary = this.gm.getPlayerSummary();
        if (!summary.enabled) return;

        const allAchievements = this.gm._getAchievementDefinitions();
        const unlocked = summary.achievements.unlocked;

        let html = '<div class="achievements-gallery">';
        html += '<h3 class="gallery-title">Prestaties</h3>';
        html += `<p class="gallery-subtitle">${unlocked.length} / ${allAchievements.length} behaald</p>`;
        html += '<div class="achievements-grid">';

        for (const achievement of allAchievements) {
            const isUnlocked = unlocked.includes(achievement.id);

            html += `
                <div class="achievement-card ${isUnlocked ? 'unlocked' : 'locked'}">
                    <div class="achievement-icon">${isUnlocked ? achievement.emoji : '🔒'}</div>
                    <div class="achievement-info">
                        <div class="achievement-title">${achievement.title}</div>
                        <div class="achievement-description">${achievement.description}</div>
                    </div>
                </div>
            `;
        }

        html += '</div></div>';
        container.innerHTML = html;
    }

    /**
     * Render statistics dashboard
     */
    renderStatsDashboard(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const summary = this.gm.getPlayerSummary();
        if (!summary.enabled) return;

        const { stats } = summary;

        const html = `
            <div class="stats-dashboard">
                <h3 class="dashboard-title">Jouw Statistieken</h3>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-card-icon">📊</div>
                        <div class="stat-card-value">${stats.totalExercises}</div>
                        <div class="stat-card-label">Oefeningen Voltooid</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-card-icon">✅</div>
                        <div class="stat-card-value">${stats.totalQuestions}</div>
                        <div class="stat-card-label">Vragen Beantwoord</div>
                    </div>

                    <div class="stat-card highlight">
                        <div class="stat-card-icon">🎯</div>
                        <div class="stat-card-value">${stats.accuracy}%</div>
                        <div class="stat-card-label">Nauwkeurigheid</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-card-icon">⏱️</div>
                        <div class="stat-card-value">${stats.timeSpent}</div>
                        <div class="stat-card-label">Minuten Geoefend</div>
                    </div>
                </div>

                <div class="stats-by-category">
                    <h4>Prestaties per Categorie</h4>
                    ${this._renderCategoryStats()}
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    /**
     * Render category statistics
     */
    _renderCategoryStats() {
        const categoryNames = {
            'gb': 'Getallen & Bewerkingen',
            'ws': 'Woordenschat',
            'wo': 'Wereldoriëntatie',
            'tl': 'Taal',
            'sv': 'Spelling',
            'bl': 'Begrijpend Lezen',
            'sp': 'Spelling',
            'mk': 'Meetkunde'
        };

        let html = '<div class="category-stats-list">';

        for (const [code, data] of Object.entries(this.gm.stats.byCategory)) {
            if (data.total === 0) continue;

            const accuracy = Math.round((data.correct / data.total) * 100);
            const name = categoryNames[code] || code.toUpperCase();

            html += `
                <div class="category-stat-item">
                    <div class="category-name">${name}</div>
                    <div class="category-progress-bar">
                        <div class="category-progress-fill" style="width: ${accuracy}%"></div>
                        <span class="category-accuracy">${accuracy}%</span>
                    </div>
                    <div class="category-count">${data.correct} / ${data.total}</div>
                </div>
            `;
        }

        html += '</div>';
        return html;
    }

    /**
     * Show level-up celebration
     */
    showLevelUp(newLevel) {
        const modal = this._createModal();

        modal.innerHTML = `
            <div class="level-up-celebration">
                <div class="celebration-animation">🎉</div>
                <h2 class="celebration-title">Level Omhoog!</h2>
                <div class="new-level-display">${newLevel}</div>
                <p class="celebration-message">Je bent nu level ${newLevel}!</p>

                ${this._checkNewUnlocks(newLevel)}

                <button class="celebration-close-btn" onclick="this.closest('.gamification-modal').remove()">
                    Geweldig!
                </button>
            </div>
        `;

        document.body.appendChild(modal);

        // Auto-close after 5 seconds
        setTimeout(() => {
            if (modal.parentNode) {
                modal.remove();
            }
        }, 5000);
    }

    /**
     * Check for new unlocks at level
     */
    _checkNewUnlocks(level) {
        const unlocks = [];

        // Check theme unlocks
        if (level === 5) unlocks.push('🌌 Ruimte thema ontgrendeld!');
        if (level === 10) unlocks.push('🌊 Onderwaterwereld thema ontgrendeld!');
        if (level === 15) unlocks.push('🌳 Bos thema ontgrendeld!');

        // Check avatar unlocks
        if (level === 3) unlocks.push('🔍 Detective avatar ontgrendeld!');
        if (level === 7) unlocks.push('🔬 Wetenschapper avatar ontgrendeld!');
        if (level === 12) unlocks.push('🚀 Astronaut avatar ontgrendeld!');

        if (unlocks.length === 0) return '';

        return `
            <div class="unlocks-list">
                <h3>Nieuwe Beloningen:</h3>
                ${unlocks.map(u => `<div class="unlock-item">${u}</div>`).join('')}
            </div>
        `;
    }

    /**
     * Show achievement unlock notification
     */
    showAchievementUnlock(achievement) {
        this.notificationQueue.push({
            type: 'achievement',
            data: achievement
        });

        this._processNotificationQueue();
    }

    /**
     * Show challenge completion notification
     */
    showChallengeComplete(challenge) {
        this.notificationQueue.push({
            type: 'challenge',
            data: challenge
        });

        this._processNotificationQueue();
    }

    /**
     * Show XP gain notification
     */
    showXPGain(xp, reason = '') {
        this.notificationQueue.push({
            type: 'xp',
            data: { xp, reason }
        });

        this._processNotificationQueue();
    }

    /**
     * Process notification queue
     */
    _processNotificationQueue() {
        if (this.isShowingNotification || this.notificationQueue.length === 0) {
            return;
        }

        this.isShowingNotification = true;
        const notification = this.notificationQueue.shift();

        const element = this._createNotification(notification);
        document.body.appendChild(element);

        // Animate in
        setTimeout(() => {
            element.classList.add('show');
        }, 10);

        // Animate out and remove
        setTimeout(() => {
            element.classList.remove('show');
            setTimeout(() => {
                element.remove();
                this.isShowingNotification = false;
                this._processNotificationQueue(); // Process next
            }, 300);
        }, 3000);
    }

    /**
     * Create notification element
     */
    _createNotification(notification) {
        const div = document.createElement('div');
        div.className = 'gamification-notification';

        switch (notification.type) {
            case 'achievement':
                div.innerHTML = `
                    <div class="notification-icon">${notification.data.emoji}</div>
                    <div class="notification-content">
                        <div class="notification-title">Badge Behaald!</div>
                        <div class="notification-message">${notification.data.title}</div>
                    </div>
                `;
                div.classList.add('achievement-notification');
                break;

            case 'challenge':
                div.innerHTML = `
                    <div class="notification-icon">🎯</div>
                    <div class="notification-content">
                        <div class="notification-title">Uitdaging Voltooid!</div>
                        <div class="notification-message">${notification.data.title}</div>
                        <div class="notification-reward">+${notification.data.reward.xp} XP</div>
                    </div>
                `;
                div.classList.add('challenge-notification');
                break;

            case 'xp':
                div.innerHTML = `
                    <div class="notification-icon">⭐</div>
                    <div class="notification-content">
                        <div class="notification-title">+${notification.data.xp} XP</div>
                        ${notification.data.reason ? `<div class="notification-message">${notification.data.reason}</div>` : ''}
                    </div>
                `;
                div.classList.add('xp-notification');
                break;
        }

        return div;
    }

    /**
     * Create modal container
     */
    _createModal() {
        const modal = document.createElement('div');
        modal.className = 'gamification-modal';

        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay';
        overlay.onclick = () => modal.remove();

        const content = document.createElement('div');
        content.className = 'modal-content';

        modal.appendChild(overlay);
        modal.appendChild(content);

        return content;
    }

    /**
     * Render mini profile (for header/navbar)
     */
    renderMiniProfile(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const summary = this.gm.getPlayerSummary();
        if (!summary.enabled) return;

        const { profile, streak } = summary;

        container.innerHTML = `
            <div class="mini-profile">
                <div class="mini-avatar">
                    <img src="/static/assets/avatars/${this.gm.profile.currentAvatar}.svg"
                         alt="Avatar"
                         onerror="this.src='/static/assets/avatars/student.svg'">
                    <span class="mini-level">${profile.level}</span>
                </div>
                <div class="mini-stats">
                    <div class="mini-xp">
                        <span class="mini-xp-bar" style="width: ${profile.xpProgress}%"></span>
                    </div>
                    <div class="mini-streak">🔥 ${streak.current}</div>
                </div>
            </div>
        `;
    }

    /**
     * Show daily streak update
     */
    showStreakUpdate(currentStreak) {
        const messages = {
            1: { emoji: '✨', text: 'Welkom terug!' },
            3: { emoji: '🔥', text: '3 dagen op rij!' },
            7: { emoji: '⭐', text: '1 week streak!' },
            14: { emoji: '🏆', text: '2 weken streak!' },
            30: { emoji: '👑', text: 'MAAND STREAK!' }
        };

        const message = messages[currentStreak] || messages[1];

        const div = document.createElement('div');
        div.className = 'streak-update-popup';
        div.innerHTML = `
            <div class="streak-emoji">${message.emoji}</div>
            <div class="streak-text">${message.text}</div>
            <div class="streak-count">Dag ${currentStreak}</div>
        `;

        document.body.appendChild(div);

        setTimeout(() => div.classList.add('show'), 10);
        setTimeout(() => {
            div.classList.remove('show');
            setTimeout(() => div.remove(), 300);
        }, 3000);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GamificationUI;
}
