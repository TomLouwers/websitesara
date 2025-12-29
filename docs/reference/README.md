# Domain Reference Files for Content Generation

## Overview

This directory contains comprehensive domain reference files aligned with the SLO (Stichting Leerplan Ontwikkeling) framework for Dutch primary education (Groep 1-8). These CSV files are designed to support systematic content generation for educational exercises.

## File Structure

### Rekenen/Wiskunde (Mathematics) - 4 Domains

1. **rekenen-getallen.csv** - Getallen (Numbers)
   - Number sense and operations
   - Place value understanding
   - Arithmetic skills (addition, subtraction, multiplication, division)
   - Mental math and algorithms
   - Coverage: Groep 1-8

2. **rekenen-verhoudingen.csv** - Verhoudingen (Ratios & Proportions)
   - Fractions and their operations
   - Decimal numbers
   - Percentages
   - Ratio tables and proportional reasoning
   - Coverage: Groep 4-8

3. **rekenen-meten-meetkunde.csv** - Meten & Meetkunde (Measurement & Geometry)
   - Measurement units (length, weight, time, volume, money)
   - 2D and 3D shapes
   - Perimeter, area, volume calculations
   - Symmetry, coordinates, and spatial reasoning
   - Coverage: Groep 1-8

4. **rekenen-verbanden.csv** - Verbanden (Patterns & Relations)
   - Number patterns and sequences
   - Formulas and algebraic thinking
   - Graphs, tables, and data interpretation
   - Basic statistics and probability
   - Coverage: Groep 1-8

### Nederlands/Taal (Dutch Language) - 4 Domains

5. **nederlands-lezen.csv** - Lezen (Reading)
   - Technical reading (fluency, speed)
   - Reading comprehension (literal, inferential, critical)
   - Different text types (narrative, informative, instructional)
   - Reading strategies (scanning, skimming, studying)
   - Coverage: Groep 1-8

6. **nederlands-schrijven.csv** - Schrijven (Writing)
   - Handwriting and spelling
   - Spelling rules and patterns
   - Sentence structure and punctuation
   - Different text types (stories, reports, letters, arguments)
   - Coverage: Groep 1-8

7. **nederlands-mondeling.csv** - Mondelinge taalvaardigheid (Oral Communication)
   - Listening comprehension
   - Speaking skills (clarity, expression)
   - Presentation and argumentation
   - Discussion and debate
   - Coverage: Groep 1-8

8. **nederlands-taalbeschouwing.csv** - Taalbeschouwing (Language Reflection)
   - Vocabulary development
   - Word relationships (synonyms, antonyms, word families)
   - Grammar (parts of speech, sentence structure)
   - Language awareness and variation
   - Coverage: Groep 1-8

### Oriëntatie op jezelf en de wereld (World Orientation) - 4 Domains

9. **orientatie-mens-maatschappij.csv** - Mens & Maatschappij (People & Society)
   - Identity and social skills
   - Democracy and citizenship
   - Rights and responsibilities
   - Cultural diversity and media literacy
   - Coverage: Groep 1-8

10. **orientatie-natuur-techniek.csv** - Natuur & Techniek (Nature & Technology)
    - Human body and health
    - Plants, animals, and ecosystems
    - Physical phenomena (energy, electricity, matter)
    - Technology and scientific method
    - Coverage: Groep 1-8

11. **orientatie-ruimte.csv** - Ruimte (Geography)
    - Spatial orientation and map reading
    - Netherlands geography (provinces, cities, landscapes)
    - Europe and world geography
    - Climate, population, and economic geography
    - Coverage: Groep 1-8

12. **orientatie-tijd.csv** - Tijd (History)
    - Time concepts and chronology
    - Dutch history (10 historical periods)
    - Historical thinking and source analysis
    - Connections between past and present
    - Coverage: Groep 1-8

## CSV File Format

Each CSV file contains the following columns:

| Column | Description |
|--------|-------------|
| **Groep** | Grade level (1-8) |
| **Code** | Unique learning objective code (e.g., 3G1, 4V2, 5MM3) |
| **Beschrijving** | Brief description of the learning objective |
| **Level** | **M** (Midden - midyear) or **E** (Eind - end of year) |
| **Toelichting** | Detailed explanation for implementation |
| **Prompt_Template** | AI-ready prompt template for automated exercise generation |

