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
            selectedGrade: null,
            words: [],
            currentIndex: 0,
            isRunning: false,
            isPaused: false,
            startTime: null,
            totalWordsSeen: 0,
            timeRemaining: 60
        };

        // Timers
        this.intervalId = null;
        this.countdownTimerId = null;

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
            // Set selected list and tempo from URL
            this.state.selectedList = list.toUpperCase();
            this.state.selectedTempo = tempo.toLowerCase();

            // Validate parameters
            if (this.wordLists[this.state.selectedList] && this.config.tempoMultipliers[this.state.selectedTempo]) {
                // Skip setup screen, go directly to practice screen with START button
                this.showPracticeScreen();
            } else {
                console.error('Invalid URL parameters:', { list, tempo });
                alert('Ongeldige parameters. Kies opnieuw je lijst en tempo.');
            }
        }
    }

    async loadData() {
        try {
            const dmtPaths = CONFIG.subjectFilePaths?.dmt;

            const listConfigs = [
                { key: 'A', config: dmtPaths?.listA },
                { key: 'B', config: dmtPaths?.listB },
                { key: 'C', config: dmtPaths?.listC }
            ];

            if (!dmtPaths || listConfigs.some(item => !item.config)) {
                throw new Error('DMT paden niet gevonden in configuratie');
            }

            const coreResponses = await Promise.all(
                listConfigs.map(({ config }) => fetch(config.core))
            );
            const supportResponses = await Promise.all(
                listConfigs.map(({ config }) => fetch(config.support))
            );

            const coreData = await Promise.all(coreResponses.map(r => r.json()));
            const supportData = await Promise.all(supportResponses.map(r => r.json()));

            this.wordLists = {
                A: this.transformDmtList(coreData[0], supportData[0]),
                B: this.transformDmtList(coreData[1], supportData[1]),
                C: this.transformDmtList(coreData[2], supportData[2])
            };

            // Norming data is not part of the split format; keep it null to disable norm lookup gracefully
            this.normingData = null;

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

    transformDmtList(coreData, supportData) {
        const mergedItems = (coreData.items || []).map(item => {
            const supportItem = supportData?.items?.find(s => s.item_id === item.id || s.id === item.id);
            return {
                ...item,
                feedback: supportItem?.feedback ?? item.feedback,
                adaptive: supportItem?.adaptive ?? item.adaptive,
                hints: supportItem?.hints ?? item.hints
            };
        });

        return mergedItems.map(entry => {
            const question = entry.question;
            return typeof question === 'string' ? question : (question?.text || '');
        });
    }

    setupEventListeners() {
        // Set default tempo to "normaal"
        this.state.selectedTempo = 'normaal';

        // List selection
        document.querySelectorAll('.dmt-list-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.dmt-list-btn').forEach(b => {
                    b.classList.remove('selected', 'intensity-1', 'intensity-2', 'intensity-3');
                });
                btn.classList.add('selected');
                const intensity = btn.dataset.intensity;
                if (intensity) {
                    btn.classList.add(`intensity-${intensity}`);
                }
                this.state.selectedList = btn.dataset.list;
                this.updateStartButton();
                this.updateSummary();
            });
        });

        // Tempo selection (old buttons - for backward compatibility)
        document.querySelectorAll('.dmt-tempo-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.dmt-tempo-btn').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                this.state.selectedTempo = btn.dataset.tempo;
                this.updateStartButton();
                this.updateSummary();
            });
        });

        // Speed slider (new design)
        const speedSlider = document.getElementById('speedSlider');
        if (speedSlider) {
            speedSlider.addEventListener('input', (e) => {
                this.handleSliderChange(parseInt(e.target.value));
            });
        }

        // Speed dial markers (fallback for old design)
        document.querySelectorAll('.dmt-speed-marker').forEach(marker => {
            marker.addEventListener('click', () => {
                document.querySelectorAll('.dmt-speed-marker').forEach(m => m.classList.remove('selected'));
                marker.classList.add('selected');
                this.state.selectedTempo = marker.dataset.tempo;

                // Also update hidden tempo buttons for backward compatibility
                document.querySelectorAll('.dmt-tempo-btn').forEach(btn => {
                    if (btn.dataset.tempo === marker.dataset.tempo) {
                        btn.classList.add('selected');
                    } else {
                        btn.classList.remove('selected');
                    }
                });

                this.updateStartButton();
                this.updateSummary();
            });
        });

        // Start button - shows practice screen with START button
        document.getElementById('startBtn').addEventListener('click', () => {
            this.showPracticeScreen();
        });

        // Word START button - actually starts the practice
        document.getElementById('wordStartBtn').addEventListener('click', () => {
            this.startPractice();
        });

        // Grade selection
        document.querySelectorAll('.dmt-grade-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.dmt-grade-btn').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                this.state.selectedGrade = parseInt(btn.dataset.grade);
                this.updateWordStartButton();
            });
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

    handleSliderChange(value) {
        const tempoMap = ['rustig', 'normaal', 'snel'];
        const labelMap = ['Schildpad', 'Haas', 'Raket'];

        this.state.selectedTempo = tempoMap[value];

        // Update current speed text
        const currentSpeed = document.getElementById('currentSpeed');
        if (currentSpeed) {
            currentSpeed.textContent = labelMap[value];
        }

        // Update emoji active states
        const emojis = ['emojiSlow', 'emojiNormal', 'emojiFast'];
        const labels = ['labelSlow', 'labelNormal', 'labelFast'];

        emojis.forEach((id, index) => {
            const emoji = document.getElementById(id);
            const label = document.getElementById(labels[index]);
            if (emoji && label) {
                if (index === value) {
                    emoji.classList.add('active');
                    label.classList.add('active');
                } else {
                    emoji.classList.remove('active');
                    label.classList.remove('active');
                }
            }
        });

        // Update hidden tempo buttons for backward compatibility
        document.querySelectorAll('.dmt-tempo-btn').forEach(btn => {
            if (btn.dataset.tempo === tempoMap[value]) {
                btn.classList.add('selected');
            } else {
                btn.classList.remove('selected');
            }
        });

        this.updateStartButton();
        this.updateSummary();
    }

    updateSummary() {
        const summaryElement = document.getElementById('summarySentence');
        if (!summaryElement) return;

        if (!this.state.selectedList || !this.state.selectedTempo) {
            summaryElement.classList.remove('show');
            return;
        }

        // List labels
        const listLabels = {
            A: 'Start-woorden',
            B: 'Groei-woorden',
            C: 'Knappe woorden'
        };

        // Tempo labels
        const tempoLabels = {
            rustig: 'op het tempo Rustig aan',
            normaal: 'op het tempo Gaat goed',
            snel: 'op het tempo Gas erop'
        };

        const listLabel = listLabels[this.state.selectedList];
        const tempoLabel = tempoLabels[this.state.selectedTempo];

        summaryElement.textContent = `Je gaat ${listLabel} lezen ${tempoLabel}!`;
        summaryElement.classList.add('show');
    }

    updateWordStartButton() {
        const wordStartBtn = document.getElementById('wordStartBtn');
        if (this.state.selectedGrade) {
            wordStartBtn.disabled = false;
        } else {
            wordStartBtn.disabled = true;
        }
    }

    showPracticeScreen() {
        // Load words for selected list (but don't start yet)
        this.state.words = [...this.wordLists[this.state.selectedList]];
        this.state.currentIndex = 0;
        this.state.totalWordsSeen = 0;
        this.state.timeRemaining = 60;

        // Hide setup, show practice screen
        document.getElementById('setupScreen').style.display = 'none';
        document.getElementById('practiceScreen').style.display = 'block';

        // Update breadcrumb
        this.updateBreadcrumb();

        // Update tempo indicator
        this.updateTempoIndicator();

        // Show START button, hide word display
        document.getElementById('wordStartBtn').classList.add('show');
        document.getElementById('wordDisplay').style.display = 'none';

        // Disable controls until START is clicked
        document.getElementById('pauseBtn').disabled = true;
        document.getElementById('tempoBtn').disabled = true;
        document.getElementById('stopBtn').disabled = true;
    }

    startPractice() {
        // Now actually start the practice
        this.state.startTime = Date.now();
        this.state.isRunning = true;
        this.state.isPaused = false;

        // Hide START button and grade selector, show word display
        document.getElementById('wordStartBtn').classList.remove('show');
        document.getElementById('gradeSelector').classList.add('hidden');
        document.getElementById('wordDisplay').style.display = 'block';

        // Enable controls now that practice has started
        document.getElementById('pauseBtn').disabled = false;
        document.getElementById('tempoBtn').disabled = false;
        document.getElementById('stopBtn').disabled = false;

        // Start countdown timer
        this.startCountdownTimer();

        // Start word rotation
        this.showNextWord();
        this.scheduleNextWord();
    }

    startCountdownTimer() {
        // Update timer display immediately
        this.updateTimerDisplay();

        // Start 1-second interval countdown
        this.countdownTimerId = setInterval(() => {
            if (!this.state.isPaused) {
                this.state.timeRemaining--;
                this.updateTimerDisplay();

                // Auto-stop at 0
                if (this.state.timeRemaining <= 0) {
                    this.stopPractice();
                }
            }
        }, 1000);
    }

    updateTimerDisplay() {
        const timerDisplay = document.getElementById('timerDisplay');
        if (timerDisplay) {
            timerDisplay.textContent = `${this.state.timeRemaining}s`;
        }
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
        this.state.isRunning = false;

        // Clear word rotation timer
        if (this.intervalId) {
            clearTimeout(this.intervalId);
            this.intervalId = null;
        }

        // Clear countdown timer
        if (this.countdownTimerId) {
            clearInterval(this.countdownTimerId);
            this.countdownTimerId = null;
        }

        this.showResults();
    }

    showResults() {
        this.state.isRunning = false;

        // Clear word rotation timer
        if (this.intervalId) {
            clearTimeout(this.intervalId);
            this.intervalId = null;
        }

        // Clear countdown timer
        if (this.countdownTimerId) {
            clearInterval(this.countdownTimerId);
            this.countdownTimerId = null;
        }

        // Calculate results
        const totalWordsSeen = this.state.totalWordsSeen;

        // Safety check: if startTime is null, practice never started
        const elapsedTime = this.state.startTime
            ? (Date.now() - this.state.startTime) / 1000
            : 0;

        const wordsPerMinute = elapsedTime > 0
            ? Math.round((totalWordsSeen / elapsedTime) * 60)
            : 0;

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
        // Use selected grade from state
        if (!this.state.selectedGrade || !this.normingData) {
            return;
        }

        const userGrade = `group_${this.state.selectedGrade}`;
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

    restart() {
        // Go back to level selector to choose again
        window.location.href = 'level-selector.html?subject=dmt';
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dmtPractice = new DMTPractice();
});
