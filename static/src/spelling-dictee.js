// Spelling Dictee Quiz Logic
let quizData = null;
let currentQuestionIndex = 0;
let score = 0;
let currentItem = null;
let hasAnswered = false;
let isPlayingAudio = false;
let wrongAnswers = []; // Track incorrect answers for results page
let tagStats = {}; // Track stats by tag for results page

// Initialize quiz on page load
document.addEventListener('DOMContentLoaded', function() {
    loadQuizData();

    // Add Enter key support
    const input = document.getElementById('spellingInput');
    if (input) {
        input.addEventListener('keypress', function(event) {
            if (event.key === 'Enter' && !hasAnswered) {
                checkAnswer();
            }
        });
    }
});

// Load quiz data from config
async function loadQuizData() {
    try {
        // Get groep and moment from localStorage (set by level-selector)
        const selectedGroep = localStorage.getItem('selectedGroep') || 'groep4';
        const selectedMoment = localStorage.getItem('selectedMoment') || 'm4';

        // Update breadcrumb
        const groepNumber = selectedGroep.replace('groep', '');
        const momentLetter = selectedMoment.charAt(0).toUpperCase();
        document.getElementById('breadcrumbLevel').textContent =
            `Groep ${groepNumber} (${momentLetter}${groepNumber})`;

        // Get file path from config
        const filePath = CONFIG.subjectFilePaths?.werkwoordspelling?.[selectedGroep]?.[selectedMoment];

        if (!filePath) {
            throw new Error(`Geen data beschikbaar voor ${selectedGroep} ${selectedMoment}`);
        }

        // Load JSON data
        const response = await fetch(filePath);

        if (!response.ok) {
            throw new Error(`Could not load ${filePath}`);
        }

        quizData = await response.json();

        // Validate data structure
        if (!quizData.set || !quizData.items || quizData.items.length === 0) {
            throw new Error('Ongeldige data structuur');
        }

        console.log('Quiz data geladen:', quizData);

        // Start the quiz
        showQuestion(0);

    } catch (error) {
        console.error('Error loading quiz data:', error);
        alert('Kon de spelling data niet laden. ' + error.message);
        window.location.href = 'index.html';
    }
}

// Show a question
function showQuestion(index) {
    if (index >= quizData.items.length) {
        showResults();
        return;
    }

    currentQuestionIndex = index;
    currentItem = quizData.items[index];
    hasAnswered = false;
    isPlayingAudio = false;

    // Update progress
    updateProgress();

    // Reset UI
    resetUI();

    // Update verb tense instruction
    updateVerbTenseInstruction();

    // Focus input
    document.getElementById('spellingInput').focus();
}

// Update progress bar and label
function updateProgress() {
    const progressLabel = document.getElementById('progressLabel');
    const progressBarFill = document.getElementById('progressBarFill');

    const total = quizData.items.length;
    const current = currentQuestionIndex + 1;
    const percentage = (current / total) * 100;

    progressLabel.textContent = `Vraag ${current} van ${total}`;
    progressBarFill.style.width = `${percentage}%`;
}

// Update score display
function updateScore() {
    document.getElementById('totalCorrect').textContent = score;
}

// Update verb tense instruction based on tags
function updateVerbTenseInstruction() {
    const verbTenseSpan = document.getElementById('verbTenseInstruction');

    if (!currentItem || !currentItem.tags || currentItem.tags.length === 0) {
        verbTenseSpan.textContent = '';
        return;
    }

    // Check for specific verb tense tags
    if (currentItem.tags.includes('werkwoord_vt')) {
        verbTenseSpan.textContent = ' in verleden tijd';
    } else if (currentItem.tags.includes('werkwoord_ttt')) {
        verbTenseSpan.textContent = ' in tegenwoordige tijd';
    } else if (currentItem.tags.includes('voltooid_deelwoord')) {
        verbTenseSpan.textContent = ' voltooid deelwoord';
    } else {
        verbTenseSpan.textContent = '';
    }
}

