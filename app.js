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

// NEW: Text-based grouping state (for Begrijpend Lezen)
let textGroups = [];           // Array of text groups
let currentTextIndex = 0;      // Which text we're on
let currentQuestionInText = 0; // Which question within current text
let currentTextGroup = null;   // Current active text group
let useTextGrouping = false;   // Flag to indicate if we should use text grouping

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

    // Update new top bar points counter
    const totalCorrectNew = document.getElementById('totalCorrectNew');
    if (totalCorrectNew) {
        totalCorrectNew.textContent = totalCorrect;
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

// NEW: Create text-based question groups (for Begrijpend Lezen)
function createTextGroups(data) {
    const textGroups = [];

    data.forEach(item => {
        // Each item represents one text with multiple questions
        const group = {
            id: item.id,
            title: item.title,
            theme: item.theme,
            text_type: item.text_type,
            text: item.text || item.content,  // Support both formats
            metadata: item.metadata,
            questions: []
        };

        // Add all questions for this text
        if (item.questions && Array.isArray(item.questions)) {
            item.questions.forEach(question => {
                group.questions.push({
                    item_id: question.item_id,
                    skill: question.skill,
                    strategy: question.strategy,
                    question: question.question,
                    hint: question.hint,
                    options: question.options,
                    correct: question.correct,
                    extra_info: question.extra_info
                });
            });
        }

        textGroups.push(group);
    });

    // Randomize the TEXT order (not individual questions)
    return shuffleArray(textGroups);
}

// Map subject name to file path
function getFilePath(subject) {
    // NEW: Check if subject uses structured file paths from CONFIG
    // Parse subject format: "subjectname-level" (e.g., "begrijpendlezen-m4", "basisvaardigheden-e5")
    const parts = subject.split('-');
    const baseSubject = parts[0];
    const level = parts[1]; // e.g., "m4", "e5"

    // Check if this subject has structured paths in CONFIG
    if (CONFIG.subjectFilePaths && CONFIG.subjectFilePaths[baseSubject]) {
        const subjectPaths = CONFIG.subjectFilePaths[baseSubject];

        // Determine groep from level (e.g., "m4" -> "groep4", "e5" -> "groep5")
        if (level && level.length >= 2) {
            const groepNumber = level.substring(1); // Extract number from "m4" -> "4"
            const groepKey = `groep${groepNumber}`;

            if (subjectPaths[groepKey] && subjectPaths[groepKey][level]) {
                return subjectPaths[groepKey][level];
            }
        }
    }

    // LEGACY: Map basisvaardigheden subjects to exercises/gb/ directory (backwards compatibility)
    const gbMapping = {
        'basisvaardigheden-m3': 'exercises/gb/gb_groep3_m3.json',
        'basisvaardigheden-e3': 'exercises/gb/gb_groep3_e3.json',
        'basisvaardigheden-m4': 'exercises/gb/gb_groep4_m4.json',
        'basisvaardigheden-e4': 'exercises/gb/gb_groep4_e4.json',
        'basisvaardigheden-m5': 'exercises/gb/gb_groep5_m5.json',
        'basisvaardigheden-e5': 'exercises/gb/gb_groep5_e5.json',
        'basisvaardigheden-m6': 'exercises/gb/gb_groep6_m6.json',
        'basisvaardigheden-e6': 'exercises/gb/gb_groep6_e6.json',
        'basisvaardigheden-m7': 'exercises/gb/gb_groep7_m7.json',
        'basisvaardigheden-e7': 'exercises/gb/gb_groep7_e7.json',
        'basisvaardigheden-e8': 'exercises/gb/gb_groep8_e8.json'
    };

    // Check if this is a GB subject
    if (gbMapping[subject]) {
        return gbMapping[subject];
    }

    // Default: use subject + Template suffix
    return subject + CONFIG.templateFileSuffix;
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

    // Subject metadata for contextual header
    const subjectMeta = {
        'verhaaltjessommen': {
            title: 'Verhaaltjessommen',
            icon: 'calculate',
            color: '#FF7F69',
            description: 'Los slimme rekenpuzzels op met contextrijke rekenproblemen'
        },
        'basisvaardigheden': {
            title: 'Getal & Bewerking',
            icon: 'functions',
            color: '#FF7F69',
            description: 'Train je rekenkundige basisvaardigheden en word steeds sneller'
        },
        'woordenschat': {
            title: 'Woordenschat',
            icon: 'local_library',
            color: '#7FD4A8',
            description: 'Vergroot je woordenkennis en leer nieuwe woorden en hun betekenis'
        },
        'wereldorientatie': {
            title: 'Wereldoriëntatie',
            icon: 'public',
            color: '#5FC5B8',
            description: 'Ontdek alles over de aarde, geschiedenis, natuur en techniek'
        }
    };

    const meta = subjectMeta[type] || {
        title: type,
        icon: 'school',
        color: '#4A7BA7',
        description: 'Kies jouw niveau om te beginnen'
    };

    // Update contextual header
    document.getElementById('levelTitle').textContent = meta.title;
    document.getElementById('levelBreadcrumb').textContent = meta.title;
    document.getElementById('levelDescription').textContent = meta.description;

    const levelSubjectIcon = document.getElementById('levelSubjectIcon');
    levelSubjectIcon.innerHTML = `<i class="material-icons">${meta.icon}</i>`;
    levelSubjectIcon.style.background = `linear-gradient(135deg, ${meta.color} 0%, ${meta.color}dd 100%)`;

    const levelGrid = document.getElementById('levelGrid');
    levelGrid.innerHTML = '';

    // Define levels with gamified progression (ordered from youngest to oldest)
    const levels = [
        {
            group: 4,
            icon: '🌱',
            title: 'Groep 4',
            description: 'M4 niveau',
            difficulty: 'Basis',
            subject: type + '-emma'
        },
        {
            group: 5,
            icon: '📖',
            title: 'Groep 5',
            description: 'M5 niveau',
            difficulty: 'Midden',
            subject: type + '-kate'
        },
        {
            group: 8,
            icon: '🏆',
            title: 'Groep 8',
            description: 'Eindtoets niveau',
            difficulty: 'CITO',
            subject: type // verhaaltjessommen or basisvaardigheden
        }
    ];

    // Create gamified level cards
    levels.forEach(level => {
        const card = document.createElement('div');
        card.className = `level-card level-${level.group}`;
        card.onclick = () => loadSubject(level.subject);

        card.innerHTML = `
            <div class="level-badge">${level.group}</div>
            <h3 class="level-card-title">${level.title}</h3>
            <p class="level-card-description">${level.description}</p>
            <div class="level-card-icon">${level.icon}</div>
            <span class="level-difficulty">${level.difficulty}</span>
        `;

        levelGrid.appendChild(card);
    });
}

// Load subject and show themes
async function loadSubject(subject) {
    const filename = getFilePath(subject);
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

    // Update header
    const subjectTitle = CONFIG.subjectTitles[subject] || subject;
    document.getElementById('subjectTitle').textContent = 'Kies wat je wilt oefenen!';
    document.getElementById('themeBreadcrumb').textContent = subjectTitle;

    const themeGrid = document.getElementById('themeGrid');
    themeGrid.innerHTML = '';

    // Calculate total questions for "all themes"
    let totalAllQuestions = 0;
    data.forEach(item => {
        if (Array.isArray(item.questions)) {
            totalAllQuestions += item.questions.length;
        } else if (item.question) {
            totalAllQuestions += 1;
        }
    });

    // TIER 1: PRIMARY MIX MODE CTA (HERO CARD)
    const primaryCTA = document.createElement('div');
    primaryCTA.className = 'theme-primary-cta';
    primaryCTA.onclick = () => startQuizWithTheme(subject, null);
    const allHighscore = getHighscore(subject, null);

    const motivationalPhrases = [
        'Klaar om jezelf uit te dagen?',
        'Hoeveel kun jij er goed beantwoorden?',
        'Verdien badges terwijl je oefent!',
        'Elke vraag maakt je wijzer!'
    ];
    const randomPhrase = motivationalPhrases[Math.floor(Math.random() * motivationalPhrases.length)];

    primaryCTA.innerHTML = `
        <div class="theme-primary-content">
            <div class="theme-primary-icon">
                <i class="material-icons">rocket_launch</i>
            </div>
            <div class="theme-primary-text">
                <h2 class="theme-primary-title">🚀 Complete Mix Mode</h2>
                <p class="theme-primary-description">${randomPhrase}</p>
                <div class="theme-primary-meta">
                    <span class="theme-primary-badge">
                        <i class="material-icons">quiz</i>
                        ${totalAllQuestions} vragen klaar!
                    </span>
                    ${allHighscore > 0 ? `
                        <span class="theme-primary-badge">
                            <i class="material-icons">emoji_events</i>
                            Highscore: ${allHighscore}
                        </span>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
    themeGrid.appendChild(primaryCTA);

    // TIER 2: SUBTOPIC CARDS
    if (themes && themes.length > 0) {
        const subtopicsSection = document.createElement('div');
        subtopicsSection.className = 'theme-subtopics-section';

        // Check if this is a math subject that needs categorization
        const isMathSubject = subject.includes('verhaaltjessommen') || subject.includes('basisvaardigheden');

        if (isMathSubject) {
            // Categorize themes for math subjects
            const themeCategories = categorizeThemes(themes);

            // Add categorized themes
            Object.entries(themeCategories).forEach(([category, categoryThemes]) => {
                if (categoryThemes.length === 0) return;

                // Add category section
                const categorySection = document.createElement('div');
                categorySection.className = 'theme-category-section';

                // Add category header
                const categoryHeader = document.createElement('div');
                categoryHeader.className = 'theme-category-header';
                categoryHeader.innerHTML = `<h3 class="theme-category-title">${category}</h3>`;
                categorySection.appendChild(categoryHeader);

                // Add theme grid for this category
                const categoryGrid = document.createElement('div');
                categoryGrid.className = 'theme-subtopics-grid';

                categoryThemes.forEach((theme, index) => {
                    addThemeCardNew(categoryGrid, theme, data, subject, index);
                });

                categorySection.appendChild(categoryGrid);
                subtopicsSection.appendChild(categorySection);
            });
        } else {
            // For non-math subjects, just list all themes without categorization
            const subtopicsGrid = document.createElement('div');
            subtopicsGrid.className = 'theme-subtopics-grid';

            themes.forEach((theme, index) => {
                addThemeCardNew(subtopicsGrid, theme, data, subject, index);
            });

            subtopicsSection.appendChild(subtopicsGrid);
        }

        themeGrid.appendChild(subtopicsSection);
    }
}

// Helper function to create NEW tier 2 subtopic card
function addThemeCardNew(container, theme, data, subject, index) {
    const filteredItems = data.filter(item => item.theme === theme);
    let questionCount = 0;

    filteredItems.forEach(item => {
        if (Array.isArray(item.questions)) {
            questionCount += item.questions.length;
        } else if (item.question) {
            questionCount += 1;
        }
    });

    // Theme-specific icons and colors
    const themeIcons = {
        'optellen': '➕',
        'aftrekken': '➖',
        'vermenigvuldigen': '✖️',
        'delen': '➗',
        'tijd': '⏰',
        'geld': '💰',
        'gewicht': '⚖️',
        'verhoudingen': '📊',
        'inhoud': '📦',
        'meetkunde': '📐',
        'oppervlakte': '📏',
        'omtrek': '🔄'
    };

    const colors = ['color-teal', 'color-blue', 'color-purple', 'color-mint', 'color-coral', 'color-yellow'];
    const colorClass = colors[index % colors.length];

    const icon = themeIcons[theme.toLowerCase()] || '📚';

    const themeCard = document.createElement('div');
    themeCard.className = `theme-subtopic-card ${colorClass}`;
    themeCard.onclick = () => startQuizWithTheme(subject, theme);
    const themeHighscore = getHighscore(subject, theme);

    themeCard.innerHTML = `
        <div class="theme-subtopic-header">
            <span class="theme-subtopic-icon">${icon}</span>
            <h3 class="theme-subtopic-title">${theme}</h3>
        </div>
        <div class="theme-subtopic-count">
            <i class="material-icons">quiz</i>
            <span>${questionCount} vragen</span>
        </div>
        ${themeHighscore > 0 ? `
            <div class="theme-subtopic-highscore">
                <i class="material-icons">emoji_events</i>
                <span>Highscore: ${themeHighscore}</span>
            </div>
        ` : ''}
        <div class="theme-subtopic-cta">
            <span>Start oefenen</span>
            <i class="material-icons">arrow_forward</i>
        </div>
    `;

    container.appendChild(themeCard);
}

// Helper function to create OLD theme card (for backwards compatibility)
function addThemeCard(container, theme, data, subject) {
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
    container.appendChild(themeCard);
}

// Categorize themes into logical groups (only for math subjects)
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
            // Default to Meten & Verhoudingen for other math-related themes
            categories['📏 Meten & Verhoudingen'].push(theme);
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

    // NEW: Check if this is a "begrijpendlezen" subject to use text grouping
    const baseSubject = subject.split('-')[0];
    useTextGrouping = (baseSubject === 'begrijpendlezen');

    let quizState;

    if (useTextGrouping) {
        // Create text groups for Begrijpend Lezen
        textGroups = createTextGroups(currentQuiz);

        // Calculate total questions across all texts
        totalQuestions = textGroups.reduce((sum, group) =>
            sum + group.questions.length, 0
        );

        // Initialize text state
        currentTextIndex = 0;
        currentQuestionInText = 0;

        // Create a flat list of all questions for category progress (optional)
        randomizedQuestions = [];
        textGroups.forEach(group => {
            group.questions.forEach(q => {
                randomizedQuestions.push({
                    ...q,
                    theme: group.theme
                });
            });
        });

        // Initialize category progress tracker
        initializeCategoryProgress(randomizedQuestions);

        // Save quiz state to sessionStorage for quiz.html
        quizState = {
            subject: subject,
            currentSubject: currentSubject,
            currentTheme: currentTheme,
            currentQuiz: currentQuiz,
            textGroups: textGroups,
            useTextGrouping: true,
            currentTextIndex: 0,
            currentQuestionInText: 0,
            totalQuestions: totalQuestions,
            currentQuestionIndex: 0,
            score: 0,
            wrongAnswers: [],
            lovaClickCount: 0,
            categoryProgress: categoryProgress
        };
    } else {
        // Create randomized questions from the current quiz data (traditional mode)
        randomizedQuestions = createRandomizedQuestions(currentQuiz);
        totalQuestions = randomizedQuestions.length;

        // Initialize category progress tracker (reset to 0)
        initializeCategoryProgress(randomizedQuestions);

        // Save quiz state to sessionStorage for quiz.html
        quizState = {
            subject: subject,
            currentSubject: currentSubject,
            currentTheme: currentTheme,
            currentQuiz: currentQuiz,
            randomizedQuestions: randomizedQuestions,
            useTextGrouping: false,
            totalQuestions: totalQuestions,
            currentQuestionIndex: 0,
            score: 0,
            wrongAnswers: [],
            lovaClickCount: 0,
            categoryProgress: categoryProgress
        };
    }

    sessionStorage.setItem('quizState', JSON.stringify(quizState));

    // Redirect to quiz.html
    window.location.href = 'quiz.html';
}

