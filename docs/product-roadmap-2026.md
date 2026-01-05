# Product Roadmap 2026: OefenPlatform Quality & Scale Initiative

**Last Updated:** 2026-01-05
**Document Owner:** Product Management
**Status:** Active Planning

## Executive Summary

**Architecture:** Static website (vanilla JS, no backend, localStorage only)
**AI Strategy:** Offline content generation (Python scripts + AI agents)
**Strategic Focus:** Exercise quality, exercise quantity, feedback richness
**Target:** 500+ exercises with 85% feedback quality by Q3 2026

---

## 🎯 THEME 1: OFFLINE AI-POWERED CONTENT GENERATION

### Epic 1.1: AI-Assisted Exercise Generation Workflow

#### US-1.1.1: AI Bulk Exercise Generator
**As a content manager, I want an AI agent that generates exercises from CSV prompt templates, so I can produce 100+ exercises per day**

**Priority:** 🔴 Critical | **Effort:** 8 story points

**Acceptance Criteria:**
- [ ] Python script: `scripts/ai-bulk-generator.py`
- [ ] Reads prompt templates from `docs/reference/*.csv`
- [ ] Uses Claude/GPT API with structured output (JSON schema)
- [ ] Generates exercises matching v2.0.0 schema (core + support)
- [ ] Output: Draft exercises to `data-v2-draft/exercises/[category]/`
- [ ] Batch processing: Generate 50 exercises per API call
- [ ] Cost estimation per batch
- [ ] Automatic SLO/CITO alignment

**Technical Implementation:**
```bash
python scripts/ai-bulk-generator.py \
  --csv docs/reference/rekenen-getallen.csv \
  --grade 4 \
  --count 100 \
  --output data-v2-draft/exercises/gb/
```

---

#### US-1.1.2: Rich Support Data Generation
**As a content reviewer, I want AI-generated exercises to include rich support data, so quality is high from the start**

**Priority:** 🔴 Critical | **Effort:** 5 story points

**Acceptance Criteria:**
- [ ] AI prompt includes support file requirements
- [ ] Each item includes: 2-3 progressive hints, per-option feedback, learning strategies, common errors
- [ ] Support file quality score ≥70% on generation
- [ ] Use existing high-quality examples as few-shot prompts

---

#### US-1.1.3: Human Review Workflow
**As a content manager, I want a review interface for AI-generated exercises, so I can approve/edit before publishing**

**Priority:** 🟡 High | **Effort:** 8 story points

**Acceptance Criteria:**
- [ ] Review tool: `tools/review-exercises.html`
- [ ] Side-by-side preview and editor
- [ ] Actions: Approve, Edit, Reject, Flag
- [ ] Approved exercises move from draft to production
- [ ] Keyboard shortcuts (A/E/R)

---

### Epic 1.2: Quality Validation & Enhancement

#### US-1.2.1: Automated Quality Checks
**As a quality manager, I want automated quality checks on all exercises, so I catch errors before students see them**

**Priority:** 🔴 Critical | **Effort:** 13 story points

**Quality Dimensions:**
- Mathematical correctness (AI verification)
- Age-appropriate vocabulary (Flesch-Douma score)
- Spelling/grammar (LanguageTool NL)
- Distractor plausibility
- Hint-answer alignment
- Cultural sensitivity

**Thresholds:**
- Math correctness: 100%
- Readability Groep 3: 80+
- Readability Groep 8: 60+
- Spelling errors: 0
- Hint quality: ≥70%

---

#### US-1.2.2: Enrich Existing Exercises
**As a content editor, I want to enrich legacy exercises with better feedback, so old content matches new standards**

**Priority:** 🟡 High | **Effort:** 8 story points

**Acceptance Criteria:**
- [ ] Script: `scripts/enrich-existing-exercises.py`
- [ ] Generate missing hints, per-option feedback, strategies, common errors
- [ ] Preserve existing good content
- [ ] Batch processing with human review
- [ ] Backup originals to `data-v2-backup/`

---

#### US-1.2.3: Granular Learning Objectives
**As a curriculum specialist, I want exercises tagged with specific sub-skills, so teachers can find exactly what they need**

