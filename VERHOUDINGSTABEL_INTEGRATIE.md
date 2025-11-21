# 📊 Verhoudingstabel Widget - Integratie Documentatie

## Overzicht

De verhoudingstabel widget is een compacte, zelfstandige JavaScript component die visuele verhoudingstabellen toont binnen de foutanalyse van verhaaltjessommen. Perfect voor het tonen van stapsgewijze berekeningen wanneer Sara een vraag fout beantwoordt.

## ✨ Features

- **4 visualisatie types**: verhouding, schaalfactor, schaal, percentage_verdeling
- **Compact design**: Past in elke foutanalyse sectie
- **Geen dependencies**: Pure JavaScript en CSS
- **Responsive**: Werkt op desktop en mobiel
- **Direct te gebruiken**: Werkt met JSON data uit `verhaaltjessommen - Template.json`

## 📦 Bestanden

```
verhoudingstabel-widget.js    # JavaScript library (~400 regels)
verhoudingstabel-widget.css   # Styling (~300 regels)
foutanalyse-integratie-voorbeeld.html  # Werkend voorbeeld
```

## 🚀 Basis Gebruik

### Stap 1: Include bestanden in je HTML

```html
<head>
    <link rel="stylesheet" href="verhoudingstabel-widget.css">
</head>
<body>
    <!-- Je content -->
    <script src="verhoudingstabel-widget.js"></script>
</body>
```

### Stap 2: Creëer een container element

```html
<div id="visualization-container"></div>
```

### Stap 3: Render de widget

```javascript
// Haal de verhoudingstabel data uit de vraag
const vraagData = /* JSON data van vraag */;
const verhoudingstabelData = vraagData.extra_info.verhoudingstabel;

// Render in container
const container = document.getElementById('visualization-container');
VerhoudingstabelWidget.render(container, verhoudingstabelData);
```

## 💡 Integratie in Foutanalyse Flow

### Scenario: Toon visualisatie bij fout antwoord

```javascript
function showFoutanalyse(vraag, selectedOptie) {
    // 1. Toon foutanalyse tekst
    document.getElementById('feedback-text').textContent = selectedOptie.foutanalyse;

    // 2. Toon verhoudingstabel INDIEN van toepassing
    const container = document.getElementById('visualization-container');
    container.innerHTML = ''; // Clear previous

    if (vraag.extra_info && vraag.extra_info.verhoudingstabel) {
        VerhoudingstabelWidget.render(
            container,
            vraag.extra_info.verhoudingstabel
        );
    }

    // 3. Toon concept uitleg (optioneel)
    if (vraag.extra_info && vraag.extra_info.concept) {
        document.getElementById('concept-text').textContent = vraag.extra_info.concept;
    }
}
```

### Voorbeeld HTML structuur

```html
<div class="feedback-section">
    <!-- Foutanalyse tekst -->
    <div class="feedback-text" id="feedback-text">
        Je hebt waarschijnlijk 300 ÷ 2 gerekend...
    </div>

    <!-- Verhoudingstabel visualisatie -->
    <div id="visualization-container"></div>

    <!-- Concept uitleg -->
    <div class="concept-section">
        <strong>Concept:</strong>
        <div id="concept-text"></div>
    </div>
</div>
```

## 📊 Ondersteunde Visualisatie Types

### 1. Verhouding (ratio)

Voor vragen met verhoudingen zoals melk:bloem = 3:2

```json
{
    "type": "verhouding",
    "ratio": "3:2",
    "labels": ["melk", "delen", "bloem"],
    "kolommen": [
        {
            "waarde": 300,
            "eenheid": "ml",
            "label": "gegeven",
            "rij": "melk",
            "kleur": "#3b82f6"
        },
        {
            "waarde": 200,
            "eenheid": "gram",
            "label": "antwoord",
            "rij": "bloem",
            "kleur": "#8b5cf6",
            "berekening": "100 × 2"
        }
    ],
    "operaties": [
        {
            "van": 0,
            "naar": 2,
            "operatie": "÷3",
            "uitleg": "Bereken 1 deel"
        }
    ]
}
```

**Toont**: Rij met waarde-boxen en pijlen die operaties tonen

### 2. Schaalfactor (recipe scaling)

Voor recepten opschalen (×1,5)

```json
{
    "type": "schaalfactor",
    "factor": 1.5,
    "kolommen": [
        {
            "waarde": 8,
            "eenheid": "personen",
            "label": "origineel",
            "icon": "👥"
        },
        {
            "waarde": 12,
            "eenheid": "personen",
            "label": "nieuw",
            "icon": "👥"
        }
    ],
    "operaties": [
        {
            "van": 0,
            "naar": 1,
            "operatie": "×1,5",
            "uitleg": "12 personen is 1,5× zoveel als 8"
        }
    ]
}
```

**Toont**: Voor/na boxen met schaalfactor pijl

### 3. Schaal (maps/blueprints)

Voor plattegronden en kaarten (1:300)

```json
{
    "type": "schaal",
    "schaal": "1:300",
    "kolommen": [
        {
            "waarde": 5,
            "eenheid": "cm",
            "label": "op tekening"
        },
        {
            "waarde": 15,
            "eenheid": "meter",
            "label": "in werkelijkheid"
        }
    ]
}
```

**Toont**: Tekening → Werkelijkheid met schaal indicator

### 4. Percentage Verdeling

Voor percentage sommen (35% + 45% + 20% = 100%)

