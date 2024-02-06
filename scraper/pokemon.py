"""Defines a Pokémon class and its attributes."""
from dataclasses import dataclass

import pydantic


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


class Pokemon(pydantic.BaseModel):
    """Represents a Pokémon with various attributes."""

    dex_no: int
    name: str
    stats: PokemonStats
    ev_yield: PokemonStats
    gender_ratio: int
    catch_rate: int
    abilities: list[str]
    pokemon_type: list[str]
    exp_group: str
    egg_group: list[str]
    height: str
    weight: str
    color: str
    level_up_moves: list[PokemonMove]
    tm_learn: list[PokemonMove]
