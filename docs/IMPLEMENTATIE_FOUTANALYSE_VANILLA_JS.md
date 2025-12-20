# Implementatielogica: Foutanalyse Modaal (Vanilla JavaScript)

## Overzicht

Deze guide beschrijft de **volledige UI/UX implementatie** van de verbeterde foutanalyse voor verhaaltjessommen in **pure HTML/CSS/JavaScript** (geen React vereist).

Perfect voor:
- ✅ GitHub Pages hosting
- ✅ Statische HTML websites
- ✅ Geen build proces nodig
- ✅ Direct werkend na deployment

---

## Stap 1: Nieuwe Velden in JSON

Zie `verhaaltjessommen_FOUTANALYSE_TEMPLATE.json` voor voorbeelden met:

```json
{
  "question": "...",
  "hint": "💡 Subtiele nudge na eerste fout",
  "options": [
    {
      "text": "...",
      "is_correct": false,
      "error_type": "conversiefout",
      "foutanalyse": "Uitleg...\n\n🤔 **Reflectievraag:** ...",
      "visual_aid_query": "Conversietabel uren naar minuten",
      "remedial_basis_id": 301
    }
  ]
}
```

**Error Types:** `conversiefout`, `leesfout_ruis`, `conceptfout`, `rekenfout_basis`

---

## Stap 2: HTML Structuur voor Modaal

Voeg toe aan je `index.html` (direct voor de sluitende `</body>` tag):

```html
<!-- Foutanalyse Modaal -->
<div id="foutanalyseModaal" class="modaal-overlay">
  <div class="modaal-content">
    <div class="modaal-header">
      <h2 id="modaalTitle">🛑 Oeps! Dit is niet juist</h2>
      <button class="modaal-close" onclick="closeFoutanalyseModaal()">✕</button>
    </div>

    <!-- Error Type Badge -->
    <div id="errorBadge" class="error-badge"></div>

    <!-- Foutanalyse Section -->
    <div class="fault-analysis-section">
      <h3>Wat ging er mis?</h3>
      <p id="mainExplanation" class="main-explanation"></p>

      <!-- Reflection Question -->
      <div id="reflectionBox" class="reflection-box" style="display: none;">
        <div class="reflection-header">
          <span class="reflection-icon">🤔</span>
          <strong>REFLECTIEVRAAG:</strong>
        </div>
        <p id="reflectionText" class="reflection-text"></p>
      </div>
    </div>

    <!-- Visual Aid Section -->
    <div id="visualAidSection" class="visual-aid-section" style="display: none;">
      <h4>
        <span class="visual-icon">📊</span>
        <span id="visualAidTitle"></span>
      </h4>
      <div id="visualAidContent" class="visual-content"></div>
      <button id="videoButton" class="video-button" style="display: none;">
        ▶️ Bekijk Uitleg: <span id="videoTitle"></span>
      </button>
    </div>

    <!-- Remedial Section -->
    <div id="remedialSection" class="remedial-section" style="display: none;">
      <div class="remedial-alert">
        🚨 Eerst de Basis Herstellen!
      </div>
      <p id="remedialExplanation" class="remedial-explanation"></p>
      <button id="remedialCta" class="remedial-cta">
        <span class="cta-icon">🎯</span>
        <span id="remedialCtaText" class="cta-text"></span>
      </button>
      <div class="exercise-info">
        <span class="info-icon">ℹ️</span>
        <span>5 eenvoudige oefenopgaven</span>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="modaal-actions">
      <button class="btn btn-primary" onclick="closeFoutanalyseModaal()">
        Probeer Opnieuw
      </button>
    </div>
  </div>
</div>

<!-- Success Modaal (na juist antwoord) -->
<div id="successModaal" class="modaal-overlay">
  <div class="modaal-content">
    <div class="modaal-header">
      <h2>✅ Goed gedaan! Hier is de uitleg</h2>
      <button class="modaal-close" onclick="closeSuccessModaal()">✕</button>
    </div>

    <!-- L.O.V.A. Accordion -->
    <div class="lova-accordion">
      <button class="accordion-toggle" onclick="toggleLovaAccordion()">
        <span id="lovaToggleIcon">▼</span>
        📚 L.O.V.A. Stappenplan (klik om uit te klappen)
      </button>
      <div id="lovaContent" class="accordion-content">
        <!-- Will be populated by JavaScript -->
      </div>
    </div>

    <!-- Berekening Tabel -->
    <div class="berekening-section">
      <h3>🧮 Berekening Stap voor Stap</h3>
      <div id="berekeningTable"></div>
    </div>

    <!-- Concept Box -->
    <div class="concept-box">
      <h3>💡 Onthoud dit Concept</h3>
      <p id="conceptText"></p>
    </div>

    <div class="modaal-actions">
      <button class="btn btn-primary" onclick="nextQuestion()">
        Volgende Vraag
      </button>
    </div>
  </div>
</div>
```

