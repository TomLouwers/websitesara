"""
Validators - Validatie van prompts en gegenereerde opdrachten.
"""

from typing import List, Optional, Dict, Any
from pydantic import ValidationError
from .prompt_library import Prompt


class ValidationResult:
    """Resultaat van een validatie."""

    def __init__(self):
        self.is_valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def add_error(self, message: str) -> None:
        """Voeg een error toe."""
        self.is_valid = False
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        """Voeg een warning toe."""
        self.warnings.append(message)


class PromptValidator:
    """Validator voor prompt bestanden."""

    @staticmethod
    def validate_prompt(prompt: Prompt) -> ValidationResult:
        """
        Valideer een prompt op structuur en inhoud.

        Args:
            prompt: De te valideren prompt.

        Returns:
            ValidationResult met eventuele errors en warnings.
        """
        result = ValidationResult()

        # Valideer ID format
        if not PromptValidator._validate_id_format(prompt.id):
            result.add_error(
                f"Ongeldige ID format: {prompt.id}. "
                f"Verwacht format: G[3-8]_[DOMEIN]_N[1-3]_[NNN]"
            )

        # Valideer groep
        if not 3 <= prompt.groep <= 8:
            result.add_error(f"Groep moet tussen 3 en 8 zijn, is: {prompt.groep}")

        # Valideer niveau
        if not 1 <= prompt.niveau <= 3:
            result.add_error(f"Niveau moet tussen 1 en 3 zijn, is: {prompt.niveau}")

        # Valideer prompts zijn niet leeg
        if not prompt.system_prompt.strip():
            result.add_error("system_prompt mag niet leeg zijn")

        if not prompt.user_prompt_template.strip():
            result.add_error("user_prompt_template mag niet leeg zijn")

        # Valideer template parameters
        template_result = PromptValidator._validate_template_parameters(prompt)
        result.errors.extend(template_result.errors)
        result.warnings.extend(template_result.warnings)

        return result

    @staticmethod
    def _validate_id_format(prompt_id: str) -> bool:
        """
        Valideer of een prompt ID het juiste format heeft.

        Format: G[3-8]_[DOMEIN]_N[1-3]_[NNN]
        Bijvoorbeeld: G3_GB_N1_001
        """
        import re
        pattern = r'^G[3-8]_[A-Z]+_N[1-3]_\d{3}$'
        return bool(re.match(pattern, prompt_id))

    @staticmethod
    def _validate_template_parameters(prompt: Prompt) -> ValidationResult:
        """
        Valideer of alle parameters in de template gedefinieerd zijn.
        """
        result = ValidationResult()

        # Extract parameters uit template
        import re
        template = prompt.user_prompt_template
        template_params = set(re.findall(r'\{(\w+)\}', template))

        # Vergelijk met gedefinieerde parameters
        defined_params = {p.name for p in prompt.parameters}

        missing = template_params - defined_params
        unused = defined_params - template_params

        for param in missing:
            result.add_error(
                f"Parameter '{param}' gebruikt in template maar niet gedefinieerd"
            )

        for param in unused:
            result.add_warning(
                f"Parameter '{param}' gedefinieerd maar niet gebruikt in template"
            )

        return result


class OpgaveValidator:
    """Validator voor gegenereerde opdrachten."""

    @staticmethod
    def validate_opgave(opgave_text: str) -> ValidationResult:
        """
        Valideer een gegenereerde opdracht op kwaliteit.

        Args:
            opgave_text: De tekst van de opgave.

        Returns:
            ValidationResult met eventuele errors en warnings.
        """
        result = ValidationResult()

        # Basis checks
        if not opgave_text or not opgave_text.strip():
            result.add_error("Opgave is leeg")
            return result

        if len(opgave_text) < 10:
            result.add_warning("Opgave is erg kort (< 10 karakters)")

        # Check op ongewenste content
        forbidden_words = ["TODO", "placeholder", "example"]
        for word in forbidden_words:
            if word.lower() in opgave_text.lower():
                result.add_warning(
                    f"Opgave bevat placeholder tekst: '{word}'"
                )

        return result

    @staticmethod
    def validate_answer_format(answer: str, expected_type: str = "number") -> ValidationResult:
        """
        Valideer of een antwoord het juiste format heeft.

        Args:
            answer: Het te valideren antwoord.
            expected_type: Het verwachte type ("number", "text", "multiple_choice").

        Returns:
            ValidationResult met eventuele errors.
        """
        result = ValidationResult()

        if expected_type == "number":
            try:
                float(answer.replace(',', '.'))
            except ValueError:
                result.add_error(f"Antwoord '{answer}' is geen geldig getal")

        return result
