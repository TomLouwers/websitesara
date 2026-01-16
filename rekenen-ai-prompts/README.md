# AI Prompt Library: Getal & Bewerkingen

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Een complete bibliotheek van AI-prompts voor het genereren van rekenopdrachten voor Nederlands basisonderwijs (groep 3-8).

## ✨ Features

- 🎯 **~1.188 gedetailleerde prompts** voor alle groepen en niveaus
- 📚 **Pedagogisch onderbouwd** volgens SLO-kerndoelen en Cito-referentieniveaus
- 🔄 **Adaptief systeem** met 4 moeilijkheidsniveaus (N1-N4)
- 🧪 **Ingebouwde validatie** en kwaliteitscontrole
- 🌐 **Open source** en volledig uitbreidbaar
- 📊 **Foutdetectie** met gerichte feedback triggers
- 🎓 **Didactisch verantwoord** met duidelijke leerlijnen

## 📋 Overzicht

### Structuur

Het systeem bevat prompts voor 4 inhoudslijnen per groep:

1. **Getalbegrip** - Herkennen, vergelijken, ordenen van getallen
2. **Strategieën** - Rekenstrategieën en handige manieren van rekenen
3. **Bewerkingen** - Optellen, aftrekken, vermenigvuldigen, delen
4. **Schriftelijk rekenen** - Procedures voor schriftelijke bewerkingen (vanaf groep 4)

Elk inhoudslijn heeft 4 niveaus:
- **N1 (Onder 1F)**: Automatiseren & herkennen
- **N2 (Richting 1F)**: Begrip in standaardcontext
- **N3 (1F-kenmerken)**: Flexibel toepassen
- **N4 (1S-kenmerken)**: Redeneren en verklaren

### Naming Convention

Elk prompt heeft een uniek ID volgens het patroon:
```
G[groep]_[inhoudslijn]_N[niveau]_[nummer]
```

Voorbeelden:
- `G3_GB_N1_001` = Groep 3, Getalbegrip, Niveau 1, variant 1
- `G6_BW_N3_012` = Groep 6, Bewerkingen, Niveau 3, variant 12
- `G8_SR_N4_005` = Groep 8, Schriftelijk rekenen, Niveau 4, variant 5

**Afkortingen:**
- `GB` = Getalbegrip
- `ST` = Strategieën
- `BW` = Bewerkingen
- `SR` = Schriftelijk rekenen

## 🚀 Snelle Start

### Installatie

```bash
git clone https://github.com/TomLouwers/websitesara.git
cd websitesara/rekenen-ai-prompts
pip install -r requirements.txt
```

### Basis Gebruik

```python
from src.prompt_library import PromptLibrary

# Initialiseer en laad prompts
library = PromptLibrary()
library.load_prompts()

# Haal specifieke prompt op
prompt = library.get_prompt("G5_GB_N2_001")

# Zoek prompts voor een niveau
prompts_groep_5 = library.search_prompts(groep=5, inhoudslijn="Getalbegrip", niveau="N2")

# Bekijk statistieken
stats = library.get_statistics()
print(stats)
```

### Genereren van Opgaven

```python
from src.opgave_generator import OpgaveGenerator
from openai import OpenAI

# Setup (gebruik je eigen AI client)
client = OpenAI(api_key="your-key")
generator = OpgaveGenerator(library, client)

# Genereer opgaven
opgaven = generator.generate_opgave(
    prompt_id="G5_GB_N2_001",
    aantal=10
)

# Gebruik gegenereerde opgaven
for opgave in opgaven:
    print(opgave['vraag_tekst'])
    print(f"Antwoord: {opgave['correct_antwoord']}")
```

## 📖 Documentatie

Volledige documentatie is beschikbaar in de `/docs` directory:

- **[Gebruikshandleiding](docs/GEBRUIKSHANDLEIDING.md)** - Complete implementatiehandleiding
- **[Architectuur](docs/ARCHITECTUUR.md)** - Systeemoverzicht en design
- **[API Reference](docs/API_REFERENCE.md)** - Volledige API documentatie
- **[Changelog](docs/CHANGELOG.md)** - Versiegeschiedenis