// Reset UI for new question
function resetUI() {
    const input = document.getElementById('spellingInput');
    input.value = '';
    input.className = 'spelling-input';
    input.disabled = false;

    const checkButton = document.getElementById('checkButton');
    checkButton.disabled = false;
    checkButton.classList.remove('hidden');

    const feedbackSection = document.getElementById('feedbackSection');
    feedbackSection.classList.add('hidden');

    const nextButton = document.getElementById('nextButton');
    nextButton.classList.add('hidden');

    const playButton = document.getElementById('audioPlayButton');
    playButton.classList.remove('playing');
    playButton.disabled = false;

    const playIcon = document.getElementById('playIcon');
    playIcon.textContent = 'volume_up';
}

// Play audio (sentence then instruction)
async function playAudio() {
    if (isPlayingAudio) return;

    isPlayingAudio = true;
    const playButton = document.getElementById('audioPlayButton');
    const playIcon = document.getElementById('playIcon');

    playButton.disabled = true;
    playButton.classList.add('playing');
    playIcon.textContent = 'volume_up';

    try {
        // Play sentence audio
        const sentenceSuccess = await playAudioFile(currentItem.audio.sentence, currentItem.prompt.sentence);

        // Small pause between sentence and instruction
        await sleep(300);

        // Play instruction audio
        const instructionText = currentItem.prompt.instruction.replace('{answer}', currentItem.target.answer);
        await playAudioFile(currentItem.audio.instruction, instructionText);

    } catch (error) {
        console.error('Error playing audio:', error);
    } finally {
        isPlayingAudio = false;
        playButton.disabled = false;
        playButton.classList.remove('playing');
    }
}

// Play a single audio file with TTS fallback
function playAudioFile(audioPath, fallbackText) {
    return new Promise((resolve, reject) => {
        // Try to play MP3 file
        const audio = new Audio();
        audio.src = 'exercises/sp/' + audioPath;

        let audioPlayed = false;

        audio.oncanplaythrough = function() {
            audioPlayed = true;
        };

        audio.onended = function() {
            resolve(true);
        };

        audio.onerror = function() {
            // Fallback to Web Speech API
            console.log('Audio file failed, using TTS for:', fallbackText);
            playTextToSpeech(fallbackText).then(resolve).catch(reject);
        };

        // Attempt to play
        audio.play().catch(error => {
            // If play fails (e.g., autoplay restrictions), use TTS
            console.log('Audio play failed, using TTS for:', fallbackText);
            playTextToSpeech(fallbackText).then(resolve).catch(reject);
        });

        // Timeout fallback after 2 seconds if audio doesn't load
        setTimeout(() => {
            if (!audioPlayed) {
                audio.pause();
                audio.src = '';
                console.log('Audio timeout, using TTS for:', fallbackText);
                playTextToSpeech(fallbackText).then(resolve).catch(reject);
            }
        }, 2000);
    });
}

// Play text using Web Speech API
function playTextToSpeech(text) {
    return new Promise((resolve, reject) => {
        if (!('speechSynthesis' in window)) {
            console.error('Speech synthesis not supported');
            resolve(false);
            return;
        }

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'nl-NL';
        utterance.rate = 0.9; // Slightly slower for clarity

        utterance.onend = function() {
            resolve(true);
        };

        utterance.onerror = function(event) {
            console.error('Speech synthesis error:', event);
            resolve(false);
        };

        window.speechSynthesis.speak(utterance);
    });
}

// Helper function to sleep
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Check answer
function checkAnswer() {
    if (hasAnswered) return;

    const input = document.getElementById('spellingInput');
    const userAnswer = input.value;

    if (!userAnswer || userAnswer.trim() === '') {
        alert('Vul eerst een antwoord in!');
        return;
    }

    hasAnswered = true;

    // Normalize answer based on flags
    const flags = quizData.set.flags;
    const normalizedUserAnswer = normalizeAnswer(userAnswer, flags);

    // Get accepted answers
    const acceptedAnswers = currentItem.target.accept || [currentItem.target.answer];
    const normalizedAcceptedAnswers = acceptedAnswers.map(ans => normalizeAnswer(ans, flags));

    // Check if correct
    const isCorrect = normalizedAcceptedAnswers.includes(normalizedUserAnswer);

    if (isCorrect) {
        handleCorrectAnswer();
    } else {
        handleIncorrectAnswer();
    }
}

