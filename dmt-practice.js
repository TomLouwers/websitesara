/**
 * DMT Word Trainer - Practice Mode
 *
 * A reusable module for practicing word reading with auto-rotation.
 * Implements tempo control, ramp-up, length-based pauses, and norming display.
 *
 * Configuration defaults (can be tuned):
 * - Base tempos: A=720ms, B=1000ms, C=1350ms (for "Normaal")
 * - Tempo multipliers: Rustig=1.25, Normaal=1.0, Snel=0.8
 * - Ramp-up: First 10 words at +15% slower, next 5 words linear interpolation
 * - Length adjustments: +150ms for words >= 12 chars, +300ms for >= 16 chars
 */

class DMTPractice {
    constructor() {
        // Configuration - EASY TO TUNE
        this.config = {
            baseTempos: {
                A: 720,   // ms per word for "Normaal"
                B: 1000,
                C: 1350
            },
            tempoMultipliers: {
                rustig: 1.25,   // 25% slower
                normaal: 1.0,   // base tempo
                snel: 0.8       // 20% faster
            },
            rampUp: {
                warmupWords: 10,        // First N words run slower
                transitionWords: 5,     // Next N words interpolate
                warmupSlowdown: 0.15    // 15% slower during warmup
            },
            lengthAdjustments: {
                medium: { minLength: 12, adjustment: 150 },  // +150ms
                long: { minLength: 16, adjustment: 300 }     // +300ms
            }
        };

        // State
        this.state = {
            selectedList: null,
            selectedTempo: null,
            words: [],
            currentIndex: 0,
            isRunning: false,
            isPaused: false,
            startTime: null,
            totalWordsSeen: 0
        };

        // Timer
        this.intervalId = null;

        // Data
        this.wordLists = {};
        this.normingData = null;

        // Init
        this.init();
    }

    async init() {
        await this.loadData();
        this.setupEventListeners();
        this.checkURLParams();
    }

    checkURLParams() {
        // Check if list and tempo are provided in URL
        const urlParams = new URLSearchParams(window.location.search);
        const list = urlParams.get('list');
        const tempo = urlParams.get('tempo');

        if (list && tempo) {
            // Auto-start with URL parameters
            this.state.selectedList = list.toUpperCase();
            this.state.selectedTempo = tempo.toLowerCase();

            // Validate parameters
            if (this.wordLists[this.state.selectedList] && this.config.tempoMultipliers[this.state.selectedTempo]) {
                // Start immediately
                this.startPractice();
            } else {
                console.error('Invalid URL parameters:', { list, tempo });
                alert('Ongeldige parameters. Kies opnieuw je lijst en tempo.');
            }
        }
    }

    async loadData() {
        try {
            // Load word lists
            const [listA, listB, listC, norming] = await Promise.all([
                fetch('exercises/tl/dmt_list_A_v1.json').then(r => r.json()),
                fetch('exercises/tl/dmt_list_B_v1.json').then(r => r.json()),
                fetch('exercises/tl/dmt_list_C_v1.json').then(r => r.json()),
                fetch('exercises/tl/dmt_norming_v1.json').then(r => r.json())
            ]);

            this.wordLists = {
                A: listA.list.words,
                B: listB.list.words,
                C: listC.list.words
            };

            this.normingData = norming;

            console.log('DMT data loaded:', {
                A: this.wordLists.A.length,
                B: this.wordLists.B.length,
                C: this.wordLists.C.length
            });
        } catch (error) {
            console.error('Error loading DMT data:', error);
            alert('Er is een fout opgetreden bij het laden van de woordenlijsten.');
        }
    }