**Priority:** 🟢 Medium | **Effort:** 8 story points

**Enhanced Metadata:**
```json
"slo_alignment": {
  "kerndoelen": ["K28"],
  "rekendomeinen": ["verhoudingen"],
  "referentieniveau": "1F",
  "cognitive_level": "toepassen",
  "sub_skills": ["breuken-optellen", "breuken-vereenvoudigen"],
  "prerequisites": ["breuken-herkennen"],
  "related": ["procenten-berekenen"]
}
```

---

## 💬 THEME 2: DRAMATICALLY BETTER FEEDBACK

### Epic 2.1: Multi-Layered Feedback System

#### US-2.1.1: Per-Option Feedback
**As a student, I want specific feedback for each wrong answer, so I understand my exact mistake**

**Priority:** 🔴 Critical | **Effort:** 13 story points

**Target:** 100% of exercises have per-option feedback (currently ~5%)

**Feedback Patterns:**
- **Reading:** "Je dacht aan X, maar de vraag vroeg naar Y"
- **Math:** "Je gebruikte X bewerking, maar het moet Y zijn"
- **Spelling:** "Deze spelling geldt voor X-woorden, maar dit is een Y-woord"

**Frontend Change:** `static/src/insight-generator.js`

---

#### US-2.1.2: Progressive 3-Level Hints
**As a struggling student, I want hints that get more specific each time, so I'm not stuck**

**Priority:** 🔴 Critical | **Effort:** 8 story points

**Hint Structure:**
- **Level 1 (Strategy):** "Welke strategie kun je gebruiken?"
- **Level 2 (Focus):** "Kijk naar alinea 2, zoek naar 'omdat'"
- **Level 3 (Near-solution):** "Het antwoord staat in de laatste zin van alinea 2"

**Point Costs:** 0, 1, 2

**Frontend:** Modify `static/src/app.js` hint system

---

#### US-2.1.3: Worked Examples
**As a student, I want step-by-step solutions after getting wrong answers, so I learn the method**

**Priority:** 🟡 High | **Effort:** 13 story points

**Example Structure:**
```json
"worked_example": {
  "type": "step_by_step",
  "steps": [
    {"number": 1, "action": "Lees de vraag", "visual": "highlight-question"},
    {"number": 2, "action": "Zoek in de tekst", "visual": "highlight-text:alinea2"},
    {"number": 3, "action": "Lees de zin", "visual": "highlight-answer"}
  ],
  "conclusion": "Het antwoord is: om brood te kopen"
}
```

**New File:** `static/src/worked-example-modal.js`

---

### Epic 2.2: Subject-Specific Feedback Intelligence

#### US-2.2.1: Reading Strategy Feedback
**As a reading student, I want feedback that teaches reading strategies, not just answers**

**Priority:** 🟡 High | **Effort:** 8 story points

**12 Core Reading Strategies:**
- Voorkennis activeren
- Signaalwoorden zoeken
- Hoofdgedachte bepalen
- Verbanden leggen
- Letterlijk vs. figuurlijk
- Structuurwoorden herkennen

**Feedback:** "Je gebruikte 'letterlijk lezen', maar hier moet je 'tussen de regels lezen'"

**Results:** Show most-used strategy in session summary

---

#### US-2.2.2: LOVA Math Feedback
**As a math student, I want feedback that identifies which problem-solving step I missed, so I know what to practice**

**Priority:** 🟡 High | **Effort:** 8 story points

**LOVA Steps:**
- **L**ezen (reading/comprehension)
- **O**rdenen (organizing information)
- **V**ormen (forming calculation)
- **A**ntwoorden (calculation/answer)

**Feedback:** "Je maakte een fout bij de O-stap (ordenen). Je gebruikte de verkeerde getallen."

**Files:** `static/src/foutanalyse-modaal.js`, `gb/*_support.json`

---

## 📚 THEME 3: MASSIVE CONTENT EXPANSION

### Epic 3.1: Fill Curriculum Gaps

#### US-3.1.1: 500+ Exercise Target
**As a curriculum manager, I want complete SLO coverage, so students can practice any topic**

