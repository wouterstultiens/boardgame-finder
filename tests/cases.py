# tests/cases.py
from dataclasses import dataclass
from typing import List, Dict

@dataclass(frozen=True)
class PromptTestCase:
    name: str
    title: str
    description: str
    expected: List[Dict[str, str]]  # [{"name": "...", "lang": "nl"|"en"|"unknown"}]


TEST_CASES: List[PromptTestCase] = [
    PromptTestCase(
        name="nl_auto_quiz",
        title="Auto Quiz",
        description="Leuk familiespel voor onderweg! Auto quiz van king. Inclusief cd. Perfect voor lange autoritten. Conditie: nieuw.",
        expected=[{"name": "Auto Quiz", "lang": "nl"}],
    ),
    PromptTestCase(
        name="nl_oud_hollands_memory",
        title="Mooi Oud Hollands Memory 50er/60er jaren spel",
        description="Het memory spel is compleet en in mooie staat. Zie mijn andere advertenties voor meer spullen.",
        expected=[{"name": "Oud Hollands Memory", "lang": "nl"}],
    ),
    PromptTestCase(
        name="nl_spokentrap",
        title="Spokentrap, goede staat",
        description="Compleet",
        expected=[{"name": "Spokentrap", "lang": "nl"}],
    ),
]