// Update breadcrumb navigation with current subject and level
function updateBreadcrumb(subject) {
    const breadcrumbSubject = document.getElementById('breadcrumbSubject');
    const breadcrumbLevel = document.getElementById('breadcrumbLevel');
    const breadcrumbLevelSep = document.getElementById('breadcrumbLevelSep');

    // Determine base subject and level
    let baseSubject = subject;
    let level = null;

    // Check if subject has level variant (emma = midden groep 4, kate = midden groep 5)
    if (subject.endsWith('-emma')) {
        baseSubject = subject.replace('-emma', '');
        level = 'Midden Groep 4';
    } else if (subject.endsWith('-kate')) {
        baseSubject = subject.replace('-kate', '');
        level = 'Midden Groep 5';
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

    // Update new breadcrumb elements
    const breadcrumbSubjectNew = document.getElementById('breadcrumbSubjectNew');
    const breadcrumbLevelNew = document.getElementById('breadcrumbLevelNew');
    const breadcrumbLevelSepNew = document.getElementById('breadcrumbLevelSepNew');

    if (breadcrumbSubjectNew) {
        breadcrumbSubjectNew.textContent = CONFIG.subjectTitles[baseSubject] || CONFIG.subjectTitles[subject] || subject;
    }

    if (breadcrumbLevelNew && breadcrumbLevelSepNew) {
        if (level) {
            breadcrumbLevelNew.textContent = level;
            breadcrumbLevelNew.style.display = 'inline';
            breadcrumbLevelSepNew.style.display = 'inline';
        } else {
            breadcrumbLevelNew.style.display = 'none';
            breadcrumbLevelSepNew.style.display = 'none';
        }
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

// Update quiz card header with subject icon, title, and subtitle
function updateQuizCardHeader(subject) {
    const iconElement = document.getElementById('quizSubjectIcon');
    const titleElement = document.getElementById('quizCardSubjectTitle');
    const subtitleElement = document.getElementById('quizCardSubtitle');

    if (!iconElement || !titleElement || !subtitleElement) {
        return;
    }

    // Determine base subject and level
    let baseSubject = subject;
    let level = null;

    // Check if subject has level variant (emma = midden groep 4, kate = midden groep 5)
    if (subject.endsWith('-emma')) {
        baseSubject = subject.replace('-emma', '');
        level = 'Midden Groep 4';
    } else if (subject.endsWith('-kate')) {
        baseSubject = subject.replace('-kate', '');
        level = 'Midden Groep 5';
    } else if (['verhaaltjessommen', 'basisvaardigheden', 'wereldorientatie', 'woordenschat'].includes(subject)) {
        level = 'Groep 8';
    }

    // Set subject icon (exclude graduation cap emoji - too much white space)
    let subjectIcon = CONFIG.subjectIcons[subject] || CONFIG.subjectIcons[baseSubject] || '📚';
    if (subjectIcon === '🎓') {
        subjectIcon = '📚'; // Replace graduation cap with book
    }
    iconElement.textContent = subjectIcon;

    // Set subject title
    const subjectTitle = CONFIG.subjectTitles[baseSubject] || CONFIG.subjectTitles[subject] || subject;
    titleElement.textContent = subjectTitle;

    // Set subtitle (level)
    if (level) {
        subtitleElement.textContent = level;
    } else {
        subtitleElement.textContent = '';
    }
}

function loadCurrentQuestion() {
    // NEW: Check if using text grouping mode
    if (useTextGrouping) {
        loadTextGroupQuestion();
        return;
    }

    // Traditional mode: load from randomizedQuestions
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

    // Sync new hint container
    const hintContainerNew = document.getElementById('hintContainerNew');
    if (hintContainerNew) {
        hintContainerNew.innerHTML = '';
    }

    // Update progress
    const progress = (currentQuestionIndex / totalQuestions) * 100;

    // Update new progress bar elements
    const progressLabel = document.getElementById('progressLabel');
    const progressPercentage = document.getElementById('progressPercentage');
    const progressBarFill = document.getElementById('progressBarFill');

    if (progressLabel) {
        progressLabel.textContent = `Vraag ${currentQuestionIndex + 1} van ${totalQuestions}`;
    }
    if (progressPercentage) {
        progressPercentage.textContent = `${Math.round(progress)}% voltooid`;
    }
    if (progressBarFill) {
        progressBarFill.style.width = `${progress}%`;
    }

    // Update new top bar progress elements
    const progressLabelNew = document.getElementById('progressLabelNew');
    const progressBarFillNew = document.getElementById('progressBarFillNew');

    if (progressLabelNew) {
        progressLabelNew.textContent = `Vraag ${currentQuestionIndex + 1} van ${totalQuestions}`;
    }
    if (progressBarFillNew) {
        progressBarFillNew.style.width = `${progress}%`;
    }

    // Also update old questionCounter for backwards compatibility
    const questionCounter = document.getElementById('questionCounter');
    if (questionCounter) {
        questionCounter.textContent = `Vraag ${currentQuestionIndex + 1} van ${totalQuestions}`;
    }

    // Update quiz card header (icon, title, subtitle)
    updateQuizCardHeader(currentSubject);

    // Update visual star progress
    updateStarProgress(progress);

    // Check for milestone celebrations
    checkMilestone(progress);

    // Show reading content if available
    const readingContent = document.getElementById('readingContent');
    const readingContentNew = document.getElementById('readingContentNew');
    const storyBlockWrapper = document.getElementById('storyBlockWrapper');

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

        // Sync to new card with story header wrapper
        if (readingContentNew) {
            // Put content inside the story-text-content div
            const storyTextContent = readingContentNew.querySelector('.story-text-content');
            if (storyTextContent) {
                storyTextContent.innerHTML = contentHtml;
            }
        }
        if (storyBlockWrapper) {
            storyBlockWrapper.classList.remove('hidden');
        }
    } else {
        readingContent.classList.add('hidden');
        if (storyBlockWrapper) {
            storyBlockWrapper.classList.add('hidden');
        }
    }

    // Load question
    document.getElementById('questionText').textContent = currentQuestion.question;

    // Sync to new question card
    const questionTextNew = document.getElementById('questionTextNew');
    if (questionTextNew) {
        questionTextNew.textContent = currentQuestion.question;
    }

    // Check if question has L.O.V.A. data
    const hasLovaData = currentQuestion.lova && currentQuestion.lova.stap1_lezen;
    const lovaHelpButton = document.getElementById('lovaHelpButton');
    const lovaHelpButtonNew = document.getElementById('lovaHelpButtonNew');
    const lovaHelpPanel = document.getElementById('lovaHelpPanel');

    if (hasLovaData) {
        // Show L.O.V.A. help button (question mark icon) and load data into panel
        lovaHelpButton.style.display = 'flex';
        if (lovaHelpButtonNew) {
            lovaHelpButtonNew.style.display = 'inline-flex';
        }
        loadLovaHelpData(currentQuestion);

        // Reset panel to collapsed state for new question
        lovaHelpPanelExpanded = false;
        lovaHelpPanel.classList.remove('expanded');
        lovaHelpPanel.classList.add('hidden');
    } else {
        // Hide L.O.V.A. help button
        lovaHelpButton.style.display = 'none';
        if (lovaHelpButtonNew) {
            lovaHelpButtonNew.style.display = 'none';
        }
        lovaHelpPanel.classList.add('hidden');
    }

    // Handle different question types (always show regular quiz)
    const optionsContainer = document.getElementById('optionsContainer');
    const textareaAnswer = document.getElementById('textareaAnswer');
    const feedbackSection = document.getElementById('feedbackSection');

    // Get new elements
    const optionsContainerNew = document.getElementById('optionsContainerNew');
    const textareaAnswerNew = document.getElementById('textareaAnswerNew');
    const feedbackSectionNew = document.getElementById('feedbackSectionNew');

    // Hide feedback section and reset classes for new question
    feedbackSection.classList.add('hidden');
    feedbackSection.classList.remove('correct', 'incorrect');
    document.getElementById('correctAnswerDisplay').classList.add('hidden');
    document.getElementById('extraInfoDisplay').classList.add('hidden');
    document.getElementById('verhoudingstabelContainer').innerHTML = ''; // Clear verhoudingstabel
    document.getElementById('strategyAndTips').classList.add('hidden');

    // Sync new feedback section
    if (feedbackSectionNew) {
        feedbackSectionNew.classList.add('hidden');
        feedbackSectionNew.classList.remove('correct', 'incorrect');
        const correctAnswerDisplayNew = document.getElementById('correctAnswerDisplayNew');
        const extraInfoDisplayNew = document.getElementById('extraInfoDisplayNew');
        const verhoudingstabelContainerNew = document.getElementById('verhoudingstabelContainerNew');
        const strategyAndTipsNew = document.getElementById('strategyAndTipsNew');

        if (correctAnswerDisplayNew) correctAnswerDisplayNew.classList.add('hidden');
        if (extraInfoDisplayNew) extraInfoDisplayNew.classList.add('hidden');
        if (verhoudingstabelContainerNew) verhoudingstabelContainerNew.innerHTML = '';
        if (strategyAndTipsNew) strategyAndTipsNew.classList.add('hidden');
    }

    if (currentQuestion.options) {
        // Multiple choice question
        optionsContainer.classList.remove('hidden');
        textareaAnswer.classList.add('hidden');

        if (optionsContainerNew) {
            optionsContainerNew.classList.remove('hidden');
        }
        if (textareaAnswerNew) {
            textareaAnswerNew.classList.add('hidden');
        }

        optionsContainer.innerHTML = '';
        if (optionsContainerNew) {
            optionsContainerNew.innerHTML = '';
        }
        currentQuestion.options.forEach((option, index) => {
            const letters = ['A', 'B', 'C', 'D', 'E', 'F'];
            const letter = letters[index] || String.fromCharCode(65 + index);

            const optionElement = document.createElement('div');
            optionElement.className = 'option';
            optionElement.textContent = typeof option === 'string' ? option : option.text;
            optionElement.onclick = () => selectOption(index);
            optionsContainer.appendChild(optionElement);

            // Sync to new container with letter prefix
            if (optionsContainerNew) {
                const optionElementNew = document.createElement('div');
                optionElementNew.className = 'option';
                optionElementNew.setAttribute('data-letter', letter);
                optionElementNew.textContent = typeof option === 'string' ? option : option.text;
                optionElementNew.onclick = () => selectOption(index);
                optionsContainerNew.appendChild(optionElementNew);
            }
        });
    } else {
        // Open question
        optionsContainer.classList.add('hidden');
        textareaAnswer.classList.remove('hidden');
        textareaAnswer.value = '';

        // Sync to new elements
        if (optionsContainerNew) {
            optionsContainerNew.classList.add('hidden');
        }
        if (textareaAnswerNew) {
            textareaAnswerNew.classList.remove('hidden');
            textareaAnswerNew.value = '';
        }
    }

    // Reset UI state
    selectedAnswer = null;
    hasAnswered = false;
    document.getElementById('submitBtn').classList.remove('hidden');
    document.getElementById('nextBtn').classList.add('hidden');
}

// NEW: Load question in text grouping mode (for Begrijpend Lezen)
function loadTextGroupQuestion() {
    // Check if we've finished all texts
    if (currentTextIndex >= textGroups.length) {
        showResults();
        return;
    }

    // Get current text group
    currentTextGroup = textGroups[currentTextIndex];

    // Check if we've finished all questions in current text
    if (currentQuestionInText >= currentTextGroup.questions.length) {
        // Move to next text
        currentTextIndex++;
        currentQuestionInText = 0;

        // Update sessionStorage
        saveTextGroupProgress();

        // Recursively load next text
        loadTextGroupQuestion();
        return;
    }

    // Get current question
    const currentQuestion = currentTextGroup.questions[currentQuestionInText];

    // Reset error tracking
    currentQuestionErrors = 0;
    incorrectOptions.clear();

    // Calculate overall progress
    const questionsCompletedSoFar = calculateQuestionsCompleted();
    const overallQuestionNumber = questionsCompletedSoFar + currentQuestionInText + 1;
    const progress = (overallQuestionNumber / totalQuestions) * 100;

    // Update progress bar
    const progressLabelNew = document.getElementById('progressLabelNew');
    const progressBarFillNew = document.getElementById('progressBarFillNew');

    if (progressLabelNew) {
        progressLabelNew.textContent = `Vraag ${currentQuestionInText + 1}/${currentTextGroup.questions.length} van "${currentTextGroup.title}"`;
    }
    if (progressBarFillNew) {
        progressBarFillNew.style.width = `${progress}%`;
    }

    // Display reading text (stays visible for all questions)
    displayReadingText(currentTextGroup);

    // Display question metadata (skill, strategy)
    displayQuestionMetadata(currentQuestion);

    // Display question text
    const questionTextNew = document.getElementById('questionTextNew');
    if (questionTextNew) {
        questionTextNew.textContent = currentQuestion.question;
    }

    // Hide hint initially
    const hintContainerNew = document.getElementById('hintContainerNew');
    if (hintContainerNew) {
        hintContainerNew.innerHTML = '';
        hintContainerNew.classList.add('hidden');
    }

    // NEW: Show/hide hint pill button based on whether question has a hint
    const hintPillContainer = document.getElementById('hintPillContainer');
    const hintDisplay = document.getElementById('hintDisplay');
    const hintDisplayText = document.getElementById('hintDisplayText');

    if (currentQuestion.hint && hintPillContainer && hintDisplay && hintDisplayText) {
        // Question has a hint - show the button
        hintPillContainer.style.display = 'block';
        hintDisplayText.textContent = currentQuestion.hint;
        // Hide the hint display by default (user needs to click to see it)
        hintDisplay.style.display = 'none';
    } else if (hintPillContainer && hintDisplay) {
        // No hint - hide both button and display
        hintPillContainer.style.display = 'none';
        hintDisplay.style.display = 'none';
    }

    // Render answer options
    renderAnswerOptions(currentQuestion);

    // Hide feedback
    const feedbackSectionNew = document.getElementById('feedbackSectionNew');
    if (feedbackSectionNew) {
        feedbackSectionNew.classList.add('hidden');
    }

    // Show submit button, hide next button
    document.getElementById('submitBtn').classList.remove('hidden');
    document.getElementById('nextBtn').classList.add('hidden');

    // Reset UI state
    selectedAnswer = null;
    hasAnswered = false;
}

// Helper: Calculate how many questions we've completed so far
function calculateQuestionsCompleted() {
    let completed = 0;
    for (let i = 0; i < currentTextIndex; i++) {
        completed += textGroups[i].questions.length;
    }
    return completed;
}

// Helper: Display reading text with metadata
function displayReadingText(textGroup) {
    const storyBlockWrapper = document.getElementById('storyBlockWrapper');
    const storyTextContent = document.querySelector('.story-text-content');
    const readingContentNew = document.getElementById('readingContentNew');

    if (!storyBlockWrapper || !readingContentNew) return;

    // Show the story block
    storyBlockWrapper.classList.remove('hidden');

    // Set reading text
    if (storyTextContent) {
        storyTextContent.innerHTML = `<p>${textGroup.text}</p>`;
    }

    // Update title in the story header
    const storyHeaderLabel = readingContentNew.querySelector('.story-header-label span:nth-child(2)');
    if (storyHeaderLabel) {
        storyHeaderLabel.textContent = textGroup.title;
    }
}

// Helper: Display question metadata (skill, strategy badges)
function displayQuestionMetadata(question) {
    const skillBadge = document.getElementById('skillBadge');
    const skillType = document.getElementById('skillType');
    const strategyBadge = document.getElementById('strategyBadge');
    const strategyType = document.getElementById('strategyType');

    // Show skill if available
    if (question.skill && skillBadge && skillType) {
        skillBadge.style.display = 'inline-flex';
        skillType.textContent = capitalizeFirst(question.skill);
    } else if (skillBadge) {
        skillBadge.style.display = 'none';
    }

    // Show strategy if available
    if (question.strategy && strategyBadge && strategyType) {
        strategyBadge.style.display = 'inline-flex';
        strategyType.textContent = capitalizeFirst(question.strategy);
    } else if (strategyBadge) {
        strategyBadge.style.display = 'none';
    }
}

// Helper: Render answer options (supports both old and new format)
function renderAnswerOptions(question) {
    const container = document.getElementById('optionsContainerNew');
    if (!container) return;

    container.innerHTML = '';
    container.classList.remove('hidden');

    question.options.forEach((option, index) => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option';

        let optionText, optionLabel, isCorrect;

        if (typeof option === 'string') {
            // Old format
            optionText = option;
            optionLabel = String.fromCharCode(65 + index); // A, B, C, D
            isCorrect = question.correct === index;
        } else {
            // NEW format
            optionText = option.text;
            optionLabel = option.label;
            isCorrect = option.is_correct;
        }

        optionDiv.setAttribute('data-letter', optionLabel);
        optionDiv.setAttribute('data-index', index);
        optionDiv.setAttribute('data-correct', isCorrect);
        optionDiv.textContent = optionText;

        optionDiv.onclick = () => selectOption(index);
        container.appendChild(optionDiv);
    });
}

// Helper: Capitalize first letter
function capitalizeFirst(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// NEW: Toggle hint display
function toggleHint() {
    const hintDisplay = document.getElementById('hintDisplay');
    const hintBtn = document.getElementById('hintPillBtn');

    if (hintDisplay.style.display === 'none') {
        hintDisplay.style.display = 'block';
        hintBtn.classList.add('active');
    } else {
        hintDisplay.style.display = 'none';
        hintBtn.classList.remove('active');
    }
}

// Helper: Save text group progress to sessionStorage
function saveTextGroupProgress() {
    if (!window.location.pathname.endsWith('quiz.html')) return;

    const quizState = JSON.parse(sessionStorage.getItem('quizState') || '{}');
    quizState.currentTextIndex = currentTextIndex;
    quizState.currentQuestionInText = currentQuestionInText;
    quizState.score = score;
    quizState.wrongAnswers = wrongAnswers;
    quizState.lovaClickCount = lovaClickCount;
    quizState.categoryProgress = categoryProgress;
    sessionStorage.setItem('quizState', JSON.stringify(quizState));
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

/**
 * Populate the enhanced learning feedback component
 * @param {boolean} isCorrect - Whether the answer was correct
 * @param {Object} currentQuestion - The current question object
 * @param {Object|null} selectedOption - The selected option (for error analysis)
 * @param {number} correctIndex - Index of correct answer
 */
function populateEnhancedFeedback(isCorrect, currentQuestion, selectedOption = null, correctIndex = null) {
    const feedbackSection = document.getElementById('feedbackSectionNew');
    if (!feedbackSection) return;

    // Show and reset feedback
    feedbackSection.classList.remove('hidden', 'correct', 'incorrect');
    feedbackSection.classList.add(isCorrect ? 'correct' : 'incorrect');

    // Get all feedback elements
    const feedbackEmoji = document.getElementById('feedbackEmojiNew');
    const feedbackHeadline = document.getElementById('feedbackHeadlineNew');
    const feedbackAnswerConfirm = document.getElementById('feedbackAnswerConfirmNew');
    const feedbackWhySection = document.getElementById('feedbackWhySection');
    const feedbackWhyContent = document.getElementById('feedbackWhyContentNew');
    const feedbackWorkedSection = document.getElementById('feedbackWorkedSection');
    const feedbackWorkedExample = document.getElementById('feedbackWorkedExampleNew');
    const feedbackTipSection = document.getElementById('feedbackTipSection');
    const feedbackTipContent = document.getElementById('feedbackTipContentNew');

    // 1. Set Encouraging Headline
    if (isCorrect) {
        if (feedbackEmoji) feedbackEmoji.textContent = '🎉';
        if (feedbackHeadline) feedbackHeadline.textContent = 'Top gedaan!';
        if (feedbackAnswerConfirm) {
            feedbackAnswerConfirm.textContent = 'Je hebt het juiste antwoord gekozen! Je bent goed bezig!';
        }
    } else {
        if (feedbackEmoji) feedbackEmoji.textContent = '🤗';
        if (feedbackHeadline) feedbackHeadline.textContent = 'Bijna! Probeer het nog een keer!';

        // Show correct answer
        if (feedbackAnswerConfirm) {
            if (correctIndex !== null && currentQuestion.options) {
                // Multiple choice question
                const correctAnswerText = typeof currentQuestion.options[correctIndex] === 'string'
                    ? currentQuestion.options[correctIndex]
                    : currentQuestion.options[correctIndex].text;

                // Get the letter for the correct answer
                const letters = ['A', 'B', 'C', 'D', 'E', 'F'];
                const correctLetter = letters[correctIndex] || '';

                feedbackAnswerConfirm.textContent = `Het goede antwoord was ${correctLetter} – ${correctAnswerText}`;
            } else if (currentQuestion.possible_answer) {
                // Open-ended question
                feedbackAnswerConfirm.textContent = `Een goed antwoord is: ${currentQuestion.possible_answer}`;
            }
        }
    }

    // 2. Show "Waarom?" section (concept explanation)
    if (feedbackWhySection && feedbackWhyContent && currentQuestion.extra_info?.concept) {
        feedbackWhySection.style.display = 'block';
        feedbackWhyContent.textContent = currentQuestion.extra_info.concept;
    } else if (feedbackWhySection) {
        feedbackWhySection.style.display = 'none';
    }

    // 3. Show "Zo werkt het:" section (worked example)
    if (feedbackWorkedSection && feedbackWorkedExample && currentQuestion.extra_info?.berekening) {
        feedbackWorkedSection.style.display = 'block';

        // Join calculation steps with line breaks
        const calculationSteps = Array.isArray(currentQuestion.extra_info.berekening)
            ? currentQuestion.extra_info.berekening.join('\n')
            : currentQuestion.extra_info.berekening;

        feedbackWorkedExample.textContent = calculationSteps;
    } else if (feedbackWorkedSection) {
        feedbackWorkedSection.style.display = 'none';
    }

    // 4. Show Tip section
    if (feedbackTipSection && feedbackTipContent) {
        let tipText = '';

        if (!isCorrect && selectedOption && typeof selectedOption === 'object' && selectedOption.foutanalyse) {
            // For incorrect answers with foutanalyse: extract just the main tip without reflectievraag
            const foutanalyse = selectedOption.foutanalyse;
            // Remove the reflectievraag part (everything from 🤔 onwards)
            tipText = foutanalyse.split('🤔')[0].trim();
            // Remove any ** markdown formatting
            tipText = tipText.replace(/\*\*/g, '');
        } else if (currentQuestion.extra_info?.tips && Array.isArray(currentQuestion.extra_info.tips) && currentQuestion.extra_info.tips.length > 0) {
            // Use general tips from extra_info
            tipText = currentQuestion.extra_info.tips[0];
        } else {
            // Default tip based on theme
            if (currentQuestion.theme && currentQuestion.theme.includes('tafels')) {
                tipText = 'Oefen de tafels regelmatig om ze beter te onthouden!';
            } else if (currentQuestion.theme && currentQuestion.theme.includes('geld')) {
                tipText = 'Let goed op de komma bij geldbedragen!';
            } else {
                tipText = 'Lees de vraag nog een keer goed door. Wat wordt er precies gevraagd?';
            }
        }

        if (tipText) {
            feedbackTipSection.style.display = 'block';
            feedbackTipContent.textContent = tipText;
        } else {
            feedbackTipSection.style.display = 'none';
        }
    }
}

function submitAnswer() {
    if (hasAnswered) return;

    // NEW: Get current question based on mode
    let currentQuestion;
    if (useTextGrouping) {
        currentQuestion = currentTextGroup.questions[currentQuestionInText];
    } else {
        currentQuestion = randomizedQuestions[currentQuestionIndex];
    }

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

    // Also show new feedback section
    const feedbackSectionNew = document.getElementById('feedbackSectionNew');
    if (feedbackSectionNew) {
        feedbackSectionNew.classList.remove('hidden');
    }

    if (currentQuestion.options) {
        // Multiple choice
        if (selectedAnswer === null) {
            alert(CONFIG.feedback.noAnswer.multipleChoice);
            feedbackSection.classList.add('hidden'); // Hide if no answer selected
            if (feedbackSectionNew) {
                feedbackSectionNew.classList.add('hidden');
            }
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

            // Also add new class for new quiz wrapper
            const newOptions = document.querySelectorAll('.quiz-answers-wrapper .option');
            if (newOptions[selectedAnswer]) {
                newOptions[selectedAnswer].classList.add('is-correct');
            }

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
                // Old feedback for other subjects (keep for backward compatibility)
                feedbackSection.classList.add('correct');
                feedbackTitle.textContent = CONFIG.feedback.correct.title;
                feedbackMessage.textContent = CONFIG.feedback.correct.message;
                correctAnswerDisplay.classList.add('hidden');
                extraInfoDisplay.classList.add('hidden');
                verhoudingstabelContainer.innerHTML = '';
                strategyAndTips.classList.add('hidden');

                // NEW: Enhanced feedback component
                populateEnhancedFeedback(true, currentQuestion, null, correctIndex);
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

                // Also add new class for new quiz wrapper
                const newOptions = document.querySelectorAll('.quiz-answers-wrapper .option');
                if (newOptions[selectedAnswer]) {
                    newOptions[selectedAnswer].classList.add('is-incorrect');
                }

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

                // Also add new classes for new quiz wrapper
                const newOptions = document.querySelectorAll('.quiz-answers-wrapper .option');
                if (newOptions[selectedAnswer]) {
                    newOptions[selectedAnswer].classList.add('is-incorrect');
                }

                // Highlight correct answer if an incorrect one was selected
                if (options[correctIndex]) {
                    options[correctIndex].classList.add('correct');
                }

                // Also highlight correct in new wrapper
                if (newOptions[correctIndex]) {
                    newOptions[correctIndex].classList.add('is-correct');
                }
                // Old feedback for other subjects (keep for backward compatibility)
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
                strategyAndTips.classList.add('hidden');

                // NEW: Enhanced feedback component
                populateEnhancedFeedback(false, currentQuestion, selectedOption, correctIndex);
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
            if (feedbackSectionNew) {
                feedbackSectionNew.classList.add('hidden');
            }
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
            extraInfoDisplay.classList.add('hidden');
            verhoudingstabelContainer.innerHTML = '';
            strategyAndTips.classList.add('hidden');

            // NEW: Enhanced feedback component (for open-ended, no correct/incorrect index)
            populateEnhancedFeedback(true, currentQuestion, null, null);

            // Update category progress tracker
            updateCategoryProgress(currentQuestion.theme, true);
        } else {
            // Increment error count for this question
            currentQuestionErrors++;

            feedbackSection.classList.add('incorrect');
            feedbackTitle.textContent = CONFIG.feedback.incorrect.title;
            feedbackMessage.textContent = CONFIG.feedback.incorrect.messageWithTips;

            // NEW: Enhanced feedback component
            // Create a pseudo-option object for open-ended questions
            const pseudoOption = {
                text: currentQuestion.possible_answer,
                foutanalyse: `Het antwoord was: "${currentQuestion.possible_answer}". Probeer het nog een keer!`
            };
            populateEnhancedFeedback(false, currentQuestion, pseudoOption, null);

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

    // NEW: Handle text grouping mode differently
    if (useTextGrouping) {
        // Move to next question in current text
        currentQuestionInText++;

        // Save progress
        saveTextGroupProgress();

        // Load next question (will handle moving to next text if needed)
        loadCurrentQuestion();
        return;
    }

    // Traditional mode
    currentQuestionIndex++;

    // Update sessionStorage with current progress
    if (window.location.pathname.endsWith('quiz.html')) {
        const quizState = JSON.parse(sessionStorage.getItem('quizState') || '{}');
        quizState.currentQuestionIndex = currentQuestionIndex;
        quizState.score = score;
        quizState.wrongAnswers = wrongAnswers;
        quizState.lovaClickCount = lovaClickCount;
        quizState.categoryProgress = categoryProgress;
        sessionStorage.setItem('quizState', JSON.stringify(quizState));
    }

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

    // Calculate stats
    const percentage = totalQuestions > 0 ? Math.round((score / totalQuestions) * 100) : 0;
    const incorrectCount = wrongAnswers.length;
    const correctCount = score;

    // 1. HERO BLOCK: Emotional Summary
    populateHeroBlock(percentage, correctCount, incorrectCount, isNewHighscore);

    // 2. SKILLS OVERVIEW: Progress Chips
    populateSkillsOverview();

    // 3. QUESTION CARDS: Collapsible Accordion
    populateQuestionAccordion();
}

// Helper: Populate Hero Block with child-friendly messaging
function populateHeroBlock(percentage, correctCount, incorrectCount, isNewHighscore) {
    const emojiEl = document.getElementById('resultEmoji');
    const headlineEl = document.getElementById('resultHeadline');
    const summaryEl = document.getElementById('resultSummary');
    const growthBadgeEl = document.getElementById('resultGrowthBadge');
    const growthTextEl = document.getElementById('growthText');

    // Select emoji and headline based on performance
    let emoji, headline;
    if (percentage >= 90) {
        emoji = '🎉';
        headline = isNewHighscore ? 'Nieuw record! Fantastisch!' : 'Wauw! Geweldig gedaan!';
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

    // Summary text - always positive framing
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

    // Growth badge - celebrate learning points
    if (incorrectCount > 0) {
        growthBadgeEl.style.display = 'flex';
        const leerpunten = incorrectCount === 1 ? '1 leerpunt' : `${incorrectCount} leerpunten`;
        growthTextEl.textContent = `Je hebt ${leerpunten} verdiend!`;
    } else {
        growthBadgeEl.style.display = 'none';
    }
}

// Helper: Populate Skills Overview with category chips
function populateSkillsOverview() {
    const skillsChipsEl = document.getElementById('skillsChips');
    const skillsOverviewEl = document.getElementById('skillsOverview');

    // Only show if we have category data
    const categories = Object.keys(categoryProgress);
    if (categories.length === 0) {
        skillsOverviewEl.style.display = 'none';
        return;
    }

    skillsOverviewEl.style.display = 'block';
    skillsChipsEl.innerHTML = '';

    categories.forEach(category => {
        const data = categoryProgress[category];
        const total = data.correct + data.incorrect;
        const percentage = total > 0 ? Math.round((data.correct / total) * 100) : 0;

        // Create chip
        const chip = document.createElement('div');
        chip.className = 'skill-chip';

        // Determine status and icon
        let statusIcon, statusText, chipClass;
        if (percentage >= 80) {
            statusIcon = '⭐';
            statusText = 'Goed gedaan!';
            chipClass = 'skill-chip-excellent';
        } else if (percentage >= 50) {
            statusIcon = '👍';
            statusText = 'Lekker bezig!';
            chipClass = 'skill-chip-good';
        } else {
            statusIcon = '💡';
            statusText = 'Hier kun je nog sterker in worden';
            chipClass = 'skill-chip-growth';
        }

        chip.classList.add(chipClass);

        // Get theme icon (use default if not found)
        const themeIcons = {
            'optellen': '➕',
            'aftrekken': '➖',
            'vermenigvuldigen': '✖️',
            'delen': '➗',
            'breuken': '½',
            'procenten': '%',
            'meten': '📏',
            'tijd': '⏰',
            'geld': '💰',
            'basis-rekenen': '🔢',
            'omrekenen-eenheden': '⚖️',
            'kommagetallen': '0.0',
            'getallenlijn': '📊',
            'verhoudingstabellen': '📈'
        };

        const themeIcon = themeIcons[category.toLowerCase()] || '📚';

        chip.innerHTML = `
            <span class="skill-chip-icon">${themeIcon}</span>
            <span class="skill-chip-label">${category}</span>
            <span class="skill-chip-status">${statusIcon} ${statusText}</span>
        `;

        skillsChipsEl.appendChild(chip);
    });
}

// Helper: Populate Question Accordion with wrong answers
function populateQuestionAccordion() {
    const accordionEl = document.getElementById('questionAccordion');
    const reviewSectionEl = document.getElementById('questionReviewSection');

    // Only show if there are wrong answers
    if (wrongAnswers.length === 0) {
        reviewSectionEl.style.display = 'none';
        return;
    }

    reviewSectionEl.style.display = 'block';
    accordionEl.innerHTML = '';

    wrongAnswers.forEach((item, index) => {
        const accordionItem = document.createElement('div');
        accordionItem.className = 'accordion-item';

        // Status tag
        let statusTag = '💡 Hier kun je nog groeien';
        let statusClass = 'status-growth';

        const accordionHeader = document.createElement('div');
        accordionHeader.className = 'accordion-header';
        accordionHeader.innerHTML = `
            <span class="accordion-status ${statusClass}">${statusTag}</span>
            <span class="accordion-title">Vraag ${index + 1}</span>
            <span class="accordion-icon">▼</span>
        `;

        const accordionContent = document.createElement('div');
        accordionContent.className = 'accordion-content';
        accordionContent.style.display = 'none';

        // Build content HTML
        let contentHTML = '';

        // Story (if available)
        if (item.question.content && item.question.content.trim()) {
            contentHTML += `
                <div class="verhaaltje-box">
                    <div class="verhaaltje-label">📖 Verhaaltje</div>
                    <p>${item.question.content}</p>
                </div>
            `;
        }

        // Question
        contentHTML += `<div class="question-text-review"><strong>Vraag:</strong> ${item.question.question}</div>`;

        // Your answer vs Correct answer
        // wrongAnswers stores the actual text, not the index
        const userAnswer = item.userAnswer || 'Niet beantwoord';
        const correctAnswer = item.correctAnswer || 'Onbekend';

        contentHTML += `
            <div class="answer-comparison">
                <div class="answer-box answer-user">
                    <div class="answer-label">Jouw antwoord:</div>
                    <div class="answer-value">${userAnswer}</div>
                </div>
                <div class="answer-box answer-correct">
                    <div class="answer-label">Goede antwoord:</div>
                    <div class="answer-value">✓ ${correctAnswer}</div>
                </div>
            </div>
        `;

        // Explanation structure
        contentHTML += `<div class="explanation-section">`;

        // A) Waarom?
        if (item.question.extra_info && item.question.extra_info.concept) {
            contentHTML += `
                <div class="explanation-block">
                    <h4 class="explanation-heading">🧠 Waarom?</h4>
                    <p>${item.question.extra_info.concept}</p>
                </div>
            `;
        }

        // B) Zo werkt het (use strategy or worked example)
        if (item.question.extra_info && item.question.extra_info.strategy) {
            contentHTML += `
                <div class="explanation-block">
                    <h4 class="explanation-heading">➡️ Zo werkt het:</h4>
                    <p>${item.question.extra_info.strategy}</p>
                </div>
            `;
        }

        // C) Tip voor de volgende keer
        if (item.question.extra_info && item.question.extra_info.tips && item.question.extra_info.tips.length > 0) {
            contentHTML += `
                <div class="explanation-block">
                    <h4 class="explanation-heading">💡 Tip voor de volgende keer:</h4>
                    <p>${item.question.extra_info.tips[0]}</p>
                </div>
            `;
        }

        contentHTML += `</div>`; // Close explanation-section

        accordionContent.innerHTML = contentHTML;

        // Toggle functionality
        accordionHeader.onclick = function() {
            const isOpen = accordionContent.style.display === 'block';
            accordionContent.style.display = isOpen ? 'none' : 'block';
            accordionHeader.querySelector('.accordion-icon').textContent = isOpen ? '▼' : '▲';
            accordionItem.classList.toggle('active', !isOpen);
        };

        accordionItem.appendChild(accordionHeader);
        accordionItem.appendChild(accordionContent);
        accordionEl.appendChild(accordionItem);
    });
}

// Restart the current quiz with the same subject and theme
function restartQuiz() {
    // Reset quiz state
    currentQuestionIndex = 0;
    score = 0;
    hasAnswered = false;
    wrongAnswers = [];
    lovaClickCount = 0;
    currentQuestionErrors = 0;
    incorrectOptions.clear();

    // Re-initialize category progress
    initializeCategoryProgress(randomizedQuestions);

    // Hide results page, show quiz page
    document.getElementById('resultsPage').style.display = 'none';
    document.getElementById('quizPage').style.display = 'block';

    // Load first question
    loadCurrentQuestion();
}

function goToLanding() {
    // Clear auto-start flags to prevent unwanted auto-starting
    localStorage.removeItem('autoStartSubject');
    localStorage.removeItem('autoStartTheme');

    // If we're on quiz.html, redirect to index.html
    if (window.location.pathname.endsWith('quiz.html')) {
        sessionStorage.removeItem('quizState'); // Clear quiz state
        window.location.href = 'index.html';
        return;
    }

    // Otherwise, handle navigation on index.html
    if (document.getElementById('landingPage')) {
        document.getElementById('landingPage').style.display = 'block';
    }
    if (document.getElementById('levelPage')) {
        document.getElementById('levelPage').style.display = 'none';
    }
    if (document.getElementById('themePage')) {
        document.getElementById('themePage').style.display = 'none';
    }
    if (document.getElementById('quizPage')) {
        document.getElementById('quizPage').style.display = 'none';
    }
    if (document.getElementById('resultsPage')) {
        document.getElementById('resultsPage').style.display = 'none';
    }
    if (document.getElementById('reviewPage')) {
        document.getElementById('reviewPage').style.display = 'none';
    }

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
    if (typeof checkForPausedQuiz === 'function') {
        checkForPausedQuiz();
    }
}

// Pause quiz and save state
// Focus Mode - Hide distractions for better concentration
function toggleFocusMode() {
    const body = document.body;
    const focusButton = document.getElementById('focusModeToggle');
    const icon = focusButton.querySelector('i');

    body.classList.toggle('focus-mode');

    if (body.classList.contains('focus-mode')) {
        icon.textContent = 'visibility';
        focusButton.title = 'Exit Focus Modus';
    } else {
        icon.textContent = 'visibility_off';
        focusButton.title = 'Focus Modus';
    }
}

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

// Stop quiz early and show results
function stopQuiz() {
    console.log('Stop button clicked. wrongAnswers:', wrongAnswers.length, wrongAnswers);

    // Calculate the number of questions answered
    const questionsAnswered = currentQuestionIndex + (hasAnswered ? 1 : 0);

    // Set totalQuestions to the number of questions answered so far
    // This ensures the results page shows the correct score calculation
    totalQuestions = questionsAnswered;

    // Show the new results page
    showResults();
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

    if (lovaHelpPanelExpanded) {
        panel.classList.add('expanded');
        panel.classList.remove('hidden');

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
        { threshold: 25, message: '🎉 Yes! Je bent al een kwart! Knap hoor!' },
        { threshold: 50, message: '💪 Wow! Je bent al op de helft! Ga zo door!' },
        { threshold: 75, message: '🌟 Top! Nog een klein stukje en je hebt het! 🚀' },
        { threshold: 100, message: '🏆 Fantastisch! Je hebt alles gemaakt! Trots op jou!' }
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
    // Check if we're on quiz.html and need to restore state
    if (window.location.pathname.endsWith('quiz.html')) {
        const quizStateStr = sessionStorage.getItem('quizState');

        if (!quizStateStr) {
            alert('Geen quiz data gevonden. Je wordt teruggestuurd naar de homepagina.');
            window.location.href = 'index.html';
            return;
        }

        // Restore quiz state
        const quizState = JSON.parse(quizStateStr);
        currentSubject = quizState.currentSubject;
        currentTheme = quizState.currentTheme;
        currentQuiz = quizState.currentQuiz;
        randomizedQuestions = quizState.randomizedQuestions || [];
        totalQuestions = quizState.totalQuestions;
        currentQuestionIndex = quizState.currentQuestionIndex;
        score = quizState.score;
        wrongAnswers = quizState.wrongAnswers;
        lovaClickCount = quizState.lovaClickCount;
        categoryProgress = quizState.categoryProgress;
        hasAnswered = false;
        selectedAnswer = null;

        // NEW: Restore text grouping state if applicable
        useTextGrouping = quizState.useTextGrouping || false;
        if (useTextGrouping) {
            textGroups = quizState.textGroups || [];
            currentTextIndex = quizState.currentTextIndex || 0;
            currentQuestionInText = quizState.currentQuestionInText || 0;
            if (textGroups.length > currentTextIndex) {
                currentTextGroup = textGroups[currentTextIndex];
            }
        }

        // Set quiz title
        if (document.getElementById('quizTitle')) {
            document.getElementById('quizTitle').textContent = CONFIG.subjectTitles[quizState.subject] || 'Quiz';
        }

        // Update breadcrumb
        updateBreadcrumb(quizState.subject);

        // Show quiz page and load first question
        if (document.getElementById('quizPage')) {
            document.getElementById('quizPage').style.display = 'block';
        }
        if (document.getElementById('resultsPage')) {
            document.getElementById('resultsPage').style.display = 'none';
        }
        if (document.getElementById('reviewPage')) {
            document.getElementById('reviewPage').style.display = 'none';
        }

        // Load the current question
        loadCurrentQuestion();
        return;
    }

    // Regular index.html initialization
    // Check for paused quiz on page load
    checkForPausedQuiz();

    // Check if we should auto-start a subject (from level selector or theme selector page)
    const autoStartSubject = localStorage.getItem('autoStartSubject');
    const autoStartTheme = localStorage.getItem('autoStartTheme');

    if (autoStartSubject) {
        // Clear the flags
        localStorage.removeItem('autoStartSubject');
        localStorage.removeItem('autoStartTheme');

        // Load the subject data and start quiz directly (skip theme selection)
        setTimeout(async () => {
            const filename = getFilePath(autoStartSubject);
            const data = await loadJsonFile(filename);

            if (!data) {
                alert('Kon quiz data niet laden.');
                return;
            }

            // Store the data
            quizData[autoStartSubject] = data;
            currentSubject = autoStartSubject;

            // Check if we need to filter by theme
            if (autoStartTheme) {
                currentTheme = autoStartTheme;
                currentQuiz = data.filter(item => item.theme === autoStartTheme);
            } else {
                currentTheme = null; // No specific theme, use all questions
                currentQuiz = data;
            }

            // Start quiz directly
            startQuizWithData(autoStartSubject);
        }, 100);
    }
});

// Handle back button navigation - clear auto-start flags if user navigates back to index.html
window.addEventListener('pageshow', function(event) {
    // If page is restored from cache (back button)
    if (event.persisted || (window.performance && window.performance.navigation.type === 2)) {
        // Clear auto-start flags when arriving via back button
        if (!window.location.pathname.endsWith('quiz.html')) {
            localStorage.removeItem('autoStartSubject');
            localStorage.removeItem('autoStartTheme');
        }
    }
});
