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
        basisvaardigheden: 'Basisvaardigheden'
    },

    // Subject icons
    subjectIcons: {
        begrijpendlezen: '📖',
        brandaan: '🏛️',
        samenvatten: '✍️',
        wereldorientatie: '🌍',
        woordenschat: '📚',
        verhaaltjessommen: '🔢',
        basisvaardigheden: '🧮'
    },

    // Subject descriptions
    subjectDescriptions: {
        begrijpendlezen: 'Test je begrip van teksten en verhalen',
        brandaan: 'Ontdek de Nederlandse geschiedenis',
        samenvatten: 'Leer teksten kort en bondig samen te vatten',
        wereldorientatie: 'Algemene kennis over de wereld',
        woordenschat: 'Vergroot je vocabulaire',
        verhaaltjessommen: 'Reken mee met CITO-niveau verhaaltjes',
        basisvaardigheden: 'Oefen de rekenkundige basisvaardigheden'
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
            title: 'Niet correct!',
            messageDefault: 'Helaas, dat is niet helemaal correct.',
            messageWithTips: 'Helaas, dat is niet helemaal correct. Hier is een voorbeeld van een goed antwoord en wat tips:'
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
        single: 'Je had 1 vraag fout. Bestudeer deze goed om ervan te leren!',
        multiple: (count) => `Je had ${count} vragen fout. Bestudeer ze goed om ervan te leren!`
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
