# OefenPlatform - CITO Practice Platform

A comprehensive educational web application for Dutch primary school students (grades 3-8) to practice for CITO exams.

## Project Structure

```
/
├── index.html                  # Main landing page
├── quiz.html                   # Main quiz interface
├── level-selector.html         # Grade/level selection
├── theme-selector.html         # Theme selection
├── spelling-quiz.html          # Spelling quiz interface
├── spelling-dictee.html        # Spelling dictation interface
├── dmt-practice.html           # DMT word trainer
├── ouders.html                 # Parent/teacher info page
│
├── static/                     # Static assets
│   ├── css/                    # Production CSS (minified)
│   │   ├── styles.min.css
│   │   └── verhoudingstabel-widget.min.css
│   ├── js/                     # Production JavaScript (minified)
│   │   ├── config.min.js
│   │   ├── app.min.js
│   │   ├── accessibility.min.js
│   │   ├── foutanalyse-modaal.min.js
│   │   ├── verhoudingstabel-widget.min.js
│   │   ├── insight-generator.min.js
│   │   ├── card-morph-feedback.min.js
│   │   ├── dmt-practice.min.js
│   │   ├── spelling-quiz.min.js
│   │   └── spelling-dictee.min.js
│   └── src/                    # Source files (unminified)
│       ├── app.js
│       ├── config.js
│       ├── accessibility.js
│       ├── styles.css
│       └── ...
│
├── data/                       # Application data
│   ├── exercises/              # Exercise JSON files
│   │   ├── tl/                 # DMT (Drie Minuten Toets)
│   │   ├── gb/                 # Reading comprehension
│   │   ├── bl/                 # Reading strategies
│   │   ├── sp/                 # Spelling
│   │   ├── wo/                 # World orientation
│   │   └── ws/                 # Vocabulary
│   └── templates/              # Template JSON files
│       ├── verhaaltjessommen - Template.json
│       ├── basisvaardigheden - Template.json
│       ├── woordenschat - Template.json
│       ├── begrijpendlezen - Template.json
│       ├── wereldorientatie - Template.json
│       ├── brandaan - Template.json
│       └── samenvatten - Template.json
│
├── modules/                    # Feature modules
│   └── leesstrategieën/        # Reading strategies module
│       ├── leesstrategieën.html
│       └── *.json              # Module data files
│
├── docs/                       # Documentation
│   ├── ANALYSIS_*.md
│   ├── IMPLEMENTATIE_*.md
│   ├── INTEGRATIE_OVERZICHT.md
│   └── README.md
│
├── tools/                      # Utility scripts
│   └── *.py                    # Python maintenance/generation scripts
│
├── archive/                    # Archived/deprecated files
│   ├── deprecated-templates/
│   └── old-data/
│
├── flutter_verhoudingstabellen/ # Flutter widget (separate project)
│
├── package.json                # Node.js dependencies
├── package-lock.json
└── purgecss.config.js          # CSS optimization config
```

## Development

### Building Assets

Minify JavaScript:
```bash
npx terser static/src/[filename].js -c -m -o static/js/[filename].min.js
```

Minify CSS:
```bash
npx csso static/src/styles.css -o static/css/styles.min.css
```

### Adding New Exercises

1. Add JSON files to appropriate `data/exercises/` subdirectory
2. Update `static/src/config.js` with new exercise paths
3. Rebuild minified config: `npx terser static/src/config.js -c -m -o static/js/config.min.js`

### File Organization

- **Production files**: All HTML files reference minified assets from `static/css/` and `static/js/`
- **Source files**: Kept in `static/src/` for development and debugging
- **Data files**: Exercise and template JSON files in `data/`
- **Documentation**: All markdown docs in `docs/`
- **Utilities**: Python scripts for data generation/maintenance in `tools/`

## Features

- 10+ subject areas (math, reading, spelling, vocabulary, etc.)
- 5000+ practice questions
- Immediate feedback with explanations
- Progress tracking
- Accessibility features
- Mobile-responsive design
- Error analysis and insights

## Tech Stack

- Vanilla JavaScript (ES6+)
- CSS3 with responsive design
- JSON-based exercise storage
- No backend required (static site)