---

## Stap 3: CSS Styling

Voeg toe aan je `styles.css`:

```css
/* ============================================
   FOUTANALYSE MODAAL STYLING
   ============================================ */

/* Modaal Overlay */
.modaal-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 1000;
  overflow-y: auto;
  animation: fadeIn 0.3s ease;
}

.modaal-overlay.show {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Modaal Content */
.modaal-content {
  background: white;
  border-radius: 20px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.4s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Modaal Header */
.modaal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 30px;
  border-bottom: 2px solid #e5e7eb;
}

.modaal-header h2 {
  margin: 0;
  color: #1f2937;
  font-size: 24px;
}

.modaal-close {
  background: none;
  border: none;
  font-size: 32px;
  cursor: pointer;
  color: #6b7280;
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
  transition: color 0.2s;
}

.modaal-close:hover {
  color: #ef4444;
}

/* Error Badge */
.error-badge {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 30px;
  background-color: #fef2f2;
  border-left: 6px solid #ef4444;
  margin: 0;
}

.error-badge.conversiefout {
  border-color: #ef4444;
  background-color: #fef2f2;
}

.error-badge.leesfout_ruis {
  border-color: #f59e0b;
  background-color: #fffbea;
}

.error-badge.conceptfout {
  border-color: #8b5cf6;
  background-color: #f5f3ff;
}

.error-badge.rekenfout_basis {
  border-color: #3b82f6;
  background-color: #eff6ff;
}

.error-emoji {
  font-size: 32px;
}

.error-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

/* Fault Analysis Section */
.fault-analysis-section {
  padding: 30px;
}

.fault-analysis-section h3 {
  color: #374151;
  margin-bottom: 16px;
  font-size: 20px;
}

.main-explanation {
  color: #4b5563;
  font-size: 16px;
  line-height: 1.8;
  margin-bottom: 20px;
}

/* Reflection Box */
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

/* Visual Aid Section */
.visual-aid-section {
  background-color: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px 30px;
  margin: 20px 30px;
}

.visual-aid-section h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #374151;
  margin-bottom: 16px;
  font-size: 18px;
}

.visual-content {
  margin: 16px 0;
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

.conversion-table th {
  background-color: #f3f4f6;
  font-weight: 700;
  color: #374151;
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

/* Remedial Section */
.remedial-section {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border: 3px solid #dc2626;
  border-radius: 16px;
  padding: 24px 30px;
  margin: 20px 30px;
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

/* L.O.V.A. Accordion */
.lova-accordion {
  margin: 20px 30px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.accordion-toggle {
  width: 100%;
  background-color: #f9fafb;
  border: none;
  padding: 16px 20px;
  font-size: 18px;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s;
}

.accordion-toggle:hover {
  background-color: #f3f4f6;
}

.accordion-content {
  display: none;
  padding: 20px;
  background-color: white;
}

.accordion-content.open {
  display: block;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 2000px;
  }
}

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

.lova-step ul {
  margin-left: 20px;
  color: #4b5563;
  line-height: 1.8;
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

/* Berekening Section */
.berekening-section {
  background-color: #f0fdf4;
  border: 2px solid #16a34a;
  border-radius: 12px;
  padding: 20px 30px;
  margin: 20px 30px;
}

.berekening-section h3 {
  color: #15803d;
  margin-bottom: 16px;
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

/* Concept Box */
.concept-box {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 3px solid #f59e0b;
  border-radius: 12px;
  padding: 20px 30px;
  margin: 20px 30px;
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

/* Modaal Actions */
.modaal-actions {
  padding: 20px 30px;
  border-top: 2px solid #e5e7eb;
  display: flex;
  justify-content: center;
  gap: 12px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .modaal-content {
    border-radius: 0;
    max-height: 100vh;
  }

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

## Stap 4: JavaScript Implementatie

Maak een nieuw bestand: `foutanalyse-modaal.js`

```javascript
// ============================================
// FOUTANALYSE MODAAL - VANILLA JAVASCRIPT
// ============================================

