# API Reference

## PromptLibrary

### `PromptLibrary()`

Hoofdklasse voor het beheren van prompts.

#### Methods

##### `load_prompts(path: str) -> None`

Laad alle prompts uit een directory.

**Parameters:**
- `path` (str): Pad naar de prompts directory

**Raises:**
- `ValidationError`: Als een prompt niet valide is

##### `get_prompt(prompt_id: str) -> Prompt`

Haal een specifieke prompt op.

**Parameters:**
- `prompt_id` (str): Unieke identifier van de prompt

**Returns:**
- `Prompt`: Het prompt object

**Raises:**
- `KeyError`: Als de prompt niet bestaat

##### `search_prompts(groep: int = None, domein: str = None, niveau: int = None) -> List[Prompt]`

Zoek prompts op basis van criteria.

**Parameters:**
- `groep` (int, optional): Groep nummer (3-8)
- `domein` (str, optional): Rekendomein
- `niveau` (int, optional): Moeilijkheidsniveau

**Returns:**
- `List[Prompt]`: Liste van matchende prompts

## OpgaveGenerator

### `OpgaveGenerator(model: str = "gpt-4")`

Generator voor rekenopdrachten.

#### Methods

##### `generate(prompt_id: str, **kwargs) -> Opgave`

Genereer een opdracht op basis van een prompt.

**Parameters:**
- `prompt_id` (str): ID van de prompt
- `**kwargs`: Parameters voor de prompt template

**Returns:**
- `Opgave`: Gegenereerde opdracht

##### `generate_batch(prompt_id: str, count: int, **kwargs) -> List[Opgave]`

Genereer meerdere opdrachten in één keer.

**Parameters:**
- `prompt_id` (str): ID van de prompt
- `count` (int): Aantal opdrachten
- `**kwargs`: Parameters voor de prompt template

**Returns:**
- `List[Opgave]`: Lijst van gegenereerde opdrachten

## AdaptiveSystem

### `AdaptiveSystem()`

Adaptief systeem voor moeilijkheidsgraad aanpassing.

#### Methods

##### `get_next_prompt(student_id: str, domein: str) -> str`

Bepaal de volgende prompt voor een leerling.

**Parameters:**
- `student_id` (str): Unieke identifier van de leerling
- `domein` (str): Rekendomein

**Returns:**
- `str`: ID van de geselecteerde prompt

##### `record_result(student_id: str, prompt_id: str, correct: bool) -> None`

Registreer een resultaat van een leerling.

**Parameters:**
- `student_id` (str): Unieke identifier van de leerling
- `prompt_id` (str): ID van de gebruikte prompt
- `correct` (bool): Of het antwoord correct was

## Data Models

### Prompt

```python
class Prompt(BaseModel):
    id: str
    titel: str
    groep: int
    domein: str
    niveau: int
    beschrijving: str
    system_prompt: str
    user_prompt_template: str
    parameters: List[PromptParameter]
```

### Opgave

```python
class Opgave(BaseModel):
    id: str
    prompt_id: str
    vraag: str
    antwoord: str
    toelichting: Optional[str]
    moeilijkheidsgraad: int
```
