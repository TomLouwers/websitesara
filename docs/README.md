# Sara's Quiz Website - Refactoring Documentation

## Overview

Sara's Quiz Website is an educational quiz platform designed for Dutch elementary school students, primarily for CITO exam preparation. The platform provides interactive quizzes across 7 different subjects with progress tracking and highscore management.

## Recent Refactoring (2025)

The codebase has been significantly refactored from a monolithic single-file application to a modular, maintainable structure.

### What Changed

#### Before Refactoring
- **Single monolithic file**: `index.html` (2,149 lines)
  - 937 lines of embedded CSS
  - ~1,000 lines of embedded JavaScript
  - Poor separation of concerns
  - Difficult to maintain and test

#### After Refactoring
- **Modular structure**:
  - `index.html` (228 lines) - Clean HTML structure
  - `styles.css` (871 lines) - All styling separated
  - `app.js` (973 lines) - Application logic
  - `config.js` (81 lines) - Configuration and constants

### Benefits of Refactoring

1. **Separation of Concerns**: HTML, CSS, and JavaScript are now in separate files
2. **Maintainability**: Easier to find and modify specific functionality
3. **Configuration Management**: All constants centralized in `config.js`
4. **Code Reusability**: Shared configuration can be reused across modules
5. **Better Developer Experience**: Clearer code structure and organization
6. **Performance**: Browser can cache CSS and JS files separately
7. **Scalability**: Easier to add new features and modules

### File Structure

```
websitesara/
├── index.html                          # Main HTML (228 lines)
├── styles.css                          # All CSS styles (871 lines)
├── app.js                              # Application logic (973 lines)
├── config.js                           # Configuration constants (81 lines)
├── *.json                              # Quiz data files (7 subjects)
│   ├── basisvaardigheden - Template.json
│   ├── begrijpendlezen - Template.json
│   ├── brandaan - Template.json
│   ├── samenvatten - Template.json
│   ├── verhaaltjessommen - Template.json
│   ├── wereldorientatie - Template.json
│   └── woordenschat - Template.json
├── modules/
│   └── leesstrategieën/               # Reading strategies module
│       ├── leesstrategieën.html
│       ├── leesstrategieën.json
│       └── img/
└── *.py                                # Python maintenance scripts (9 files)
```

## Configuration (config.js)

All configuration is centralized in `config.js`:

### Subject Titles and Metadata
```javascript
CONFIG.subjectTitles = {
    begrijpendlezen: 'Begrijpend Lezen',
    brandaan: 'Geschiedenis',
    // ... other subjects
}
```

### Feedback Messages
```javascript
CONFIG.feedback = {
    correct: { title: 'Correct!', message: '...' },
    incorrect: { title: 'Niet correct!', message: '...' }
}
```

### Score Thresholds
```javascript
CONFIG.scoreThresholds = {
    excellent: 90,  // >= 90%
    good: 70,       // >= 70%
    fair: 50        // >= 50%
}
```

## Features

### 7 Subject Areas
1. **Begrijpend Lezen** (Reading Comprehension) - 4 questions
2. **Geschiedenis** (History - Brandaan) - 50 questions
3. **Samenvatten** (Summarizing) - 80 questions
4. **Wereldoriëntatie** (World Orientation) - 649 questions
5. **Woordenschat** (Vocabulary) - 268 questions
6. **Verhaaltjessommen** (Word Problems) - 375 questions
7. **Getal & Bewerking** (Number & Operations) - 203 questions

**Total**: 1,629 quiz questions

### Question Types
- **Multiple Choice**: Select from options with error analysis
- **Open-Ended**: Text input with example answers
- **L.O.V.A. Support**: Step-by-step problem-solving guidance for word problems

### Progress Tracking
- Category-based progress tracking
- Correct/incorrect answer counters
- Theme-specific highscores
- Overall highscores per subject

### Educational Features
- **L.O.V.A. Method**: Structured problem-solving for math word problems
  - Stap 1: Lezen (Reading)
  - Stap 2: Ordenen (Organizing)
  - Stap 3: Vormen (Formulating)
  - Stap 4: Antwoorden (Answering)
- **Error Analysis**: Specific feedback for common mistakes
- **Extra Info**: Contextual explanations and tips
- **Review Mode**: Study wrong answers after quiz completion

### Accessibility Features
- **Dyslexia-friendly font**: Lexend typeface
- **Neuroscience-optimized colors**: Reduced cognitive load
- **WCAG AAA compliance**: High contrast ratios
- **Mobile-responsive**: Optimized for tablets and phones
- **Clear visual hierarchy**: Consistent spacing and sizing

## Technology Stack

- **Frontend**: Pure HTML5/CSS3/Vanilla JavaScript (no frameworks)
- **Styling**: CSS Custom Properties (CSS Variables)
- **Data**: JSON files for quiz content
- **Storage**: localStorage for user state and highscores
- **Maintenance**: Python 3 scripts for data quality

## Development

### Adding New Questions

Questions are stored in JSON files following this structure:

```json
{
  "id": 1,
  "title": "Problem title",
  "theme": "category",
  "content": "Context text",
  "questions": [{
    "question": "Question text?",
    "options": ["A", "B", "C", "D"],
    "correct": 0,
    "extra_info": {
      "concept": "Explanation",
      "berekening": ["Step 1", "Step 2"]
    }
  }]
}
```

### Data Maintenance Scripts

- `add_new_tips.py` - Adds educational tips
- `add_remaining_tips.py` - Fills missing tip sections
- `check_missing_tips.py` - Validates data completeness
- `fix_cito_conformity.py` - Ensures CITO exam standards
- `fix_currency.py` - Standardizes currency formatting
- `fix_final_issues.py` - General bug fixes
- `fix_remaining_duplicates.py` - Removes duplicates
- `improve_template.py` - Enhances question quality
- `restore_extra_info.py` - Restores educational metadata

### Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Requires JavaScript enabled
- Requires localStorage support

## Future Improvements

### Recommended Next Steps

1. **Modularize JavaScript Further**
   - Separate state management
   - Extract UI rendering functions
   - Create quiz logic module

2. **Add Error Handling**
   - Validation layer for JSON data
   - Better error messages
   - Fallback for localStorage failures

3. **Testing**
   - Unit tests for core functions
   - Integration tests for quiz flow
   - E2E tests with Playwright

4. **Build Process**
   - Implement bundler (Vite/Webpack)
   - Code minification
   - CSS autoprefixer

5. **Progressive Web App**
   - Service worker for offline support
   - App manifest
   - Install prompts

6. **Shared Module Assets**
   - Extract common styles to shared CSS
   - Share JavaScript utilities
   - Centralize configuration

## Credits

- **Design**: Neuroscience-optimized color palette for enhanced focus
- **Font**: Lexend (dyslexia-friendly typeface)
- **Icons**: Material Icons by Google
- **Educational Method**: L.O.V.A. problem-solving framework

## License

Educational use for Dutch elementary school students.

---

**Refactored by**: Claude (Anthropic)
**Date**: November 2025
**Lines of Code Reduction**: 2,149 → 228 lines in main HTML file (89% reduction)