// Error type labels
const errorTypeLabels = {
  conversiefout: {
    emoji: "🛑",
    title: "Oeps! Je bent een omrekenstap vergeten!",
    color: "#ef4444",
    concept: "het omrekenen van eenheden"
  },
  leesfout_ruis: {
    emoji: "📖",
    title: "Let op! Je hebt iets over het hoofd gezien in de tekst!",
    color: "#f59e0b",
    concept: "het herkennen van belangrijke informatie"
  },
  conceptfout: {
    emoji: "🧠",
    title: "Hmm, dit is een denkfout over hoe de som werkt!",
    color: "#8b5cf6",
    concept: "het toepassen van de juiste rekenregel"
  },
  rekenfout_basis: {
    emoji: "🔢",
    title: "Check je rekenwerk nog eens!",
    color: "#3b82f6",
    concept: "de basis rekenvaardigheid"
  }
};

// Exercise titles mapping (voor remedial_basis_id)
const exerciseTitles = {
  301: "Tijd omrekenen",
  205: "Positieve en negatieve getallen",
  102: "Tafels van vermenigvuldiging (1-10)",
  // Voeg hier meer oefeningen toe
};

// Track attempt count per question
let attemptCount = 0;
let hintShown = false;

// ============================================
// SHOW FOUTANALYSE MODAAL
// ============================================

function showFoutanalyseModaal(selectedOption, extraInfo) {
  const modaal = document.getElementById('foutanalyseModaal');

  // Update error badge
  const errorInfo = errorTypeLabels[selectedOption.error_type] || errorTypeLabels.rekenfout_basis;
  const errorBadge = document.getElementById('errorBadge');
  errorBadge.className = `error-badge ${selectedOption.error_type}`;
  errorBadge.innerHTML = `
    <span class="error-emoji">${errorInfo.emoji}</span>
    <span class="error-title">${errorInfo.title}</span>
  `;

  // Parse foutanalyse voor main text en reflection question
  const { mainText, reflectionQuestion } = parseFoutanalyse(selectedOption.foutanalyse);

  document.getElementById('mainExplanation').textContent = mainText;

  // Show reflection question if exists
  const reflectionBox = document.getElementById('reflectionBox');
  if (reflectionQuestion) {
    document.getElementById('reflectionText').textContent = reflectionQuestion;
    reflectionBox.style.display = 'block';
  } else {
    reflectionBox.style.display = 'none';
  }

  // Show visual aid if exists
  const visualAidSection = document.getElementById('visualAidSection');
  if (selectedOption.visual_aid_query) {
    document.getElementById('visualAidTitle').textContent = selectedOption.visual_aid_query;
    renderVisualAid(selectedOption.visual_aid_query);

    // Show video button if video exists
    const videoButton = document.getElementById('videoButton');
    if (extraInfo && extraInfo.video_uitleg) {
      document.getElementById('videoTitle').textContent = extraInfo.video_uitleg.titel;
      videoButton.style.display = 'flex';
      videoButton.onclick = () => window.open(extraInfo.video_uitleg.url, '_blank');
    } else {
      videoButton.style.display = 'none';
    }

    visualAidSection.style.display = 'block';
  } else {
    visualAidSection.style.display = 'none';
  }

  // Show remedial section if remedial_basis_id exists
  const remedialSection = document.getElementById('remedialSection');
  if (selectedOption.remedial_basis_id) {
    const exerciseTitle = exerciseTitles[selectedOption.remedial_basis_id] || `Oefening ${selectedOption.remedial_basis_id}`;

    document.getElementById('remedialExplanation').textContent =
      `Het lijkt erop dat je nog moeite hebt met ${errorInfo.concept}.`;

    document.getElementById('remedialCtaText').innerHTML = `
      Oefen Basissom #${selectedOption.remedial_basis_id}:<br />
      <strong>"${exerciseTitle}"</strong>
    `;

    document.getElementById('remedialCta').onclick = () => {
      navigateToExercise(selectedOption.remedial_basis_id);
    };

    remedialSection.style.display = 'block';
  } else {
    remedialSection.style.display = 'none';
  }

  // Show modaal
  modaal.classList.add('show');
}

