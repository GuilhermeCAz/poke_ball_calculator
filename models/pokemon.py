"""Defines a Pokémon class and its attributes."""
import math
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum, auto

from pydantic import BaseModel

from models.exceptions import InexistentTypeError


@dataclass
class PokemonStats:
    """Represents the base stats of a Pokémon."""

    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


@dataclass
class PokemonMove:
    """Represents a move that a Pokémon can learn."""

    name: str
    tm: int | None = None


class PokemonType(StrEnum):
    """Represents a Pokémon type."""

    NORMAL = auto()
    FIRE = auto()
    WATER = auto()
    ELECTRIC = auto()
    GRASS = auto()
    ICE = auto()
    FIGHTING = auto()
    POISON = auto()
    GROUND = auto()
    FLYING = auto()
    PSYCHIC = auto()
    BUG = auto()
    ROCK = auto()
    GHOST = auto()
    DRAGON = auto()
    DARK = auto()
    STEEL = auto()
    FAIRY = auto()


class PokemonGender(StrEnum):
    """Represents the possible genders of a Pokémon."""

    MALE = auto()
    FEMALE = auto()
    UNKNOWN = auto()


@dataclass
class PokemonEvolution:
    """Represents the data of a Pokémon evolution."""

    method: str
    level: int | None
    species: str
    item: str | None


class Pokemon(BaseModel):
    """Represents a Pokémon with various attributes."""

    dex_no: int
    name: str
    stats: PokemonStats
    ev_yield: PokemonStats
    gender_ratio: int
    catch_rate: int
    abilities: list[str]
    types: list[PokemonType]
    exp_group: str
    egg_group: list[str]
    height: Decimal
    weight: Decimal
    color: str
    level_up_moves: list[PokemonMove]
    tm_learn_moves: list[PokemonMove]
    evolution: PokemonEvolution | None = None
    level: int = 1

    def _get_hp_by_iv(self, iv: int) -> int:
        return (
            math.floor(((2 * self.stats.hp + iv) * self.level) / 100)
            + self.level
            + 10
        )

    @property
    def min_hp(self) -> int:
        return self._get_hp_by_iv(0)

    @property
    def max_hp(self) -> int:
        return self._get_hp_by_iv(31)


def select_pokemon_type(type_str: str) -> PokemonType:
    for type_ in PokemonType:
        if type_str.lower() == type_.value:
            return type_

    raise InexistentTypeError(type_str)
