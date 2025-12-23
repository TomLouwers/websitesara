/**
 * StreakAnimationController - Visual feedback and animations for reward system
 *
 * DESIGN PRINCIPLES:
 * - Non-blocking animations (≤ 600ms)
 * - Skippable by user interaction
 * - Graduated reward ladder
 * - No negative/loss animations
 * - Age-appropriate complexity
 *
 * @version 1.0.0
 */

class StreakAnimationController {
    constructor(options = {}) {
        this.options = {
            grade: options.grade || 4,
            reducedMotion: this._prefersReducedMotion(),
            ...options
        };

        // Animation queue
        this.animationQueue = [];
        this.isAnimating = false;

        // DOM elements (cached)
        this.elements = {
            scoreDisplay: null,
            streakCard: null,
            multiplierBadge: null,
            shieldBadge: null,
            nearMissCard: null,
            pointBurstContainer: null,
            progressStar: null
        };

        // Initialize
        this._initializeDOMElements();
    }

    /**
     * Check if user prefers reduced motion
     */
    _prefersReducedMotion() {
        if (typeof window === 'undefined') {
            return false;
        }
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    /**
     * Initialize and cache DOM elements
     */
    _initializeDOMElements() {
        if (typeof document === 'undefined') {
            return;
        }

        this.elements.scoreDisplay = document.getElementById('currentScore');
        this.elements.streakCard = document.getElementById('streakCard');
        this.elements.multiplierBadge = document.getElementById('multiplierBadge');
        this.elements.shieldBadge = document.getElementById('shieldBadge');
        this.elements.nearMissCard = document.getElementById('nearMissCard');
        this.elements.pointBurstContainer = document.getElementById('pointBurstContainer');
        this.elements.progressStar = document.getElementById('progressStar');
    }


    /**
     * Play correct answer feedback
     * @param {Object} feedback - Feedback object from SessionRewardManager
     */
    async playCorrectFeedback(feedback) {
        if (this.options.reducedMotion) {
            // Simplified feedback for reduced motion
            this._updateScoreDisplay(feedback.score);
            return;
        }

        // Queue animations
        const animations = [];

        // 1. Base correct feedback (subtle)
        animations.push(() => this._playCorrectPing());

        // 2. Point burst and fly to star
        animations.push(() => this._playPointBurst(feedback.totalPointsEarned, feedback.score));

        // 3. Streak milestone card (if reached)
        if (feedback.streakMilestone) {
            animations.push(() => this._playStreakMilestone(feedback.streakMilestone));
        }

        // 4. Shield unlock (if applicable)
        if (feedback.shieldUnlocked) {
            animations.push(() => this._playShieldUnlock());
        }

        // 5. Multiplier activation (if applicable, grades 6-8)
        if (feedback.multiplierActive && feedback.currentStreak === 3) {
            animations.push(() => this._playMultiplierActivation());
        }

        // Execute animation sequence
        await this._executeAnimationQueue(animations);
    }

    /**
     * Play incorrect answer feedback
     * @param {Object} feedback - Feedback object from SessionRewardManager
     */
    async playIncorrectFeedback(feedback) {
        if (this.options.reducedMotion) {
            // Simplified feedback
            if (feedback.nearMiss) {
                this._showNearMissMessage(feedback.nearMissMessage);
            }
            return;
        }

        const animations = [];

        // 1. Shield protection (if applicable)
        if (feedback.streakProtected) {
            animations.push(() => this._playShieldProtection());
        }

        // 2. Near-miss encouragement (if applicable)
        if (feedback.nearMiss && !feedback.streakProtected) {
            animations.push(() => this._playNearMiss(feedback.nearMissMessage));
        }

        // 3. Gentle multiplier deactivation (silent, no animation for grades 6-8)
        // Multiplier just disappears, no loss framing

        // Execute animation sequence
        await this._executeAnimationQueue(animations);
    }

    /**
     * Execute animation queue sequentially
     */
    async _executeAnimationQueue(animations) {
        this.isAnimating = true;

        for (const animation of animations) {
            try {
                await animation();
            } catch (e) {
                console.warn('Animation failed:', e);
            }
        }

        this.isAnimating = false;
    }

    /**
     * Play subtle correct answer ping
     */
    async _playCorrectPing() {
        // Subtle visual (small check mark bounce)
        const checkmark = document.querySelector('.answer-feedback-check');
        if (checkmark) {
            checkmark.style.animation = 'gentle-bounce 300ms ease-out';
            await this._wait(300);
            checkmark.style.animation = '';
        }
    }

    /**
     * Play point burst and fly to star animation
     * @param {number} points - Points earned
     * @param {number} totalScore - New total score
     */
    async _playPointBurst(points, totalScore) {
        if (!this.elements.pointBurstContainer) {
            this._updateScoreDisplay(totalScore);
            return;
        }

        // Create point particles
        const particles = this._createPointParticles(points);

        // Burst animation (200ms)
        await this._animatePointBurst(particles);

        // Fly to star (400ms)
        await this._animatePointsToStar(particles);

        // Update score display
        this._updateScoreDisplay(totalScore);

        // Clean up particles
        particles.forEach(p => p.remove());
    }

    /**
     * Create point particles for animation
     */
    _createPointParticles(points) {
        const container = this.elements.pointBurstContainer;
        const particles = [];

        // Create 3-5 particles per point (max 15 total)
        const particleCount = Math.min(points * 3, 15);

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'point-particle';
            particle.textContent = '⭐';
            particle.style.cssText = `
                position: absolute;
                font-size: 1.2rem;
                pointer-events: none;
                opacity: 0;
            `;
            container.appendChild(particle);
            particles.push(particle);
        }

        return particles;
    }

