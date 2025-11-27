# Implementatielogica: Foutanalyse Modaal

## Overzicht

Deze guide beschrijft de **volledige UI/UX implementatie** van de verbeterde foutanalyse voor verhaaltjessommen. De focus ligt op het maximaliseren van het leermoment door gebruik te maken van:

1. **Gelaagde Hints** (Scaffolding)
2. **Diagnostische Error Types**
3. **Metacognitieve Reflectievragen**
4. **Visuele Correctie**
5. **Remedial Loops** (Herstel van basistaken)

---

## Nieuwe JSON-velden

### Per Vraag (`question` object):

```json
{
  "question": "...",
  "hint": "💡 Subtiele aanmoediging om de leerling te helpen",
  "options": [ ... ]
}
```

### Per Optie (`options` object):

```json
{
  "text": "Antwoord A",
  "is_correct": false,
  "error_type": "conversiefout",  // ← NIEUW
  "foutanalyse": "Diagnostische uitleg...\n\n🤔 **Reflectievraag:** Wat is ...?",  // ← Eindigt met reflectie
  "visual_aid_query": "Conversietabel uren naar minuten",  // ← NIEUW (optioneel)
  "remedial_basis_id": 301  // ← NIEUW (optioneel, koppeling naar basisoefening)
}
```

### Error Types

Gebruik **altijd** één van de volgende vier types:

| `error_type` | Betekenis | Voorbeeld |
|--------------|-----------|-----------|
| `conversiefout` | Leerling vergat een eenheid om te rekenen | Uren niet omgezet naar minuten |
| `leesfout_ruis` | Leerling miste relevante info of werd afgeleid door ruis | Rustpauze vergeten af te trekken |
| `conceptfout` | Leerling paste de verkeerde rekenregel toe | Alle ballen vermenigvuldigen i.p.v. alleen raak |
| `rekenfout_basis` | Rekenregel correct, maar uitvoering fout | 9 × 3 = 24 in plaats van 27 |

---

## UI Flow: Stap voor Stap

### **Fase 1: Pre-Feedback (Vóór het Antwoorden)**

#### **State bij eerste poging:**
- `hint` veld is **verborgen**
- Leerling ziet alleen de vraag en de 4 opties

#### **Na de eerste fout:**
- Toon een **subtiele knop** onder de vraag:
  ```html
  <button class="hint-toggle" onclick="toggleHint()">
    💡 Hulp nodig?
  </button>
  ```
- Bij klik: toon de inhoud van `hint` in een **lichtgeel kader**:

```jsx
{showHint && (
  <div className="hint-box">
    <span className="hint-icon">💡</span>
    {question.hint}
  </div>
)}
```

**CSS:**
```css
.hint-box {
  background-color: #fffbea;
  border-left: 4px solid #f59e0b;
  padding: 12px 16px;
  margin-top: 12px;
  border-radius: 6px;
  font-size: 14px;
  color: #92400e;
}

.hint-icon {
  margin-right: 8px;
  font-size: 18px;
}
```

---

### **Fase 2: Na Fout Antwoord (De Leermoment-Modaal)**

Wanneer de leerling fout antwoordt, open een **fullscreen modaal** met de volgende secties:

#### **1. Error Type Badge**

Vertaal de `error_type` naar kindvriendelijke taal:

```jsx
const errorTypeLabels = {
  conversiefout: {
    emoji: "🛑",
    title: "Oeps! Je bent een omrekenstap vergeten!",
    color: "#ef4444"
  },
  leesfout_ruis: {
    emoji: "📖",
    title: "Let op! Je hebt iets over het hoofd gezien in de tekst!",
    color: "#f59e0b"
  },
  conceptfout: {
    emoji: "🧠",
    title: "Hmm, dit is een denkfout over hoe de som werkt!",
    color: "#8b5cf6"
  },
  rekenfout_basis: {
    emoji: "🔢",
    title: "Check je rekenwerk nog eens!",
    color: "#3b82f6"
  }
};

// Render logic
const errorInfo = errorTypeLabels[selectedOption.error_type];

<div className="error-badge" style={{ borderColor: errorInfo.color }}>
  <span className="error-emoji">{errorInfo.emoji}</span>
  <span className="error-title">{errorInfo.title}</span>
</div>
```

