/**
 * QUIZ APPLICATION - MAIN LOGIC
 *
 * This application supports multiple question formats and subjects:
 *
 * 1. ANSWER FORMATS:
 *    - Legacy format: currentQuestion.correct holds the answer index (integer)
 *    - New format: Each option has is_correct boolean field (used by verhaaltjessommen)
 *
 * 2. SUBJECTS:
 *    - verhaaltjessommen: Story problems with layered error analysis and L.O.V.A. framework
 *    - Other subjects: Traditional quiz with immediate feedback
 *
 * 3. VERHAALTJESSOMMEN FEATURES:
 *    - Error classification (conversiefout, leesfout_ruis, conceptfout, rekenfout_basis)
 *    - Layered feedback protocol (attempt 1: error analysis, attempt 2: visual aids, attempt 3: full solution)
 *    - Pre-feedback hints shown after first error
 *    - Retry mechanism (incorrect options are disabled, but user can try other options)
 *    - Success modal with L.O.V.A. 4-step breakdown for correct answers
 */

// Quiz data will be loaded from JSON files
let quizData = {};
const jsonPath = CONFIG.jsonPath;

// Quiz state
let currentQuiz = null;
let randomizedQuestions = []; // Array to hold randomized questions
let currentSubject = null;
let currentTheme = null; // Track current theme for highscore
let currentQuestionIndex = 0;
let score = 0;
let totalQuestions = 0;
let selectedAnswer = null;
let hasAnswered = false;
let wrongAnswers = []; // Track wrong answers for review
let currentQuestionErrors = 0; // Track errors for current question (for hint display)
let incorrectOptions = new Set(); // Track which options were already tried (to disable them)

// Progress tracker by category
let categoryProgress = {};
let lovaClickCount = 0; // Track L.O.V.A. button clicks

// Helper function to render verhoudingstabel widget
function renderVerhoudingstabel(containerElement, extraInfo) {
    // Clear the container first
    containerElement.innerHTML = '';

    // Check if verhoudingstabel data exists
    if (extraInfo && extraInfo.verhoudingstabel) {
        VerhoudingstabelWidget.render(containerElement, extraInfo.verhoudingstabel);
    }
}

// Highscore management
function getHighscoreKey(subject, theme) {
    return `${CONFIG.storageKeys.highscorePrefix}${subject}_${theme || 'all'}`;
}

function getHighscore(subject, theme) {
    const key = getHighscoreKey(subject, theme);
    const stored = localStorage.getItem(key);
    return stored ? parseInt(stored) : 0;
}

function saveHighscore(subject, theme, score) {
    const key = getHighscoreKey(subject, theme);
    const currentHighscore = getHighscore(subject, theme);
    if (score > currentHighscore) {
        localStorage.setItem(key, score.toString());
        return true; // New highscore achieved
    }
    return false; // No new highscore
}

// Get user name
function getUserName() {
    let name = localStorage.getItem(CONFIG.storageKeys.userName);
    if (!name) {
        name = prompt(CONFIG.defaults.userPrompt) || CONFIG.defaults.userName;
        localStorage.setItem(CONFIG.storageKeys.userName, name);
    }
    return name;
}

// Initialize category progress tracker
function initializeCategoryProgress(questions) {
    categoryProgress = {};

    // Extract all unique categories from the questions
    const categories = [...new Set(questions.map(q => q.theme).filter(theme => theme))];

    // Initialize counters for each category
    categories.forEach(category => {
        categoryProgress[category] = {
            correct: 0,
            incorrect: 0,
            lovaClicks: 0
        };
    });

    // Update the display
    updateProgressTrackerDisplay();
}

// Update category progress after answering
function updateCategoryProgress(theme, isCorrect) {
    if (!theme || !categoryProgress[theme]) return;

    if (isCorrect) {
        categoryProgress[theme].correct++;
    } else {
        categoryProgress[theme].incorrect++;
    }

    // Update the display
    updateProgressTrackerDisplay();
}

// Display the progress tracker
function updateProgressTrackerDisplay() {
    // Calculate totals
    let totalCorrect = 0;
    let totalIncorrect = 0;

    // Sort categories alphabetically for consistent display
    const sortedCategories = Object.keys(categoryProgress).sort();

    sortedCategories.forEach(category => {
        const stats = categoryProgress[category];
        totalCorrect += stats.correct;
        totalIncorrect += stats.incorrect;
    });

    // Update summary totals only (compact display)
    const totalCorrectEl = document.getElementById('totalCorrect');
    if (totalCorrectEl) {
        totalCorrectEl.textContent = totalCorrect;
    }

    // totalIncorrect display removed for anxiety reduction - only show positive count
    const lovaClicksEl = document.getElementById('lovaClicks');
    if (lovaClicksEl) {
        lovaClicksEl.textContent = lovaClickCount;
    }
}