// ============================================
// CLOSE FOUTANALYSE MODAAL
// ============================================

function closeFoutanalyseModaal() {
  const modaal = document.getElementById('foutanalyseModaal');
  modaal.classList.remove('show');
}

// ============================================
// SHOW SUCCESS MODAAL (na juist antwoord)
// ============================================

function showSuccessModaal(question, extraInfo) {
  const modaal = document.getElementById('successModaal');

  // Render L.O.V.A. content if exists
  if (question.lova) {
    renderLovaContent(question.lova);
  }

  // Render berekening tabel
  if (extraInfo && extraInfo.berekening_tabel) {
    renderBerekeningTabel(extraInfo.berekening_tabel);
  }

  // Show concept
  if (extraInfo && extraInfo.concept) {
    document.getElementById('conceptText').textContent = extraInfo.concept;
  }

  // Show modaal
  modaal.classList.add('show');
}

// ============================================
// CLOSE SUCCESS MODAAL
// ============================================

function closeSuccessModaal() {
  const modaal = document.getElementById('successModaal');
  modaal.classList.remove('show');
}

// ============================================
// PARSE FOUTANALYSE
// ============================================

function parseFoutanalyse(text) {
  // Split op reflectievraag pattern
  const parts = text.split(/🤔 \*\*Reflectievraag:\*\*/);

  return {
    mainText: parts[0].trim(),
    reflectionQuestion: parts[1] ? parts[1].trim() : null
  };
}

// ============================================
// RENDER VISUAL AID
// ============================================

function renderVisualAid(visualAidQuery) {
  const container = document.getElementById('visualAidContent');

  // Map query to rendering function
  const visualAids = {
    "Conversietabel uren naar minuten": renderTimeConversionTable,
    "Tijdlijn met rustpauze": renderTimelineWithBreak,
    "Puntentabel raak vs mis": renderPointsTable,
    "Verhoudingstabel positieve en negatieve punten": renderRatioTable,
  };

  const renderFunction = visualAids[visualAidQuery];
  if (renderFunction) {
    container.innerHTML = '';
    renderFunction(container);
  } else {
    container.innerHTML = '<p>Visuele hulp wordt geladen...</p>';
  }
}

// ============================================
// VISUAL AID COMPONENTS
// ============================================

function renderTimeConversionTable(container) {
  container.innerHTML = `
    <table class="conversion-table">
      <thead>
        <tr>
          <th>Uren</th>
          <th>Minuten</th>
        </tr>
      </thead>
      <tbody>
        <tr class="highlight">
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
  `;
}