```json
{
    "type": "percentage_verdeling",
    "totaal": 800,
    "eenheid": "boeken",
    "categorieën": [
        {
            "label": "kinderboek",
            "percentage": 35,
            "aantal": 280,
            "kleur": "#60a5fa",
            "berekening": "35% van 800"
        },
        {
            "label": "roman",
            "percentage": 45,
            "aantal": 360,
            "kleur": "#a78bfa"
        }
    ]
}
```

**Toont**: Lijst met percentages en visuele balk met kleuren

## 🎨 Styling Aanpassen

De widget gebruikt CSS classes met het prefix `vt-` om conflicten te voorkomen.

### Kleuren aanpassen

In `verhoudingstabel-widget.css`:

```css
.vt-value-box.answer {
    background: #d4edda;  /* Groen voor antwoord */
    border-color: #28a745;
}

.vt-scale-arrow {
    color: #667eea;  /* Paars voor pijlen */
    border-color: #667eea;
}
```

### Compactheid aanpassen

```css
.verhoudingstabel-widget {
    padding: 20px;  /* Verander naar 15px voor compacter */
    margin: 15px 0;
}

.vt-value-box {
    min-width: 90px;  /* Verander naar 70px voor smaller */
}
```

## 📱 Responsive Design

De widget past automatisch aan op mobiel:

```css
@media (max-width: 768px) {
    .vt-ratio-row {
        flex-direction: column;  /* Stack verticaal */
    }

    .vt-value {
        font-size: 1.3em;  /* Kleinere tekst */
    }
}
```

## 🔧 Advanced Gebruik

### Conditioneel renderen

```javascript
function renderVisualization(vraag) {
    const container = document.getElementById('viz-container');
    const data = vraag.extra_info?.verhoudingstabel;

    if (!data) {
        container.style.display = 'none';
        return;
    }

    container.style.display = 'block';
    VerhoudingstabelWidget.render(container, data);
}
```

### Dynamisch data laden

```javascript
fetch('verhaaltjessommen - Template.json')
    .then(response => response.json())
    .then(data => {
        const vraag = data.vragen.find(v => v.id === 1);

        if (vraag.extra_info.verhoudingstabel) {
            VerhoudingstabelWidget.render(
                document.getElementById('container'),
                vraag.extra_info.verhoudingstabel
            );
        }
    });
```

### Error handling

```javascript
try {
    VerhoudingstabelWidget.render(container, data);
} catch (error) {
    console.error('Fout bij renderen verhoudingstabel:', error);
    container.innerHTML = '<p>Visualisatie kon niet worden geladen.</p>';
}
```

## ✅ Checklist voor Integratie

- [ ] Include `verhoudingstabel-widget.css` in `<head>`
- [ ] Include `verhoudingstabel-widget.js` voor sluiting `</body>`
- [ ] Creëer container element met ID in je foutanalyse sectie
- [ ] Check of `verhoudingstabel` data bestaat in `extra_info`
- [ ] Roep `VerhoudingstabelWidget.render()` aan bij fout antwoord
- [ ] Test op desktop én mobiel
- [ ] Test alle 4 visualisatie types

## 🧪 Testen

### Lokaal testen

1. Open `foutanalyse-integratie-voorbeeld.html` in browser
2. Klik op een fout antwoord
3. Controleer of verhoudingstabel verschijnt
4. Test responsive design (resize browser)

### Met je eigen app

```javascript
// Test data
const testData = {
    "type": "verhouding",
    "ratio": "3:2",
    "kolommen": [/* ... */]
};

VerhoudingstabelWidget.render(
    document.getElementById('test-container'),
    testData
);
```

## 🐛 Troubleshooting

### Widget verschijnt niet

**Probleem**: Niets wordt getoond
**Oplossing**:
- Check of CSS is geladen: `<link rel="stylesheet" href="verhoudingstabel-widget.css">`
- Check browser console voor errors
- Controleer of `verhoudingstabel` data bestaat en correct format heeft

### Styling ziet er raar uit

**Probleem**: Kleuren of layout kloppen niet
**Oplossing**:
- Check voor CSS conflicts met bestaande styles
- Gebruik browser dev tools om CSS te inspecteren
- Voeg `!important` toe aan widget CSS indien nodig

### Data wordt niet getoond

**Probleem**: Widget toont "Geen data"
**Oplossing**:
- Controleer JSON structuur: moet `type` en `kolommen` bevatten
- Check browser console voor parsing errors
- Validate JSON met online tool

## 📚 Voorbeelden

Zie de volgende bestanden voor complete voorbeelden:

- **`foutanalyse-integratie-voorbeeld.html`** - Werkende integratie met foutanalyse flow
- **`verhoudingstabellen_visualizer.html`** - Standalone demo met alle types
- **`verhaaltjessommen - Template.json`** - JSON data voorbeelden (zie `extra_info.verhoudingstabel`)

## 🎯 Best Practices

1. **Conditionally render**: Toon alleen als data beschikbaar is
2. **Clear container**: Roep `container.innerHTML = ''` aan voor elke render
3. **Error handling**: Wrap render call in try-catch
4. **Mobile first**: Test altijd op mobiel formaat
5. **Accessibility**: Container moet screenreader vriendelijk zijn

## 💬 Vragen?

Voor implementatie vragen of bugs, check:
- De voorbeeld HTML bestanden
- De JSON structuur in Template.json
- Browser console voor error messages

---

**Gemaakt voor Sara's wiskunde oefeningen** 🎓
