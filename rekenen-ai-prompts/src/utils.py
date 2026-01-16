"""
Utils - Hulpfuncties voor het project.
"""

from typing import Dict, Any, List
from pathlib import Path
import yaml


def load_yaml_file(file_path: Path) -> Dict[str, Any]:
    """
    Laad een YAML bestand.

    Args:
        file_path: Pad naar het YAML bestand.

    Returns:
        Dictionary met de inhoud van het bestand.

    Raises:
        FileNotFoundError: Als het bestand niet bestaat.
        yaml.YAMLError: Als het bestand geen valide YAML is.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Bestand niet gevonden: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml_file(data: Dict[str, Any], file_path: Path) -> None:
    """
    Sla data op als YAML bestand.

    Args:
        data: Data om op te slaan.
        file_path: Pad waar het bestand moet worden opgeslagen.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)


def format_prompt_id(
    groep: int,
    domein_code: str,
    niveau: int,
    nummer: int
) -> str:
    """
    Formatteer een prompt ID volgens de standaard.

    Args:
        groep: Groep nummer (3-8).
        domein_code: Korte code voor het domein (bijv. "GB" voor getalbegrip).
        niveau: Niveau (1-3).
        nummer: Volgnummer (1-999).

    Returns:
        Geformatteerd ID, bijv. "G3_GB_N1_001".

    Example:
        >>> format_prompt_id(3, "GB", 1, 1)
        'G3_GB_N1_001'
    """
    if not 3 <= groep <= 8:
        raise ValueError(f"Groep moet tussen 3 en 8 zijn, is: {groep}")
    if not 1 <= niveau <= 3:
        raise ValueError(f"Niveau moet tussen 1 en 3 zijn, is: {niveau}")
    if not 1 <= nummer <= 999:
        raise ValueError(f"Nummer moet tussen 1 en 999 zijn, is: {nummer}")

    return f"G{groep}_{domein_code.upper()}_N{niveau}_{nummer:03d}"


def parse_prompt_id(prompt_id: str) -> Dict[str, Any]:
    """
    Parse een prompt ID naar zijn componenten.

    Args:
        prompt_id: Het prompt ID om te parsen.

    Returns:
        Dictionary met groep, domein_code, niveau, en nummer.

    Raises:
        ValueError: Als het ID niet het juiste format heeft.

    Example:
        >>> parse_prompt_id("G3_GB_N1_001")
        {'groep': 3, 'domein_code': 'GB', 'niveau': 1, 'nummer': 1}
    """
    import re
    pattern = r'^G([3-8])_([A-Z]+)_N([1-3])_(\d{3})$'
    match = re.match(pattern, prompt_id)

    if not match:
        raise ValueError(f"Ongeldige prompt ID: {prompt_id}")

    return {
        'groep': int(match.group(1)),
        'domein_code': match.group(2),
        'niveau': int(match.group(3)),
        'nummer': int(match.group(4)),
    }


def get_domein_codes() -> Dict[str, str]:
    """
    Haal een mapping op van domein codes naar volledige namen.

    Returns:
        Dictionary met domein codes als keys en volledige namen als values.
    """
    return {
        'GB': 'getalbegrip',
        'ST': 'strategieën',
        'BW': 'bewerkingen',
        'SR': 'schriftelijk_rekenen',
        'MT': 'meten',
        'GM': 'meetkunde',
        'VH': 'verhoudingen',
    }


def find_prompts_by_pattern(
    prompts_path: Path,
    groep: int = None,
    domein: str = None
) -> List[Path]:
    """
    Vind prompt bestanden op basis van een patroon.

    Args:
        prompts_path: Basis pad van de prompts directory.
        groep: Optioneel groep filter.
        domein: Optioneel domein filter.

    Returns:
        Lijst van Path objecten naar matchende prompt bestanden.
    """
    pattern = "**/*.yaml"
    all_files = list(prompts_path.glob(pattern))

    # Filter op basis van groep en domein
    filtered = []
    for file_path in all_files:
        include = True

        if groep is not None:
            if f"groep_{groep}" not in str(file_path):
                include = False

        if domein is not None:
            if domein not in str(file_path):
                include = False

        if include:
            filtered.append(file_path)

    return filtered
