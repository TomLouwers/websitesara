// ============================================
// FOUTANALYSE MODAAL - VANILLA JAVASCRIPT
// Compatible met GitHub Pages / Statische HTML
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

// ============================================
// SHOW FOUTANALYSE MODAAL
// ============================================

function showFoutanalyseModaal(selectedOption, extraInfo, attemptNumber = 1, currentQuestion = null) {
  // Gelaagd protocol: verschillende content per poging
  const isFirstAttempt = attemptNumber === 1;
  const isSecondAttempt = attemptNumber === 2;
  const isThirdOrMoreAttempt = attemptNumber >= 3;

  // Na 3 pogingen: toon volledige L.O.V.A. oplossing in success modaal
  if (isThirdOrMoreAttempt && currentQuestion) {
    showFullSolution(currentQuestion, extraInfo);
    return;
  }

  const modaal = document.getElementById('foutanalyseModaal');
  if (!modaal) {
    console.error('Foutanalyse modaal element niet gevonden. Voeg de HTML toe aan index.html');
    return;
  }

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

  // Show visual aid - ONLY from 2nd attempt onwards OR if it exists
  const visualAidSection = document.getElementById('visualAidSection');
  if (!isFirstAttempt && selectedOption.visual_aid_query) {
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

  // Show remedial section ONLY from 2nd attempt onwards AND if remedial_basis_id exists
  // AND only for specific error types (conversiefout or rekenfout_basis)
  const remedialSection = document.getElementById('remedialSection');
  const shouldShowRemedial = !isFirstAttempt &&
                             selectedOption.remedial_basis_id &&
                             (selectedOption.error_type === 'conversiefout' ||
                              selectedOption.error_type === 'rekenfout_basis');

  if (shouldShowRemedial) {
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

  // After first attempt: show hint button when modaal is closed
  if (isFirstAttempt && currentQuestion && currentQuestion.hint) {
    // Store hint text in a data attribute so we can access it when closing
    modaal.dataset.showHintAfterClose = 'true';
    modaal.dataset.hintText = currentQuestion.hint;
  } else {
    modaal.dataset.showHintAfterClose = 'false';
  }
}

// ============================================
// CLOSE FOUTANALYSE MODAAL
// ============================================

function closeFoutanalyseModaal() {
  const modaal = document.getElementById('foutanalyseModaal');
  modaal.classList.remove('show');

  // Check if we should show hint after closing (first attempt only)
  // Use setTimeout to ensure hint appears after modal is fully hidden
  if (modaal.dataset.showHintAfterClose === 'true' && modaal.dataset.hintText) {
    const hintText = modaal.dataset.hintText; // Store before clearing

    // Clear the data attributes first
    modaal.dataset.showHintAfterClose = 'false';
    modaal.dataset.hintText = '';

    // Show hint after a small delay to ensure modal is closed
    setTimeout(() => {
      showHintButton(hintText);
    }, 100);
  }
}

// ============================================
// SHOW FULL SOLUTION (na 3 foute pogingen)
// ============================================

function showFullSolution(question, extraInfo) {
  const modaal = document.getElementById('successModaal');
  if (!modaal) {
    console.error('Success modaal element niet gevonden.');
    return;
  }

  // Change title to reflect this is after errors
  const header = modaal.querySelector('.modaal-header h2');
  if (header) {
    header.textContent = '📖 Hier is de volledige oplossing';
  }

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

  // Change button text to "Volgende Vraag" and mark as wrong
  const nextButton = modaal.querySelector('.modaal-actions button');
  if (nextButton) {
    nextButton.textContent = 'Volgende Vraag';
    nextButton.onclick = () => {
      closeSuccessModaal();
      // Mark question as wrong and move to next
      if (typeof nextQuestion === 'function') {
        nextQuestion();
      }
    };
  }

  // Show modaal
  modaal.classList.add('show');
}

// ============================================
// SHOW SUCCESS MODAAL (na juist antwoord)
// ============================================

function showSuccessModaal(question, extraInfo) {
  const modaal = document.getElementById('successModaal');
  if (!modaal) {
    console.error('Success modaal element niet gevonden. Voeg de HTML toe aan index.html');
    return;
  }

  // Reset title for correct answers
  const header = modaal.querySelector('.modaal-header h2');
  if (header) {
    header.textContent = '✅ Goed gedaan! Hier is de uitleg';
  }

  // Reset button text to default
  const nextButton = modaal.querySelector('.modaal-actions button');
  if (nextButton) {
    nextButton.textContent = 'Volgende Vraag';
    nextButton.onclick = () => nextQuestion();
  }

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
    "Geld uitgeven visualisatie": renderMoneySpendingVisualization,
  };

  const renderFunction = visualAids[visualAidQuery];
  if (renderFunction) {
    container.innerHTML = '';
    renderFunction(container);
  } else {
    container.innerHTML = '<p style="color: #6b7280;">Visuele hulp wordt geladen...</p>';
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

function renderMoneySpendingVisualization(container) {
  container.innerHTML = `
    <div style="text-align: center; padding: 20px;">
      <p style="font-size: 16px; margin-bottom: 20px; font-weight: 600;">
        Geld uitgeven betekent <strong>aftrekken</strong>!
      </p>
      <div style="display: flex; justify-content: center; align-items: center; gap: 15px; flex-wrap: wrap;">
        <div style="background: #d4edda; padding: 20px; border-radius: 12px; min-width: 140px; border: 3px solid #28a745;">
          <div style="font-size: 40px; margin-bottom: 8px;">💰</div>
          <div style="font-weight: bold; font-size: 18px; color: #155724;">Start Budget</div>
          <div style="font-size: 24px; color: #28a745; margin-top: 5px;">€400</div>
        </div>

        <div style="font-size: 40px; color: #dc3545;">➖</div>

        <div style="background: #f8d7da; padding: 20px; border-radius: 12px; min-width: 140px; border: 3px solid #dc3545;">
          <div style="font-size: 40px; margin-bottom: 8px;">💸</div>
          <div style="font-weight: bold; font-size: 18px; color: #721c24;">Uitgegeven</div>
          <div style="font-size: 24px; color: #dc3545; margin-top: 5px;">€372</div>
        </div>

        <div style="font-size: 40px; color: #28a745;">=</div>

        <div style="background: #fff3cd; padding: 20px; border-radius: 12px; min-width: 140px; border: 3px solid #ffc107;">
          <div style="font-size: 40px; margin-bottom: 8px;">✨</div>
          <div style="font-weight: bold; font-size: 18px; color: #856404;">Overblijft</div>
          <div style="font-size: 24px; color: #ffc107; margin-top: 5px;">€28</div>
        </div>
      </div>
      <div style="margin-top: 20px; padding: 15px; background: #e7f3ff; border-radius: 8px; border-left: 4px solid #007bff;">
        <div style="font-size: 14px; color: #004085; font-weight: 600;">
          💡 Rekenregel: Budget - Uitgaven = Overblijft
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
  if (typeof loadSubject === 'function') {
    loadSubject('basisvaardigheden');
  }

  // Na een korte delay, filter op de juiste exercise
  setTimeout(() => {
    console.log(`Navigeren naar basisoefening: ${remedialId}`);
    // TODO: Implementeer hier de logica om naar de specifieke oefening te gaan
    // Bijvoorbeeld: scrollToExercise(remedialId) of filterExercises(remedialId)
  }, 500);
}

// ============================================
// HELPER: SHOW HINT BUTTON
// ============================================

function showHintButton(hintText) {
  if (!hintText) return;

  // Check if hint is already shown
  const hintContainer = document.getElementById('hintContainer');
  if (hintContainer && hintContainer.innerHTML.trim() === '') {
    hintContainer.innerHTML = `
      <button class="hint-toggle" onclick="toggleHint()">
        💡 Hulp nodig?
      </button>
      <div id="hintBox" class="hint-box" style="display: none;">
        <span class="hint-icon">💡</span>
        ${hintText}
      </div>
    `;
  }
}

function toggleHint() {
  const hintBox = document.getElementById('hintBox');
  if (hintBox) {
    hintBox.style.display = hintBox.style.display === 'none' ? 'block' : 'none';
  }
}

// ============================================
// RESET ATTEMPT TRACKING
// ============================================

function resetAttemptTracking() {
  attemptCount = 0;
  // currentQuestionErrors is reset in loadCurrentQuestion() in app.js
}

// ============================================
// MODAAL OVERLAY CLICK HANDLER
// ============================================

// Close modaal when clicking on overlay (not on content)
document.addEventListener('DOMContentLoaded', () => {
  const foutanalyseModaal = document.getElementById('foutanalyseModaal');
  if (foutanalyseModaal) {
    foutanalyseModaal.addEventListener('click', (e) => {
      // Only close if clicking directly on overlay (not on content inside)
      if (e.target === foutanalyseModaal) {
        closeFoutanalyseModaal();
      }
    });
  }
});

// ============================================
// CONSOLE INFO
// ============================================

console.log('✅ Foutanalyse Modaal geladen (Vanilla JavaScript versie)');
console.log('📖 Gebruik showFoutanalyseModaal(option, extraInfo) om de modaal te openen');
console.log('✅ Gebruik showSuccessModaal(question, extraInfo) voor juiste antwoorden');
