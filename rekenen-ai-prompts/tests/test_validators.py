"""
Tests voor de validators.
"""

import pytest
from src.validators import PromptValidator, OpgaveValidator, ValidationResult
from src.prompt_library import Prompt, PromptParameter


class TestPromptValidator:
    """Test suite voor PromptValidator."""

    def test_validate_id_format_valid(self):
        """Test validatie van valide ID formats."""
        valid_ids = [
            "G3_GB_N1_001",
            "G8_ST_N3_999",
            "G5_BW_N2_042",
        ]
        for prompt_id in valid_ids:
            assert PromptValidator._validate_id_format(prompt_id)

    def test_validate_id_format_invalid(self):
        """Test validatie van invalide ID formats."""
        invalid_ids = [
            "G2_GB_N1_001",  # Groep te laag
            "G9_GB_N1_001",  # Groep te hoog
            "G3_GB_N4_001",  # Niveau te hoog
            "G3_GB_N1_1",    # Nummer te kort
            "g3_gb_n1_001",  # Lowercase
        ]
        for prompt_id in invalid_ids:
            assert not PromptValidator._validate_id_format(prompt_id)

    def test_validate_prompt_valid(self):
        """Test validatie van valide prompt."""
        prompt = Prompt(
            id="G3_GB_N1_001",
            titel="Test",
            groep=3,
            domein="getalbegrip",
            niveau=1,
            beschrijving="Test beschrijving",
            system_prompt="Test system prompt",
            user_prompt_template="Maak {aantal} opdrachten",
            parameters=[
                PromptParameter(name="aantal", type="integer", default=5)
            ]
        )
        result = PromptValidator.validate_prompt(prompt)
        assert result.is_valid

    def test_validate_prompt_invalid_groep(self):
        """Test validatie met ongeldige groep."""
        prompt = Prompt(
            id="G3_GB_N1_001",
            titel="Test",
            groep=2,  # Ongeldig
            domein="getalbegrip",
            niveau=1,
            beschrijving="Test",
            system_prompt="Test",
            user_prompt_template="Test"
        )
        result = PromptValidator.validate_prompt(prompt)
        assert not result.is_valid
        assert any("Groep" in error for error in result.errors)


class TestOpgaveValidator:
    """Test suite voor OpgaveValidator."""

    def test_validate_opgave_empty(self):
        """Test validatie van lege opgave."""
        result = OpgaveValidator.validate_opgave("")
        assert not result.is_valid

    def test_validate_opgave_too_short(self):
        """Test validatie van te korte opgave."""
        result = OpgaveValidator.validate_opgave("Test")
        assert len(result.warnings) > 0

    def test_validate_opgave_with_placeholder(self):
        """Test validatie van opgave met placeholder tekst."""
        result = OpgaveValidator.validate_opgave("TODO: Maak opgave")
        assert len(result.warnings) > 0

    def test_validate_answer_format_number_valid(self):
        """Test validatie van geldig nummer antwoord."""
        result = OpgaveValidator.validate_answer_format("42", "number")
        assert result.is_valid

    def test_validate_answer_format_number_invalid(self):
        """Test validatie van ongeldig nummer antwoord."""
        result = OpgaveValidator.validate_answer_format("abc", "number")
        assert not result.is_valid
