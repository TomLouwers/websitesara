# 🎨 Verhoudingstabellen Visualisaties - Gebruiksaanwijzing

## ✨ Super Simpel - Geen Installatie Nodig!

### Stap 1: Open het bestand
**Klik dubbel** op `verhoudingstabellen_visualizer.html`

Of:
- Rechtermuisknop → "Openen met" → Kies je browser (Chrome, Firefox, Safari, Edge)

### Stap 2: Klaar! 🎉

De visualisaties openen zich automatisch in je browser. **Niets installeren nodig!**

---

## 📚 Wat zie je?

### 3 Interactieve Visualisaties:

#### 1. 🥛 **Verhouding 3:2** (Melk & Bloem)
```
Melk  │ 300ml → 100ml → Bloem
Delen │   3   →  1   →   2
Bloem │              → 200g
```
- **Klik op "Volgende Stap"** om de berekening stap-voor-stap te zien
- **Klik op "Opnieuw"** om het nog een keer te doen

#### 2. 🎂 **Recept Opschalen ×1,5**
```
8 personen  →  12 personen
200g bloem  →  300g bloem (geanimeerd!)
```
- **Klik op "Start Animatie"** om de bloem te zien groeien van 200 naar 300

#### 3. 📚 **Percentages** (800 Boeken)
```
🥧 Pie Chart met:
- 35% kinderboeken (blauw)
- 45% romans (paars)
- 20% stripboeken (oranje)
```
- **Klik op een categorie** om de berekening te zien
- **Zie de som**: 280 + 360 + 160 = 800

---

## 🎯 Voor Sara:

1. **Open het bestand** in je browser
2. **Klik op de tabs** bovenaan om te wisselen tussen visualisaties
3. **Gebruik de knoppen** om de animaties te besturen
4. **Klik op de gekleurde vakjes** voor details

---

## 📱 Werkt op:

✅ **Computer** (Windows, Mac, Linux)
✅ **Tablet** (iPad, Android tablet)
✅ **Telefoon** (iPhone, Android)

---

## 🔧 Integratie in je Website/App

### Optie 1: Direct insluiten
```html
<iframe src="verhoudingstabellen_visualizer.html"
        width="100%"
        height="800px"
        style="border:none;">
</iframe>
```

### Optie 2: Data vanuit JSON laden

Open `verhoudingstabellen_visualizer.html` en pas deze regels aan:

```javascript
// Vervang deze data met data uit je JSON:
const ratioData = vraag.extra_info.verhoudingstabel;
```

---

## 🎨 Aanpassen

### Kleuren veranderen:
Zoek in het bestand naar:
```javascript
const colors = {
    melk: '#2196F3',   // Blauw - verander naar elke kleur!
    delen: '#FF9800',  // Oranje
    bloem: '#795548'   // Bruin
};
```

### Animatie snelheid:
Zoek naar:
```javascript
const duration = 1500;  // In milliseconden (1500 = 1,5 seconde)
```

### Teksten vertalen:
Alle teksten staan gewoon in de HTML. Gebruik Ctrl+F om te zoeken:
- `"Volgende Stap"` → `"Next Step"`
- `"Opnieuw"` → `"Reset"`
- etc.

---

## ❓ Problemen?

### Visualisatie ziet er raar uit?
- **Ververs de pagina** (F5 of Ctrl+R)
- **Open in een andere browser** (Chrome werkt het beste)

### Animaties lopen niet smooth?
- **Sluit andere tabbladen**
- **Update je browser** naar de nieuwste versie

### Kleuren kloppen niet?
- Kijk of je browser in "Dark Mode" staat
- Sommige dark mode extensies kunnen kleuren veranderen

---

## 🚀 Volgende Stappen

### Wil je meer visualisaties?

Het is super makkelijk om nieuwe toe te voegen! Voeg gewoon een nieuwe tab toe:

```html
<button class="tab" onclick="showViz('nieuw')">
    🌟 Mijn Nieuwe Visualisatie
</button>

<div id="nieuwViz" class="visualization">
    <!-- Je nieuwe visualisatie hier -->
</div>
```

---

## 📸 Screenshots

![Ratio Table](screenshots/ratio.png)
![Scale Factor](screenshots/scale.png)
![Percentage Chart](screenshots/percentage.png)

*(Screenshots worden automatisch gemaakt als je de pagina opent)*

---

## 💡 Tips voor Docenten

1. **Projecteer op het digibord** voor klassikale instructie
2. **Deel de file via Teams/Google Classroom** - leerlingen kunnen het zelf openen
3. **Print QR code** die naar het bestand linkt
4. **Voeg toe aan je website** met een iframe

---

## 📄 Technische Details

| Aspect | Details |
|--------|---------|
| Bestandsgrootte | ~20 KB |
| Dependencies | Geen! Pure HTML/CSS/JS |
| Browsers | Alle moderne browsers |
| Internet nodig? | Nee, werkt offline |
| Installatie | Nee |

---

**Gemaakt met ❤️ voor Sara**

Vragen? Check de code zelf - alles staat in 1 bestand en is goed gedocumenteerd!