// Normalize answer based on flags
function normalizeAnswer(answer, flags) {
    let normalized = answer;

    if (flags.trim) {
        normalized = normalized.trim();
    }

    if (!flags.case_sensitive) {
        normalized = normalized.toLowerCase();
    }

    return normalized;
}

// Handle correct answer
function handleCorrectAnswer() {
    score++;
    updateScore();

    // Track tag stats
    if (currentItem.tags) {
        currentItem.tags.forEach(tag => {
            if (!tagStats[tag]) {
                tagStats[tag] = { correct: 0, total: 0 };
            }
            tagStats[tag].correct++;
            tagStats[tag].total++;
        });
    }

    const input = document.getElementById('spellingInput');
    input.classList.add('correct');
    input.disabled = true;

    document.getElementById('checkButton').classList.add('hidden');

    // Show feedback
    const feedbackSection = document.getElementById('feedbackSection');
    const feedbackIcon = document.getElementById('feedbackIcon');
    const feedbackTitle = document.getElementById('feedbackTitle');
    const correctAnswerDisplay = document.getElementById('correctAnswerDisplay');
    const nextButton = document.getElementById('nextButton');

    feedbackSection.className = 'feedback-card correct';
    feedbackIcon.textContent = '🎉';
    feedbackTitle.textContent = quizData.set.feedback_templates.correct || 'Goed gedaan!';
    correctAnswerDisplay.textContent = 'Het juiste antwoord is: ' + currentItem.target.answer;

    // Hide extra info for correct answers
    document.getElementById('extraInfoSection').style.display = 'none';

    // Show next button
    nextButton.classList.remove('hidden');
}

// Handle incorrect answer
function handleIncorrectAnswer() {
    // Track wrong answer
    wrongAnswers.push({
        index: currentQuestionIndex,
        item: currentItem,
        userAnswer: document.getElementById('spellingInput').value
    });

    // Track tag stats
    if (currentItem.tags) {
        currentItem.tags.forEach(tag => {
            if (!tagStats[tag]) {
                tagStats[tag] = { correct: 0, total: 0 };
            }
            tagStats[tag].total++;
        });
    }

    const input = document.getElementById('spellingInput');
    input.classList.add('incorrect');
    input.disabled = true;

    // Shake animation
    input.style.animation = 'shake 0.4s';
    setTimeout(() => {
        input.style.animation = '';
    }, 400);

    document.getElementById('checkButton').classList.add('hidden');

    // Show feedback
    const feedbackSection = document.getElementById('feedbackSection');
    const feedbackIcon = document.getElementById('feedbackIcon');
    const feedbackTitle = document.getElementById('feedbackTitle');
    const correctAnswerDisplay = document.getElementById('correctAnswerDisplay');
    const nextButton = document.getElementById('nextButton');

    feedbackSection.className = 'feedback-card incorrect';
    feedbackIcon.textContent = '💡';
    feedbackTitle.textContent = quizData.set.feedback_templates.incorrect ||
        'Nog niet helemaal! Hier is het juiste antwoord:';
    correctAnswerDisplay.textContent = 'Het juiste antwoord is: ' + currentItem.target.answer;

    // Show extra info if available
    const extraInfoSection = document.getElementById('extraInfoSection');
    const ruleSection = document.getElementById('ruleSection');
    const tipSection = document.getElementById('tipSection');
    const examplesSection = document.getElementById('examplesSection');

    if (currentItem.extra_info) {
        let hasAnyInfo = false;

        // Show rule
        if (currentItem.extra_info.rule) {
            ruleSection.style.display = 'block';
            document.getElementById('ruleContent').textContent = currentItem.extra_info.rule;
            hasAnyInfo = true;
        } else {
            ruleSection.style.display = 'none';
        }

        // Show tip
        if (currentItem.extra_info.tip) {
            tipSection.style.display = 'block';
            document.getElementById('tipContent').textContent = currentItem.extra_info.tip;
            hasAnyInfo = true;
        } else {
            tipSection.style.display = 'none';
        }

        // Show examples
        if (currentItem.extra_info.examples && currentItem.extra_info.examples.length > 0) {
            examplesSection.style.display = 'block';
            const examplesHTML = currentItem.extra_info.examples
                .map(ex => `<div style="margin: 4px 0;">• ${ex}</div>`)
                .join('');
            document.getElementById('examplesContent').innerHTML = examplesHTML;
            hasAnyInfo = true;
        } else {
            examplesSection.style.display = 'none';
        }

        // Show the extra info section if we have at least one piece of info
        if (hasAnyInfo) {
            extraInfoSection.style.display = 'block';
        } else {
            extraInfoSection.style.display = 'none';
        }
    } else {
        extraInfoSection.style.display = 'none';
    }

    // Show next button
    nextButton.classList.remove('hidden');
}

