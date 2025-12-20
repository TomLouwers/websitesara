/**
 * Shared Utility Modules for Educational Platform
 * Provides reusable functionality across all quiz modules
 */

// ============================================================================
// STORAGE MANAGER - Optimized localStorage operations with caching
// ============================================================================

class StorageManager {
    constructor() {
        this.cache = new Map();
        this.writeQueue = new Map();
        this.flushTimer = null;
    }

    /**
     * Get value from cache or localStorage
     * @param {string} key - Storage key
     * @param {*} defaultValue - Default value if not found
     * @returns {*} Retrieved value or default
     */
    get(key, defaultValue = null) {
        if (this.cache.has(key)) {
            return this.cache.get(key);
        }

        try {
            const value = localStorage.getItem(key);
            if (value !== null) {
                const parsed = this.parseValue(value);
                this.cache.set(key, parsed);
                return parsed;
            }
        } catch (e) {
            console.warn(`StorageManager: Failed to get ${key}:`, e);
        }

        return defaultValue;
    }

    /**
     * Set value with write batching for performance
     * @param {string} key - Storage key
     * @param {*} value - Value to store
     */
    set(key, value) {
        this.cache.set(key, value);
        this.writeQueue.set(key, value);

        clearTimeout(this.flushTimer);
        this.flushTimer = setTimeout(() => this.flush(), 300);
    }

    /**
     * Flush pending writes to localStorage
     */
    flush() {
        this.writeQueue.forEach((value, key) => {
            try {
                const serialized = typeof value === 'string' ? value : JSON.stringify(value);
                localStorage.setItem(key, serialized);
            } catch (e) {
                console.warn(`StorageManager: Failed to set ${key}:`, e);
            }
        });
        this.writeQueue.clear();
    }

    /**
     * Remove item from cache and storage
     * @param {string} key - Storage key
     */
    remove(key) {
        this.cache.delete(key);
        this.writeQueue.delete(key);
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.warn(`StorageManager: Failed to remove ${key}:`, e);
        }
    }

    /**
     * Parse stored value (handles JSON and primitives)
     * @param {string} value - Raw stored value
     * @returns {*} Parsed value
     */
    parseValue(value) {
        // Try parsing as JSON first
        if (value.startsWith('{') || value.startsWith('[')) {
            try {
                return JSON.parse(value);
            } catch (e) {
                return value;
            }
        }

        // Handle booleans
        if (value === 'true') return true;
        if (value === 'false') return false;

        // Handle numbers
        if (!isNaN(value) && value !== '') {
            return Number(value);
        }

        return value;
    }

    /**
     * Clear all cache and optionally storage
     * @param {boolean} clearStorage - Whether to clear localStorage too
     */
    clear(clearStorage = false) {
        this.cache.clear();
        this.writeQueue.clear();
        clearTimeout(this.flushTimer);

        if (clearStorage) {
            try {
                localStorage.clear();
            } catch (e) {
                console.warn('StorageManager: Failed to clear storage:', e);
            }
        }
    }
}

// Global instance
const storage = new StorageManager();


// ============================================================================
// AUDIO MANAGER - Unified audio playback with TTS fallback
// ============================================================================

class AudioManager {
    constructor() {
        this.currentAudio = null;
        this.isPlaying = false;
    }

    /**
     * Play audio file with automatic fallback to Text-to-Speech
     * @param {string} audioPath - Path to audio file
     * @param {string} fallbackText - Text for TTS if audio fails
     * @param {Object} options - Playback options
     * @returns {Promise<void>}
     */
    async playAudio(audioPath, fallbackText, options = {}) {
        const { timeout = 2000, onProgress = null } = options;

        // Stop any currently playing audio
        this.stop();

        // Try playing audio file first
        try {
            await this.playAudioFile(audioPath, timeout, onProgress);
        } catch (error) {
            console.log('Audio playback failed, using TTS:', error.message);

            // Fallback to Text-to-Speech
            if (fallbackText) {
                await this.playTextToSpeech(fallbackText);
            } else {
                throw new Error('No fallback text provided for TTS');
            }
        }
    }