**Priority:** 🔴 Critical | **Effort:** 21 story points

**Content Targets:**
- Begrijpend Lezen: 100 exercises (currently ~20)
- Getallenbegrip: 150 exercises (currently ~25)
- Spelling: 120 exercises (currently ~15)
- Woordenschat: 80 exercises (currently ~5)
- Wereldoriëntatie: 100 exercises (currently ~6)
- Verhaaltjessommen: 50 exercises

**Workflow:**
1. Gap analysis: `python scripts/analyze-curriculum-coverage.py`
2. Generate: `python scripts/ai-bulk-generator.py --fill-gaps`
3. Review batch
4. Publish approved

---

#### US-3.1.2: Context Variety
**As a student, I want exercises with varied contexts, so content stays interesting**

**Priority:** 🟢 Medium | **Effort:** 5 story points

**Context Examples (Fractions):**
- Pizza delen (food)
- Voetbalteam verdelen (sports)
- Planten water geven (nature)
- Game levels (technology)
- Klasgenoten groepjes (school)

**Diversity:** Names, locations, activities, family structures

---

#### US-3.1.3: CITO-Style Practice
**As a teacher, I want CITO-format exercises, so students are prepared for standardized tests**

**Priority:** 🟡 High | **Effort:** 13 story points

**Requirements:**
- CITO question patterns (multi-step, tables/graphs, context-rich)
- Difficulty calibrated to 1F, 1S, 2F levels
- Metadata: `cito_relevant: true`
- 50 CITO-style exercises per subject (Groep 8 focus)

---

### Epic 3.2: Exercise Presentation Improvements

#### US-3.2.1: Math Notation (KaTeX)
**As a math student, I want properly formatted math notation, so problems are clear**

**Priority:** 🟡 High | **Effort:** 5 story points

**Implementation:**
- Integrate KaTeX (lightweight, static-compatible)
- Support LaTeX: `$\frac{3}{4} + \frac{1}{2}$`
- Auto-convert legacy plain text
- Symbols: ×, ÷, √, ², ³, fractions

**Quick Win:** Can implement this week

---

#### US-3.2.2: Images & Diagrams
**As a visual learner, I want images in exercises, so I can see the problem**

**Priority:** 🟢 Medium | **Effort:** 8 story points

**Schema Extension:**
```json
"question": {
  "text": "Hoeveel graden is deze hoek?",
  "image": {
    "src": "/static/assets/exercises/mk/groep6_hoek_45.png",
    "alt": "Een driehoek met één hoek gemarkeerd",
    "position": "above"
  }
}
```

**Storage:** `static/assets/exercises/[category]/`

---

#### US-3.2.3: Text Highlighting Tools
**As a reading student, I want to highlight text while reading, so I can mark important information**

**Priority:** 🟢 Medium | **Effort:** 8 story points

**Features:**
- Click to highlight (4 colors)
- Saves in sessionStorage
- "Show highlights" toggle
- Mobile: Long-press
- Works with text-to-speech

**New File:** `static/src/text-highlighter.js`

---

## 🎨 THEME 4: UI/UX ENHANCEMENTS

### Epic 4.1: Better Visual Feedback

#### US-4.1.1: Celebratory Animations
**As a student, I want milestone animations, so achievements feel rewarding**

**Priority:** 🟢 Medium | **Effort:** 5 story points

**Enhanced Animations:**
- First correct: Gentle sparkle
- 5-streak: Star burst
- 10-streak: Confetti + sound
- New high score: Trophy animation
- Exercise completion: Progress ring fill

**CSS-only, respects `prefers-reduced-motion`**

---

#### US-4.1.2: Question Type Visual Indicators
**As a student, I want visual distinction between question types, so I know what's expected**

**Priority:** 🟢 Medium | **Effort:** 3 story points

**Indicators:**
- 📖 Reading: Book icon, blue accent
- 🔢 Math: Calculator icon, orange accent
- ✏️ Spelling: Pencil icon, purple accent
- 🌍 Science: Globe icon, green accent

**Quick Win:** CSS + icons only

---

### Epic 4.2: Session Gamification Enhancements