### Code Structure

Learning objective codes follow this pattern:
- First digit: Grade level (1-8)
- Letter(s): Domain abbreviation
  - G = Getallen
  - V = Verhoudingen
  - MM = Meten & Meetkunde
  - VB = Verbanden
  - L = Lezen
  - S = Schrijven
  - M = Mondeling
  - T = Taalbeschouwing
  - MM, NT, R, T = Oriëntatie subdomains
- Last digit(s): Sequential number within grade/domain

Example: **4G1** = Groep 4, Getallen, objective 1

## Level Indicators

**M (Midden)** - Learning objectives for midyear assessment:
- Skills expected halfway through the school year
- Foundation for end-of-year objectives
- Typically more basic or introductory concepts

**E (Eind)** - Learning objectives for end-of-year assessment:
- Skills expected at the end of the school year
- Build upon midyear objectives
- Aligned with grade-level referentieniveaus

## Usage for Content Generation

### 1. **Selecting Learning Objectives**
Filter by:
- Grade level (Groep)
- Domain
- Time of year (M or E)

Example: Generate exercises for Groep 4, end-of-year, Getallen domain
```csv
Groep,Code,Beschrijving,Level
4,4G4,Getalbegrip tot 1000,E
4,4G5,Vermenigvuldigen en delen,E
4,4G6,Hoofdrekenen strategieën,E
```

### 2. **Generating Exercise Content**
Use the **Toelichting** (explanation) column to:
- Understand the scope of the learning objective
- Determine appropriate difficulty level
- Create contextually relevant questions
- Ensure alignment with SLO kerndoelen

### 3. **Progressive Learning Paths**
Track progression across grades:
- Same domain across multiple grades shows skill development
- M objectives prepare for E objectives within same grade
- E objectives in one grade connect to M objectives in next grade

Example progression for Breuken (Fractions):
```
4V2: Breuken 1/2 en 1/4 (M)
4V3: Eenvoudige breuken herkennen (E)
5V1: Breuken tot 1/10 (M)
5V5: Breuken optellen (gelijke noemer) (E)
6V1: Breuken alle bewerkingen (M)
```

### 4. **Alignment with Referentieniveaus**
End-of-Groep-8 objectives explicitly reference:
- **1F** - Fundamenteel niveau (fundamental level)
- **1S/2F** - Streefniveau (aspiration level)

Use these to ensure exercises prepare students for national standards.

### 5. **Using Prompt Templates for AI-Generated Exercises**

Each learning objective includes a **Prompt_Template** column containing ready-to-use prompts for automated exercise generation. These templates ensure:
- Correct domain and subject area
- Appropriate grade level (Groep)
- Accurate kerndoel references (SLO framework)
- Proper inhoudslijn alignment
- Midyear (M) or end-of-year (E) level specification

#### Prompt Template Structure

All prompt templates follow this consistent format:

```
Genereer [aantal] oefeningen voor Groep [X] ([midden/eind] schooljaar).
Kerndoel: [K-nummer] ([naam]).
Inhoudslijn: [domein] - [specifiek onderwerp].
Leerdoel ([code]): [beschrijving].
Niveau: [M/E] ([uitleg]).
[Specifieke instructies voor deze leerdoel].
Vraagtypen: [voorbeelden].
Format: [gewenste opmaak].
```

#### Example Prompt Templates

**Rekenen - Getallen (Groep 4, Midyear):**
```csv
"Genereer 10 oefeningen voor Groep 4 (midden schooljaar). Kerndoel: K23 (Automatiseren).
Inhoudslijn: Getallen - Bewerkingen. Leerdoel (4G1): Alle tafels tot en met 10 automatisch beheersen.
Niveau: M (midden groep 4). Alle tafels 1-10 gemengd. Vraagtypen: 7×8=?, 6×9=?, 8×4=?, ook deelsommen.
Format: snelle automatiseringsoefeningen, mixed."
```