// Shuffle array function (Fisher-Yates algorithm)
function shuffleArray(array) {
    const shuffled = [...array]; // Create a copy to avoid modifying original
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// Create flattened and randomized question list
function createRandomizedQuestions(data) {
    const flatQuestions = [];

    data.forEach(item => {
        if (item.questions && Array.isArray(item.questions)) {
            // For items with multiple sub-questions
            item.questions.forEach(question => {
                flatQuestions.push({
                    content: item.content,
                    visual: item.visual, // Visual data (tables, etc.)
                    question: question.question,
                    options: question.options, // Options array; each option can be string (old) or object with is_correct (new)
                    correct: question.correct, // Legacy field for old format (index-based); new format uses is_correct in options
                    originalId: item.id,
                    theme: item.theme,
                    title: item.title,
                    strategy: question.strategy,
                    tips: question.tips,
                    possible_answer: question.possible_answer, // For open-ended questions
                    extra_info: question.extra_info, // Additional learning content (concept, berekening, etc.)
                    lova: question.lova, // L.O.V.A. 4-step framework data
                    hint: question.hint // Pre-feedback hint shown after first error
                });
            });
        } else if (item.question) {
            // For items with single question (like samenvatten)
            flatQuestions.push({
                content: item.content,
                visual: item.visual, // Visual data (tables, etc.)
                question: item.question,
                options: item.options, // Options array; each option can be string (old) or object with is_correct (new)
                correct: item.correct, // Legacy field for old format (index-based); new format uses is_correct in options
                originalId: item.id,
                theme: item.theme,
                title: item.title,
                strategy: item.strategy,
                tips: item.tips,
                possible_answer: item.possible_answer, // For open-ended questions
                extra_info: item.extra_info, // Additional learning content (concept, berekening, etc.)
                lova: item.lova, // L.O.V.A. 4-step framework data
                hint: item.hint // Pre-feedback hint shown after first error
            });
        }
    });

    return shuffleArray(flatQuestions);
}

// Load JSON file
async function loadJsonFile(filename) {
    try {
        // Add cache-busting parameter to prevent browser from using cached version
        const cacheBuster = new Date().getTime();
        const response = await fetch(jsonPath + filename + '?v=' + cacheBuster);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error loading JSON file:', error);
        alert('Fout bij het laden van het bestand. Controleer of de bestanden beschikbaar zijn.');
        return null;
    }
}

// Show level selection page for subjects with multiple levels
function showLevelSelection(type) {
    document.getElementById('landingPage').style.display = 'none';
    document.getElementById('levelPage').style.display = 'block';

    // Map subject type to display title
    const titleMap = {
        'verhaaltjessommen': 'Verhaaltjessommen',
        'basisvaardigheden': 'Basisvaardigheden',
        'woordenschat': 'Woordenschat',
        'wereldorientatie': 'Wereldoriëntatie'
    };
    const levelTitle = titleMap[type] || type;
    document.getElementById('levelTitle').textContent = levelTitle + ' - Kies je groep';

    const levelGrid = document.getElementById('levelGrid');
    levelGrid.innerHTML = '';

    // Define levels with their corresponding subject names (ordered from youngest to oldest)
    const levels = [
        {
            icon: 'eco',
            title: 'Groep 4 - M4 niveau',
            description: 'M4 niveau oefeningen',
            subject: type + '-emma'
        },
        {
            icon: 'auto_stories',
            title: 'Groep 5 - M5 niveau',
            description: 'M5 niveau oefeningen',
            subject: type + '-kate'
        },
        {
            icon: 'workspace_premium',
            title: 'Groep 8 - Eindtoets niveau',
            description: 'E8 niveau oefeningen',
            subject: type // verhaaltjessommen or basisvaardigheden
        }
    ];

    // Create cards for each level
    levels.forEach(level => {
        const card = document.createElement('div');
        card.className = 'subject-card';
        card.onclick = () => loadSubject(level.subject);

        card.innerHTML = `
            <div class="subject-icon-wrapper">
                <i class="material-icons subject-icon-material">${level.icon}</i>
            </div>
            <div style="flex: 1;">
                <h3>${level.title}</h3>
                <p>${level.description}</p>
            </div>
        `;

        levelGrid.appendChild(card);
    });
}

// Load subject and show themes
async function loadSubject(subject) {
    const filename = subject + CONFIG.templateFileSuffix;
    const data = await loadJsonFile(filename);

    if (!data) return;

    quizData[subject] = data; // Store the full data for the subject
    currentSubject = subject;

    // Extract themes. Ensure 'theme' property exists for all items if you expect them to be categorized.
    const themes = [...new Set(data.map(item => item.theme).filter(theme => theme))];
    console.log("Loaded themes for subject:", subject, themes);

    // Transition to theme selection page
    showThemeSelection(subject, themes, data);
}

// Show theme selection page
function showThemeSelection(subject, themes, data) {
    document.getElementById('landingPage').style.display = 'none';
    document.getElementById('levelPage').style.display = 'none';
    document.getElementById('themePage').style.display = 'block';

    document.getElementById('subjectTitle').textContent = CONFIG.subjectTitles[subject] + ' - Kies een thema';

    const themeGrid = document.getElementById('themeGrid');
    themeGrid.innerHTML = '';
    themeGrid.classList.remove('theme-grid'); // Remove compact grid for categorized layout

    const userName = getUserName();

    // Calculate total questions for "all themes"
    let totalAllQuestions = 0;
    data.forEach(item => {
        if (Array.isArray(item.questions)) {
            totalAllQuestions += item.questions.length;
        } else if (item.question) {
            totalAllQuestions += 1;
        }
    });

    // PROMINENT "Alle thema's" card
    const allThemeCard = document.createElement('div');
    allThemeCard.className = 'theme-card-prominent';
    allThemeCard.onclick = () => startQuizWithTheme(subject, null);
    const allHighscore = getHighscore(subject, null);
    allThemeCard.innerHTML = `
        <div class="prominent-icon">
            <i class="material-icons">quiz</i>
        </div>
        <div class="prominent-content">
            <h3>Alle thema's</h3>
            <p class="prominent-description">Start met een mix van alle onderwerpen!</p>
            <p class="prominent-meta">${totalAllQuestions} vragen beschikbaar</p>
            ${allHighscore > 0 ? `
                <div class="theme-highscore">
                    <i class="material-icons">emoji_events</i>
                    <span>Highscore: ${allHighscore}</span>
                </div>
            ` : ''}
        </div>
    `;
    themeGrid.appendChild(allThemeCard);

    // Categorize themes
    const themeCategories = categorizeThemes(themes);

    // Add categorized themes
    Object.entries(themeCategories).forEach(([category, categoryThemes]) => {
        if (categoryThemes.length === 0) return;

        // Add section header
        const sectionHeader = document.createElement('div');
        sectionHeader.className = 'theme-section-header';
        sectionHeader.innerHTML = `<h3>${category}</h3>`;
        themeGrid.appendChild(sectionHeader);

        // Add theme grid for this category
        const categoryGrid = document.createElement('div');
        categoryGrid.className = 'theme-category-grid';

        categoryThemes.forEach(theme => {
            const filteredItems = data.filter(item => item.theme === theme);
            let questionCount = 0;

            filteredItems.forEach(item => {
                if (Array.isArray(item.questions)) {
                    questionCount += item.questions.length;
                } else if (item.question) {
                    questionCount += 1;
                }
            });

            const themeCard = document.createElement('div');
            themeCard.className = 'subject-card theme-card-small';
            themeCard.onclick = () => startQuizWithTheme(subject, theme);
            const themeHighscore = getHighscore(subject, theme);
            themeCard.innerHTML = `
                <div class="subject-icon-wrapper">
                    <i class="material-icons subject-icon-material">topic</i>
                </div>
                <div style="flex: 1;">
                    <h3>${theme}</h3>
                    <p>${questionCount} vragen</p>
                    ${themeHighscore > 0 ? `
                        <div class="theme-highscore">
                            <i class="material-icons">emoji_events</i>
                            <span>Highscore: ${themeHighscore}</span>
                        </div>
                    ` : ''}
                </div>
            `;
            categoryGrid.appendChild(themeCard);
        });

        themeGrid.appendChild(categoryGrid);
    });
}

// Categorize themes into logical groups
function categorizeThemes(themes) {
    const categories = {
        '🔢 Rekenen': [],
        '📏 Meten & Verhoudingen': []
    };

    const rekenCategories = ['optellen', 'aftrekken', 'vermenigvuldigen', 'delen'];
    const metenCategories = ['tijd', 'geld', 'gewicht', 'verhoudingen', 'inhoud', 'meetkunde', 'oppervlakte', 'omtrek'];

    themes.forEach(theme => {
        const themeLower = theme.toLowerCase();
        if (rekenCategories.includes(themeLower)) {
            categories['🔢 Rekenen'].push(theme);
        } else if (metenCategories.includes(themeLower)) {
            categories['📏 Meten & Verhoudingen'].push(theme);
        } else {
            // Default to Rekenen if not categorized
            categories['🔢 Rekenen'].push(theme);
        }
    });

    return categories;
}

// Start quiz with specific theme
function startQuizWithTheme(subject, theme) {
    // Store current theme for highscore tracking
    currentTheme = theme;

    // currentQuiz should be set from the globally available quizData[subject]
    let dataToUse = quizData[subject];

    if (theme) {
        // Filter data by theme
        currentQuiz = dataToUse.filter(item => item.theme === theme);
    } else {
        // Use all data for the subject if no theme is selected
        currentQuiz = dataToUse;
    }

    startQuizWithData(subject); // Proceed to start the quiz with the filtered/full data
}

function startQuizWithData(subject) {
    currentQuestionIndex = 0;
    score = 0;
    hasAnswered = false;
    wrongAnswers = []; // Reset wrong answers for new quiz
    lovaClickCount = 0; // Reset L.O.V.A. click counter
    resetMilestones(); // Reset visual progress milestones

    // Create randomized questions from the current quiz data
    randomizedQuestions = createRandomizedQuestions(currentQuiz);
    totalQuestions = randomizedQuestions.length;

    // Initialize category progress tracker (reset to 0)
    initializeCategoryProgress(randomizedQuestions);

    document.getElementById('landingPage').style.display = 'none';
    document.getElementById('themePage').style.display = 'none';
    document.getElementById('quizPage').style.display = 'block';
    document.getElementById('resultsPage').style.display = 'none';

    // Set quiz title
    document.getElementById('quizTitle').textContent = CONFIG.subjectTitles[subject] || 'Quiz';

    // Update breadcrumb navigation
    updateBreadcrumb(subject);

    // L.O.V.A. help button will be shown/hidden automatically per question based on lova data

    loadCurrentQuestion();
}

// Update breadcrumb navigation with current subject and level
function updateBreadcrumb(subject) {
    const breadcrumbSubject = document.getElementById('breadcrumbSubject');
    const breadcrumbLevel = document.getElementById('breadcrumbLevel');
    const breadcrumbLevelSep = document.getElementById('breadcrumbLevelSep');

    // Determine base subject and level
    let baseSubject = subject;
    let level = null;

    // Check if subject has level variant (emma = groep 4, kate = groep 5)
    if (subject.endsWith('-emma')) {
        baseSubject = subject.replace('-emma', '');
        level = 'Groep 4';
    } else if (subject.endsWith('-kate')) {
        baseSubject = subject.replace('-kate', '');
        level = 'Groep 5';
    } else if (['verhaaltjessommen', 'basisvaardigheden', 'wereldorientatie', 'woordenschat'].includes(subject)) {
        level = 'Groep 8';
    }

    // Set subject name
    breadcrumbSubject.textContent = CONFIG.subjectTitles[baseSubject] || CONFIG.subjectTitles[subject] || subject;

    // Show/hide level if applicable
    if (level) {
        breadcrumbLevel.textContent = level;
        breadcrumbLevel.style.display = 'inline';
        breadcrumbLevelSep.style.display = 'inline';
    } else {
        breadcrumbLevel.style.display = 'none';
        breadcrumbLevelSep.style.display = 'none';
    }
}

// Render visual data (tables) as HTML with mobile-responsive wrapper
function renderVisualData(visualData) {
    if (!visualData || visualData.type !== 'table') {
        return '';
    }

    // Wrap table in responsive container for mobile scrolling
    let html = '<div class="table-container">';
    html += '<table style="width: 100%; border-collapse: collapse; background-color: white;">';

    // Add headers
    html += '<thead><tr>';
    visualData.headers.forEach(header => {
        html += `<th style="border: 2px solid #4A7BA7; padding: 12px; background-color: #4A7BA7; color: white; font-weight: 500; text-align: left; white-space: nowrap;">${header}</th>`;
    });
    html += '</tr></thead>';

    // Add rows
    html += '<tbody>';
    visualData.rows.forEach((row, rowIndex) => {
        const bgColor = rowIndex % 2 === 0 ? '#f8f8f8' : '#ffffff';
        html += `<tr style="background-color: ${bgColor};">`;
        row.forEach(cell => {
            html += `<td style="border: 1px solid #e0e0e0; padding: 10px; color: #2C3E50; word-wrap: break-word;">${cell}</td>`;
        });
        html += '</tr>';
    });
    html += '</tbody></table>';
    html += '</div>'; // Close responsive container

    return html;
}

function loadCurrentQuestion() {
    if (currentQuestionIndex >= randomizedQuestions.length) {
        showResults();
        return;
    }

    const currentQuestion = randomizedQuestions[currentQuestionIndex];

    // Reset error tracking for new question
    currentQuestionErrors = 0;
    incorrectOptions.clear(); // Clear disabled options

    // Clear hint container for new question
    const hintContainer = document.getElementById('hintContainer');
    if (hintContainer) {
        hintContainer.innerHTML = '';
    }

    // Update progress
    const progress = (currentQuestionIndex / totalQuestions) * 100;
    document.getElementById('progressBar').style.width = progress + '%';
    document.getElementById('questionCounter').textContent = `Vraag ${currentQuestionIndex + 1} van ${totalQuestions}`;

    // Update visual star progress
    updateStarProgress(progress);

    // Check for milestone celebrations
    checkMilestone(progress);

    // Show reading content if available
    const readingContent = document.getElementById('readingContent');
    if (currentQuestion.content || currentQuestion.visual) {
        let contentHtml = '';

        // Add text content if available
        if (currentQuestion.content) {
            contentHtml += currentQuestion.content;
        }

        // Add visual table if available
        if (currentQuestion.visual) {
            contentHtml += renderVisualData(currentQuestion.visual);
        }

        readingContent.innerHTML = contentHtml;
        readingContent.classList.remove('hidden');
    } else {
        readingContent.classList.add('hidden');
    }

    // Load question
    document.getElementById('questionText').textContent = currentQuestion.question;

    // Check if question has L.O.V.A. data
    const hasLovaData = currentQuestion.lova && currentQuestion.lova.stap1_lezen;
    const lovaHelpButton = document.getElementById('lovaHelpButton');
    const lovaHelpPanel = document.getElementById('lovaHelpPanel');

    if (hasLovaData) {
        // Show L.O.V.A. help button and load data into panel
        lovaHelpButton.classList.remove('hidden');
        loadLovaHelpData(currentQuestion);

        // Reset panel to collapsed state for new question
        lovaHelpPanelExpanded = false;
        lovaHelpPanel.classList.remove('expanded');
        lovaHelpPanel.classList.add('hidden');
        document.getElementById('lovaToggleIcon').textContent = '▼';
    } else {
        // Hide L.O.V.A. help button
        lovaHelpButton.classList.add('hidden');
        lovaHelpPanel.classList.add('hidden');
    }

    // Handle different question types (always show regular quiz)
    const optionsContainer = document.getElementById('optionsContainer');
    const textareaAnswer = document.getElementById('textareaAnswer');
    const feedbackSection = document.getElementById('feedbackSection');

    // Hide feedback section and reset classes for new question
    feedbackSection.classList.add('hidden');
    feedbackSection.classList.remove('correct', 'incorrect');
    document.getElementById('correctAnswerDisplay').classList.add('hidden');
    document.getElementById('extraInfoDisplay').classList.add('hidden');
    document.getElementById('verhoudingstabelContainer').innerHTML = ''; // Clear verhoudingstabel
    document.getElementById('strategyAndTips').classList.add('hidden');

    if (currentQuestion.options) {
        // Multiple choice question
        optionsContainer.classList.remove('hidden');
        textareaAnswer.classList.add('hidden');

        optionsContainer.innerHTML = '';
        currentQuestion.options.forEach((option, index) => {
            const optionElement = document.createElement('div');
            optionElement.className = 'option';
            optionElement.textContent = typeof option === 'string' ? option : option.text;
            optionElement.onclick = () => selectOption(index);
            optionsContainer.appendChild(optionElement);
        });
    } else {
        // Open question
        optionsContainer.classList.add('hidden');
        textareaAnswer.classList.remove('hidden');
        textareaAnswer.value = '';
    }

    // Reset UI state
    selectedAnswer = null;
    hasAnswered = false;
    document.getElementById('submitBtn').classList.remove('hidden');
    document.getElementById('nextBtn').classList.add('hidden');
}

function selectOption(index) {
    if (hasAnswered) return;

    // Don't allow selecting an option that was already marked incorrect
    if (incorrectOptions.has(index)) {
        return; // Silently ignore clicks on disabled options
    }

    // Remove previous selection
    document.querySelectorAll('.option').forEach(opt => {
        opt.classList.remove('selected'); // Don't remove 'incorrect' class - keep disabled options marked
    });

    // Select new option
    document.querySelectorAll('.option')[index].classList.add('selected');
    selectedAnswer = index;
}

/**
 * Submit and validate the user's answer
 *
 * Answer Validation Logic:
 * - New format (verhaaltjessommen): Options have is_correct boolean field
 * - Old format (other subjects): currentQuestion.correct stores the index
 *
 * Verhaaltjessommen Flow:
 * - Correct answer → Show success modal with L.O.V.A. breakdown
 * - Incorrect answer → Show error analysis modal, allow retry (doesn't set hasAnswered)
 *
 * Other Subjects Flow:
 * - Correct answer → Traditional feedback
 * - Incorrect answer → Traditional feedback with correct answer revealed
 */
function submitAnswer() {
    if (hasAnswered) return;

    const currentQuestion = randomizedQuestions[currentQuestionIndex];
    const feedbackSection = document.getElementById('feedbackSection');
    const feedbackTitle = document.getElementById('feedbackTitle');
    const feedbackMessage = document.getElementById('feedbackMessage');
    const correctAnswerDisplay = document.getElementById('correctAnswerDisplay');
    const extraInfoDisplay = document.getElementById('extraInfoDisplay'); // NIEUW: extraInfoDisplay element
    const verhoudingstabelContainer = document.getElementById('verhoudingstabelContainer'); // Container for widget
    const strategyAndTips = document.getElementById('strategyAndTips');
    const strategyText = document.getElementById('strategyText');
    const tipsList = document.getElementById('tipsList');

    feedbackSection.classList.remove('hidden'); // Show feedback section

    if (currentQuestion.options) {
        // Multiple choice
        if (selectedAnswer === null) {
            alert(CONFIG.feedback.noAnswer.multipleChoice);
            feedbackSection.classList.add('hidden'); // Hide if no answer selected
            return;
        }

        const options = document.querySelectorAll('.option');

        // Find the correct answer index - supports both old and new format
        let correctIndex = currentQuestion.options.findIndex(opt => {
            // New format: object with is_correct field (verhaaltjessommen)
            if (typeof opt === 'object' && opt.hasOwnProperty('is_correct')) {
                return opt.is_correct === true;
            }
            return false;
        });

        // If no is_correct found, fall back to old format (other subjects)
        if (correctIndex === -1 && currentQuestion.correct !== null && currentQuestion.correct !== undefined) {
            correctIndex = currentQuestion.correct;
        }

        // Validate correctIndex - check if question data is incomplete
        if (correctIndex === -1 || correctIndex >= options.length) {
            // Check if this is an incomplete question (has object options but no is_correct field)
            const hasObjectOptions = currentQuestion.options.some(opt => typeof opt === 'object' && opt.text);
            const hasIsCorrectField = currentQuestion.options.some(opt => typeof opt === 'object' && 'is_correct' in opt);

            if (hasObjectOptions && !hasIsCorrectField) {
                console.error('Incomplete question data - missing is_correct field', {
                    questionId: currentQuestion.originalId,
                    title: currentQuestion.title,
                    question: currentQuestion.question
                });
                alert(`Deze vraag is nog niet compleet bijgewerkt in het systeem (ID: ${currentQuestion.originalId}).\n\nGa door naar de volgende vraag.`);
            } else {
                console.error('Error: Could not determine correct answer index', {
                    correctIndex,
                    optionsLength: options.length,
                    questionId: currentQuestion.originalId
                });
                alert('Er is een fout opgetreden bij het controleren van het antwoord. Probeer opnieuw of neem contact op met de beheerder.');
            }
            feedbackSection.classList.add('hidden');

            // Allow moving to next question
            hasAnswered = true;
            document.getElementById('submitBtn').classList.add('hidden');
            document.getElementById('nextBtn').classList.remove('hidden');
            return;
        }

        if (selectedAnswer === correctIndex) {
            options[selectedAnswer].classList.add('correct');
            score++;

            // Update category progress tracker
            updateCategoryProgress(currentQuestion.theme, true);

            // Check if this is a verhaaltjessom with new error analysis fields
            const selectedOption = currentQuestion.options[selectedAnswer];
            const isVerhaaltjessom = currentSubject === 'verhaaltjessommen' &&
                                     currentQuestion.lova &&
                                     currentQuestion.extra_info;

            if (isVerhaaltjessom) {
                // Remove from wrongAnswers if they eventually got it correct (after retry)
                const wrongAnswerIndex = wrongAnswers.findIndex(wa => wa.question.originalId === currentQuestion.originalId);
                if (wrongAnswerIndex !== -1) {
                    wrongAnswers.splice(wrongAnswerIndex, 1);
                }

                // Show success modaal for verhaaltjessommen
                feedbackSection.classList.add('hidden'); // Hide old feedback
                showSuccessModaal(currentQuestion, currentQuestion.extra_info);
            } else {
                // Old feedback for other subjects
                feedbackSection.classList.add('correct');
                feedbackTitle.textContent = CONFIG.feedback.correct.title;
                feedbackMessage.textContent = CONFIG.feedback.correct.message;
                correctAnswerDisplay.classList.add('hidden');
                extraInfoDisplay.classList.add('hidden'); // NIEUW: extraInfo verbergen bij correct
                verhoudingstabelContainer.innerHTML = ''; // Clear verhoudingstabel
                strategyAndTips.classList.add('hidden');
            }
        } else {
            // Increment error count for this question
            currentQuestionErrors++;

            // Update category progress tracker
            updateCategoryProgress(currentQuestion.theme, false);

            // Show error analysis if available for the selected wrong answer
            const selectedOption = currentQuestion.options[selectedAnswer];
            const errorAnalysis = (typeof selectedOption === 'object' && selectedOption.foutanalyse) ? selectedOption.foutanalyse : '';

            // Check if this is a verhaaltjessom with new error analysis fields
            const isVerhaaltjessom = currentSubject === 'verhaaltjessommen' &&
                                     selectedOption.error_type &&
                                     currentQuestion.extra_info;

            console.log('Incorrect answer check:', {
                currentSubject,
                hasErrorType: !!selectedOption.error_type,
                hasExtraInfo: !!currentQuestion.extra_info,
                isVerhaaltjessom
            });

            if (isVerhaaltjessom) {
                // For verhaaltjessommen: mark selected answer as incorrect but DON'T reveal correct answer
                // This allows the user to try again after seeing the error modal
                options[selectedAnswer].classList.add('incorrect');
                incorrectOptions.add(selectedAnswer); // Disable this option for future attempts

                // Track wrong answer for review (only add once per question)
                const alreadyTracked = wrongAnswers.some(wa => wa.question.originalId === currentQuestion.originalId);
                if (!alreadyTracked) {
                    const userAnswerText = typeof selectedOption === 'string' ? selectedOption : selectedOption.text;
                    const correctAnswerText = typeof currentQuestion.options[correctIndex] === 'string'
                        ? currentQuestion.options[correctIndex]
                        : currentQuestion.options[correctIndex].text;

                    wrongAnswers.push({
                        question: currentQuestion,
                        userAnswer: userAnswerText,
                        correctAnswer: correctAnswerText,
                        explanation: errorAnalysis || 'Zie foutanalyse voor uitleg',
                        questionType: 'verhaaltjessom'
                    });
                    console.log('✓ Tracked wrong answer. Total wrongAnswers:', wrongAnswers.length, wrongAnswers);
                } else {
                    console.log('Already tracked this question');
                }

                // Show foutanalyse modaal with attempt number
                feedbackSection.classList.add('hidden'); // Hide old feedback
                showFoutanalyseModaal(selectedOption, currentQuestion.extra_info, currentQuestionErrors, currentQuestion);

                // DON'T set hasAnswered to true here - allow retry
                // Return early to skip setting hasAnswered at the end
                return;
            } else {
                // For other subjects: mark incorrect and reveal correct answer immediately
                options[selectedAnswer].classList.add('incorrect');
                // Highlight correct answer if an incorrect one was selected
                if (options[correctIndex]) {
                    options[correctIndex].classList.add('correct');
                }
                // Old feedback for other subjects
                feedbackSection.classList.add('incorrect');
                feedbackTitle.textContent = CONFIG.feedback.incorrect.title;

                if (errorAnalysis) {
                    feedbackMessage.textContent = errorAnalysis;
                } else {
                    feedbackMessage.textContent = CONFIG.feedback.incorrect.messageDefault;
                }

                // Show correct answer - handle both string and object format
                const correctAnswerText = typeof currentQuestion.options[correctIndex] === 'string'
                    ? currentQuestion.options[correctIndex]
                    : currentQuestion.options[correctIndex].text;
                correctAnswerDisplay.textContent = `Het juiste antwoord was: "${correctAnswerText}"`;
                correctAnswerDisplay.classList.remove('hidden');
                strategyAndTips.classList.add('hidden'); // No strategy/tips for MC by default
            }

            // Track wrong answer for review
            const userAnswerText = typeof selectedOption === 'string'
                ? selectedOption
                : selectedOption.text;
            const correctAnswerText = typeof currentQuestion.options[correctIndex] === 'string'
                ? currentQuestion.options[correctIndex]
                : currentQuestion.options[correctIndex].text;
            wrongAnswers.push({
                question: currentQuestion,
                userAnswer: userAnswerText,
                correctAnswer: correctAnswerText,
                explanation: errorAnalysis || feedbackMessage.textContent,
                questionType: 'multiple-choice'
            });

            // NIEUW: Toon extra_info bij incorrect antwoord (meerkeuze)
            if (currentQuestion.extra_info) {
                // Render verhoudingstabel widget if available
                renderVerhoudingstabel(verhoudingstabelContainer, currentQuestion.extra_info);

                if (typeof currentQuestion.extra_info === 'string') {
                    // Simple string format (like brandaan)
                    extraInfoDisplay.innerHTML = `<h4>Achtergrondinfo:</h4><p>${currentQuestion.extra_info}</p>`;
                    extraInfoDisplay.classList.remove('hidden');
                } else if (currentQuestion.extra_info.concept || currentQuestion.extra_info.berekening) {
                    // New format with concept and berekening
                    let infoHtml = '';
                    if (currentQuestion.extra_info.concept) {
                        infoHtml += `<h4>Concept:</h4><p>${currentQuestion.extra_info.concept}</p>`;
                    }
                    if (currentQuestion.extra_info.berekening && currentQuestion.extra_info.berekening.length > 0) {
                        infoHtml += '<h4>Berekening:</h4><ul>';
                        currentQuestion.extra_info.berekening.forEach(step => {
                            infoHtml += `<li>${step}</li>`;
                        });
                        infoHtml += '</ul>';
                    }
                    extraInfoDisplay.innerHTML = infoHtml;
                    extraInfoDisplay.classList.remove('hidden');
                } else if (currentQuestion.extra_info.tips) {
                    // Old format with tips array (like begrijpendlezen)
                    let tipsHtml = '<h4>Extra Tips:</h4><ul>';
                    currentQuestion.extra_info.tips.forEach(tip => {
                        tipsHtml += `<li>${tip}</li>`;
                    });
                    tipsHtml += '</ul>';
                    extraInfoDisplay.innerHTML = tipsHtml;
                    extraInfoDisplay.classList.remove('hidden');
                } else {
                    extraInfoDisplay.classList.add('hidden');
                }
            } else {
                extraInfoDisplay.classList.add('hidden');
                verhoudingstabelContainer.innerHTML = ''; // Clear if no extra_info
            }
        }
    } else {
        // Open question (e.g., Samenvatten)
        const userAnswer = document.getElementById('textareaAnswer').value.trim();
        if (!userAnswer) {
            alert(CONFIG.feedback.noAnswer.openEnded);
            feedbackSection.classList.add('hidden'); // Hide if no answer entered
            return;
        }

        // Compare user answer with possible_answer from JSON (case-insensitive, trimmed)
        const possibleAnswer = currentQuestion.possible_answer ? currentQuestion.possible_answer.toLowerCase().trim() : '';
        const isCorrect = (userAnswer.toLowerCase() === possibleAnswer);

        if (isCorrect) {
            score++;
            feedbackSection.classList.add('correct');
            feedbackTitle.textContent = CONFIG.feedback.correct.title;
            feedbackMessage.textContent = CONFIG.feedback.correct.message;
            correctAnswerDisplay.classList.add('hidden');
            extraInfoDisplay.classList.add('hidden'); // NIEUW: extraInfo verbergen bij correct
            verhoudingstabelContainer.innerHTML = ''; // Clear verhoudingstabel
            strategyAndTips.classList.add('hidden');

            // Update category progress tracker
            updateCategoryProgress(currentQuestion.theme, true);
        } else {
            // Increment error count for this question
            currentQuestionErrors++;

            feedbackSection.classList.add('incorrect');
            feedbackTitle.textContent = CONFIG.feedback.incorrect.title;
            feedbackMessage.textContent = CONFIG.feedback.incorrect.messageWithTips;

            // Update category progress tracker
            updateCategoryProgress(currentQuestion.theme, false);

            // Show hint button after first mistake (if hint exists)
            if (currentQuestionErrors === 1 && currentQuestion.hint) {
                showHintButton(currentQuestion.hint);
            }

            correctAnswerDisplay.textContent = `Voorbeeld antwoord: "${currentQuestion.possible_answer}"`;
            correctAnswerDisplay.classList.remove('hidden');

            // Track wrong answer for review
            wrongAnswers.push({
                question: currentQuestion,
                userAnswer: userAnswer,
                correctAnswer: currentQuestion.possible_answer,
                explanation: feedbackMessage.textContent,
                questionType: 'open-ended'
            });

            // Display strategy and tips if available
            if (currentQuestion.strategy || (currentQuestion.tips && currentQuestion.tips.length > 0)) {
                strategyAndTips.classList.remove('hidden');
                strategyText.textContent = currentQuestion.strategy || 'Geen specifieke strategie beschikbaar.';
                tipsList.innerHTML = '';
                if (currentQuestion.tips && currentQuestion.tips.length > 0) {
                    currentQuestion.tips.forEach(tip => {
                        const li = document.createElement('li');
                        li.textContent = tip;
                        tipsList.appendChild(li);
                    });
                } else {
                    tipsList.innerHTML = '<li>Geen specifieke tips beschikbaar.</li>';
                }
            } else {
                strategyAndTips.classList.add('hidden');
            }

            // NIEUW: Toon extra_info bij incorrect antwoord (open vraag)
            if (currentQuestion.extra_info) {
                // Render verhoudingstabel widget if available
                renderVerhoudingstabel(verhoudingstabelContainer, currentQuestion.extra_info);

                extraInfoDisplay.textContent = `Achtergrondinfo: ${currentQuestion.extra_info}`;
                extraInfoDisplay.classList.remove('hidden');
            } else {
                extraInfoDisplay.classList.add('hidden');
                verhoudingstabelContainer.innerHTML = ''; // Clear if no extra_info
            }
        }
    }

    hasAnswered = true;
    document.getElementById('submitBtn').classList.add('hidden');
    document.getElementById('nextBtn').classList.remove('hidden');
}

function nextQuestion() {
    // Close modals if they are open
    closeSuccessModaal();
    closeFoutanalyseModaal();

    // Reset attempt tracking for new question
    if (typeof resetAttemptTracking === 'function') {
        resetAttemptTracking();
    }

    // Clear hint container
    const hintContainer = document.getElementById('hintContainer');
    if (hintContainer) {
        hintContainer.innerHTML = '';
    }

    currentQuestionIndex++;

    if (currentQuestionIndex >= randomizedQuestions.length) {
        showResults();
    } else {
        loadCurrentQuestion();
    }
}

function showResults() {
    document.getElementById('quizPage').style.display = 'none';
    document.getElementById('resultsPage').style.display = 'block';

    // Check for new highscore
    const isNewHighscore = saveHighscore(currentSubject, currentTheme, score);

    // Ensure totalQuestions is not zero to avoid division by zero
    const percentage = totalQuestions > 0 ? Math.round((score / totalQuestions) * 100) : 0;
    document.getElementById('finalScore').textContent = `${score}/${totalQuestions}`;

    let message = '';
    if (isNewHighscore) {
        message = CONFIG.scoreMessages.newHighscore;
    }

    if (percentage >= CONFIG.scoreThresholds.excellent) {
        message += CONFIG.scoreMessages.excellent;
    } else if (percentage >= CONFIG.scoreThresholds.good) {
        message += CONFIG.scoreMessages.good;
    } else if (percentage >= CONFIG.scoreThresholds.fair) {
        message += CONFIG.scoreMessages.fair;
    } else {
        message += CONFIG.scoreMessages.needsPractice;
    }

    document.getElementById('resultsMessage').textContent = message;
}

function goToLanding() {
    document.getElementById('landingPage').style.display = 'block';
    document.getElementById('levelPage').style.display = 'none';
    document.getElementById('themePage').style.display = 'none';
    document.getElementById('quizPage').style.display = 'none';
    document.getElementById('resultsPage').style.display = 'none';
    document.getElementById('reviewPage').style.display = 'none';
    // Reset quiz state when returning to landing page
    currentQuiz = null;
    randomizedQuestions = [];
    currentSubject = null;
    currentTheme = null;
    currentQuestionIndex = 0;
    score = 0;
    totalQuestions = 0;
    selectedAnswer = null;
    hasAnswered = false;
    wrongAnswers = [];
    lovaClickCount = 0; // Reset L.O.V.A. click counter
    // Reset L.O.V.A. panel state
    lovaHelpPanelExpanded = false;

    // Check for paused quiz and show resume banner
    checkForPausedQuiz();
}

// Pause quiz and save state
function pauseQuiz() {
    const quizState = {
        subject: currentSubject,
        theme: currentTheme,
        quiz: currentQuiz,
        randomizedQuestions: randomizedQuestions,
        currentQuestionIndex: currentQuestionIndex,
        score: score,
        totalQuestions: totalQuestions,
        wrongAnswers: wrongAnswers,
        categoryProgress: categoryProgress,
        lovaClickCount: lovaClickCount,
        timestamp: Date.now()
    };

    localStorage.setItem('pausedQuiz', JSON.stringify(quizState));
    alert('Quiz gepauzeerd! Je kunt later doorgaan waar je gebleven bent.');
    goToLanding();
}

// Check if there's a paused quiz
function checkForPausedQuiz() {
    const pausedQuizData = localStorage.getItem('pausedQuiz');
    const resumeBanner = document.getElementById('resumeBanner');
    const resumeDetails = document.getElementById('resumeDetails');

    if (pausedQuizData) {
        try {
            const quizState = JSON.parse(pausedQuizData);
            const subjectName = CONFIG.subjectTitles[quizState.subject] || quizState.subject;
            const progress = `${quizState.currentQuestionIndex} van ${quizState.totalQuestions} vragen`;

            resumeDetails.textContent = `${subjectName} - ${progress} beantwoord`;
            resumeBanner.style.display = 'flex';
        } catch (e) {
            console.error('Error parsing paused quiz:', e);
            localStorage.removeItem('pausedQuiz');
        }
    } else {
        resumeBanner.style.display = 'none';
    }
}

// Resume paused quiz
function resumePausedQuiz() {
    const pausedQuizData = localStorage.getItem('pausedQuiz');

    if (!pausedQuizData) {
        alert('Geen gepauzeerde quiz gevonden.');
        return;
    }

    try {
        const quizState = JSON.parse(pausedQuizData);

        // Restore quiz state
        currentSubject = quizState.subject;
        currentTheme = quizState.theme;
        currentQuiz = quizState.quiz;
        randomizedQuestions = quizState.randomizedQuestions;
        currentQuestionIndex = quizState.currentQuestionIndex;
        score = quizState.score;
        totalQuestions = quizState.totalQuestions;
        wrongAnswers = quizState.wrongAnswers;
        categoryProgress = quizState.categoryProgress;
        lovaClickCount = quizState.lovaClickCount || 0;
        hasAnswered = false;
        selectedAnswer = null;

        // Show quiz page
        document.getElementById('landingPage').style.display = 'none';
        document.getElementById('quizPage').style.display = 'block';

        // Set quiz title and breadcrumb
        document.getElementById('quizTitle').textContent = CONFIG.subjectTitles[currentSubject] || 'Quiz';
        updateBreadcrumb(currentSubject);

        // Load current question
        loadCurrentQuestion();

        // Clear paused state
        localStorage.removeItem('pausedQuiz');

    } catch (e) {
        console.error('Error resuming quiz:', e);
        alert('Fout bij het hervatten van de quiz. De opgeslagen data is mogelijk beschadigd.');
        localStorage.removeItem('pausedQuiz');
    }
}

// Clear paused quiz
function clearPausedQuiz() {
    if (confirm('Weet je zeker dat je de gepauzeerde quiz wilt verwijderen?')) {
        localStorage.removeItem('pausedQuiz');
        document.getElementById('resumeBanner').style.display = 'none';
    }
}

// Stop quiz early and show review of wrong answers
function stopQuiz() {
    console.log('Stop button clicked. wrongAnswers:', wrongAnswers.length, wrongAnswers);
    if (wrongAnswers.length === 0) {
        alert(CONFIG.feedback.noWrongAnswers);
        return;
    }

    // Calculate the number of questions answered
    const questionsAnswered = currentQuestionIndex + (hasAnswered ? 1 : 0);

    // Show review page
    showReviewPage(questionsAnswered);
}

// Generate compact progress tracker table
function generateProgressTrackerTable() {
    let tableHtml = `
        <div style="margin: 20px 0; padding: 20px; background-color: #f8f9fa; border-radius: 8px;">
            <h3 style="color: var(--primary-color); margin-bottom: 15px; font-size: 1.2em;">📊 Voortgang Overzicht</h3>
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <thead>
                        <tr style="background-color: var(--primary-color); color: white;">
                            <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Categorie</th>
                            <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">✓ Goed</th>
                            <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">✗ Fout</th>
                            <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">📋 L.O.V.A.</th>
                        </tr>
                    </thead>
                    <tbody>
    `;

    // Sort categories alphabetically
    const sortedCategories = Object.keys(categoryProgress).sort();

    // Calculate totals
    let totalCorrect = 0;
    let totalIncorrect = 0;
    let totalLovaClicks = 0;

    let visibleRowIndex = 0;
    sortedCategories.forEach((category) => {
        const stats = categoryProgress[category];
        totalCorrect += stats.correct;
        totalIncorrect += stats.incorrect;
        totalLovaClicks += stats.lovaClicks;

        // Skip rows where no questions were practiced (all values are 0)
        if (stats.correct === 0 && stats.incorrect === 0 && stats.lovaClicks === 0) {
            return;
        }

        const bgColor = visibleRowIndex % 2 === 0 ? '#f8f8f8' : '#ffffff';
        tableHtml += `
            <tr style="background-color: ${bgColor};">
                <td style="padding: 10px; border: 1px solid #ddd; font-weight: 500;">${category}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center; color: #28a745; font-weight: bold;">${stats.correct}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center; color: #dc3545; font-weight: bold;">${stats.incorrect}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center; color: var(--secondary-color); font-weight: bold;">${stats.lovaClicks}</td>
            </tr>
        `;
        visibleRowIndex++;
    });

    // Add totals row
    tableHtml += `
                        <tr style="background-color: var(--primary-color); color: white; font-weight: bold;">
                            <td style="padding: 12px; border: 1px solid #ddd;">Totaal</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">${totalCorrect}</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">${totalIncorrect}</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">${totalLovaClicks}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `;

    return tableHtml;
}

// Display review page with wrong answers
function showReviewPage(questionsAnswered) {
    document.getElementById('quizPage').style.display = 'none';
    document.getElementById('reviewPage').style.display = 'block';

    // Update score
    const correctAnswers = questionsAnswered - wrongAnswers.length;
    document.getElementById('reviewScore').textContent = `${correctAnswers}/${questionsAnswered}`;

    // Update message
    if (wrongAnswers.length === 1) {
        document.getElementById('reviewMessage').textContent = CONFIG.reviewMessages.single;
    } else {
        document.getElementById('reviewMessage').textContent = CONFIG.reviewMessages.multiple(wrongAnswers.length);
    }

    // Display wrong answers
    const container = document.getElementById('wrongAnswersContainer');
    container.innerHTML = '';

    // Add progress tracker table at the top
    const progressTableDiv = document.createElement('div');
    progressTableDiv.innerHTML = generateProgressTrackerTable();
    container.appendChild(progressTableDiv);

    wrongAnswers.forEach((item, index) => {
        const reviewItem = document.createElement('div');
        reviewItem.className = 'review-item';

        let contentHtml = '';

        // Add reading content if available
        if (item.question.content) {
            contentHtml += `<div class="review-content">${item.question.content}</div>`;
        }

        // Add visual table if available
        if (item.question.visual) {
            contentHtml += `<div class="review-content">${renderVisualData(item.question.visual)}</div>`;
        }

        reviewItem.innerHTML = `
            <div class="review-item-header">Vraag ${index + 1}</div>
            ${contentHtml}
            <div class="review-question">${item.question.question}</div>

            <div class="review-answer-section">
                <span class="review-label">Jouw antwoord:</span>
                <span class="review-your-answer">${item.userAnswer}</span>
            </div>

            <div class="review-answer-section">
                <span class="review-label">Juiste antwoord:</span>
                <span class="review-correct-answer">${item.correctAnswer}</span>
            </div>

            ${item.explanation ? `<div class="review-explanation"><strong>Uitleg:</strong> ${item.explanation}</div>` : ''}

            ${item.question.extra_info ? generateExtraInfoHtml(item.question.extra_info) : ''}

            ${item.questionType === 'open-ended' && (item.question.strategy || item.question.tips) ? generateStrategyTipsHtml(item.question) : ''}
        `;

        container.appendChild(reviewItem);
    });
}

// Helper function to generate extra_info HTML
function generateExtraInfoHtml(extra_info) {
    let html = '<div class="review-explanation">';

    if (typeof extra_info === 'string') {
        html += `<strong>Achtergrondinfo:</strong> ${extra_info}`;
    } else if (extra_info.concept || extra_info.berekening) {
        if (extra_info.concept) {
            html += `<strong>Concept:</strong> ${extra_info.concept}<br><br>`;
        }
        if (extra_info.berekening && extra_info.berekening.length > 0) {
            html += '<strong>Berekening:</strong><ul>';
            extra_info.berekening.forEach(step => {
                html += `<li>${step}</li>`;
            });
            html += '</ul>';
        }
    } else if (extra_info.tips) {
        html += '<strong>Extra Tips:</strong><ul>';
        extra_info.tips.forEach(tip => {
            html += `<li>${tip}</li>`;
        });
        html += '</ul>';
    }

    html += '</div>';
    return html;
}

// Helper function to generate strategy and tips HTML
function generateStrategyTipsHtml(question) {
    let html = '<div class="review-explanation">';

    if (question.strategy) {
        html += `<strong>Strategie:</strong> ${question.strategy}<br><br>`;
    }

    if (question.tips && question.tips.length > 0) {
        html += '<strong>Tips:</strong><ul>';
        question.tips.forEach(tip => {
            html += `<li>${tip}</li>`;
        });
        html += '</ul>';
    }

    html += '</div>';
    return html;
}

// ========================================
// L.O.V.A. Help Panel (Simplified)
// ========================================

let lovaHelpPanelExpanded = false;

// Toggle L.O.V.A. help panel
function toggleLovaPanel() {
    lovaHelpPanelExpanded = !lovaHelpPanelExpanded;
    const panel = document.getElementById('lovaHelpPanel');
    const icon = document.getElementById('lovaToggleIcon');

    if (lovaHelpPanelExpanded) {
        panel.classList.add('expanded');
        panel.classList.remove('hidden');
        icon.textContent = '▲';

        // Increment L.O.V.A. click counter (global)
        lovaClickCount++;
        document.getElementById('lovaClicks').textContent = lovaClickCount;

        // Increment L.O.V.A. click counter per category
        const currentQuestion = randomizedQuestions[currentQuestionIndex];
        if (currentQuestion && currentQuestion.theme && categoryProgress[currentQuestion.theme]) {
            categoryProgress[currentQuestion.theme].lovaClicks++;
        }
    } else {
        panel.classList.remove('expanded');
        setTimeout(() => {
            if (!lovaHelpPanelExpanded) {
                panel.classList.add('hidden');
            }
        }, CONFIG.lova.panelTransitionDuration);
        icon.textContent = '▼';
    }
}

// Load L.O.V.A. help data into the panel
function loadLovaHelpData(question) {
    if (!question || !question.lova) return;

    const lova = question.lova;

    // Stap 1: Lezen
    if (lova.stap1_lezen) {
        document.getElementById('lovaHelpHoofdvraag').textContent = lova.stap1_lezen.hoofdvraag;

        const ruisList = document.getElementById('lovaHelpRuis');
        ruisList.innerHTML = '';
        lova.stap1_lezen.ruis.forEach(r => {
            const li = document.createElement('li');
            li.textContent = r;
            ruisList.appendChild(li);
        });

        const tussenstappenList = document.getElementById('lovaHelpTussenstappen');
        tussenstappenList.innerHTML = '';
        lova.stap1_lezen.tussenstappen.forEach(t => {
            const li = document.createElement('li');
            li.textContent = t;
            tussenstappenList.appendChild(li);
        });
    }

    // Stap 2: Ordenen
    if (lova.stap2_ordenen) {
        const getallenList = document.getElementById('lovaHelpGetallen');
        getallenList.innerHTML = '';
        Object.entries(lova.stap2_ordenen.relevante_getallen).forEach(([label, value]) => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${label}:</strong> ${value}`;
            getallenList.appendChild(li);
        });

        document.getElementById('lovaHelpTool').textContent = lova.stap2_ordenen.tool;
    }

    // Stap 3: Vormen
    if (lova.stap3_vormen && lova.stap3_vormen.bewerkingen) {
        const bewerkingenContainer = document.getElementById('lovaHelpBewerkingen');
        bewerkingenContainer.innerHTML = '';

        lova.stap3_vormen.bewerkingen.forEach((bew, index) => {
            const bewDiv = document.createElement('div');
            bewDiv.className = 'lova-help-bewerking';
            bewDiv.innerHTML = `
                <div class="lova-help-bewerking-stap">${index + 1}. ${bew.stap}</div>
                <div class="lova-help-bewerking-uitleg">${bew.uitleg}</div>
                <div class="lova-help-bewerking-calc">${bew.berekening} = ${bew.resultaat}</div>
            `;
            bewerkingenContainer.appendChild(bewDiv);
        });
    }

    // Stap 4: Antwoorden
    if (lova.stap4_antwoorden) {
        document.getElementById('lovaHelpEenheid').textContent = lova.stap4_antwoorden.verwachte_eenheid;
        document.getElementById('lovaHelpLogica').textContent = lova.stap4_antwoorden.logica_check;
    }
}

// (All old L.O.V.A. step-by-step functions removed - now using simpler help panel)

// Update visual star progress based on percentage
let lastMilestone = 0; // Track last milestone shown

function updateStarProgress(progress) {
    const stars = document.querySelectorAll('.star-icon');
    const filledStars = Math.floor((progress / 100) * 5);

    stars.forEach((star, index) => {
        if (index < filledStars) {
            if (!star.classList.contains('filled')) {
                // Add filled class with slight delay for stagger effect
                setTimeout(() => {
                    star.textContent = 'star';
                    star.classList.add('filled');
                }, index * 100);
            }
        } else {
            star.textContent = 'star_border';
            star.classList.remove('filled');
        }
    });
}

// Check and display milestone celebrations
function checkMilestone(progress) {
    const milestones = [
        { threshold: 25, message: '🎉 Kwart klaar! Je doet het geweldig!' },
        { threshold: 50, message: '💪 Halverwege! Goed bezig!' },
        { threshold: 75, message: '🌟 Bijna klaar! Je bent er bijna!' },
        { threshold: 100, message: '🏆 Gelukt! Je hebt alle vragen beantwoord!' }
    ];

    const celebration = document.getElementById('milestoneCelebration');
    const message = document.getElementById('milestoneMessage');

    // Find the milestone we just passed
    const passedMilestone = milestones.find(m =>
        progress >= m.threshold && lastMilestone < m.threshold
    );

    if (passedMilestone) {
        lastMilestone = passedMilestone.threshold;
        message.textContent = passedMilestone.message;
        celebration.classList.remove('hidden');

        // Hide after 3 seconds
        setTimeout(() => {
            celebration.classList.add('hidden');
        }, 3000);
    }
}

// Reset milestone tracker when starting new quiz
function resetMilestones() {
    lastMilestone = 0;
}

// Initialize app when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Check for paused quiz on page load
    checkForPausedQuiz();
});
