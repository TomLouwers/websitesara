// Configuration file for Sara's Quiz Website

const CONFIG = {
    // Data loading configuration
    jsonPath: './',

    // Subject titles mapping
    subjectTitles: {
        begrijpendlezen: 'Begrijpend Lezen',
        brandaan: 'Geschiedenis',
        samenvatten: 'Samenvatten',
        wereldorientatie: 'Wereldoriëntatie',
        woordenschat: 'Woordenschat',
        verhaaltjessommen: 'Verhaaltjessommen',
        'verhaaltjessommen-emma': 'Verhaaltjessommen Emma',
        'verhaaltjessommen-kate': 'Verhaaltjessommen Kate',
        basisvaardigheden: 'Basisvaardigheden',
        'basisvaardigheden-emma': 'Basisvaardigheden Emma',
        'basisvaardigheden-kate': 'Basisvaardigheden Kate'
    },

    // Subject icons
    subjectIcons: {
        begrijpendlezen: '📖',
        brandaan: '🏛️',
        samenvatten: '✍️',
        wereldorientatie: '🌍',
        woordenschat: '📚',
        verhaaltjessommen: '🔢',
        'verhaaltjessommen-emma': '🧒',
        'verhaaltjessommen-kate': '🎓',
        basisvaardigheden: '🧮',
        'basisvaardigheden-emma': '🧒',
        'basisvaardigheden-kate': '🎓'
    },

    // Subject descriptions
    subjectDescriptions: {
        begrijpendlezen: 'Test je begrip van teksten en verhalen',
        brandaan: 'Ontdek de Nederlandse geschiedenis',
        samenvatten: 'Leer teksten kort en bondig samen te vatten',
        wereldorientatie: 'Algemene kennis over de wereld',
        woordenschat: 'Vergroot je vocabulaire',
        verhaaltjessommen: 'Reken mee met CITO-niveau verhaaltjes',
        'verhaaltjessommen-emma': 'M4 verhaaltjessommen voor Groep 4',
        'verhaaltjessommen-kate': 'M5 verhaaltjessommen voor Groep 5',
        basisvaardigheden: 'Oefen de rekenkundige basisvaardigheden',
        'basisvaardigheden-emma': 'M4 basisvaardigheden voor Groep 4 (330 opgaven)',
        'basisvaardigheden-kate': 'M5 basisvaardigheden voor Groep 5 (240 opgaven)'
    },

    // File naming pattern
    templateFileSuffix: ' - Template.json',

    // Feedback messages
    feedback: {
        correct: {
            title: 'Correct!',
            message: 'Dat is helemaal juist!'
        },
        incorrect: {
            title: 'Bijna goed! 💪',
            messageDefault: 'Je bent op de goede weg! Fouten helpen je leren.',
            messageWithTips: 'Je bent op de goede weg! Hier is een voorbeeld van een goed antwoord en wat tips:'
        },
        noAnswer: {
            multipleChoice: 'Selecteer eerst een antwoord!',
            openEnded: 'Vul eerst een antwoord in!'
        },
        noWrongAnswers: 'Geweldig! Je hebt nog geen fouten gemaakt. Ga door met oefenen!'
    },

    // Score messages
    scoreMessages: {
        newHighscore: '🎉 NIEUWE HIGHSCORE! ',
        excellent: '🏆 Uitstekend! Je bent een echte expert!',
        good: '👏 Goed gedaan! Je hebt het goed onder de knie!',
        fair: '👍 Niet slecht! Met wat oefening wordt het nog beter!',
        needsPractice: '💪 Blijf oefenen, je kunt het!'
    },

    // Score thresholds (percentages)
    scoreThresholds: {
        excellent: 90,
        good: 70,
        fair: 50
    },

    // Mobile breakpoint
    mobileBreakpoint: 768,

    // LocalStorage keys
    storageKeys: {
        userName: 'userName',
        highscorePrefix: 'highscore_'
    },

    // Default values
    defaults: {
        userName: 'Speler',
        userPrompt: 'Wat is je naam?'
    },

    // Review page messages
    reviewMessages: {
        single: 'Je hebt 1 leerpunt om mee aan de slag te gaan! Fouten helpen je groeien! 💪',
        multiple: (count) => `Je hebt ${count} leerpunten om mee aan de slag te gaan! Fouten helpen je groeien! 💪`
    },

    // L.O.V.A. configuration
    lova: {
        panelTransitionDuration: 400 // milliseconds
    }
};

// Make CONFIG available globally
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
