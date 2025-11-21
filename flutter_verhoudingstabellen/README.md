# 🎨 Verhoudingstabellen voor Sara

**Kindvriendelijke Flutter widgets** om verhoudingen, percentages en schaal visueel te leren begrijpen!

## ✨ Features

### 1. **RatioTableWidget** - Verhoudingen (3:2)
- 🥛 Melk:Bloem verhoudingen
- 📊 Stap-voor-stap animaties
- 🎯 Interactief met knoppen
- 💡 Duidelijke uitleg per stap

### 2. **ScaleFactorWidget** - Recepten Opschalen (×1,5)
- 🎂 Recepten voor meer personen
- 👥 Visuele personen icoontjes
- 🌾 Groeiende ingrediënten
- ✨ Smooth animaties

### 3. **PercentageDistributionWidget** - Percentage Verdeling
- 📚 Pie chart met percentages
- 🎨 Kleurrijke categorieën
- 👆 Klikbaar voor details
- 📊 Gestapelde balk met som

## 🚀 Installatie

### Stap 1: Flutter installeren
Als je Flutter nog niet hebt:
```bash
# Download Flutter: https://docs.flutter.dev/get-started/install
```

### Stap 2: Project opzetten
```bash
cd flutter_verhoudingstabellen
flutter pub get
```

### Stap 3: App starten
```bash
# Voor desktop (Windows/Mac/Linux)
flutter run -d windows
flutter run -d macos
flutter run -d linux

# Voor mobiel
flutter run -d android
flutter run -d ios

# Voor web
flutter run -d chrome
```

## 📖 Gebruik in je eigen app

### Basis gebruik

```dart
import 'package:flutter/material.dart';
import 'widgets/verhoudingstabel/verhoudingstabel_widget.dart';

// In je widget:
VerhoudingstabelWidget(
  verhoudingstabelJson: {
    "type": "verhouding",
    "ratio": "3:2",
    "kolommen": [
      {"waarde": 300, "eenheid": "ml", "rij": "melk"},
      // ... meer kolommen
    ],
    "operaties": [
      {"operatie": "÷3", "uitleg": "Bereken 1 deel"},
    ]
  },
)
```

### Integratie met verhaaltjessommen JSON

De widgets werken **direct** met de JSON structuur uit `verhaaltjessommen - Template.json`:

```dart
// Lees de vraag data
final vraag = jsonDecode(vraagJsonString);
final extraInfo = vraag['extra_info'];

// Toon de verhoudingstabel als deze bestaat
if (extraInfo['verhoudingstabel'] != null) {
  return VerhoudingstabelWidget(
    verhoudingstabelJson: extraInfo['verhoudingstabel'],
  );
}
```

## 🎯 Ondersteunde Types

| Type | JSON `"type"` | Widget | Gebruik Voor |
|------|---------------|--------|--------------|
| Verhoudingen | `"verhouding"` | RatioTableWidget | Melk:bloem 3:2 |
| Schaalfactor | `"schaalfactor"` | ScaleFactorWidget | Recepten ×1,5 |
| Schaal | `"schaal"` | ScaleFactorWidget | Plattegrond 1:300 |
| Percentage | `"percentage_verdeling"` | PercentageDistributionWidget | 35%+45%+20%=100% |

## 🎨 Design Principes voor Kinderen

### ✅ Wat we doen:
- 🎨 **Kleurrijk**: Elke stap heeft eigen kleur
- 🎬 **Animaties**: Smooth transitions (niet te snel!)
- 👆 **Interactief**: Knoppen om stappen te besturen
- 💬 **Duidelijke taal**: "Je hebt 300 ml melk" ipv "input=300"
- 🎯 **Grote knoppen**: Makkelijk te klikken
- ✨ **Beloning**: "Klaar!" met groen vinkje

### ❌ Wat we vermijden:
- ❌ Geen kleine tekstjes
- ❌ Geen ingewikkelde wiskundige notatie
- ❌ Geen te snelle animaties
- ❌ Geen verborgen functies

## 🔧 Aanpassingen maken

### Kleuren veranderen

In elke widget file (bv. `ratio_table_widget.dart`):

```dart
// Vind deze kleuren en pas aan:
Colors.purple.shade300  // Hoofdkleur
Colors.blue.shade300    // Accent kleur
Colors.green.shade100   // Succes kleur
```

### Animatie snelheid

```dart
// In StatefulWidget initState():
_controller = AnimationController(
  duration: const Duration(milliseconds: 1500), // Verander deze waarde
  vsync: this,
);
```

### Teksten vertalen

Alle tekstjes staan in de widgets zelf. Zoek naar:
- `"Volgende Stap"` → `"Next Step"`
- `"Opnieuw"` → `"Restart"`
- etc.

## 📱 Screenshots

*Screenshots worden automatisch gegenereerd als je de app runt*

## 🤝 Voor Developers

### Project Structuur

```
flutter_verhoudingstabellen/
├── lib/
│   ├── models/
│   │   └── verhoudingstabel_model.dart    # Data models
│   ├── widgets/
│   │   └── verhoudingstabel/
│   │       ├── verhoudingstabel_widget.dart        # Main router
│   │       ├── ratio_table_widget.dart             # Verhoudingen
│   │       ├── scale_factor_widget.dart            # Recepten
│   │       ├── percentage_distribution_widget.dart # Percentages
│   │       └── animated_arrow.dart                 # Helper
│   └── main.dart                          # Demo app
├── pubspec.yaml
└── README.md
```

### Nieuwe widget type toevoegen

1. Maak model in `verhoudingstabel_model.dart`
2. Maak widget in `widgets/verhoudingstabel/`
3. Voeg case toe in `verhoudingstabel_widget.dart`
4. Voeg voorbeeld toe in `main.dart`

## 💡 Tips voor Sara

1. **Start met "Volgende Stap" knop**: Zo zie je stap-voor-stap hoe het werkt
2. **Klik op de kleuren**: In de percentage widget kun je op elke categorie klikken
3. **Kijk naar de pijlen**: Ze laten zien welke bewerking je doet (÷3, ×2)
4. **Lees de gekleurde uitleg**: Onder de tabel staat wat er gebeurt

## 🐛 Problemen oplossen

### App start niet
```bash
flutter clean
flutter pub get
flutter run
```

### Animaties haperen
- Sluit andere apps
- Probeer een andere platform (web is sneller dan emulator)

### Kleuren zien er raar uit
- Check je Flutter versie: `flutter --version`
- Update: `flutter upgrade`

## 📄 Licentie

Dit is gemaakt voor educatieve doeleinden voor Sara's wiskundeoefeningen! 🎓

---

**Gemaakt met ❤️ en Flutter**