    /**
     * Play audio file with timeout
     * @private
     */
    playAudioFile(audioPath, timeout, onProgress) {
        return new Promise((resolve, reject) => {
            const audio = new Audio(audioPath);
            this.currentAudio = audio;
            this.isPlaying = true;

            let timeoutId = null;
            let hasResolved = false;

            const cleanup = () => {
                clearTimeout(timeoutId);
                this.isPlaying = false;
                if (this.currentAudio === audio) {
                    this.currentAudio = null;
                }
            };

            const complete = (error = null) => {
                if (hasResolved) return;
                hasResolved = true;
                cleanup();
                error ? reject(error) : resolve();
            };

            // Set timeout for loading
            timeoutId = setTimeout(() => {
                complete(new Error('Audio loading timeout'));
            }, timeout);

            // Event handlers
            audio.addEventListener('ended', () => complete());
            audio.addEventListener('error', (e) => {
                complete(new Error(`Audio error: ${e.message || 'Unknown error'}`));
            });

            if (onProgress) {
                audio.addEventListener('timeupdate', () => {
                    onProgress(audio.currentTime, audio.duration);
                });
            }

            // Start playback
            audio.play().catch((e) => {
                complete(new Error(`Playback failed: ${e.message}`));
            });
        });
    }

    /**
     * Use Web Speech API for text-to-speech
     * @private
     */
    playTextToSpeech(text) {
        return new Promise((resolve, reject) => {
            if (!('speechSynthesis' in window)) {
                reject(new Error('Text-to-Speech not supported'));
                return;
            }

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'nl-NL';
            utterance.rate = 0.9;

            this.isPlaying = true;

            utterance.addEventListener('end', () => {
                this.isPlaying = false;
                resolve();
            });

            utterance.addEventListener('error', (e) => {
                this.isPlaying = false;
                reject(new Error(`TTS error: ${e.error}`));
            });

            window.speechSynthesis.speak(utterance);
        });
    }

    /**
     * Stop current audio playback
     */
    stop() {
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
            this.currentAudio = null;
        }

        if (window.speechSynthesis && window.speechSynthesis.speaking) {
            window.speechSynthesis.cancel();
        }

        this.isPlaying = false;
    }

    /**
     * Check if audio is currently playing
     * @returns {boolean}
     */
    getIsPlaying() {
        return this.isPlaying;
    }
}

// Global instance
const audioManager = new AudioManager();


// ============================================================================
// BASE QUIZ MODULE - Shared quiz functionality
// ============================================================================

class BaseQuizModule {
    constructor(config = {}) {
        this.state = {
            data: [],
            currentIndex: 0,
            score: 0,
            totalQuestions: 0,
            currentItem: null,
            hasAnswered: false,
            wrongAnswers: [],
            startTime: null,
            endTime: null
        };

        this.config = {
            storagePrefix: config.storagePrefix || 'quiz_',
            enableProgressTracking: config.enableProgressTracking !== false,
            ...config
        };

        this.elements = {};
    }

    /**
     * Initialize quiz with data
     * @param {Array} data - Quiz questions/items
     */
    initialize(data) {
        this.state.data = data;
        this.state.totalQuestions = data.length;
        this.state.currentIndex = 0;
        this.state.score = 0;
        this.state.wrongAnswers = [];
        this.state.startTime = Date.now();
        this.state.endTime = null;

        this.loadCurrentItem();
    }

    /**
     * Load current item based on index
     */
    loadCurrentItem() {
        if (this.state.currentIndex < this.state.data.length) {
            this.state.currentItem = this.state.data[this.state.currentIndex];
            this.state.hasAnswered = false;
            return this.state.currentItem;
        }
        return null;
    }

    /**
     * Move to next item
     * @returns {boolean} True if there are more items
     */
    nextItem() {
        this.state.currentIndex++;

        if (this.state.currentIndex >= this.state.totalQuestions) {
            this.state.endTime = Date.now();
            return false;
        }

        return this.loadCurrentItem() !== null;
    }

    /**
     * Check answer and update score
     * @param {*} userAnswer - User's answer
     * @param {*} correctAnswer - Correct answer
     * @param {boolean} caseSensitive - Whether comparison is case-sensitive
     * @returns {boolean} True if answer is correct
     */
    checkAnswer(userAnswer, correctAnswer, caseSensitive = false) {
        if (this.state.hasAnswered) {
            return false;
        }

        const normalizedUser = caseSensitive
            ? String(userAnswer).trim()
            : String(userAnswer).trim().toLowerCase();

        const normalizedCorrect = caseSensitive
            ? String(correctAnswer).trim()
            : String(correctAnswer).trim().toLowerCase();

        const isCorrect = normalizedUser === normalizedCorrect;

        if (isCorrect) {
            this.state.score++;
        } else {
            this.state.wrongAnswers.push({
                index: this.state.currentIndex,
                item: this.state.currentItem,
                userAnswer,
                correctAnswer
            });
        }

        this.state.hasAnswered = true;
        return isCorrect;
    }

    /**
     * Update progress display
     */
    updateProgress() {
        const progressText = `${this.state.currentIndex + 1} / ${this.state.totalQuestions}`;
        const progressPercent = ((this.state.currentIndex + 1) / this.state.totalQuestions) * 100;

        if (this.elements.progressText) {
            this.elements.progressText.textContent = progressText;
        }

        if (this.elements.progressBar) {
            this.elements.progressBar.style.width = `${progressPercent}%`;
        }
    }