#### US-4.2.1: Session Progress Visualization
**As a student, I want to see my progress visually, so I feel motivated**

**Priority:** 🟢 Medium | **Effort:** 5 story points

**Features:**
- Progress wheel (% complete)
- Mini achievements: "Halfway!", "Almost done!"
- Session summary: Time, accuracy, strategies used
- "Play again?" prompt

---

#### US-4.2.2: localStorage Personalization
**As a returning student, I want my preferences saved, so the experience feels personalized**

**Priority:** 🟢 Medium | **Effort:** 5 story points

**Save to localStorage:**
- Last played subjects
- Total lifetime questions answered
- Favorite subject
- Accessibility preferences (already done)
- Suggested next exercise

**Landing Page:**
- "Welcome back! Last time: Begrijpend Lezen"
- "You've answered 127 questions total 🎯"

---

#### US-4.2.3: Advanced Power-Ups (Groep 6-8)
**As an older student, I want strategic power-ups, so gameplay is more engaging**

**Priority:** 🟢 Medium | **Effort:** 8 story points

**Power-Ups:**
- 🛡️ Shield (existing): Protect streak
- ⏭️ Skip: Skip 1 hard question (earn at 10 correct)
- 💡 Free Hint: No point cost (earn at 3-streak)
- 🎯 50-50: Eliminate 2 wrong answers (earn at 7 correct)

**Age-gated:** Groep 6-8 only

---

## 🛠️ THEME 5: DEVELOPER TOOLS

### Epic 5.1: Content Creation Tools

#### US-5.1.1: Visual Exercise Editor
**As a content creator, I want a GUI editor, so I don't edit JSON manually**

**Priority:** 🟡 High | **Effort:** 13 story points

**Tool:** `tools/exercise-editor.html`

**Features:**
- Form-based editor (question, options, hints, feedback, metadata)
- Live preview pane
- Export/import JSON
- Validation before export
- Templates for common types

---

#### US-5.1.2: Comprehensive Test Suite
**As a developer, I want automated validation, so we catch bugs early**

**Priority:** 🔴 Critical | **Effort:** 8 story points

**Tests:**
- Schema validation
- Answer key correctness
- Hint quality (no duplicates, no empty)
- Feedback presence
- File naming convention
- JSON syntax

**Output:** HTML report with pass/fail

**Command:**
```bash
python scripts/comprehensive_check.py --all --report validation-report.html
```

---

#### US-5.1.3: Usage Analytics (localStorage)
**As a content manager, I want to see which exercises students complete, so I know what needs improvement**

**Priority:** 🔵 Low | **Effort:** 5 story points

**Track:**
- Completion count per exercise
- Average accuracy per exercise
- Average time spent
- Hint usage rate

**Tool:** `tools/analytics.html` (reads localStorage, export CSV)

**Note:** Single-device data only, useful for testing

---

## 📊 IMPLEMENTATION ROADMAP

### Phase 1: Content Foundation (Months 1-2)
**Goal:** 3x quantity, 10x feedback quality

| User Story | Effort | Outcome |
|------------|--------|---------|
| US-1.1.1: AI Bulk Generator | 8 | Generate 100+ exercises/day |
| US-1.1.2: Rich Support Generation | 5 | AI creates hints+feedback |
| US-2.1.1: Per-Option Feedback | 13 | All exercises have specific error feedback |
| US-2.1.2: Progressive Hints | 8 | 3-level scaffolded support |
| US-1.2.1: Quality Validation | 13 | Automated quality gates |
| US-5.1.2: Test Suite | 8 | Prevent bad exercises shipping |

**Total:** 55 story points

**Deliverables:**
- AI generation pipeline operational
- 200+ new exercises published
- Feedback quality: 70%+ (from 7%)
- Quality validation automated

---

### Phase 2: Content Expansion (Months 3-4)
**Goal:** Complete curriculum coverage, visual enhancements

