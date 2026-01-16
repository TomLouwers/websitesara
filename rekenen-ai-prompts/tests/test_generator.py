"""
Tests voor de OpgaveGenerator class.
"""

import pytest
from src.opgave_generator import OpgaveGenerator, Opgave
from src.prompt_library import PromptLibrary


class TestOpgaveGenerator:
    """Test suite voor OpgaveGenerator."""

    def test_init(self):
        """Test initialisatie van OpgaveGenerator."""
        generator = OpgaveGenerator()
        assert generator.library is not None

    def test_init_with_custom_library(self):
        """Test initialisatie met custom library."""
        library = PromptLibrary()
        generator = OpgaveGenerator(prompt_library=library)
        assert generator.library is library

    def test_generate_nonexistent_prompt(self):
        """Test genereren met niet-bestaande prompt."""
        generator = OpgaveGenerator()
        with pytest.raises(KeyError):
            generator.generate("NONEXISTENT")

    def test_generate_batch(self):
        """Test batch generatie."""
        # TODO: Mock een prompt en test batch generation
        pass

    def test_fill_parameters_with_defaults(self):
        """Test parameter filling met defaults."""
        # TODO: Test parameter filling logica
        pass

    def test_fill_parameters_missing_required(self):
        """Test dat error wordt gegeven bij missende required parameters."""
        # TODO: Test error handling voor missende parameters
        pass
