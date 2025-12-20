/**
 * Spelling Quiz Module - Refactored Version
 * Uses BaseQuizModule and AudioManager from utils.js
 * Optimized with improved error handling and performance
 */

class SpellingQuiz extends BaseQuizModule {
    constructor() {
        super({
            storagePrefix: 'spelling_quiz_',
            enableProgressTracking: true
        });

        this.attemptCount = 0;
        this.maxAttempts = 3;
        this.currentAudioPath = null;
    }

    /**
     * Initialize the quiz
     */
    async init() {
        try {
            this.cacheElements({
                spellingInput: 'spellingInput',
                checkButton: 'checkButton',
                audioPlayButton: 'audioPlayButton',
                playIcon: 'playIcon',
                nextButton: 'nextButton',
                feedbackSection: 'feedbackSection',
                feedbackIcon: 'feedbackIcon',
                feedbackTitle: 'feedbackTitle',
                correctSpellingDisplay: 'correctSpellingDisplay',
                explanationContent: 'explanationContent',
                visualExplanation: 'visualExplanation',
                progressLabel: 'progressLabel',
                progressBarFill: 'progressBarFill',
                scoreDisplay: 'scoreDisplay',
                breadcrumbLevel: 'breadcrumbLevel'
            });

            await this.loadSpellingData();
            this.attachEventListeners();
            this.showWord(0);
        } catch (error) {
            console.error('Error initializing spelling quiz:', error);
            this.showError('Kon de spellingquiz niet laden. Probeer het opnieuw.');
        }
    }