**CSS:**
```css
.error-badge {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background-color: #fef2f2;
  border-left: 6px solid;
  border-radius: 8px;
  margin-bottom: 24px;
}

.error-emoji {
  font-size: 32px;
}

.error-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}
```

---

#### **2. Foutanalyse met Reflectievraag**

Parse de `foutanalyse` om de reflectievraag te scheiden van de hoofdtekst:

```jsx
function parseFoutanalyse(text) {
  // Split op het reflectievraag-patroon
  const parts = text.split(/🤔 \*\*Reflectievraag:\*\*/);

  return {
    mainText: parts[0].trim(),
    reflectionQuestion: parts[1] ? parts[1].trim() : null
  };
}

// In component:
const { mainText, reflectionQuestion } = parseFoutanalyse(selectedOption.foutanalyse);

<div className="fault-analysis-section">
  <h3>Wat ging er mis?</h3>
  <p className="main-explanation">{mainText}</p>

  {reflectionQuestion && (
    <div className="reflection-box">
      <div className="reflection-header">
        <span className="reflection-icon">🤔</span>
        <strong>REFLECTIEVRAAG:</strong>
      </div>
      <p className="reflection-text">{reflectionQuestion}</p>
    </div>
  )}
</div>
```

**CSS:**
```css
.reflection-box {
  background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
  border: 2px solid #3b82f6;
  border-radius: 12px;
  padding: 16px;
  margin-top: 20px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}

.reflection-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  color: #1e40af;
  font-weight: 700;
}

.reflection-icon {
  font-size: 24px;
}

.reflection-text {
  color: #1e3a8a;
  font-size: 15px;
  line-height: 1.6;
  margin: 0;
}
```

---

#### **3. Visuele Correctie (visual_aid_query)**

Als het veld `visual_aid_query` gevuld is, render een visuele hulp:

```jsx
// Mapping van query → component
const visualAidComponents = {
  "Conversietabel uren naar minuten": TimeConversionTable,
  "Tijdlijn met rustpauze": TimelineWithBreak,
  "Puntentabel raak vs mis": PointsTable,
  "Verhoudingstabel positieve en negatieve punten": RatioTable,
  "Diagram Ongelijknamige Breuken": FractionDiagram
};

// In component:
{selectedOption.visual_aid_query && (
  <div className="visual-aid-section">
    <h4>
      <span className="visual-icon">📊</span>
      {selectedOption.visual_aid_query}
    </h4>

    <div className="visual-content">
      {React.createElement(
        visualAidComponents[selectedOption.visual_aid_query]
      )}
    </div>

    {extra_info.video_uitleg && (
      <button
        className="video-button"
        onClick={() => openVideo(extra_info.video_uitleg.url)}
      >
        ▶️ Bekijk Uitleg: {extra_info.video_uitleg.titel}
      </button>
    )}
  </div>
)}
```

**Voorbeeld Component: TimeConversionTable**

```jsx
function TimeConversionTable() {
  return (
    <table className="conversion-table">
      <thead>
        <tr>
          <th>Uren</th>
          <th>Minuten</th>
        </tr>
      </thead>
      <tbody>
        <tr className="highlight">
          <td>1 uur</td>
          <td>60 minuten 👈</td>
        </tr>
        <tr>
          <td>2 uur</td>
          <td>120 minuten</td>
        </tr>
        <tr>
          <td>3 uur</td>
          <td>180 minuten</td>
        </tr>
      </tbody>
    </table>
  );
}
```