## 🏗️ Project Structuur

```
rekenen-ai-prompts/
├── prompts/                  # YAML prompt bestanden
│   ├── groep_3/
│   │   ├── getalbegrip/
│   │   ├── strategieën/
│   │   ├── bewerkingen/
│   │   └── schriftelijk_rekenen/
│   ├── groep_4/
│   └── ...
├── src/                      # Python broncode
│   ├── prompt_library.py     # Prompt beheer
│   ├── opgave_generator.py   # AI opgave generatie
│   ├── adaptive_system.py    # Adaptief systeem
│   ├── validators.py         # Kwaliteitscontrole
│   └── utils.py              # Hulpfuncties
├── tests/                    # Unit tests
├── examples/                 # Voorbeeldscripts
├── scripts/                  # Utility scripts
└── docs/                     # Documentatie
```

## 🎯 Use Cases

### 1. Adaptief Leersysteem

```python
from src.adaptive_system import AdaptiveSystem

adaptive = AdaptiveSystem(generator)

# Krijg volgende opgave voor leerling
opgave = adaptive.get_next_opgave(
    leerling_id="student_123",
    groep=5,
    inhoudslijn="Getalbegrip"
)

# Verwerk antwoord
result = adaptive.process_antwoord(
    leerling_id="student_123",
    opgave_id=opgave['vraag_id'],
    antwoord="42"
)

print(result['feedback'])
```

### 2. Batch Generatie

```python
# Pre-genereer opgaven voor cache
for prompt_id in library.prompts.keys():
    opgaven = generator.generate_opgave(prompt_id, aantal=50)
    # Sla op in database
```

### 3. Kwaliteitscontrole

```python
from src.validators import PromptValidator

validator = PromptValidator()
result = validator.validate_prompt(prompt)

if not result.is_valid:
    print("Fouten gevonden:", result.errors)
```

## 🧪 Testing

```bash
# Run alle tests
pytest tests/

# Met coverage
pytest --cov=src tests/

# Specifieke test
pytest tests/test_prompt_library.py
```

## 🤝 Bijdragen

Contributions zijn welkom! Zie [CONTRIBUTING.md](CONTRIBUTING.md) voor richtlijnen.

### Development Setup

```bash
# Clone en setup virtual environment
git clone https://github.com/TomLouwers/websitesara.git
cd websitesara/rekenen-ai-prompts
python -m venv venv
source venv/bin/activate  # of `venv\Scripts\activate` op Windows

# Installeer dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Voor development

# Run tests
pytest
```

## 📊 Statistieken

- **Totaal prompts**: ~1.188
- **Groepen**: 6 (groep 3 t/m 8)
- **Inhoudslijnen**: 4 per groep
- **Niveaus**: 4 per inhoudslijn
- **Varianten**: 10-35 per niveau

## 🔐 Licentie

Dit project is gelicenseerd onder de MIT License - zie het [LICENSE](LICENSE) bestand voor details.

## ✍️ Auteurs

- **Tom Louwers** - *Initial work* - [TomLouwers](https://github.com/TomLouwers)

## 🙏 Acknowledgments

- Gebaseerd op SLO-kerndoelen en Cito-referentieniveaus
- Ontwikkeld voor gebruik in educatieve platforms
- Met dank aan alle contributors

## 📧 Contact

Voor vragen of suggesties, open een [GitHub Issue](https://github.com/TomLouwers/websitesara/issues).

## 🗺️ Roadmap

**Versie 1.0** (Huidig)
- ✅ Volledige prompt library Getal & Bewerkingen
- ✅ Basis generator implementatie
- ✅ Validatie framework

**Versie 1.1** (Q2 2025)
- ⬜ Meten & Meetkunde prompts
- ⬜ Verhoudingen prompts
- ⬜ Uitgebreide foutdetectie

**Versie 2.0** (Q3 2025)
- ⬜ Multi-language support (Engels, Frans)
- ⬜ Adaptieve moeilijkheidsgraad binnen prompt
- ⬜ Automatische prompt optimization via feedback

---

**Made with ❤️ for Dutch education**
