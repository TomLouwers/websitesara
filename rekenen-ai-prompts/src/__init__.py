"""
Rekenen AI Prompts - Een bibliotheek voor het genereren van rekenopdrachten.
"""

__version__ = "0.1.0"

from .prompt_library import PromptLibrary
from .opgave_generator import OpgaveGenerator
from .adaptive_system import AdaptiveSystem

__all__ = [
    "PromptLibrary",
    "OpgaveGenerator",
    "AdaptiveSystem",
]