    /**
     * Animate point burst (spread out)
     */
    async _animatePointBurst(particles) {
        const centerX = this.elements.pointBurstContainer.offsetWidth / 2;
        const centerY = this.elements.pointBurstContainer.offsetHeight / 2;

        particles.forEach((particle, i) => {
            const angle = (Math.PI * 2 * i) / particles.length;
            const distance = 40 + Math.random() * 20;
            const tx = Math.cos(angle) * distance;
            const ty = Math.sin(angle) * distance;

            particle.style.left = `${centerX}px`;
            particle.style.top = `${centerY}px`;
            particle.style.transition = 'all 200ms ease-out';
            particle.style.opacity = '1';

            // Trigger reflow
            particle.offsetHeight;

            particle.style.transform = `translate(${tx}px, ${ty}px)`;
        });

        await this._wait(200);
    }

    /**
     * Animate points flying to star
     */
    async _animatePointsToStar(particles) {
        if (!this.elements.progressStar) {
            return;
        }

        const starRect = this.elements.progressStar.getBoundingClientRect();
        const containerRect = this.elements.pointBurstContainer.getBoundingClientRect();

        const targetX = starRect.left - containerRect.left + starRect.width / 2;
        const targetY = starRect.top - containerRect.top + starRect.height / 2;

        particles.forEach((particle, i) => {
            // Stagger timing slightly
            setTimeout(() => {
                particle.style.transition = 'all 400ms cubic-bezier(0.4, 0.0, 0.2, 1)';
                particle.style.left = `${targetX}px`;
                particle.style.top = `${targetY}px`;
                particle.style.opacity = '0';
                particle.style.transform = 'scale(0.3)';
            }, i * 30);
        });

        await this._wait(400);

        // Star pulse on arrival
        if (this.elements.progressStar) {
            this.elements.progressStar.style.animation = 'star-pulse 300ms ease-out';
            await this._wait(300);
            this.elements.progressStar.style.animation = '';
        }
    }

    /**
     * Update score display with count-up animation
     */
    _updateScoreDisplay(newScore) {
        if (!this.elements.scoreDisplay) {
            return;
        }

        const currentScore = parseInt(this.elements.scoreDisplay.textContent) || 0;

        if (newScore === currentScore) {
            return;
        }

        // Count up animation (fast)
        const duration = 300;
        const steps = Math.min(newScore - currentScore, 10);
        const stepDuration = duration / steps;
        let current = currentScore;

        const interval = setInterval(() => {
            current += Math.ceil((newScore - current) / 2);
            if (current >= newScore) {
                current = newScore;
                clearInterval(interval);
            }
            this.elements.scoreDisplay.textContent = current;
        }, stepDuration);
    }