function renderTimelineWithBreak(container) {
  container.innerHTML = `
    <div style="text-align: center; padding: 20px;">
      <div style="font-size: 16px; margin-bottom: 10px;">
        🚴 ──────── 🛑 (15 min pauze) ──────── 🏠
      </div>
      <div style="font-size: 14px; color: #6b7280;">
        <strong>Totale tijd:</strong> 1 uur 45 min<br>
        <strong>Rustpauze:</strong> 15 min<br>
        <strong>Netto fitstijd:</strong> 105 - 15 = 90 min
      </div>
    </div>
  `;
}

function renderPointsTable(container) {
  container.innerHTML = `
    <table class="conversion-table">
      <thead>
        <tr>
          <th>Type</th>
          <th>Aantal</th>
          <th>Punten per bal</th>
          <th>Totaal</th>
        </tr>
      </thead>
      <tbody>
        <tr class="highlight">
          <td>✅ Raak</td>
          <td>9</td>
          <td>+3</td>
          <td>+27 punten</td>
        </tr>
        <tr>
          <td>❌ Mis</td>
          <td>6</td>
          <td>-1</td>
          <td>-6 punten</td>
        </tr>
        <tr style="background-color: #fef3c7; font-weight: bold;">
          <td colspan="3">Eindtotaal</td>
          <td>21 punten</td>
        </tr>
      </tbody>
    </table>
  `;
}

function renderRatioTable(container) {
  container.innerHTML = `
    <div style="text-align: center; padding: 20px;">
      <p style="font-size: 16px; margin-bottom: 15px;">
        Bij positieve en negatieve getallen moet je <strong>twee bewerkingen</strong> uitvoeren:
      </p>
      <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; min-width: 150px;">
          <div style="font-size: 32px;">➕</div>
          <div style="font-weight: bold; margin-top: 8px;">Positief</div>
          <div style="font-size: 14px; color: #155724;">Tel de winst op</div>
        </div>
        <div style="background: #f8d7da; padding: 15px; border-radius: 8px; min-width: 150px;">
          <div style="font-size: 32px;">➖</div>
          <div style="font-weight: bold; margin-top: 8px;">Negatief</div>
          <div style="font-size: 14px; color: #721c24;">Trek het verlies af</div>
        </div>
      </div>
    </div>
  `;
}

// ============================================
// RENDER L.O.V.A. CONTENT
// ============================================

function renderLovaContent(lova) {
  const container = document.getElementById('lovaContent');

  let html = '';

  // Stap 1: LEZEN
  html += `
    <div class="lova-step">
      <h4>📖 Stap 1: LEZEN</h4>
      <ul>
        <li><strong>Hoofdvraag:</strong> ${lova.stap1_lezen.hoofdvraag}</li>
        <li><strong>Ruis (negeer):</strong> ${lova.stap1_lezen.ruis.join(', ')}</li>
        <li><strong>Tussenstappen:</strong>
          <ol>
            ${lova.stap1_lezen.tussenstappen.map(stap => `<li>${stap}</li>`).join('')}
          </ol>
        </li>
      </ul>
    </div>
  `;

  // Stap 2: ORDENEN
  html += `
    <div class="lova-step">
      <h4>📋 Stap 2: ORDENEN</h4>
      <ul>
        <li><strong>Relevante getallen:</strong>
          <ul>
            ${Object.entries(lova.stap2_ordenen.relevante_getallen)
              .map(([key, val]) => `<li>${key}: ${val}</li>`)
              .join('')}
          </ul>
        </li>
        <li><strong>Tool:</strong> ${lova.stap2_ordenen.tool}</li>
        ${lova.stap2_ordenen.conversies.length > 0 ?
          `<li><strong>Conversies:</strong> ${lova.stap2_ordenen.conversies.join(', ')}</li>` : ''}
      </ul>
    </div>
  `;

  // Stap 3: VORMEN
  html += `
    <div class="lova-step">
      <h4>🔧 Stap 3: VORMEN (berekeningen)</h4>
      ${lova.stap3_vormen.bewerkingen.map(bew => `
        <div class="calculation-step">
          <strong>${bew.stap}:</strong><br>
          <code>${bew.berekening}</code> = <strong>${bew.resultaat}</strong><br>
          <em>(${bew.uitleg})</em>
        </div>
      `).join('')}
    </div>
  `;

  // Stap 4: ANTWOORDEN
  html += `
    <div class="lova-step">
      <h4>✍️ Stap 4: ANTWOORDEN</h4>
      <ul>
        <li><strong>Verwachte eenheid:</strong> ${lova.stap4_antwoorden.verwachte_eenheid}</li>
        <li><strong>Logica check:</strong> ${lova.stap4_antwoorden.logica_check}</li>
        <li><strong>Antwoord:</strong> <span class="final-answer">${lova.stap4_antwoorden.antwoord}</span></li>
      </ul>
    </div>
  `;

  container.innerHTML = html;
}

