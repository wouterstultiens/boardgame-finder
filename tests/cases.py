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
    PromptTestCase(
        name="nl_empty",
        title="200 spellen nieuw in doos",
        description="De opbrengst van de verkoop is voor mijn dochter die voor de world jamboree (scouting) aan het sparen isde opbrengst van de verkoo",
        expected=[{"name": "", "lang": "unknown"}],
    ),
    PromptTestCase(
        name="nl_roemrijke_ridders",
        title="Roemrijke Ridders - HABA",
        description="Aangeboden een mooi vormgegeven spel roemrijke ridders van haba. Het spel is compleet en in goede staat",
        expected=[{"name": "Roemrijke Ridders", "lang": "nl"}],
    ),
    PromptTestCase(
        name="nl_land_in_zicht",
        title="Land in Zicht - 999 Games",
        description="Het spel is compleet en in nette staat. Een mooi bordspel van 999 games. Lichte gebruikssporen op de doos.",
        expected=[{"name": "Land in Zicht", "lang": "nl"}],
    ),
    PromptTestCase(
        name="nl_stratego_scifi",
        title="Stratego Sci-Fi",
        description="Een variant op het bekende bordspel stratego: scifi editie. Het spel is compleet en de onderdelen zijn in keurige nette staat. De ",
        expected=[{"name": "Stratego Sci-Fi", "lang": "en"}],
    )
]