    /**
     * Play streak milestone animation - FESTIVE AND PLAYFUL FOR KIDS!
     */
    async _playStreakMilestone(milestone) {
        if (!this.elements.streakCard) {
            return;
        }

        const { emoji, title, tier, bonusPoints, multiplierApplied, threshold } = milestone;

        // Build super playful card content with extra visual elements
        let bonusText = `+${bonusPoints} punten!`;
        if (multiplierApplied) {
            bonusText = `+${bonusPoints} punten! (x2 bonus)`;
        }

        // Add playful decorations based on tier
        let decorations = '';
        if (tier === 'celebration') {
            decorations = '<div class="streak-sparkles">✨🎉✨🎊✨🎉✨</div>';
        } else if (tier === 'skill') {
            decorations = '<div class="streak-sparkles">⭐🌟⭐🌟⭐</div>';
        } else {
            decorations = '<div class="streak-sparkles">🌟✨🌟</div>';
        }

        // Playful motivational messages
        const motivationalMessages = {
            3: ['Je bent lekker bezig!', 'Goed zo!', 'Zo kan het!'],
            5: ['Wauw, super!', 'Je bent een kei!', 'Ontzettend knap!'],
            10: ['Ongelooflijk!', 'Wow, geweldig!', 'Je bent een kampioen!']
        };
        const randomMessage = motivationalMessages[threshold][Math.floor(Math.random() * motivationalMessages[threshold].length)];

        this.elements.streakCard.innerHTML = `
            <div class="streak-card-content streak-tier-${tier}">
                ${decorations}
                <div class="streak-emoji-big">${emoji}${emoji}${emoji}</div>
                <div class="streak-title-playful">${title}</div>
                <div class="streak-message">${randomMessage}</div>
                <div class="streak-bonus-big">${bonusText}</div>
                <div class="streak-decoration-bottom">🎈🎈🎈</div>
            </div>
        `;

        // Show card with bouncy slide-in animation
        this.elements.streakCard.style.display = 'block';
        this.elements.streakCard.style.animation = 'streak-bounce-in 500ms cubic-bezier(0.68, -0.55, 0.265, 1.55)';
        await this._wait(500);

        // Show confetti for 10-streak (celebration tier)
        if (tier === 'celebration' && !this.options.reducedMotion) {
            this._playConfetti();
        }

        // Hold card visible for 2500ms (bit longer for kids to enjoy)
        await this._wait(2500);

        // Bounce out
        this.elements.streakCard.style.animation = 'streak-bounce-out 400ms ease-in';
        await this._wait(400);

        this.elements.streakCard.style.display = 'none';
        this.elements.streakCard.style.animation = '';
    }

    /**
     * Play confetti animation (rare, only for 10-streak)
     */
    _playConfetti() {
        if (typeof confetti === 'undefined') {
            return; // Confetti library not loaded
        }

        confetti({
            particleCount: 50,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#FFD700', '#FFA500', '#FF69B4', '#00CED1']
        });
    }

    /**
     * Play shield unlock animation
     */
    async _playShieldUnlock() {
        if (!this.elements.shieldBadge) {
            return;
        }

        this.elements.shieldBadge.innerHTML = `
            <div class="shield-badge-content">
                <div class="shield-icon">🛡️</div>
                <div class="shield-label">Schild verdiend!</div>
            </div>
        `;

        // Show badge
        this.elements.shieldBadge.style.display = 'flex';
        this.elements.shieldBadge.style.animation = 'shield-appear 500ms ease-out';
        await this._wait(500);

        this.elements.shieldBadge.style.animation = '';
    }

    /**
     * Play multiplier activation animation (grades 6-8)
     */
    async _playMultiplierActivation() {
        if (!this.elements.multiplierBadge) {
            return;
        }

        this.elements.multiplierBadge.innerHTML = `
            <div class="multiplier-badge-content">
                <span class="multiplier-value">x2</span>
            </div>
        `;

        // Show badge
        this.elements.multiplierBadge.style.display = 'flex';
        this.elements.multiplierBadge.style.animation = 'multiplier-pulse 500ms ease-out';
        await this._wait(500);

        this.elements.multiplierBadge.style.animation = '';
    }