    /**
     * Load spelling data from localStorage and JSON file
     * @private
     */
    async loadSpellingData() {
        try {
            // Get subject info from localStorage (set by theme-selector)
            const subject = storage.get('autoStartSubject');
            const theme = storage.get('autoStartTheme');
            const level = storage.get('autoStartLevel', 'groep4');

            // Update breadcrumb
            if (this.elements.breadcrumbLevel) {
                this.elements.breadcrumbLevel.textContent = this.formatLevel(level);
            }

            // Load JSON data
            const filename = `spelling-${level}.json`;
            const response = await fetch(filename);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: Could not load ${filename}`);
            }

            let spellingData = await response.json();

            // Validate data
            if (!Array.isArray(spellingData) || spellingData.length === 0) {
                throw new Error('Invalid or empty spelling data');
            }

            // Filter by theme if specified
            if (theme) {
                spellingData = spellingData.filter(word => word.theme === theme);
            }

            // Shuffle words for variety
            this.shuffleArray(spellingData);

            // Initialize with data
            this.initialize(spellingData);

            if (spellingData.length === 0) {
                throw new Error('No spelling words found for this level/theme');
            }
        } catch (error) {
            console.error('Error loading spelling data:', error);
            throw error; // Re-throw to be caught by init()
        }
    }

    /**
     * Attach event listeners
     * @private
     */
    attachEventListeners() {
        const { spellingInput, checkButton, audioPlayButton, nextButton } = this.elements;

        // Check button
        if (checkButton) {
            checkButton.addEventListener('click', () => this.checkAnswer());
        }

        // Enter key to check
        if (spellingInput) {
            spellingInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !this.state.hasAnswered) {
                    this.checkAnswer();
                }
            });
        }

        // Audio play button
        if (audioPlayButton) {
            audioPlayButton.addEventListener('click', () => this.playAudio());
        }

        // Next button
        if (nextButton) {
            nextButton.addEventListener('click', () => this.next());
        }
    }

    /**
     * Show a word
     * @param {number} index - Word index
     */
    showWord(index) {
        if (index >= this.state.totalQuestions) {
            this.showResults();
            return;
        }

        this.state.currentIndex = index;
        this.loadCurrentItem();
        this.attemptCount = 0;

        // Update UI
        this.updateProgress();
        this.resetWordUI();
        this.loadAudioPath();

        // Focus input
        this.elements.spellingInput?.focus();

        // Auto-play audio on load (optional)
        // this.playAudio();
    }

    /**
     * Load audio path for current word
     * @private
     */
    loadAudioPath() {
        const word = this.state.currentItem;
        if (!word) return;

        // Determine audio path
        if (word.audio_url) {
            this.currentAudioPath = word.audio_url;
        } else if (word.audio_file) {
            this.currentAudioPath = `audio/spelling/${word.audio_file}`;
        } else {
            this.currentAudioPath = null; // Will use TTS
        }
    }

    /**
     * Play word audio with fallback to TTS
     */
    async playAudio() {
        const { audioPlayButton, playIcon } = this.elements;
        const word = this.state.currentItem;

        if (!word) return;

        try {
            // Update button state
            if (audioPlayButton) {
                audioPlayButton.classList.add('playing');
            }
            if (playIcon) {
                playIcon.textContent = 'volume_up';
            }

            // Use AudioManager
            await audioManager.playAudio(
                this.currentAudioPath,
                word.word,
                {
                    timeout: CONFIG.ui.audioTimeout,
                    onProgress: null
                }
            );

            // Reset button state
            if (audioPlayButton) {
                audioPlayButton.classList.remove('playing');
            }
            if (playIcon) {
                playIcon.textContent = 'play_arrow';
            }
        } catch (error) {
            console.warn('Audio playback error:', error);

            // Reset button state
            if (audioPlayButton) {
                audioPlayButton.classList.remove('playing');
            }

            // Show fallback message if TTS also failed
            if (!('speechSynthesis' in window)) {
                alert(`Audio niet beschikbaar. Het woord is: ${word.word}`);
            }
        }
    }

    /**
     * Check spelling answer
     */
    checkAnswer() {
        if (this.state.hasAnswered) return;

        const { spellingInput } = this.elements;
        const userAnswer = spellingInput?.value.trim();

        if (!userAnswer) {
            alert(CONFIG.feedback.noAnswer.openEnded);
            return;
        }

        this.attemptCount++;

        const word = this.state.currentItem;
        const isCorrect = this.checkAnswerLogic(userAnswer, word.word, false);

        if (isCorrect) {
            this.handleCorrectAnswer();
        } else {
            this.handleIncorrectAnswer(userAnswer);
        }
    }

    /**
     * Check answer logic (case-insensitive)
     * @private
     */
    checkAnswerLogic(userAnswer, correctAnswer, caseSensitive = false) {
        const normalizedUser = caseSensitive
            ? userAnswer.trim()
            : userAnswer.trim().toLowerCase();

        const normalizedCorrect = caseSensitive
            ? correctAnswer.trim()
            : correctAnswer.trim().toLowerCase();

        return normalizedUser === normalizedCorrect;
    }

    /**
     * Handle correct answer
     * @private
     */
    handleCorrectAnswer() {
        this.state.hasAnswered = true;

        // Only count as correct on first attempt
        if (this.attemptCount === 1) {
            this.state.score++;
            this.updateScore();
        }

        // Update input styling
        const { spellingInput, checkButton } = this.elements;
        if (spellingInput) {
            spellingInput.classList.add('correct');
            spellingInput.disabled = true;
        }

        if (checkButton) {
            checkButton.disabled = true;
        }

        // Show feedback
        this.showFeedback(true);
    }

    /**
     * Handle incorrect answer
     * @private
     */
    handleIncorrectAnswer(userAnswer) {
        const { spellingInput, checkButton } = this.elements;

        if (this.attemptCount >= this.maxAttempts) {
            // After max attempts, show the answer
            this.state.hasAnswered = true;

            if (spellingInput) {
                spellingInput.classList.add('incorrect');
                spellingInput.disabled = true;
            }

            if (checkButton) {
                checkButton.disabled = true;
            }

            this.showFeedback(false);

            // Track wrong answer
            if (!this.state.wrongAnswers) {
                this.state.wrongAnswers = [];
            }
            this.state.wrongAnswers.push({
                word: this.state.currentItem.word,
                userAnswer,
                attemptCount: this.attemptCount
            });
        } else {
            // Allow retry
            if (spellingInput) {
                spellingInput.classList.add('incorrect');

                // Visual feedback animation
                spellingInput.style.animation = 'shake 0.4s';
                setTimeout(() => {
                    spellingInput.style.animation = '';
                    spellingInput.classList.remove('incorrect');
                }, 400);

                // Select text for easy retry
                spellingInput.select();
            }

            // Show attempt-specific message
            const messages = [
                null, // No message on 0 attempts
                'Probeer het nog een keer! Luister goed naar het woord.',
                'Nog één kans! Let goed op alle letters.'
            ];

            if (messages[this.attemptCount]) {
                alert(messages[this.attemptCount]);
            }
        }
    }

    /**
     * Show feedback
     * @private
     */
    showFeedback(isCorrect) {
        const {
            feedbackSection,
            feedbackIcon,
            feedbackTitle,
            correctSpellingDisplay,
            explanationContent,
            visualExplanation
        } = this.elements;

        if (!feedbackSection) return;

        const word = this.state.currentItem;

        // Set feedback based on correctness
        if (isCorrect) {
            feedbackSection.className = 'feedback-section show correct';
            if (feedbackIcon) feedbackIcon.textContent = '🎉';

            if (feedbackTitle) {
                feedbackTitle.textContent = this.attemptCount === 1
                    ? 'Perfect! Helemaal goed!'
                    : 'Goed gedaan!';
            }
        } else {
            feedbackSection.className = 'feedback-section show incorrect';
            if (feedbackIcon) feedbackIcon.textContent = '💡';
            if (feedbackTitle) feedbackTitle.textContent = 'Bijna! Hier is de juiste spelling:';
        }

        // Show correct spelling
        if (correctSpellingDisplay) {
            correctSpellingDisplay.textContent = word.word;
        }

        // Show visual explanation if available
        if (word.visual_explanation && visualExplanation && explanationContent) {
            visualExplanation.style.display = 'block';
            explanationContent.innerHTML = this.formatExplanation(word.visual_explanation);
        } else if (visualExplanation) {
            visualExplanation.style.display = 'none';
        }
    }

    /**
     * Format explanation with special formatting
     * @private
     */
    formatExplanation(explanation) {
        if (typeof explanation === 'string') {
            return `<p>${explanation}</p>`;
        } else if (Array.isArray(explanation)) {
            return '<ul>' + explanation.map(item => `<li>${item}</li>`).join('') + '</ul>';
        } else if (typeof explanation === 'object') {
            let html = '';
            if (explanation.rule) {
                html += `<p><strong>Regel:</strong> ${explanation.rule}</p>`;
            }
            if (explanation.examples) {
                html += '<p><strong>Voorbeelden:</strong></p>';
                html += '<ul>' + explanation.examples.map(ex => `<li>${ex}</li>`).join('') + '</ul>';
            }
            if (explanation.tip) {
                html += `<p><strong>💡 Tip:</strong> ${explanation.tip}</p>`;
            }
            return html;
        }
        return '';
    }

    /**
     * Move to next word
     */
    next() {
        const hasMore = this.nextItem();
        if (hasMore) {
            this.showWord(this.state.currentIndex);
        } else {
            this.showResults();
        }
    }

    /**
     * Reset UI for new word
     * @private
     */
    resetWordUI() {
        DOMUtils.resetFormElements(['spellingInput', 'checkButton']);

        const { feedbackSection, audioPlayButton } = this.elements;

        if (feedbackSection) {
            feedbackSection.classList.remove('show');
        }

        if (audioPlayButton) {
            audioPlayButton.classList.remove('playing');
        }
    }

    /**
     * Update progress bar and label
     */
    updateProgress() {
        const { progressLabel, progressBarFill } = this.elements;

        const current = this.state.currentIndex + 1;
        const total = this.state.totalQuestions;
        const percentage = (current / total) * 100;

        if (progressLabel) {
            progressLabel.textContent = `${current} / ${total}`;
        }

        if (progressBarFill) {
            progressBarFill.style.width = `${percentage}%`;
        }
    }

    /**
     * Update score display
     */
    updateScore() {
        const { scoreDisplay } = this.elements;

        if (scoreDisplay) {
            scoreDisplay.textContent = `Score: ${this.state.score} / ${this.state.totalQuestions}`;
        }
    }

    /**
     * Show results
     */
    showResults() {
        const results = this.getResults();

        // Save results to storage
        storage.set('spelling_quiz_results', results);

        // Redirect to results page or show modal
        alert(`Quiz voltooid!\n\nScore: ${results.score} / ${results.total} (${results.percentage}%)`);

        // Could redirect to a results page:
        // window.location.href = 'results.html';

        // Or go back to selection:
        window.location.href = 'index.html';
    }

    /**
     * Show error message
     * @private
     */
    showError(message) {
        alert(message);
        window.location.href = 'index.html';
    }

    /**
     * Format level for display
     * @private
     */
    formatLevel(level) {
        const levelMap = {
            'groep3': 'Groep 3',
            'groep4': 'Groep 4',
            'groep5': 'Groep 5',
            'groep6': 'Groep 6',
            'groep7': 'Groep 7',
            'groep8': 'Groep 8'
        };
        return levelMap[level] || level;
    }

    /**
     * Shuffle array in place
     * @private
     */
    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
}

// Initialize quiz on page load
document.addEventListener('DOMContentLoaded', async function() {
    const quiz = new SpellingQuiz();
    await quiz.init();

    // Expose globally for debugging
    window.spellingQuiz = quiz;
});