// ============================================
// TOGGLE L.O.V.A. ACCORDION
// ============================================

function toggleLovaAccordion() {
  const content = document.getElementById('lovaContent');
  const icon = document.getElementById('lovaToggleIcon');

  if (content.classList.contains('open')) {
    content.classList.remove('open');
    icon.textContent = '▼';
  } else {
    content.classList.add('open');
    icon.textContent = '▲';
  }
}

// ============================================
// RENDER BEREKENING TABEL
// ============================================

function renderBerekeningTabel(berekeningArray) {
  const container = document.getElementById('berekeningTable');

  // Join array en render als markdown table (simple HTML conversion)
  const markdownTable = berekeningArray.join('\n');

  // Simple markdown table parser
  const lines = markdownTable.split('\n').filter(line => line.trim());

  let html = '<table>';
  lines.forEach((line, index) => {
    if (index === 1) return; // Skip separator line

    const cells = line.split('|').filter(cell => cell.trim()).map(cell => cell.trim());

    if (index === 0) {
      html += '<thead><tr>';
      cells.forEach(cell => {
        html += `<th>${cell}</th>`;
      });
      html += '</tr></thead><tbody>';
    } else {
      html += '<tr>';
      cells.forEach(cell => {
        html += `<td>${cell}</td>`;
      });
      html += '</tr>';
    }
  });
  html += '</tbody></table>';

  container.innerHTML = html;
}

// ============================================
// NAVIGATE TO EXERCISE
// ============================================

function navigateToExercise(remedialId) {
  // Sluit de modaal
  closeFoutanalyseModaal();

  // Navigeer naar basisvaardigheden met de specifieke ID
  // Pas deze URL aan naar jouw routing systeem
  loadSubject('basisvaardigheden');

  // Na een korte delay, filter op de juiste exercise
  setTimeout(() => {
    // Implementeer hier de logica om naar de specifieke oefening te gaan
    console.log(`Navigeren naar basisoefening: ${remedialId}`);
  }, 500);
}

// ============================================
// INTEGRATIE MET BESTAANDE APP.JS
// ============================================

// Roep deze functie aan wanneer een antwoord wordt geselecteerd
function handleAnswerSelection(optionIndex) {
  const currentQuestion = randomizedQuestions[currentQuestionIndex];
  const selectedOption = currentQuestion.questions[0].options[optionIndex];
  const extraInfo = currentQuestion.questions[0].extra_info;

  // Increment attempt count
  attemptCount++;

  // Check if correct
  if (selectedOption.is_correct) {
    // Show success modaal
    showSuccessModaal(currentQuestion.questions[0], extraInfo);
  } else {
    // Show foutanalyse modaal
    showFoutanalyseModaal(selectedOption, extraInfo);

    // Show hint na eerste fout (implementeer in je main app.js)
    if (attemptCount === 1 && !hintShown) {
      showHintButton(currentQuestion.questions[0].hint);
    }
  }
}

