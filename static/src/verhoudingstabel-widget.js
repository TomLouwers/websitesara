/**
 * Verhoudingstabel Widget Library
 * Compact, herbruikbaar component voor het tonen van verhoudingstabellen in foutanalyse
 *
 * Gebruik:
 * VerhoudingstabelWidget.render(containerElement, verhoudingstabelData);
 */

const VerhoudingstabelWidget = (function() {
    'use strict';

    // Kleuren schema
    const COLORS = {
        melk: '#2196F3',
        delen: '#FF9800',
        bloem: '#795548',
        primary: '#667eea',
        success: '#28a745',
        categories: ['#2196F3', '#9C27B0', '#FF9800', '#4CAF50', '#F44336']
    };

    /**
     * Main render functie - detecteert type en rendert juiste visualisatie
     */
    function render(container, data) {
        if (!container || !data) {
            console.error('VerhoudingstabelWidget: container en data zijn verplicht');
            return;
        }

        // Clear container
        container.innerHTML = '';
        container.classList.add('verhoudingstabel-widget');

        // Render op basis van type
        switch(data.type) {
            case 'verhouding':
                renderRatioTable(container, data);
                break;
            case 'schaalfactor':
                renderScaleFactor(container, data);
                break;
            case 'schaal':
                renderScaleMap(container, data);
                break;
            case 'percentage_verdeling':
                renderPercentageDistribution(container, data);
                break;
            default:
                container.innerHTML = `<div class="vt-error">Onbekend type: ${data.type}</div>`;
        }
    }

    /**
     * Render Ratio Table (verhouding 3:2)
     */
    function renderRatioTable(container, data) {
        const rows = ['melk', 'delen', 'bloem'];
        const icons = {melk: '🥛', delen: '📊', bloem: '🌾'};

        let html = '<div class="vt-ratio-table">';

        rows.forEach(rowName => {
            const rowData = data.kolommen.filter(k => k.rij === rowName);
            if (rowData.length === 0) return;

            html += `<div class="vt-ratio-row">`;
            html += `<div class="vt-ratio-label" style="color: ${COLORS[rowName]}">
                        <span>${icons[rowName]}</span>
                        <span>${rowName.charAt(0).toUpperCase() + rowName.slice(1)}</span>
                     </div>`;
            html += `<div class="vt-ratio-values">`;

            // Kolom 1: Gegeven
            if (rowData[0]) {
                html += createValueBox(rowData[0], COLORS[rowName]);
            }

            // Pijl 1
            if (data.operaties && data.operaties[0]) {
                html += createArrow(data.operaties[0].operatie, COLORS[rowName]);
            }

            // Kolom 2: 1 deel
            if (rowData[1]) {
                html += createValueBox(rowData[1], COLORS[rowName]);
            }

            // Pijl 2
            if (data.operaties && data.operaties[1] && rowData[2]) {
                html += createArrow(data.operaties[1].operatie, COLORS[rowName]);
            }

            // Kolom 3: Antwoord
            if (rowData[2]) {
                html += createValueBox(rowData[2], COLORS[rowName], true);
            }

            html += `</div></div>`;
        });

        html += '</div>';

        // Uitleg toevoegen
        if (data.operaties && data.operaties.length > 0) {
            html += '<div class="vt-explanation">';
            html += '<strong>Stappen:</strong><br>';
            data.operaties.forEach((op, i) => {
                html += `${i + 1}. ${op.uitleg}<br>`;
            });
            html += '</div>';
        }

        container.innerHTML = html;
    }

    /**
     * Render Scale Factor (recepten opschalen)
     */
    function renderScaleFactor(container, data) {
        const personen = data.kolommen.filter(k => k.eenheid === 'personen');
        const bloem = data.kolommen.filter(k => k.eenheid === 'gram');

        let html = '<div class="vt-scale-factor">';

        // Personen rij
        if (personen.length === 2) {
            html += '<div class="vt-scale-row">';
            html += createScaleBox(personen[0], '👥', false);
            html += `<div class="vt-scale-arrow">×${data.factor}</div>`;
            html += createScaleBox(personen[1], '👥', true);
            html += '</div>';
        }

        // Bloem rij
        if (bloem.length === 2) {
            html += '<div class="vt-scale-row">';
            html += createScaleBox(bloem[0], '🌾', false);
            html += `<div class="vt-scale-arrow">×${data.factor}</div>`;
            html += createScaleBox(bloem[1], '🌾', true);
            html += '</div>';
        }

        html += '</div>';

        // Uitleg
        html += `<div class="vt-explanation">
                    <strong>Opschalen:</strong><br>
                    Alle ingrediënten × ${data.factor} = recept voor ${personen[1].waarde} personen
                 </div>`;

        container.innerHTML = html;
    }

    /**
     * Render Scale Map (plattegrond/kaart)
     */
    function renderScaleMap(container, data) {
        const schaal = data.schaal || '1:?';

        let html = '<div class="vt-scale-map">';
        html += `<div class="vt-scale-header">Schaal: <strong>${schaal}</strong></div>`;

        html += '<div class="vt-scale-row">';

        data.kolommen.forEach((kolom, index) => {
            const isLast = index === data.kolommen.length - 1;
            html += `<div class="vt-scale-box ${isLast ? 'answer' : ''}">
                        <div class="vt-value">${kolom.waarde}</div>
                        <div class="vt-unit">${kolom.eenheid}</div>
                        <div class="vt-label">${kolom.label}</div>
                     </div>`;

            if (!isLast && data.operaties && data.operaties[index]) {
                html += `<div class="vt-scale-arrow">${data.operaties[index].operatie}</div>`;
            }
        });

        html += '</div>';
        html += '</div>';

        // Uitleg
        if (data.operaties && data.operaties[0]) {
            html += `<div class="vt-explanation">
                        <strong>Let op:</strong> ${data.operaties[0].uitleg}
                     </div>`;
        }

        container.innerHTML = html;
    }

    /**
     * Render Percentage Distribution (pie chart + tabel)
     */
    function renderPercentageDistribution(container, data) {
        let html = '<div class="vt-percentage">';

        // Categorieën lijst
        html += '<div class="vt-percentage-list">';
        data.categorieën.forEach((cat, index) => {
            const color = COLORS.categories[index % COLORS.categories.length];
            html += `<div class="vt-percentage-item" style="border-left: 5px solid ${color}">
                        <div class="vt-percentage-header">
                            <span class="vt-percentage-label">${cat.label.toUpperCase()}</span>
                            <span class="vt-percentage-badge" style="background: ${color}">${cat.percentage}%</span>
                        </div>
                        <div class="vt-percentage-value">${cat.aantal} ${data.eenheid}</div>
                        <div class="vt-percentage-calc">📝 ${cat.berekening}</div>
                     </div>`;
        });
        html += '</div>';

        // Totaal balk
        html += '<div class="vt-total-bar-container">';
        html += '<div class="vt-total-bar">';
        data.categorieën.forEach((cat, index) => {
            const color = COLORS.categories[index % COLORS.categories.length];
            html += `<div class="vt-total-segment" style="flex: ${cat.percentage}; background: ${color}">
                        ${cat.percentage}%
                     </div>`;
        });
        html += '</div>';

        // Som
        const sumParts = data.categorieën.map(c => c.aantal).join(' + ');
        html += `<div class="vt-total-sum">${sumParts} = <strong>${data.totaal} ${data.eenheid}</strong></div>`;
        html += '</div>';

        html += '</div>';

        container.innerHTML = html;
    }

    /**
     * Helper: Create value box voor ratio table
     */
    function createValueBox(kolom, color, isAnswer = false) {
        return `<div class="vt-value-box ${isAnswer ? 'answer' : ''}" style="border-color: ${color}">
                    <div class="vt-value" style="color: ${color}">${kolom.waarde}</div>
                    <div class="vt-unit">${kolom.eenheid}</div>
                    ${kolom.berekening ? `<div class="vt-calc">${kolom.berekening}</div>` : ''}
                </div>`;
    }

    /**
     * Helper: Create arrow
     */
    function createArrow(operatie, color) {
        return `<div class="vt-arrow" style="color: ${color}">
                    <div class="vt-arrow-label">${operatie}</div>
                    <div class="vt-arrow-symbol">→</div>
                </div>`;
    }

    /**
     * Helper: Create scale box
     */
    function createScaleBox(kolom, icon, isNew) {
        return `<div class="vt-scale-box ${isNew ? 'new' : ''}">
                    <div class="vt-icon">${icon}</div>
                    <div class="vt-value">${kolom.waarde}</div>
                    <div class="vt-unit">${kolom.eenheid}</div>
                </div>`;
    }

    // Public API
    return {
        render: render
    };
})();

// Export voor gebruik in modules (optioneel)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VerhoudingstabelWidget;
}
