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

    // Subject descriptions - Engaging and motivational
    subjectDescriptions: {
        begrijpendlezen: 'Word een échte leesmeester! 📖',
        brandaan: 'Reis terug in de tijd! ⏰✨',
        samenvatten: 'Leer teksten slim samen te vatten! 💡',
        wereldorientatie: 'Ontdek de grote wereld! 🌍',
        woordenschat: 'Leer gaaf nieuwe woorden! 📚',
        verhaaltjessommen: 'Los wiskundige puzzels op! 🧩',
        'verhaaltjessommen-emma': 'Reken mee met Emma! 🧒',
        'verhaaltjessommen-kate': 'Reken mee met Kate! 🎓',
        basisvaardigheden: 'Train je rekenskills! 🧮',
        'basisvaardigheden-emma': 'Word een rekenprof met Emma! (330 opgaven)',
        'basisvaardigheden-kate': 'Word een rekenprof met Kate! (240 opgaven)'
    },

    // File naming pattern
    templateFileSuffix: ' - Template.json',

    // Feedback messages - Warm, encouraging, child-friendly tone
    feedback: {
        correct: {
            title: 'Top gedaan! 🎉',
            message: 'Je bent goed bezig! Zo leer je steeds meer!'
        },
        incorrect: {
            title: 'Bijna! Probeer het nog eens 👀✨',
            messageDefault: 'Je komt er wel! Fouten maken hoort bij leren.',
            messageWithTips: 'Je leert elke vraag erbij! Hier is een voorbeeld en wat tips:'
        },
        noAnswer: {
            multipleChoice: 'Kies eerst een antwoord! 😊',
            openEnded: 'Vul eerst je antwoord in! ✍️'
        },
        noWrongAnswers: 'Fantastisch! Je hebt nog geen fouten gemaakt! 🌟 Ga zo door!'
    },

    // Score messages - Celebratory and motivational
    scoreMessages: {
        newHighscore: '🎉 NIEUWE HIGHSCORE! Ongelooflijk knap! ',
        excellent: '🏆 Wauw! Dit heb je écht verdiend! Je bent een ster!',
        good: '👏 Super gedaan! Je bent op de goede weg!',
        fair: '👍 Goed bezig! Blijf oefenen en je wordt nóg beter!',
        needsPractice: '💪 Niet opgeven! Elke keer word je een beetje beter!'
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
