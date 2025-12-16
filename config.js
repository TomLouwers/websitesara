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
        basisvaardigheden: 'Getal & Bewerking',
        'basisvaardigheden-emma': 'Getal & Bewerking Emma',
        'basisvaardigheden-kate': 'Getal & Bewerking Kate',
        spelling: 'Spelling',
        dmt: 'DMT Woordtrainer'
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
        'basisvaardigheden-kate': '🎓',
        spelling: '✏️',
        dmt: '⚡'
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
        'basisvaardigheden-kate': 'Word een rekenprof met Kate! (240 opgaven)',
        spelling: 'Leer correct spellen! ✏️',
        dmt: 'Word een snellere lezer! ⚡'
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
    },

    // File path mapping for subjects with groep/level structure
    subjectFilePaths: {
        begrijpendlezen: {
            groep3: {
                m3: 'exercises/bl/bl_groep3_m3_1.json',
                e3: 'exercises/bl/bl_groep3_e3_1.json'
            },
            groep4: {
                m4: 'exercises/bl/bl_groep4_m4_1.json',
                e4: 'exercises/bl/bl_groep4_e4_1.json'
            },
            groep5: {
                m5: 'exercises/bl/bl_groep5_m5_1.json',
                e5: 'exercises/bl/bl_groep5_e5_1.json'
            },
            groep6: {
                m6: 'exercises/bl/bl_groep6_m6_1.json',
                e6: 'exercises/bl/bl_groep6_e6_1.json'
            },
            groep7: {
                m7: 'exercises/bl/bl_groep7_m7_1.json',
                e7: 'exercises/bl/bl_groep7_e7_1.json'
            },
            groep8: {
                m8: 'exercises/bl/bl_groep8_m8_1.json',
                e8: 'exercises/bl/bl_groep8_e8_1.json'
            }
        },
        basisvaardigheden: {
            groep3: {
                m3: 'exercises/gb/gb_groep3_m3.json',
                e3: 'exercises/gb/gb_groep3_e3.json'
            },
            groep4: {
                m4: 'exercises/gb/gb_groep4_m4.json',
                e4: 'exercises/gb/gb_groep4_e4.json'
            },
            groep5: {
                m5: 'exercises/gb/gb_groep5_m5.json',
                e5: 'exercises/gb/gb_groep5_e5.json'
            },
            groep6: {
                m6: 'exercises/gb/gb_groep6_m6.json',
                e6: 'exercises/gb/gb_groep6_e6.json'
            },
            groep7: {
                m7: 'exercises/gb/gb_groep7_m7.json',
                e7: 'exercises/gb/gb_groep7_e7.json'
            },
            groep8: {
                m8: 'exercises/gb/gb_groep8_e8.json',
                e8: 'exercises/gb/gb_groep8_e8.json'
            }
        }
    }
};

// Make CONFIG available globally
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
