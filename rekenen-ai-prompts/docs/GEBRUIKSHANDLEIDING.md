# Gebruikshandleiding

## Inleiding

Deze handleiding beschrijft hoe je de Rekenen AI Prompts bibliotheek gebruikt voor het genereren van rekenopdrachten.

## Installatie

1. Clone de repository:
   ```bash
   git clone https://github.com/yourusername/rekenen-ai-prompts.git
   cd rekenen-ai-prompts
   ```

2. Installeer dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Basisgebruik

### Prompts laden

```python
from src.prompt_library import PromptLibrary

# Laad de prompt bibliotheek
library = PromptLibrary()

# Haal een specifieke prompt op
prompt = library.get_prompt("G3_GB_N1_001")
```

### Opdrachten genereren

```python
from src.opgave_generator import OpgaveGenerator

generator = OpgaveGenerator()
opgave = generator.generate(prompt_id="G3_GB_N1_001", moeilijkheidsgraad=1)
```

## Geavanceerd gebruik

Zie de `examples/` directory voor meer voorbeelden.

## Prompt structuur

Elke prompt is opgeslagen als YAML bestand met de volgende structuur:

```yaml
id: G3_GB_N1_001
titel: "Getalbegrip tot 20"
groep: 3
domein: "getalbegrip"
niveau: 1
beschrijving: "Opdrachten voor getalbegrip tot 20"
system_prompt: "..."
user_prompt_template: "..."
parameters:
  - name: "aantal"
    type: "integer"
    default: 5
```

## Troubleshooting

Voor vragen en problemen, zie de [API Reference](API_REFERENCE.md).
