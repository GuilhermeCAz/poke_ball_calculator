import math
from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from typing import Any

from settings import ASSETS_URL
from src.api import get_resource


class PokemonSprites:
    def __init__(self, sprites: dict[str, Any]) -> None:
        self.home = HomeSprites(sprites['other']['home'])
        self.official_artwork = OfficialArtworkSprites(
            sprites['other']['official-artwork'],
        )


class HomeSprites:
    def __init__(self, sprites: dict[str, Any]) -> None:
        self.default = sprites['front_default']
        self.female = sprites['front_female']
        self.shiny = sprites['front_shiny']
        self.shiny_female = sprites['front_shiny_female']


class OfficialArtworkSprites:
    def __init__(self, sprites: dict[str, Any]) -> None:
        self.default = sprites['front_default']
        self.shiny = sprites['front_shiny']


@dataclass
class PokemonStats:
    """Represents the base stats of a Pokémon."""

    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


class PokemonStatus(Enum):
    """Represents the statuses a Pokémon might have and their catch bonus."""

    ASLEEP = 10240
    FROZEN = 10240
    BURNED = 6144
    PARALYZED = 6144
    POISONED = 6144


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

    @property
    def url(self) -> str:
        return f'{ASSETS_URL}/types/{self.value}.png'


class PokemonSpecies:
    def __init__(self, species_id: str | int, level: int = 1) -> None:
        self.species_page = get_resource('pokemon-species', species_id)
        self.level = level
        self.dex_no: int = self.species_page['id']
        self.name: str = self.species_page['name']
        self.catch_rate: int = self.species_page['capture_rate']
        self.evolution_chain: str = self.species_page['evolution_chain']['url']
        self.gender_rate: int = self.species_page['gender_rate']
        self.has_gender_differences: bool = self.species_page[
            'has_gender_differences'
        ]
        self.pokedex_numbers: list[dict[str, Any]] = self.species_page[
            'pokedex_numbers'
        ]
        self.varieties: list[dict[str, Any]] = self.species_page['varieties']

        self.evolution = None


class Pokemon(PokemonSpecies):
    def __init__(self, form_id: str | int, level: int = 1) -> None:
        self.form_page = get_resource('pokemon', form_id)
        self.abilities: list[dict[str, Any]] = self.form_page['abilities']
        self.height: float = self.form_page['height'] / 10  # meters
        self.moves = self.form_page['moves']
        self.sprites = PokemonSprites(self.form_page['sprites'])
        self.stats = PokemonStats(
            *[stat['base_stat'] for stat in self.form_page['stats']],
        )
        self.types = [
            PokemonType[entry['type']['name'].upper()]
            for entry in self.form_page['types']
        ]
        self.weight: float = self.form_page['weight'] / 10  # meters

        super().__init__(self.form_page['species']['name'], level)

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