**CSS:**
```css
.visual-aid-section {
  background-color: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  margin-top: 24px;
}

.visual-aid-section h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #374151;
  margin-bottom: 16px;
}

.conversion-table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
}

.conversion-table th,
.conversion-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.conversion-table .highlight {
  background-color: #fef3c7;
  font-weight: 600;
}

.video-button {
  background-color: #dc2626;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  transition: background-color 0.2s;
}

.video-button:hover {
  background-color: #b91c1c;
}
```

---

#### **4. Remedial Loop (Herstel de Basis)**

Als `remedial_basis_id` is gevuld, toon dit als de **primaire CTA** (Call to Action):

```jsx
{selectedOption.remedial_basis_id && (
  <div className="remedial-section">
    <div className="remedial-alert">
      🚨 Eerst de Basis Herstellen!
    </div>

    <p className="remedial-explanation">
      Het lijkt erop dat je nog moeite hebt met {getConceptName(selectedOption.error_type)}.
    </p>

    <button
      className="remedial-cta"
      onClick={() => navigateToExercise(selectedOption.remedial_basis_id)}
    >
      <span className="cta-icon">🎯</span>
      <span className="cta-text">
        Oefen Basissom #{selectedOption.remedial_basis_id}:
        <br />
        <strong>"{getExerciseTitle(selectedOption.remedial_basis_id)}"</strong>
      </span>
    </button>

    <div className="exercise-info">
      <span className="info-icon">ℹ️</span>
      <span>5 eenvoudige oefenopgaven</span>
    </div>
  </div>
)}
```

**Helper functies:**

```jsx
function getConceptName(errorType) {
  const conceptNames = {
    conversiefout: "het omrekenen van eenheden",
    leesfout_ruis: "het herkennen van belangrijke informatie",
    conceptfout: "het toepassen van de juiste rekenregel",
    rekenfout_basis: "de basis rekenvaardigheid"
  };
  return conceptNames[errorType] || "deze vaardigheid";
}

function getExerciseTitle(remedialId) {
  // Fetch van database of hardcoded mapping
  const exercises = {
    301: "Tijd omrekenen",
    205: "Positieve en negatieve getallen",
    102: "Tafels van vermenigvuldiging (1-10)"
  };
  return exercises[remedialId] || `Oefening ${remedialId}`;
}

function navigateToExercise(remedialId) {
  // Route naar de basis-oefening pagina
  window.location.href = `/oefeningen/basis/${remedialId}`;
}
```

**CSS:**
```css
.remedial-section {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border: 3px solid #dc2626;
  border-radius: 16px;
  padding: 24px;
  margin-top: 32px;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
}

.remedial-alert {
  background-color: #dc2626;
  color: white;
  font-size: 18px;
  font-weight: 700;
  padding: 12px 20px;
  border-radius: 8px;
  text-align: center;
  margin-bottom: 16px;
}

.remedial-explanation {
  color: #7f1d1d;
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.remedial-cta {
  width: 100%;
  background-color: #16a34a;
  color: white;
  border: none;
  padding: 20px;
  border-radius: 12px;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s;
  box-shadow: 0 4px 8px rgba(22, 163, 74, 0.3);
}

.remedial-cta:hover {
  background-color: #15803d;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(22, 163, 74, 0.4);
}

.cta-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.cta-text {
  text-align: left;
  line-height: 1.5;
}

.exercise-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  color: #7f1d1d;
  font-size: 14px;
  justify-content: center;
}

.info-icon {
  font-size: 16px;
}
```

---

### **Fase 3: Na Juist Antwoord (Volledige Uitleg)**

#### **1. L.O.V.A. Stappenplan (Accordion)**