    /**
     * Play shield protection animation
     */
    async _playShieldProtection() {
        if (!this.elements.shieldBadge) {
            return;
        }

        // Update shield to show it was used
        this.elements.shieldBadge.innerHTML = `
            <div class="shield-badge-content shield-used">
                <div class="shield-icon">🛡️</div>
                <div class="shield-label">Bonus gered!</div>
            </div>
        `;

        // Flash animation
        this.elements.shieldBadge.style.animation = 'shield-protect 600ms ease-out';
        await this._wait(600);

        // Fade out (shield is consumed)
        this.elements.shieldBadge.style.animation = 'fade-out 300ms ease-out';
        await this._wait(300);

        this.elements.shieldBadge.style.display = 'none';
        this.elements.shieldBadge.style.animation = '';
    }

    /**
     * Play near-miss encouragement
     */
    async _playNearMiss(message) {
        if (!this.elements.nearMissCard) {
            return;
        }

        this.elements.nearMissCard.innerHTML = `
            <div class="near-miss-content">
                <div class="near-miss-emoji">💪</div>
                <div class="near-miss-message">${message}</div>
            </div>
        `;

        // Show card
        this.elements.nearMissCard.style.display = 'block';
        this.elements.nearMissCard.style.animation = 'slide-in-up 300ms ease-out';
        await this._wait(300);

        // Hold for 2000ms
        await this._wait(2000);

        // Fade out
        this.elements.nearMissCard.style.animation = 'fade-out 300ms ease-out';
        await this._wait(300);

        this.elements.nearMissCard.style.display = 'none';
        this.elements.nearMissCard.style.animation = '';
    }

    /**
     * Show near-miss message (simplified, no animation)
     */
    _showNearMissMessage(message) {
        if (!this.elements.nearMissCard) {
            return;
        }

        this.elements.nearMissCard.innerHTML = `
            <div class="near-miss-content">
                <div class="near-miss-emoji">💪</div>
                <div class="near-miss-message">${message}</div>
            </div>
        `;

        this.elements.nearMissCard.style.display = 'block';

        setTimeout(() => {
            this.elements.nearMissCard.style.display = 'none';
        }, 2000);
    }


    /**
     * Utility: wait for specified duration
     */
    _wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Update progress star fill level
     * @param {string} level - 'empty', 'bronze', 'silver', 'gold'
     */
    updateProgressStar(level) {
        if (!this.elements.progressStar) {
            return;
        }

        // Remove all level classes
        this.elements.progressStar.classList.remove('star-empty', 'star-bronze', 'star-silver', 'star-gold');

        // Add new level class
        this.elements.progressStar.classList.add(`star-${level}`);

        // Play fill animation
        if (level !== 'empty' && !this.options.reducedMotion) {
            this.elements.progressStar.style.animation = 'star-fill 600ms ease-out';
            setTimeout(() => {
                this.elements.progressStar.style.animation = '';
            }, 600);
        }
    }

    /**
     * Show sticker collection on end screen
     * @param {Array} stickers - Array of sticker IDs
     * @param {Function} getStickerMetadata - Function to get sticker metadata
     */
    renderStickers(stickers, getStickerMetadata) {
        const container = document.getElementById('stickerCollection');
        if (!container) {
            return;
        }

        if (stickers.length === 0) {
            container.style.display = 'none';
            return;
        }

        let html = '<div class="sticker-collection-title">Wat je deze ronde hebt ontdekt:</div>';
        html += '<div class="sticker-grid">';

        stickers.forEach(stickerId => {
            const meta = getStickerMetadata(stickerId);
            if (!meta) {
                return;
            }

            html += `
                <div class="sticker-card">
                    <div class="sticker-emoji">${meta.emoji}</div>
                    <div class="sticker-title">${meta.title}</div>
                    <div class="sticker-description">${meta.description}</div>
                </div>
            `;
        });

        html += '</div>';
        html += '<div class="sticker-disclaimer">Blijft bewaard op dit apparaat.</div>';

        container.innerHTML = html;
        container.style.display = 'block';
    }

    /**
     * Clean up and reset
     */
    reset() {
        // Hide all UI elements
        if (this.elements.streakCard) {
            this.elements.streakCard.style.display = 'none';
        }
        if (this.elements.multiplierBadge) {
            this.elements.multiplierBadge.style.display = 'none';
        }
        if (this.elements.shieldBadge) {
            this.elements.shieldBadge.style.display = 'none';
        }
        if (this.elements.nearMissCard) {
            this.elements.nearMissCard.style.display = 'none';
        }

        // Clear animation queue
        this.animationQueue = [];
        this.isAnimating = false;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { StreakAnimationController };
}