    /**
     * Update score display
     */
    updateScore() {
        const scoreText = `${this.state.score} / ${this.state.totalQuestions}`;

        if (this.elements.scoreText) {
            this.elements.scoreText.textContent = scoreText;
        }
    }

    /**
     * Calculate final results
     * @returns {Object} Results object
     */
    getResults() {
        const percentage = (this.state.score / this.state.totalQuestions) * 100;
        const duration = this.state.endTime ? this.state.endTime - this.state.startTime : 0;

        return {
            score: this.state.score,
            total: this.state.totalQuestions,
            percentage: Math.round(percentage),
            wrongAnswers: this.state.wrongAnswers,
            duration,
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Save progress to storage
     */
    saveProgress() {
        if (!this.config.enableProgressTracking) return;

        const key = `${this.config.storagePrefix}progress`;
        storage.set(key, {
            currentIndex: this.state.currentIndex,
            score: this.state.score,
            wrongAnswers: this.state.wrongAnswers,
            timestamp: Date.now()
        });
    }

    /**
     * Load progress from storage
     * @returns {Object|null} Saved progress or null
     */
    loadProgress() {
        if (!this.config.enableProgressTracking) return null;

        const key = `${this.config.storagePrefix}progress`;
        return storage.get(key);
    }

    /**
     * Clear saved progress
     */
    clearProgress() {
        const key = `${this.config.storagePrefix}progress`;
        storage.remove(key);
    }

    /**
     * Reset quiz state
     */
    reset() {
        this.state.currentIndex = 0;
        this.state.score = 0;
        this.state.wrongAnswers = [];
        this.state.hasAnswered = false;
        this.state.startTime = Date.now();
        this.state.endTime = null;
        this.loadCurrentItem();
    }

    /**
     * Cache DOM elements for performance
     * @param {Object} elementMap - Map of element IDs/selectors
     */
    cacheElements(elementMap) {
        Object.entries(elementMap).forEach(([key, selector]) => {
            this.elements[key] = document.getElementById(selector) || document.querySelector(selector);
        });
    }
}


// ============================================================================
// DOM UTILITIES - Efficient DOM manipulation helpers
// ============================================================================

const DOMUtils = {
    /**
     * Reset form elements to initial state
     * @param {Array<string>} elementIds - Array of element IDs
     */
    resetFormElements(elementIds) {
        elementIds.forEach(id => {
            const el = document.getElementById(id);
            if (!el) return;

            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.value = '';
                el.disabled = false;
            }

            el.classList.remove('incorrect', 'correct', 'disabled', 'active');
        });
    },

    /**
     * Toggle button states in a group
     * @param {NodeList} buttons - Button elements
     * @param {string} activeValue - Value of active button
     * @param {string} dataAttribute - Data attribute to check (default: 'data-value')
     */
    toggleButtonGroup(buttons, activeValue, dataAttribute = 'value') {
        buttons.forEach(btn => {
            const isActive = btn.dataset[dataAttribute] === activeValue;
            btn.classList.toggle('active', isActive);
        });
    },

    /**
     * Show element with optional animation
     * @param {HTMLElement} element - Element to show
     * @param {string} display - Display value (default: 'block')
     */
    show(element, display = 'block') {
        if (!element) return;
        element.style.display = display;
    },

    /**
     * Hide element
     * @param {HTMLElement} element - Element to hide
     */
    hide(element) {
        if (!element) return;
        element.style.display = 'none';
    },

    /**
     * Toggle element visibility
     * @param {HTMLElement} element - Element to toggle
     * @param {boolean} force - Force show (true) or hide (false)
     */
    toggle(element, force) {
        if (!element) return;

        if (force !== undefined) {
            element.style.display = force ? 'block' : 'none';
        } else {
            element.style.display = element.style.display === 'none' ? 'block' : 'none';
        }
    },

    /**
     * Create element from HTML string
     * @param {string} html - HTML string
     * @returns {HTMLElement} Created element
     */
    createFromHTML(html) {
        const template = document.createElement('template');
        template.innerHTML = html.trim();
        return template.content.firstChild;
    },

    /**
     * Debounce function calls
     * @param {Function} func - Function to debounce
     * @param {number} delay - Delay in milliseconds
     * @returns {Function} Debounced function
     */
    debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }
};


// ============================================================================
// EXPORT FOR MODULE USAGE
// ============================================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        StorageManager,
        storage,
        AudioManager,
        audioManager,
        BaseQuizModule,
        DOMUtils
    };
}