**Nederlands - Lezen (Groep 5, End of year):**
```csv
"Genereer 10 oefeningen voor Groep 5 (eind schooljaar). Kerndoel: K1 (Lezen).
Inhoudslijn: Lezen - Leesstrategieën. Leerdoel (5L7): Voorspellen, vragen stellen, visualiseren.
Niveau: E (eind groep 5). Focus op actieve leesstrategieën. Vraagtypen: wat verwacht je,
welke vraag stel je, wat zie je voor je. Format: korte teksten met open vragen."
```

**Oriëntatie - Ruimte (Groep 4, Midyear):**
```csv
"Genereer 10 oefeningen voor Groep 4 (midden schooljaar). Kerndoel: O8-O10 (Ruimtelijke oriëntatie,
Kaartvaardigheden). Inhoudslijn: Oriëntatie - Ruimte (Aardrijkskunde) - Provincies.
Leerdoel (4R1): 12 provincies van Nederland kennen. Niveau: M (midden groep 4).
Gebruik kaart van Nederland met provincies. Vraagtypen: welke provincie is dit, waar ligt Friesland,
hoeveel provincies heeft Nederland. Format: topografie multiple choice."
```

#### Using Prompt Templates Programmatically

**Python Example:**
```python
import pandas as pd

# Load domain reference file
df = pd.read_csv('docs/reference/rekenen-getallen.csv')

# Filter for specific grade and level
groep_4_midyear = df[(df['Groep'] == 4) & (df['Level'] == 'M')]

# Get prompt template for specific learning objective
prompt = groep_4_midyear[groep_4_midyear['Code'] == '4G1']['Prompt_Template'].values[0]

# Send to AI model for exercise generation
# exercises = ai_model.generate(prompt)
```

**TypeScript Example:**
```typescript
import { parse } from 'csv-parse/sync';
import { readFileSync } from 'fs';

// Load and parse CSV
const csv = readFileSync('docs/reference/nederlands-lezen.csv', 'utf-8');
const records = parse(csv, { columns: true });

// Filter for end-of-year objectives for Groep 6
const groep6End = records.filter(r =>
  r.Groep === '6' && r.Level === 'E'
);

// Generate exercises for all objectives
groep6End.forEach(objective => {
  const prompt = objective.Prompt_Template;
  // await generateExercises(prompt);
});
```

#### Customizing Prompt Templates

While templates are ready to use, you can customize them by:
- Adjusting the number of exercises (default: 10)
- Adding specific context (e.g., "gebruik dieren als context")
- Specifying format preferences (multiple choice, open questions, etc.)
- Including difficulty modifiers (extra moeilijk, met hulp, etc.)

**Example Customization:**
```
Original: "Genereer 10 oefeningen..."
Modified: "Genereer 15 extra moeilijke oefeningen... Gebruik de context van een speeltuin."
```

## Integration with Exercise System

When generating exercises:
1. **Select domain and grade** from these reference files
2. **Choose M or E level** based on time of year
3. **Use Code** for tracking and categorization
4. **Reference Beschrijving** in exercise metadata
5. **Follow Toelichting** for content guidelines

## Maintenance

These reference files should be updated when:
- SLO kerndoelen are revised (next major update: 2026-2031)
- New referentieniveaus are published
- Exercise gap analysis reveals missing objectives

## Related Documents

- `/docs/slo-reference-framework.md` - Complete SLO framework documentation
- `/docs/slo-content-inventory.md` - Analysis of existing exercises
- `/docs/slo-gap-analysis.md` - Identified content gaps

## Version History

- **v1.1** (2025-12-29): Added AI-ready prompt templates
  - Added Prompt_Template column to all 13 domain files
  - 436 total learning objectives with detailed generation prompts
  - Consistent template structure across all domains
  - Ready for automated exercise generation with AI models

- **v1.0** (2025-12-29): Initial creation of 13 domain reference files
  - Aligned with SLO Kerndoelen 2006 (current framework)
  - Prepared for transition to 2025 framework (2026-2031)
  - Comprehensive coverage of all primary education domains

---

**Created:** 2025-12-29
**Status:** Production ready for content generation
**Next Review:** Upon SLO framework update (2026)
