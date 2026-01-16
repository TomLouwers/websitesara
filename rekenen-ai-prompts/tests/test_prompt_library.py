"""
Tests voor de PromptLibrary class.
"""

import pytest
from pathlib import Path
from src.prompt_library import PromptLibrary, Prompt


class TestPromptLibrary:
    """Test suite voor PromptLibrary."""

    def test_init(self):
        """Test initialisatie van PromptLibrary."""
        library = PromptLibrary()
        assert library.prompts == {}
        assert library.prompts_path is not None

    def test_init_with_custom_path(self, tmp_path):
        """Test initialisatie met custom path."""
        library = PromptLibrary(prompts_path=tmp_path)
        assert library.prompts_path == tmp_path

    def test_load_prompts_nonexistent_path(self, tmp_path):
        """Test laden van prompts uit niet-bestaande directory."""
        library = PromptLibrary(prompts_path=tmp_path / "nonexistent")
        with pytest.raises(FileNotFoundError):
            library.load_prompts()

    def test_get_prompt_not_found(self):
        """Test ophalen van niet-bestaande prompt."""
        library = PromptLibrary()
        with pytest.raises(KeyError):
            library.get_prompt("NONEXISTENT")

    def test_search_prompts_empty_library(self):
        """Test zoeken in lege library."""
        library = PromptLibrary()
        results = library.search_prompts(groep=3)
        assert results == []

    def test_search_prompts_by_groep(self):
        """Test zoeken op groep."""
        library = PromptLibrary()
        # TODO: Add test prompts and verify filtering
        pass

    def test_list_domains(self):
        """Test ophalen van domein lijst."""
        library = PromptLibrary()
        domains = library.list_domains()
        assert isinstance(domains, list)