    setupEventListeners() {
        // Set default tempo to "normaal"
        this.state.selectedTempo = 'normaal';

        // List selection
        document.querySelectorAll('.dmt-list-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.dmt-list-btn').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                this.state.selectedList = btn.dataset.list;
                this.updateStartButton();
            });
        });

        // Tempo selection
        document.querySelectorAll('.dmt-tempo-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.dmt-tempo-btn').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                this.state.selectedTempo = btn.dataset.tempo;
                this.updateStartButton();
            });
        });

        // Start button
        document.getElementById('startBtn').addEventListener('click', () => {
            this.startPractice();
        });

        // Practice controls
        document.getElementById('pauseBtn').addEventListener('click', () => {
            this.togglePause();
        });

        document.getElementById('tempoBtn').addEventListener('click', () => {
            this.showTempoModal();
        });

        document.getElementById('stopBtn').addEventListener('click', () => {
            this.stopPractice();
        });

        // Tempo modal
        document.querySelectorAll('.dmt-tempo-modal-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.changeTempo(btn.dataset.tempo);
            });
        });

        document.getElementById('tempoModalClose').addEventListener('click', () => {
            this.hideTempoModal();
        });

        // Results buttons
        document.getElementById('restartBtn').addEventListener('click', () => {
            this.restart();
        });

        document.getElementById('homeBtn').addEventListener('click', () => {
            window.location.href = 'index.html';
        });
    }

    updateStartButton() {
        const startBtn = document.getElementById('startBtn');
        if (this.state.selectedList && this.state.selectedTempo) {
            startBtn.disabled = false;
        } else {
            startBtn.disabled = true;
        }
    }

    startPractice() {
        // Load words for selected list
        this.state.words = [...this.wordLists[this.state.selectedList]];
        this.state.currentIndex = 0;
        this.state.totalWordsSeen = 0;
        this.state.startTime = Date.now();
        this.state.isRunning = true;
        this.state.isPaused = false;

        // Show practice screen
        document.getElementById('setupScreen').style.display = 'none';
        document.getElementById('practiceScreen').style.display = 'block';

        // Update breadcrumb
        this.updateBreadcrumb();

        // Update tempo indicator
        this.updateTempoIndicator();

        // Start word rotation
        this.showNextWord();
        this.scheduleNextWord();
    }

    updateBreadcrumb() {
        const tempoLabels = {
            rustig: 'Rustig aan',
            normaal: 'Gaat goed',
            snel: 'Gas erop'
        };

        const breadcrumbInfo = document.getElementById('breadcrumbInfo');
        if (breadcrumbInfo) {
            breadcrumbInfo.textContent = `Lijst ${this.state.selectedList} - ${tempoLabels[this.state.selectedTempo]}`;
        }
    }

    showNextWord() {
        if (this.state.currentIndex >= this.state.words.length) {
            // All words shown, go to results
            this.showResults();
            return;
        }

        const word = this.state.words[this.state.currentIndex];
        document.getElementById('wordDisplay').textContent = word.word;
        this.state.totalWordsSeen++;
        document.getElementById('wordCount').textContent = this.state.totalWordsSeen;
    }

    scheduleNextWord() {
        if (!this.state.isRunning || this.state.isPaused) {
            return;
        }

        const interval = this.calculateInterval(this.state.currentIndex);

        this.intervalId = setTimeout(() => {
            this.state.currentIndex++;
            this.showNextWord();
            this.scheduleNextWord();
        }, interval);
    }

    calculateInterval(wordIndex) {
        // 1. Get base tempo for this list and selected tempo
        const baseTempo = this.config.baseTempos[this.state.selectedList];
        const tempoMultiplier = this.config.tempoMultipliers[this.state.selectedTempo];
        let interval = baseTempo * tempoMultiplier;

        // 2. Apply ramp-up (first 15 words)
        const { warmupWords, transitionWords, warmupSlowdown } = this.config.rampUp;

        if (wordIndex < warmupWords) {
            // Warmup phase: add 15% to interval
            interval = interval * (1 + warmupSlowdown);
        } else if (wordIndex < warmupWords + transitionWords) {
            // Transition phase: linearly interpolate from warmup to normal
            const transitionProgress = (wordIndex - warmupWords) / transitionWords;
            const warmupInterval = interval * (1 + warmupSlowdown);
            const normalInterval = interval;
            interval = warmupInterval + (normalInterval - warmupInterval) * transitionProgress;
        }

        // 3. Apply length-based adjustments
        const word = this.state.words[wordIndex];
        const wordLength = word.word.length;

        if (wordLength >= this.config.lengthAdjustments.long.minLength) {
            interval += this.config.lengthAdjustments.long.adjustment;
        } else if (wordLength >= this.config.lengthAdjustments.medium.minLength) {
            interval += this.config.lengthAdjustments.medium.adjustment;
        }

        return Math.round(interval);
    }

    togglePause() {
        this.state.isPaused = !this.state.isPaused;

        const pauseBtn = document.getElementById('pauseBtn');
        const pauseBtnIcon = document.getElementById('pauseBtnIcon');
        const pauseBtnText = document.getElementById('pauseBtnText');
        const pausedOverlay = document.getElementById('pausedOverlay');

        if (this.state.isPaused) {
            // Pause
            if (this.intervalId) {
                clearTimeout(this.intervalId);
                this.intervalId = null;
            }
            pauseBtnIcon.textContent = '▶';
            pauseBtnText.textContent = 'Hervatten';
            pausedOverlay.classList.add('show');
        } else {
            // Resume
            pauseBtnIcon.textContent = '⏸';
            pauseBtnText.textContent = 'Pauze';
            pausedOverlay.classList.remove('show');
            this.scheduleNextWord();
        }
    }

    showTempoModal() {
        // Pause if running
        if (this.state.isRunning && !this.state.isPaused) {
            this.togglePause();
        }

        // Show modal
        document.getElementById('tempoModal').classList.add('show');

        // Highlight current tempo
        document.querySelectorAll('.dmt-tempo-modal-btn').forEach(btn => {
            if (btn.dataset.tempo === this.state.selectedTempo) {
                btn.classList.add('selected');
            } else {
                btn.classList.remove('selected');
            }
        });
    }

    hideTempoModal() {
        document.getElementById('tempoModal').classList.remove('show');

        // Resume if was paused by modal
        if (this.state.isRunning && this.state.isPaused) {
            this.togglePause();
        }
    }

    changeTempo(newTempo) {
        this.state.selectedTempo = newTempo;
        this.updateTempoIndicator();
        this.hideTempoModal();
    }

    updateTempoIndicator() {
        const tempoEmojis = {
            rustig: '🐢',
            normaal: '🙂',
            snel: '🚀'
        };

        const tempoLabels = {
            rustig: 'Rustig aan',
            normaal: 'Gaat goed',
            snel: 'Gas erop'
        };

        document.getElementById('tempoEmoji').textContent = tempoEmojis[this.state.selectedTempo];
        document.getElementById('tempoLabel').textContent = tempoLabels[this.state.selectedTempo];
    }

    stopPractice() {
        if (confirm('Weet je zeker dat je wilt stoppen? Je voortgang gaat verloren.')) {
            this.state.isRunning = false;
            if (this.intervalId) {
                clearTimeout(this.intervalId);
                this.intervalId = null;
            }
            this.showResults();
        }
    }

    showResults() {
        this.state.isRunning = false;
        if (this.intervalId) {
            clearTimeout(this.intervalId);
            this.intervalId = null;
        }

        // Calculate results
        const totalWordsSeen = this.state.totalWordsSeen;
        const elapsedTime = (Date.now() - this.state.startTime) / 1000; // seconds
        const wordsPerMinute = Math.round((totalWordsSeen / elapsedTime) * 60);

        // Update results display
        document.getElementById('totalWordsResult').textContent = totalWordsSeen;
        document.getElementById('wordsPerMinuteResult').textContent = wordsPerMinute;

        // Calculate norming
        this.displayNorming(wordsPerMinute);

        // Show results screen
        document.getElementById('practiceScreen').style.display = 'none';
        document.getElementById('resultsScreen').style.display = 'block';
    }

    displayNorming(wordsPerMinute) {
        // Try to get user's grade level from localStorage
        const userGrade = this.getUserGrade();

        if (!userGrade || !this.normingData) {
            return;
        }

        const listId = this.state.selectedList;
        const norms = this.normingData.norms[listId];

        if (!norms || !norms[userGrade]) {
            return;
        }

        const gradeNorms = norms[userGrade];

        // Determine band with positive framing
        let band = 'average';
        let bandLabel = 'Goed bezig!';
        let bandClass = 'average';

        if (wordsPerMinute <= gradeNorms.weak_max) {
            band = 'developing';
            bandLabel = 'Je bent aan het groeien! 🌱';
            bandClass = 'developing';
        } else if (wordsPerMinute >= gradeNorms.good_min + 20) {
            // Excellent: significantly above good threshold
            band = 'excellent';
            bandLabel = 'Supergoed! 🌟';
            bandClass = 'excellent';
        } else if (wordsPerMinute >= gradeNorms.good_min) {
            band = 'good';
            bandLabel = 'Knap gedaan! 👍';
            bandClass = 'good';
        }

        // Update display
        const normingBand = document.getElementById('normingBand');
        normingBand.textContent = bandLabel;
        normingBand.className = `dmt-norming-band ${bandClass}`;

        // Update explanation with positive messaging
        let explanation = '';
        if (band === 'developing') {
            explanation = `Je bent goed bezig met oefenen! Met meer oefening word je steeds sneller en beter. Je kunt het! 💪`;
        } else if (band === 'average') {
            explanation = `Je leest lekker door! Je score ligt binnen het gemiddelde voor jouw leeftijd (${gradeNorms.average_min}-${gradeNorms.average_max} woorden/min). Ga zo door! 👍`;
        } else if (band === 'good') {
            explanation = `Wat lees je goed! Je score ligt boven het gemiddelde voor jouw leeftijd. Geweldig gedaan! 🎉`;
        } else if (band === 'excellent') {
            explanation = `Wauw! Je bent een super snelle lezer! Je score is fantastisch voor jouw leeftijd. Heel knap! 🌟⭐`;
        }

        document.getElementById('normingExplanation').textContent = explanation;
    }

    getUserGrade() {
        // Try to get grade from various localStorage keys
        // This is a fallback - ideally the app should have a consistent way to store this
        const level = localStorage.getItem('selectedLevel');

        if (level) {
            // Convert level like "groep8" to "group_8"
            const match = level.match(/groep(\d+)/);
            if (match) {
                return `group_${match[1]}`;
            }
        }

        // Default to group_6 if not found (middle of the range)
        return 'group_6';
    }

    restart() {
        // Go back to level selector to choose again
        window.location.href = 'level-selector.html?subject=dmt';
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dmtPractice = new DMTPractice();
});
