# Architectuur

## Overzicht

Het Rekenen AI Prompts systeem bestaat uit verschillende componenten die samenwerken om hoogwaardige rekenopdrachten te genereren.

## Componenten

### 1. Prompt Library (`src/prompt_library.py`)

De centrale bibliotheek voor het laden en beheren van prompts.

**Verantwoordelijkheden:**
- Prompts laden uit YAML bestanden
- Validatie van prompt structuur
- Zoeken en filteren van prompts

### 2. Opgave Generator (`src/opgave_generator.py`)

Genereert concrete opdrachten op basis van prompts.

**Verantwoordelijkheden:**
- Prompt parameters invullen
- AI model aanroepen
- Output formatteren

### 3. Adaptive System (`src/adaptive_system.py`)

Past moeilijkheidsgraad aan op basis van leerling prestaties.

**Verantwoordelijkheden:**
- Track leerling voortgang
- Pas moeilijkheidsgraad aan
- Selecteer passende prompts

### 4. Validators (`src/validators.py`)

Valideert prompts en gegenereerde opdrachten.

**Verantwoordelijkheden:**
- Schema validatie
- Inhoudelijke checks
- Kwaliteitscontrole

## Data Flow

```
YAML Prompts → Prompt Library → Opgave Generator → Gegenereerde Opdracht
                      ↓
                  Validators
                      ↓
                Adaptive System
```

## Design Principes

1. **Modulariteit**: Elk component heeft een duidelijke verantwoordelijkheid
2. **Uitbreidbaarheid**: Nieuwe prompts en domeinen kunnen eenvoudig worden toegevoegd
3. **Validatie**: Strikte validatie op alle niveaus
4. **Type Safety**: Gebruik van Pydantic voor type checking

## Database Schema

(Optioneel, indien database wordt gebruikt)

## API Design

Zie [API Reference](API_REFERENCE.md) voor details.
