from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import re


@dataclass(frozen=True)
class Rule:
    code: str
    description: str
    pattern: re.Pattern
    severity: str  # "FAIL" or "WARN"


def _rx(s: str) -> re.Pattern:
    return re.compile(s, re.IGNORECASE | re.MULTILINE)


# Generic rules that prevent "easy-answer-in-prompt" and MCQ template traps
GENERIC_RULES: List[Rule] = [
    Rule(
        code="PROMPT-HINT-01",
        description="MCQ prompt bevat al het antwoord (woorden als 'handiger', 'beste', 'past hierbij') zonder extra discriminatie.",
        pattern=_rx(r"\b(handiger|beste|past hierbij|past hier|wat gebeurt hier)\b"),
        severity="WARN",
    ),
    Rule(
        code="MCQ-STATIC-OPTIONS-01",
        description="Kans op vaste MCQ-option-sets (meer/minder/evenveel/weet ik niet) zonder variatie.",
        pattern=_rx(r"\[\s*\"meer\"\s*,\s*\"minder\"\s*,\s*\"evenveel\""),
        severity="FAIL",
    ),
    Rule(
        code="N2-FORBIDDEN-EXPLAIN",
        description="N2 batch-prompt vraagt om uitleg/waarom of foutanalyse (verboden).",
        pattern=_rx(r"\b(leg uit|waarom|verklaar|analyseer|wat gaat er mis)\b"),
        severity="FAIL",
    ),
]

# Topic-specific extra checks (lightweight)
TOPIC_RULES: Dict[str, List[Rule]] = {
    # plattegronden-lezen: 'kaart' dominance risk
    "plattegronden-lezen": [
        Rule(
            code="CTX-DOM-KAART",
            description="Risico op context-dominance: 'kaart' te vaak in prompts.",
            pattern=_rx(r"\bkaart\b"),
            severity="WARN",
        )
    ],
    # breuken-vergelijken: risk of too few types
    "breuken-vergelijken": [
        Rule(
            code="BV-ONLY-GROTER",
            description="Risico: alleen 'Welke is groter?' -> duplicatie. Gebruik meerdere vraagtypes.",
            pattern=_rx(r"welke\s+is\s+groter\?"),
            severity="WARN",
        )
    ],
}

LEVEL_RULES: Dict[str, List[Rule]] = {
    "n2": [
        Rule(
            code="N2-NO-ERROR-ANALYSIS",
            description="N2: geen error_analysis/strategy_comparison in taskForm.",
            pattern=_rx(r"\"taskForm\"\s*:\s*\"(error_analysis|strategy_comparison|reasoned_explanation|explain_what_happens)\""),
            severity="FAIL",
        )
    ],
    "n3": [
        Rule(
            code="N3-NEED-VARIATION",
            description="N3 MCQ: verplicht meerdere MCQ-families / vraagtypes om duplicatie te voorkomen.",
            pattern=_rx(r"\bexact\s+\d+\s*×\s*type\s+[abc]\b"),
            severity="WARN",
        )
    ],
}


def get_rules(level: Optional[str], topic: Optional[str]) -> List[Rule]:
    rules: List[Rule] = []
    rules.extend(GENERIC_RULES)
    if level and level in LEVEL_RULES:
        rules.extend(LEVEL_RULES[level])
    if topic and topic in TOPIC_RULES:
        rules.extend(TOPIC_RULES[topic])
    return rules