// Move to next question
function nextQuestion() {
    showQuestion(currentQuestionIndex + 1);
}

// Pause quiz
function pauseQuiz() {
    if (confirm('Wil je de quiz pauzeren?')) {
        // Could save state to localStorage here if needed
        window.location.href = 'index.html';
    }
}

// Stop quiz - go directly to results
function stopQuiz() {
    showResults();
}

// Show results at the end
function showResults() {
    // Hide quiz, show results
    document.getElementById('quizContainer').style.display = 'none';
    document.getElementById('resultsPage').style.display = 'block';

    // Scroll to top
    window.scrollTo(0, 0);

    const totalQuestions = quizData.items.length;
    const correctCount = score;
    const incorrectCount = wrongAnswers.length;
    const percentage = totalQuestions > 0 ? Math.round((correctCount / totalQuestions) * 100) : 0;

    // 1. Populate Hero Block
    populateHeroBlock(percentage, correctCount, incorrectCount);

    // 2. Populate Skills Overview
    populateSkillsOverview();

    // 3. Populate Question Accordion (incorrect answers only)
    populateQuestionAccordion();
}

// Helper: Populate Hero Block
function populateHeroBlock(percentage, correctCount, incorrectCount) {
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

    emojiEl.textContent = emoji;
    headlineEl.textContent = headline;

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

    summaryEl.textContent = summaryText;

    // Growth badge
    if (incorrectCount > 0) {
        growthBadgeEl.style.display = 'flex';
        const leerpunten = incorrectCount === 1 ? '1 leerpunt' : `${incorrectCount} leerpunten`;
        growthTextEl.textContent = `Je hebt ${leerpunten} verdiend!`;
    } else {
        growthBadgeEl.style.display = 'none';
    }
}

// Helper: Populate Skills Overview
function populateSkillsOverview() {
    const skillsChipsEl = document.getElementById('skillsChips');
    const skillsOverviewEl = document.getElementById('skillsOverview');

    const tags = Object.keys(tagStats);
    if (tags.length === 0) {
        skillsOverviewEl.style.display = 'none';
        return;
    }

    skillsOverviewEl.style.display = 'block';
    skillsChipsEl.innerHTML = '';

    // Create chips for each tag
    tags.forEach(tag => {
        const stats = tagStats[tag];
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
        const tagName = formatTagName(tag);

        chip.innerHTML = `
            <div class="skill-info">
                <div class="skill-name">📚 ${tagName}</div>
                ${status}
            </div>
        `;

        skillsChipsEl.appendChild(chip);
    });
}

// Helper: Format tag name for display
function formatTagName(tag) {
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

// Helper: Populate Question Accordion
function populateQuestionAccordion() {
    const accordionEl = document.getElementById('questionAccordion');
    const questionReviewSectionEl = document.getElementById('questionReviewSection');

    if (wrongAnswers.length === 0) {
        questionReviewSectionEl.style.display = 'none';
        return;
    }

    questionReviewSectionEl.style.display = 'block';
    accordionEl.innerHTML = '';

    wrongAnswers.forEach((wrong, index) => {
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

// Restart quiz
function restartQuiz() {
    // Clear localStorage
    localStorage.removeItem('autoStartSubject');
    localStorage.removeItem('selectedGroep');
    localStorage.removeItem('selectedMoment');

    // Reload page
    window.location.reload();
}

// Go to landing page
function goToLanding() {
    // Clear localStorage
    localStorage.removeItem('autoStartSubject');
    localStorage.removeItem('selectedGroep');
    localStorage.removeItem('selectedMoment');

    // Go to index
    window.location.href = 'index.html';
}