// Helper: show hint button
function showHintButton(hintText) {
  if (!hintText) return;

  // Voeg hint button toe aan je vraag UI
  const hintContainer = document.getElementById('hintContainer'); // Moet je toevoegen aan HTML
  if (hintContainer) {
    hintContainer.innerHTML = `
      <button class="hint-toggle" onclick="toggleHint()">
        💡 Hulp nodig?
      </button>
      <div id="hintBox" class="hint-box" style="display: none;">
        <span class="hint-icon">💡</span>
        ${hintText}
      </div>
    `;
    hintShown = true;
  }
}

function toggleHint() {
  const hintBox = document.getElementById('hintBox');
  if (hintBox) {
    hintBox.style.display = hintBox.style.display === 'none' ? 'block' : 'none';
  }
}

// Reset attempt count when moving to next question
function resetAttemptTracking() {
  attemptCount = 0;
  hintShown = false;
}
```

---

## Stap 5: Integratie met je Bestaande `app.js`

Voeg toe aan je `index.html` (voor de sluitende `</body>` tag):

```html
<script src="foutanalyse-modaal.js"></script>
```

Pas je bestaande answer handling logica in `app.js` aan:

```javascript
// In je checkAnswer() functie (of waar je antwoorden controleert)
function checkAnswer() {
  if (hasAnswered) return;
  if (selectedAnswer === null) {
    alert('Selecteer eerst een antwoord!');
    return;
  }

  hasAnswered = true;
  const currentQuestion = randomizedQuestions[currentQuestionIndex];
  const selectedOption = currentQuestion.questions[0].options[selectedAnswer];
  const correctAnswer = currentQuestion.questions[0].correct;
  const isCorrect = selectedAnswer === correctAnswer;
  const extraInfo = currentQuestion.questions[0].extra_info;

  // Update score
  if (isCorrect) {
    score++;
  } else {
    wrongAnswers.push({
      question: currentQuestion,
      selectedAnswer: selectedAnswer,
      correctAnswer: correctAnswer
    });
  }

  // Show modaal instead of inline feedback
  if (isCorrect) {
    showSuccessModaal(currentQuestion.questions[0], extraInfo);
  } else {
    showFoutanalyseModaal(selectedOption, extraInfo);
  }

  // Update progress tracker
  updateCategoryProgress(currentQuestion.theme, isCorrect);
}

// Update nextQuestion functie
function nextQuestion() {
  closeSuccessModaal(); // Close modaal als deze open is
  resetAttemptTracking(); // Reset attempt counter

  // Je bestaande next question logica...
  currentQuestionIndex++;
  if (currentQuestionIndex < totalQuestions) {
    displayQuestion();
  } else {
    showResults();
  }
}
```

---

## Stap 6: Testing Checklist

- [ ] Modaal opent wanneer fout antwoord wordt geselecteerd
- [ ] Error badge toont juiste emoji en kleur voor elk error_type
- [ ] Reflectievraag wordt correct geparsed en getoond
- [ ] Visual aid rendert correct (conversietabel, etc.)
- [ ] Remedial CTA navigeert naar basisvaardigheden
- [ ] Success modaal toont na juist antwoord
- [ ] L.O.V.A. accordion kan in/uitklappen
- [ ] Berekening tabel rendert markdown correct
- [ ] Modaal werkt op mobile devices
- [ ] Video uitleg knop opent in nieuwe tab
- [ ] Hint verschijnt na eerste fout
- [ ] Modaal sluit correct met X knop

---

## Deployment

Gewoon pushen naar GitHub en het werkt! Geen build proces nodig.

```bash
git add .
git commit -m "Add foutanalyse modaal met Vanilla JS"
git push
```

---

**Perfect voor:** Statische websites, GitHub Pages, geen dependencies!