```jsx
import { Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

function LovaAccordion({ lova }) {
  return (
    <Accordion defaultExpanded={false}>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <h3>📚 L.O.V.A. Stappenplan (klik om uit te klappen)</h3>
      </AccordionSummary>

      <AccordionDetails>
        {/* Stap 1: LEZEN */}
        <div className="lova-step">
          <h4>📖 Stap 1: LEZEN</h4>
          <ul>
            <li>
              <strong>Hoofdvraag:</strong> {lova.stap1_lezen.hoofdvraag}
            </li>
            <li>
              <strong>Ruis (negeer):</strong>{' '}
              {lova.stap1_lezen.ruis.join(', ')}
            </li>
            <li>
              <strong>Tussenstappen:</strong>
              <ol>
                {lova.stap1_lezen.tussenstappen.map((stap, idx) => (
                  <li key={idx}>{stap}</li>
                ))}
              </ol>
            </li>
          </ul>
        </div>

        {/* Stap 2: ORDENEN */}
        <div className="lova-step">
          <h4>📋 Stap 2: ORDENEN</h4>
          <ul>
            <li>
              <strong>Relevante getallen:</strong>
              <ul>
                {Object.entries(lova.stap2_ordenen.relevante_getallen).map(([key, val]) => (
                  <li key={key}>{key}: {val}</li>
                ))}
              </ul>
            </li>
            <li><strong>Tool:</strong> {lova.stap2_ordenen.tool}</li>
            {lova.stap2_ordenen.conversies.length > 0 && (
              <li>
                <strong>Conversies:</strong> {lova.stap2_ordenen.conversies.join(', ')}
              </li>
            )}
          </ul>
        </div>

        {/* Stap 3: VORMEN */}
        <div className="lova-step">
          <h4>🔧 Stap 3: VORMEN (berekeningen)</h4>
          {lova.stap3_vormen.bewerkingen.map((bew, idx) => (
            <div key={idx} className="calculation-step">
              <strong>{bew.stap}:</strong>
              <br />
              <code>{bew.berekening}</code> = <strong>{bew.resultaat}</strong>
              <br />
              <em>({bew.uitleg})</em>
            </div>
          ))}
        </div>

        {/* Stap 4: ANTWOORDEN */}
        <div className="lova-step">
          <h4>✍️ Stap 4: ANTWOORDEN</h4>
          <ul>
            <li>
              <strong>Verwachte eenheid:</strong> {lova.stap4_antwoorden.verwachte_eenheid}
            </li>
            <li>
              <strong>Logica check:</strong> {lova.stap4_antwoorden.logica_check}
            </li>
            <li>
              <strong>Antwoord:</strong> <span className="final-answer">{lova.stap4_antwoorden.antwoord}</span>
            </li>
          </ul>
        </div>
      </AccordionDetails>
    </Accordion>
  );
}
```

**CSS:**
```css
.lova-step {
  background-color: #f9fafb;
  border-left: 4px solid #3b82f6;
  padding: 16px;
  margin-bottom: 16px;
  border-radius: 8px;
}

.lova-step h4 {
  color: #1e40af;
  margin-bottom: 12px;
}

.calculation-step {
  background-color: #e0f2fe;
  padding: 12px;
  margin: 8px 0;
  border-radius: 6px;
  line-height: 1.8;
}

.calculation-step code {
  background-color: #1e293b;
  color: #fbbf24;
  padding: 4px 8px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
}

.final-answer {
  background-color: #fbbf24;
  color: #1f2937;
  padding: 4px 12px;
  border-radius: 6px;
  font-weight: 700;
  font-size: 18px;
}
```

---

#### **2. Berekening Tabel (Markdown Rendering)**

```jsx
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

function BerekeningTabel({ berekening_tabel }) {
  // Join array naar markdown string
  const markdown = berekening_tabel.join('\n');

  return (
    <div className="berekening-section">
      <h3>🧮 Berekening Stap voor Stap</h3>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {markdown}
      </ReactMarkdown>
    </div>
  );
}
```