| User Story | Effort | Outcome |
|------------|--------|---------|
| US-3.1.1: Fill Curriculum Gaps | 21 | 500+ total exercises |
| US-3.1.3: CITO-Style Exercises | 13 | Test prep exercises |
| US-1.2.2: Enrich Legacy Content | 8 | Old = new quality |
| US-3.2.1: KaTeX Math Notation | 5 | Professional formatting |
| US-5.1.1: Visual Editor | 13 | Non-technical content creation |
| US-1.1.3: Review Workflow | 8 | Quality control process |

**Total:** 68 story points

**Deliverables:**
- 500+ exercises (all major SLO objectives)
- Legacy content upgraded
- Math beautifully formatted
- Content workflow streamlined

---

### Phase 3: UX Polish & Advanced Feedback (Months 5-6)
**Goal:** Best-in-class UX, intelligent feedback

| User Story | Effort | Outcome |
|------------|--------|---------|
| US-2.1.3: Worked Examples | 13 | Step-by-step solutions |
| US-2.2.1: Reading Strategies | 8 | Teach strategies |
| US-2.2.2: LOVA Math Feedback | 8 | Identify problem-solving step |
| US-3.2.2: Images & Diagrams | 8 | Visual content |
| US-3.2.3: Text Highlighting | 8 | Active reading tools |
| US-4.1.1: Milestone Animations | 5 | Rewarding achievements |
| US-4.2.2: localStorage Personalization | 5 | Remember preferences |

**Total:** 55 story points

**Deliverables:**
- Industry-leading feedback intelligence
- Visual learning supports
- Polished, delightful UX

---

## 🎯 SUCCESS METRICS

### Content Quality & Quantity
| Metric | Current | 3 Months | 6 Months |
|--------|---------|----------|----------|
| Total Exercises | 74 | 300 | 500+ |
| Avg Feedback Quality | 7% | 70% | 85% |
| 3-Level Hints | ~5% | 80% | 100% |
| Per-Option Feedback | ~5% | 60% | 100% |
| Worked Examples | 0% | 20% | 40% |
| SLO Coverage | ~30% | 70% | 95% |

### User Engagement (localStorage)
| Metric | Target 3mo | Target 6mo |
|--------|------------|------------|
| Avg Session Duration | 10 min | 15 min |
| Exercises per Session | 8 | 12 |
| Hint Usage Rate | 30% | 25% |
| Retry After Incorrect | N/A | 40% |

### Technical Quality
| Metric | Current | Target |
|--------|---------|--------|
| Schema Validation | ~80% | 100% |
| Accessibility Score | 95 | 100 |
| Performance Score | 90 | 95 |
| Math Notation Support | 0% | 100% |

---

## 🚀 QUICK WINS (Start This Week)

1. **KaTeX Math Notation** (5pts, 1 week) - Immediate visual improvement
2. **Question Type Icons** (3pts, 3 days) - Better UX clarity
3. **Expand Test Suite** (8pts, 1 week) - Prevent quality regression
4. **Enrich 10 Legacy Exercises** (3pts, 3 days) - Prove AI workflow

---

## 💡 AI GENERATION WORKFLOW

### Option A: Semi-Automated Scripts
```bash
# 1. Generate drafts
python scripts/ai-bulk-generator.py --csv docs/reference/rekenen-getallen.csv --count 50

# 2. Validate
python scripts/comprehensive_check.py --directory data-v2-draft/gb/

# 3. Review (browser)
open tools/review-exercises.html

# 4. Publish
python scripts/publish-approved.py --from data-v2-draft/gb/ --to data-v2/exercises/gb/

# 5. Rebuild index
python scripts/build-index.py
```

### Option B: AI Agent Assistants
Use Claude Code agents to:
- Read CSV templates
- Generate exercise batches
- Run validation
- Create PR for review

---

## 📋 RECOMMENDED FIRST STEPS

**This Week:**
1. Create AI generation script skeleton
2. Set up Claude/GPT API access
3. Generate 10 pilot exercises (test quality)
4. Enhance validation script
5. Add KaTeX (quick win)

**Weeks 2-4:**
6. Build review tool
7. Generate first batch (100 exercises)
8. Implement per-option feedback in frontend
9. Add 3-level hints to frontend
10. Enrich 50 legacy exercises

---

**Document Version:** 1.0
**Next Review:** 2026-02-05
