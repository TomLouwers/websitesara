"""
Prompt Library - Beheer en laden van prompt bestanden.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class PromptParameter(BaseModel):
    """Parameter definitie voor een prompt."""
    name: str
    type: str
    default: Optional[any] = None
    min: Optional[int] = None
    max: Optional[int] = None
    options: Optional[List[str]] = None


class PromptMetadata(BaseModel):
    """Metadata voor een prompt."""
    auteur: str = "System"
    versie: str = "1.0"
    laatst_bijgewerkt: str
    tags: List[str] = Field(default_factory=list)


class Prompt(BaseModel):
    """Representatie van een prompt."""
    id: str
    titel: str
    groep: int = Field(ge=3, le=8)
    domein: str
    niveau: int = Field(ge=1, le=3)
    beschrijving: str
    system_prompt: str
    user_prompt_template: str
    parameters: List[PromptParameter] = Field(default_factory=list)
    metadata: Optional[PromptMetadata] = None


class PromptLibrary:
    """Centrale bibliotheek voor het beheren van prompts."""

    def __init__(self, prompts_path: Optional[Path] = None):
        """
        Initialiseer de prompt library.

        Args:
            prompts_path: Pad naar de prompts directory. Indien None,
                         wordt de standaard 'prompts/' directory gebruikt.
        """
        self.prompts_path = prompts_path or Path(__file__).parent.parent / "prompts"
        self.prompts: Dict[str, Prompt] = {}

    def load_prompts(self, path: Optional[Path] = None) -> None:
        """
        Laad alle prompts uit een directory.

        Args:
            path: Pad naar de prompts directory. Gebruikt self.prompts_path indien None.

        Raises:
            ValidationError: Als een prompt niet valide is.
        """
        load_path = path or self.prompts_path

        if not load_path.exists():
            raise FileNotFoundError(f"Prompts directory niet gevonden: {load_path}")

        # Laad alle YAML bestanden recursief
        for yaml_file in load_path.rglob("*.yaml"):
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                prompt = Prompt(**data)
                self.prompts[prompt.id] = prompt

    def get_prompt(self, prompt_id: str) -> Prompt:
        """
        Haal een specifieke prompt op.

        Args:
            prompt_id: Unieke identifier van de prompt.

        Returns:
            Het prompt object.

        Raises:
            KeyError: Als de prompt niet bestaat.
        """
        if prompt_id not in self.prompts:
            raise KeyError(f"Prompt niet gevonden: {prompt_id}")
        return self.prompts[prompt_id]

    def search_prompts(
        self,
        groep: Optional[int] = None,
        domein: Optional[str] = None,
        niveau: Optional[int] = None,
    ) -> List[Prompt]:
        """
        Zoek prompts op basis van criteria.

        Args:
            groep: Groep nummer (3-8).
            domein: Rekendomein.
            niveau: Moeilijkheids niveau.

        Returns:
            Lijst van matchende prompts.
        """
        results = list(self.prompts.values())

        if groep is not None:
            results = [p for p in results if p.groep == groep]
        if domein is not None:
            results = [p for p in results if p.domein == domein]
        if niveau is not None:
            results = [p for p in results if p.niveau == niveau]

        return results

    def list_domains(self, groep: Optional[int] = None) -> List[str]:
        """
        Haal een lijst van alle beschikbare domeinen op.

        Args:
            groep: Optioneel, filter op groep.

        Returns:
            Lijst van unieke domein namen.
        """
        prompts = self.search_prompts(groep=groep)
        return sorted(set(p.domein for p in prompts))
