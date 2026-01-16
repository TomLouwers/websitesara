"""
Opgave Generator - Genereert concrete opdrachten op basis van prompts.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from .prompt_library import Prompt, PromptLibrary


class Opgave(BaseModel):
    """Representatie van een gegenereerde opdracht."""
    id: str
    prompt_id: str
    vraag: str
    antwoord: Optional[str] = None
    toelichting: Optional[str] = None
    moeilijkheidsgraad: int


class OpgaveGenerator:
    """Generator voor rekenopdrachten op basis van prompts."""

    def __init__(self, prompt_library: Optional[PromptLibrary] = None):
        """
        Initialiseer de opgave generator.

        Args:
            prompt_library: Een PromptLibrary instantie. Indien None wordt
                          een nieuwe aangemaakt.
        """
        self.library = prompt_library or PromptLibrary()
        if not self.library.prompts:
            self.library.load_prompts()

    def generate(
        self,
        prompt_id: str,
        **kwargs: Any
    ) -> Opgave:
        """
        Genereer een opdracht op basis van een prompt.

        Args:
            prompt_id: ID van de prompt om te gebruiken.
            **kwargs: Parameters voor de prompt template.

        Returns:
            Een gegenereerde Opgave.

        Raises:
            KeyError: Als de prompt niet bestaat.
        """
        prompt = self.library.get_prompt(prompt_id)

        # Vul parameters in met defaults indien niet opgegeven
        params = self._fill_parameters(prompt, kwargs)

        # Format de user prompt met parameters
        user_prompt = prompt.user_prompt_template.format(**params)

        # Hier zou de daadwerkelijke AI call komen
        # Voor nu een placeholder implementatie
        opgave = Opgave(
            id=f"{prompt_id}_001",
            prompt_id=prompt_id,
            vraag="Placeholder vraag - hier komt AI gegenereerde content",
            antwoord="Placeholder antwoord",
            moeilijkheidsgraad=prompt.niveau
        )

        return opgave

    def generate_batch(
        self,
        prompt_id: str,
        count: int,
        **kwargs: Any
    ) -> List[Opgave]:
        """
        Genereer meerdere opdrachten in één keer.

        Args:
            prompt_id: ID van de prompt om te gebruiken.
            count: Aantal opdrachten om te genereren.
            **kwargs: Parameters voor de prompt template.

        Returns:
            Lijst van gegenereerde Opgave objecten.
        """
        return [
            self.generate(prompt_id, **kwargs)
            for _ in range(count)
        ]

    def _fill_parameters(
        self,
        prompt: Prompt,
        provided_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Vul parameters in met defaults waar nodig.

        Args:
            prompt: De prompt met parameter definities.
            provided_params: Door gebruiker opgegeven parameters.

        Returns:
            Complete set van parameters.
        """
        params = {}

        for param_def in prompt.parameters:
            if param_def.name in provided_params:
                params[param_def.name] = provided_params[param_def.name]
            elif param_def.default is not None:
                params[param_def.name] = param_def.default
            else:
                raise ValueError(
                    f"Vereiste parameter '{param_def.name}' niet opgegeven"
                )

        return params
