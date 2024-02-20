"""Defines a Pokéball class and its attributes."""
from enum import StrEnum, auto

from settings import ROOT


class PokeBall(StrEnum):
    POKÉ_BALL = auto()
    GREAT_BALL = auto()
    ULTRA_BALL = auto()
    MASTER_BALL = auto()
    SAFARI_BALL = auto()
    FAST_BALL = auto()
    LEVEL_BALL = auto()
    LURE_BALL = auto()
    HEAVY_BALL = auto()
    LOVE_BALL = auto()
    FRIEND_BALL = auto()
    MOON_BALL = auto()
    SPORT_BALL = auto()
    NET_BALL = auto()
    NEST_BALL = auto()
    REPEAT_BALL = auto()
    TIMER_BALL = auto()
    LUXURY_BALL = auto()
    PREMIER_BALL = auto()
    DIVE_BALL = auto()
    DUSK_BALL = auto()
    HEAL_BALL = auto()
    QUICK_BALL = auto()
    CHERISH_BALL = auto()
    PARK_BALL = auto()
    DREAM_BALL = auto()
    BEAST_BALL = auto()
    STRANGE_BALL = auto()

    def __init__(self, value: str) -> None:
        self._value_ = value.replace('_', ' ').title()
        self.image = (
            ROOT / 'assets' / 'items' / f'{value.lower()}.png'
        )  # .relative_to(ROOT)
