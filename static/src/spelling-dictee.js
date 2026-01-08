/**
 * Spelling Dictee Module - Refactored Version
 * Uses BaseQuizModule and AudioManager from utils.js
 * Specialized for verb spelling exercises (werkwoordspelling)
 */

class SpellingDictee extends BaseQuizModule {
    constructor() {
        super({
            storagePrefix: 'spelling_dictee_',
            enableProgressTracking: true
        });

        this.quizData = null;
        this.tagStats = {};
        this.isPlayingAudio = false;
        this.audioBasePath = 'data/exercises/sp/';
    }

    /**
     * Shuffle array using Fisher-Yates algorithm
     * @private
     */
    shuffleArray(array) {
        const shuffled = [...array]; // Create a copy to avoid modifying original
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
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
                correctAnswerDisplay: 'correctAnswerDisplay',
                extraInfoSection: 'extraInfoSection',
                ruleSection: 'ruleSection',
                ruleContent: 'ruleContent',
                tipSection: 'tipSection',
                tipContent: 'tipContent',
                examplesSection: 'examplesSection',
                examplesContent: 'examplesContent',
                progressLabel: 'progressLabel',
                progressBarFill: 'progressBarFill',
                totalCorrect: 'totalCorrect',
                breadcrumbLevel: 'breadcrumbLevel',
                verbTenseInstruction: 'verbTenseInstruction',
                quizContainer: 'quizContainer',
                resultsPage: 'resultsPage'
            });

            await this.loadQuizData();
            this.attachEventListeners();
            this.showQuestion(0);
        } catch (error) {
            console.error('Error initializing spelling dictee:', error);
            this.showError('Kon de spelling data niet laden. ' + error.message);
        }
    }

    /**
     * Load quiz data from config
     * @private
     */
    async loadQuizData() {
        try {
            // Get groep and moment from localStorage (set by level-selector)
            const selectedGroep = storage.get('selectedGroep', 'groep4');
            const selectedMoment = storage.get('selectedMoment', 'm4');

            // Update breadcrumb
            if (this.elements.breadcrumbLevel) {
                const groepNumber = selectedGroep.replace('groep', '');
                const momentLetter = selectedMoment.charAt(0).toUpperCase();
                this.elements.breadcrumbLevel.textContent =
                    `Groep ${groepNumber} (${momentLetter}${groepNumber})`;
            }

            // Get file path from config
            const pathConfig = CONFIG.subjectFilePaths?.werkwoordspelling?.[selectedGroep]?.[selectedMoment];

            if (!pathConfig) {
                throw new Error(`Geen data beschikbaar voor ${selectedGroep} ${selectedMoment}`);
            }

            const corePath = typeof pathConfig === 'string' ? pathConfig : pathConfig.core;
            const supportPath = typeof pathConfig === 'object' ? pathConfig.support : null;

            // Always keep audio pointing to the original audio folder
            this.audioBasePath = 'data/exercises/sp/';

            const coreResponse = await fetch(corePath);
            if (!coreResponse.ok) {
                throw new Error(`Could not load ${corePath}`);
            }
            const coreData = await coreResponse.json();

            let supportData = null;
            if (supportPath) {
                const supportResponse = await fetch(supportPath);
                if (!supportResponse.ok) {
                    throw new Error(`Could not load ${supportPath}`);
                }
                supportData = await supportResponse.json();
            }

            const merged = this.mergeSpellingData(coreData, supportData);
            this.quizData = this.transformSpellingToLegacy(merged);

            // Validate data structure
            if (!this.quizData.set || !this.quizData.items || this.quizData.items.length === 0) {
                throw new Error('Ongeldige data structuur');
            }

            // Shuffle items for random order (like other quiz pages)
            const shuffledItems = this.shuffleArray(this.quizData.items);

            // Initialize base quiz module with shuffled items
            this.initialize(shuffledItems);

        } catch (error) {
            console.error('Error loading quiz data:', error);
            throw error;
        }
    }

    /**
     * Merge core and support data (schema v2 split format)
     * @private
     */
    mergeSpellingData(coreData, supportData) {
        if (!supportData) {
            return coreData;
        }

        const mergedItems = (coreData.items || []).map(item => {
            const supportItem = supportData.items?.find(s => s.item_id === item.id || s.id === item.id);
            return {
                ...item,
                feedback: supportItem?.feedback ?? item.feedback,
                adaptive: supportItem?.adaptive ?? item.adaptive,
                hints: supportItem?.hints ?? item.hints
            };
        });

        return {
            ...coreData,
            items: mergedItems,
            feedback: supportData.feedback || coreData.feedback
        };
    }

    /**
     * Convert schema v2 spelling data to legacy shape expected by the module
     * @private
     */
    transformSpellingToLegacy(data) {
        const firstAnswer = data.items?.[0]?.answer || {};
        const feedbackTemplates = data.feedback?.templates || {};
        const instructionText = data.items?.[0]?.question?.text || 'Schrijf op: {answer}.';

        const legacyItems = (data.items || []).map(item => {
            const answer = item.answer || {};
            return {
                id: item.id,
                difficulty: item.difficulty,
                tags: item.theme ? [item.theme] : [],
                audio: item.audio,
                prompt: {
                    sentence: item.prompt?.sentence || '',
                    instruction: item.question?.text || item.prompt?.instruction || 'Schrijf op: {answer}.'
                },
                target: {
                    answer: answer.correct_value || answer.value || '',
                    accept: answer.accepted_values || answer.accept || (answer.correct_value ? [answer.correct_value] : []),
                    case_sensitive: answer.case_sensitive,
                    trim: answer.trim_whitespace
                },
                extra_info: item.extra_info || (item.feedback?.explanation?.text ? { rule: item.feedback.explanation.text } : undefined),
                feedback: item.feedback,
                adaptive: item.adaptive,
                hints: item.hints
            };
        });

        return {
            set: {
                grade: data.metadata?.grade,
                level: data.metadata?.level,
                mode: 'dictee',
                category: data.metadata?.category || 'woordspelling',
                flags: {
                    case_sensitive: firstAnswer.case_sensitive === true,
                    trim: firstAnswer.trim_whitespace !== false
                },
                feedback_templates: {
                    correct: feedbackTemplates.correct?.default || feedbackTemplates.correct || 'Goed gedaan!',
                    incorrect: feedbackTemplates.incorrect?.first_attempt || feedbackTemplates.incorrect || 'Nog niet. Luister nog eens en probeer opnieuw.',
                    instruction: instructionText
                }
            },
            items: legacyItems
        };
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

        // Enter key support
        if (spellingInput) {
            spellingInput.addEventListener('keypress', (event) => {
                if (event.key === 'Enter' && !this.state.hasAnswered) {
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
            nextButton.addEventListener('click', () => this.nextQuestion());
        }
    }

    /**
     * Show a question
     * @param {number} index - Question index
     */
    showQuestion(index) {
        if (index >= this.state.totalQuestions) {
            this.showResults();
            return;
        }

        this.state.currentIndex = index;
        this.loadCurrentItem();

        // Update UI
        this.updateProgress();
        this.updateScore();
        this.resetUI();
        this.updateVerbTenseInstruction();

        // Focus input
        this.elements.spellingInput?.focus();
    }

    /**
     * Update progress bar and label
     */
    updateProgress() {
        const { progressLabel, progressBarFill } = this.elements;

        const total = this.state.totalQuestions;
        const current = this.state.currentIndex + 1;
        const percentage = (current / total) * 100;

        if (progressLabel) {
            progressLabel.textContent = `Vraag ${current} van ${total}`;
        }

        if (progressBarFill) {
            progressBarFill.style.width = `${percentage}%`;
        }
    }

    /**
     * Update score display
     */
    updateScore() {
        if (this.elements.totalCorrect) {
            this.elements.totalCorrect.textContent = this.state.score;
        }
    }

    /**
     * Update verb tense instruction based on tags
     * @private
     */
    updateVerbTenseInstruction() {
        const { verbTenseInstruction } = this.elements;
        if (!verbTenseInstruction) return;

        const currentItem = this.state.currentItem;

        if (!currentItem || !currentItem.tags || currentItem.tags.length === 0) {
            verbTenseInstruction.textContent = '';
            return;
        }

        // Check for specific verb tense tags
        if (currentItem.tags.includes('werkwoord_vt')) {
            verbTenseInstruction.textContent = ' in verleden tijd';
        } else if (currentItem.tags.includes('werkwoord_ttt')) {
            verbTenseInstruction.textContent = ' in tegenwoordige tijd';
        } else if (currentItem.tags.includes('voltooid_deelwoord')) {
            verbTenseInstruction.textContent = ' voltooid deelwoord';
        } else {
            verbTenseInstruction.textContent = '';
        }
    }

    /**
     * Reset UI for new question
     * @private
     */
    resetUI() {
        const { spellingInput, checkButton, feedbackSection, nextButton,
                audioPlayButton, playIcon } = this.elements;

        if (spellingInput) {
            spellingInput.value = '';
            spellingInput.className = 'spelling-input';
            spellingInput.disabled = false;
        }

        if (checkButton) {
            checkButton.disabled = false;
            checkButton.classList.remove('hidden');
        }

        if (feedbackSection) {
            feedbackSection.classList.add('hidden');
        }

        if (nextButton) {
            nextButton.classList.add('hidden');
        }

        if (audioPlayButton) {
            audioPlayButton.classList.remove('playing');
            audioPlayButton.disabled = false;
        }

        if (playIcon) {
            playIcon.textContent = 'volume_up';
        }
    }

    /**
     * Play audio (sentence then instruction)
     */
    async playAudio() {
        if (this.isPlayingAudio) return;

        this.isPlayingAudio = true;
        const { audioPlayButton, playIcon } = this.elements;
        const currentItem = this.state.currentItem;

        if (audioPlayButton) {
            audioPlayButton.disabled = true;
            audioPlayButton.classList.add('playing');
        }

        if (playIcon) {
            playIcon.textContent = 'volume_up';
        }

        try {
            // Play sentence audio
            const sentenceAudioPath = this.audioBasePath + currentItem.audio.sentence;
            await this.playAudioFile(sentenceAudioPath, currentItem.prompt.sentence);

            // Small pause between sentence and instruction
            await this.sleep(300);

            // Play instruction audio
            const instructionText = currentItem.prompt.instruction.replace(
                '{answer}',
                currentItem.target.answer
            );
            const instructionAudioPath = this.audioBasePath + currentItem.audio.instruction;
            await this.playAudioFile(instructionAudioPath, instructionText);

        } catch (error) {
            console.error('Error playing audio:', error);
        } finally {
            this.isPlayingAudio = false;
            if (audioPlayButton) {
                audioPlayButton.disabled = false;
                audioPlayButton.classList.remove('playing');
            }
        }
    }

    /**
     * Play a single audio file with TTS fallback
     * @private
     */
    async playAudioFile(audioPath, fallbackText) {
        try {
            await audioManager.playAudio(audioPath, fallbackText, {
                timeout: 5000  // Increased from 2000ms to 5000ms to prevent premature TTS fallback
            });
        } catch (error) {
            console.warn('Audio playback failed:', error);
            // AudioManager already handles TTS fallback
        }
    }

    /**
     * Helper function to sleep
     * @private
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Check answer
     */
    checkAnswer() {
        if (this.state.hasAnswered) return;

        const { spellingInput } = this.elements;
        const userAnswer = spellingInput?.value;

        if (!userAnswer || userAnswer.trim() === '') {
            alert('Vul eerst een antwoord in!');
            return;
        }

        this.state.hasAnswered = true;

        // Normalize answer based on flags
        const flags = this.quizData.set.flags;
        const normalizedUserAnswer = this.normalizeAnswer(userAnswer, flags);

        // Get accepted answers
        const currentItem = this.state.currentItem;
        const acceptedAnswers = currentItem.target.accept || [currentItem.target.answer];
        const normalizedAcceptedAnswers = acceptedAnswers.map(ans =>
            this.normalizeAnswer(ans, flags)
        );

        // Check if correct
        const isCorrect = normalizedAcceptedAnswers.includes(normalizedUserAnswer);

        if (isCorrect) {
            this.handleCorrectAnswer();
        } else {
            this.handleIncorrectAnswer(userAnswer);
        }
    }

    /**
     * Normalize answer based on flags
     * @private
     */
    normalizeAnswer(answer, flags) {
        let normalized = answer;

        if (flags.trim) {
            normalized = normalized.trim();
        }

        if (!flags.case_sensitive) {
            normalized = normalized.toLowerCase();
        }

        return normalized;
    }

    /**
     * Handle correct answer
     * @private
     */
    handleCorrectAnswer() {
        this.state.score++;
        this.updateScore();

        // Track tag stats
        const currentItem = this.state.currentItem;
        if (currentItem.tags) {
            currentItem.tags.forEach(tag => {
                if (!this.tagStats[tag]) {
                    this.tagStats[tag] = { correct: 0, total: 0 };
                }
                this.tagStats[tag].correct++;
                this.tagStats[tag].total++;
            });
        }

        const { spellingInput, checkButton, feedbackSection, feedbackIcon,
                feedbackTitle, correctAnswerDisplay, extraInfoSection, nextButton } = this.elements;

        if (spellingInput) {
            spellingInput.classList.add('correct');
            spellingInput.disabled = true;
        }

        if (checkButton) {
            checkButton.classList.add('hidden');
        }

        // Show feedback
        if (feedbackSection) {
            feedbackSection.className = 'feedback-card correct';
        }

        if (feedbackIcon) {
            feedbackIcon.textContent = '🎉';
        }

        if (feedbackTitle) {
            feedbackTitle.textContent = this.quizData.set.feedback_templates.correct || 'Goed gedaan!';
        }

        if (correctAnswerDisplay) {
            correctAnswerDisplay.textContent = 'Het juiste antwoord is: ' + currentItem.target.answer;
        }

        // Hide extra info for correct answers
        if (extraInfoSection) {
            extraInfoSection.style.display = 'none';
        }

        // Show feedback section and next button
        if (feedbackSection) {
            feedbackSection.classList.remove('hidden');
        }

        if (nextButton) {
            nextButton.classList.remove('hidden');
        }
    }

    /**
     * Handle incorrect answer
     * @private
     */
    handleIncorrectAnswer(userAnswer) {
        // Track wrong answer
        const currentItem = this.state.currentItem;
        this.state.wrongAnswers.push({
            index: this.state.currentIndex,
            item: currentItem,
            userAnswer: userAnswer
        });

        // Track tag stats
        if (currentItem.tags) {
            currentItem.tags.forEach(tag => {
                if (!this.tagStats[tag]) {
                    this.tagStats[tag] = { correct: 0, total: 0 };
                }
                this.tagStats[tag].total++;
            });
        }

        const { spellingInput, checkButton, feedbackSection, feedbackIcon,
                feedbackTitle, correctAnswerDisplay, extraInfoSection,
                ruleSection, ruleContent, tipSection, tipContent,
                examplesSection, examplesContent, nextButton } = this.elements;

        if (spellingInput) {
            spellingInput.classList.add('incorrect');
            spellingInput.disabled = true;

            // Shake animation
            spellingInput.style.animation = 'shake 0.4s';
            setTimeout(() => {
                spellingInput.style.animation = '';
            }, 400);
        }

        if (checkButton) {
            checkButton.classList.add('hidden');
        }

        // Show feedback
        if (feedbackSection) {
            feedbackSection.className = 'feedback-card incorrect';
        }

        if (feedbackIcon) {
            feedbackIcon.textContent = '💡';
        }

        if (feedbackTitle) {
            feedbackTitle.textContent = this.quizData.set.feedback_templates.incorrect ||
                'Nog niet helemaal! Hier is het juiste antwoord:';
        }

        if (correctAnswerDisplay) {
            correctAnswerDisplay.textContent = 'Het juiste antwoord is: ' + currentItem.target.answer;
        }

        // Show extra info if available
        if (currentItem.extra_info && extraInfoSection) {
            let hasAnyInfo = false;

            // Show rule
            if (currentItem.extra_info.rule && ruleSection && ruleContent) {
                ruleSection.style.display = 'block';
                ruleContent.textContent = currentItem.extra_info.rule;
                hasAnyInfo = true;
            } else if (ruleSection) {
                ruleSection.style.display = 'none';
            }

            // Show tip
            if (currentItem.extra_info.tip && tipSection && tipContent) {
                tipSection.style.display = 'block';
                tipContent.textContent = currentItem.extra_info.tip;
                hasAnyInfo = true;
            } else if (tipSection) {
                tipSection.style.display = 'none';
            }

            // Show examples
            if (currentItem.extra_info.examples && currentItem.extra_info.examples.length > 0
                && examplesSection && examplesContent) {
                examplesSection.style.display = 'block';
                const examplesHTML = currentItem.extra_info.examples
                    .map(ex => `<div style="margin: 4px 0;">• ${ex}</div>`)
                    .join('');
                examplesContent.innerHTML = examplesHTML;
                hasAnyInfo = true;
            } else if (examplesSection) {
                examplesSection.style.display = 'none';
            }

            // Show the extra info section if we have at least one piece of info
            extraInfoSection.style.display = hasAnyInfo ? 'block' : 'none';
        } else if (extraInfoSection) {
            extraInfoSection.style.display = 'none';
        }

        // Show feedback section and next button
        if (feedbackSection) {
            feedbackSection.classList.remove('hidden');
        }

        if (nextButton) {
            nextButton.classList.remove('hidden');
        }
    }

    /**
     * Move to next question
     */
    nextQuestion() {
        const hasMore = this.nextItem();
        if (hasMore) {
            this.showQuestion(this.state.currentIndex);
        } else {
            this.showResults();
        }
    }

    /**
     * Pause quiz
     */
    pauseQuiz() {
        if (confirm('Wil je de quiz pauzeren?')) {
            window.location.href = 'index.html';
        }
    }

    /**
     * Stop quiz - go directly to results
     */
    stopQuiz() {
        this.showResults();
    }

    /**
     * Show results at the end
     */
    showResults() {
        const { quizContainer, resultsPage } = this.elements;

        // Hide quiz, show results
        if (quizContainer) {
            quizContainer.style.display = 'none';
        }

        if (resultsPage) {
            resultsPage.style.display = 'block';
        }

        // Scroll to top
        window.scrollTo(0, 0);

        const totalQuestions = this.state.totalQuestions;
        const correctCount = this.state.score;
        const incorrectCount = this.state.wrongAnswers.length;
        const percentage = totalQuestions > 0 ?
            Math.round((correctCount / totalQuestions) * 100) : 0;

        // Populate results sections
        this.populateHeroBlock(percentage, correctCount, incorrectCount);
        this.populateSkillsOverview();
        this.populateQuestionAccordion();
    }

    /**
     * Populate Hero Block
     * @private
     */
    populateHeroBlock(percentage, correctCount, incorrectCount) {
        const emojiEl = document.getElementById('resultEmoji');
        const headlineEl = document.getElementById('resultHeadline');
        const summaryEl = document.getElementById('resultSummary');
        const growthBadgeEl = document.getElementById('resultGrowthBadge');
        const growthTextEl = document.getElementById('growthText');

        // Select emoji and headline based on performance
        let emoji, headline;
        if (percentage >= 90) {
            emoji = '🎉';
            headline = 'Wauw! Geweldig gedaan!';
        } else if (percentage >= 70) {
            emoji = '🌟';
            headline = 'Knap gewerkt!';
        } else if (percentage >= 50) {
            emoji = '💪';
            headline = 'Goed bezig!';
        } else {
            emoji = '🚀';
            headline = 'Elke vraag maakt je sterker!';
        }

        if (emojiEl) emojiEl.textContent = emoji;
        if (headlineEl) headlineEl.textContent = headline;

        // Summary text
        let summaryText = '';
        if (correctCount === 1) {
            summaryText = 'Je hebt 1 vraag goed beantwoord!';
        } else if (correctCount > 1) {
            summaryText = `Je hebt ${correctCount} vragen goed beantwoord!`;
        } else {
            summaryText = 'Elke vraag is een leerkans!';
        }

        if (incorrectCount > 0) {
            if (incorrectCount === 1) {
                summaryText += ' En 1 vraag maakt je weer een beetje sterker!';
            } else {
                summaryText += ` En ${incorrectCount} vragen maken je weer een beetje sterker!`;
            }
        }

        if (summaryEl) summaryEl.textContent = summaryText;

        // Growth badge
        if (growthBadgeEl) {
            if (incorrectCount > 0) {
                growthBadgeEl.style.display = 'flex';
                const leerpunten = incorrectCount === 1 ? '1 leerpunt' : `${incorrectCount} leerpunten`;
                if (growthTextEl) {
                    growthTextEl.textContent = `Je hebt ${leerpunten} verdiend!`;
                }
            } else {
                growthBadgeEl.style.display = 'none';
            }
        }
    }

    /**
     * Populate Skills Overview
     * @private
     */
    populateSkillsOverview() {
        const skillsChipsEl = document.getElementById('skillsChips');
        const skillsOverviewEl = document.getElementById('skillsOverview');

        if (!skillsChipsEl || !skillsOverviewEl) return;

        const tags = Object.keys(this.tagStats);
        if (tags.length === 0) {
            skillsOverviewEl.style.display = 'none';
            return;
        }

        skillsOverviewEl.style.display = 'block';
        skillsChipsEl.innerHTML = '';

        // Create chips for each tag
        tags.forEach(tag => {
            const stats = this.tagStats[tag];
            const percentage = Math.round((stats.correct / stats.total) * 100);

            const chip = document.createElement('div');
            chip.className = 'skill-chip';

            // Determine status
            let status = '';
            if (percentage >= 80) {
                status = '<span class="status-icon">✅</span>';
            } else {
                status = '<span class="status-icon grow">💡</span><span class="grow-text">Hier kun je nog sterker in worden</span>';
            }

            // Format tag name
            const tagName = this.formatTagName(tag);

            chip.innerHTML = `
                <div class="skill-info">
                    <div class="skill-name">📚 ${tagName}</div>
                    ${status}
                </div>
            `;

            skillsChipsEl.appendChild(chip);
        });
    }

    /**
     * Format tag name for display
     * @private
     */
    formatTagName(tag) {
        const tagNames = {
            'werkwoord_vt': 'Verleden tijd',
            'werkwoord_ttt': 'Tegenwoordige tijd',
            'voltooid_deelwoord': 'Voltooid deelwoord',
            'verlengingsregel': 'Verlengingsregel',
            'open_lettergreep': 'Open lettergreep',
            'gesloten_lettergreep': 'Gesloten lettergreep',
            'tweetekenklank_ui': 'Tweeklank ui',
            'tweetekenklank_ou': 'Tweeklank ou',
            'lange_klank_aa': 'Lange klank aa',
            'cluster_ng': 'Lettercluster ng',
            'cluster_nk': 'Lettercluster nk',
            'cluster_sch': 'Lettercluster sch',
            'cluster_ch': 'Lettercluster ch',
            'ei_ij': 'ei of ij',
            'au_ou': 'au of ou'
        };

        return tagNames[tag] || tag;
    }

    /**
     * Populate Question Accordion
     * @private
     */
    populateQuestionAccordion() {
        const accordionEl = document.getElementById('questionAccordion');
        const questionReviewSectionEl = document.getElementById('questionReviewSection');

        if (!accordionEl || !questionReviewSectionEl) return;

        if (this.state.wrongAnswers.length === 0) {
            questionReviewSectionEl.style.display = 'none';
            return;
        }

        questionReviewSectionEl.style.display = 'block';
        accordionEl.innerHTML = '';

        this.state.wrongAnswers.forEach((wrong) => {
            const item = wrong.item;
            const questionNumber = wrong.index + 1;

            const accordionItem = document.createElement('div');
            accordionItem.className = 'accordion-item';

            const header = document.createElement('div');
            header.className = 'accordion-header';
            header.innerHTML = `
                <div class="accordion-label">
                    <span class="grow-icon">💡</span>
                    <span>Hier kun je nog groeien</span>
                </div>
                <div class="accordion-question">Vraag ${questionNumber}</div>
                <i class="material-icons accordion-icon">expand_more</i>
            `;

            const content = document.createElement('div');
            content.className = 'accordion-content';
            content.style.display = 'none';

            // Build extra info HTML
            let extraInfoHTML = '';
            if (item.extra_info) {
                if (item.extra_info.rule) {
                    extraInfoHTML += `
                        <div class="feedback-section-wrapper">
                            <div class="feedback-section-title">📖 Spellingregel</div>
                            <div class="feedback-section-content">${item.extra_info.rule}</div>
                        </div>
                    `;
                }
                if (item.extra_info.tip) {
                    extraInfoHTML += `
                        <div class="feedback-tip">
                            <div class="feedback-tip-title">
                                <span>💡</span>
                                <span>Tip</span>
                            </div>
                            <div class="feedback-tip-content">${item.extra_info.tip}</div>
                        </div>
                    `;
                }
                if (item.extra_info.examples && item.extra_info.examples.length > 0) {
                    const examplesHTML = item.extra_info.examples
                        .map(ex => `<div style="margin: 4px 0;">• ${ex}</div>`)
                        .join('');
                    extraInfoHTML += `
                        <div class="feedback-section-wrapper">
                            <div class="feedback-section-title">✨ Voorbeelden</div>
                            <div class="feedback-section-content">${examplesHTML}</div>
                        </div>
                    `;
                }
            }

            content.innerHTML = `
                <div class="accordion-answer incorrect">
                    <strong>Jouw antwoord:</strong> ${wrong.userAnswer || '(geen antwoord)'}
                </div>
                <div class="accordion-answer correct">
                    <strong>Juiste antwoord:</strong> ${item.target.answer}
                </div>
                ${extraInfoHTML}
            `;

            // Toggle accordion
            header.addEventListener('click', () => {
                const isOpen = content.style.display === 'block';
                content.style.display = isOpen ? 'none' : 'block';
                header.querySelector('.accordion-icon').textContent = isOpen ? 'expand_more' : 'expand_less';
            });

            accordionItem.appendChild(header);
            accordionItem.appendChild(content);
            accordionEl.appendChild(accordionItem);
        });
    }

    /**
     * Restart quiz
     */
    restartQuiz() {
        // Clear localStorage
        storage.remove('autoStartSubject');
        storage.remove('selectedGroep');
        storage.remove('selectedMoment');
        storage.flush();

        // Reload page
        window.location.reload();
    }

    /**
     * Go to landing page
     */
    goToLanding() {
        // Clear localStorage
        storage.remove('autoStartSubject');
        storage.remove('selectedGroep');
        storage.remove('selectedMoment');
        storage.flush();

        // Go to index
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
}

// Initialize quiz on page load
document.addEventListener('DOMContentLoaded', async function() {
    try {
        const quiz = new SpellingDictee();
        await quiz.init();

        // Expose globally for debugging and external calls
        window.spellingDictee = quiz;

        // Make functions available globally for HTML onclick handlers
        window.checkAnswer = () => quiz.checkAnswer();
        window.nextQuestion = () => quiz.nextQuestion();
        window.playAudio = () => quiz.playAudio();
        window.pauseQuiz = () => quiz.pauseQuiz();
        window.stopQuiz = () => quiz.stopQuiz();
        window.restartQuiz = () => quiz.restartQuiz();
        window.goToLanding = () => quiz.goToLanding();
    } catch (error) {
        console.error('Failed to initialize spelling dictee:', error);
        alert('Kon de quiz niet laden. Probeer het opnieuw.');
        window.location.href = 'index.html';
    }
});