**CSS:**
```css
.berekening-section {
  background-color: #f0fdf4;
  border: 2px solid #16a34a;
  border-radius: 12px;
  padding: 20px;
  margin-top: 24px;
}

.berekening-section table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}

.berekening-section th,
.berekening-section td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #d1d5db;
}

.berekening-section th {
  background-color: #16a34a;
  color: white;
  font-weight: 700;
}

.berekening-section td:last-child {
  font-weight: 600;
}
```

---

#### **3. Concept Verankering**

```jsx
<div className="concept-box">
  <h3>💡 Onthoud dit Concept</h3>
  <p>{extra_info.concept}</p>
</div>
```

**CSS:**
```css
.concept-box {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 3px solid #f59e0b;
  border-radius: 12px;
  padding: 20px;
  margin-top: 24px;
  box-shadow: 0 4px 8px rgba(245, 158, 11, 0.2);
}

.concept-box h3 {
  color: #92400e;
  margin-bottom: 12px;
}

.concept-box p {
  color: #78350f;
  font-size: 15px;
  line-height: 1.7;
  margin: 0;
}
```

---

## State Management

Gebruik de volgende state variabelen:

```jsx
const [selectedOptionIndex, setSelectedOptionIndex] = useState(null);
const [isCorrect, setIsCorrect] = useState(null);
const [attemptCount, setAttemptCount] = useState(0);
const [showHint, setShowHint] = useState(false);
const [showFeedbackModal, setShowFeedbackModal] = useState(false);

function handleAnswerSubmit(optionIndex) {
  setAttemptCount(prev => prev + 1);
  setSelectedOptionIndex(optionIndex);

  const option = question.options[optionIndex];
  setIsCorrect(option.is_correct);
  setShowFeedbackModal(true);

  // Na eerste fout: hint beschikbaar maken
  if (!option.is_correct && attemptCount === 0) {
    setShowHint(true);
  }
}
```

---

## Responsive Design

Zorg dat de modaal **mobile-friendly** is:

```css
@media (max-width: 768px) {
  .error-badge {
    flex-direction: column;
    text-align: center;
  }

  .remedial-cta {
    flex-direction: column;
    padding: 16px;
  }

  .cta-icon {
    font-size: 28px;
  }

  .cta-text {
    text-align: center;
  }

  .conversion-table {
    font-size: 14px;
  }

  .conversion-table th,
  .conversion-table td {
    padding: 8px;
  }
}
```

---

## Testing Checklist

- [ ] Hint verschijnt **alleen na eerste fout**
- [ ] Error type badge toont juiste emoji en kleur
- [ ] Reflectievraag wordt correct geparsed en gestyled
- [ ] Visual aid query laadt correct component
- [ ] Remedial CTA navigeert naar juiste basis-oefening
- [ ] L.O.V.A. accordion kan uit/inklappen
- [ ] Berekening tabel rendert markdown correct (met emojis)
- [ ] Concept box is zichtbaar na correct antwoord
- [ ] Modaal werkt op mobile devices
- [ ] Video uitleg knop opent video in nieuwe tab

---

## Voorbeeld Data Structuur

Zie het bestand `verhaaltjessommen_FOUTANALYSE_TEMPLATE.json` voor twee volledige voorbeelden met alle nieuwe velden.

---

## Volgende Stappen

1. **Implementeer de UI componenten** zoals beschreven in deze guide
2. **Update alle vragen** in `verhaaltjessommen - Template.json` met de nieuwe velden:
   - Voeg `hint` toe aan elke vraag
   - Voeg `error_type` toe aan elke foute optie
   - Eindig elke `foutanalyse` met een reflectievraag
   - Voeg optioneel `visual_aid_query` en `remedial_basis_id` toe
3. **Test de flow** met echte leerlingen
4. **Verzamel feedback** over de effectiviteit van de remedial loops

---

**Gemaakt op:** 2025-11-27
**Focus:** Optimale foutanalyse en leermoment voor Groep 8 Doorstroomtoets
