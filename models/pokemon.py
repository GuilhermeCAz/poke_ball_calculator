"""Defines a Pokémon class and its attributes."""
import asyncio
import contextlib
import itertools
import math
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, StrEnum, auto

import aiohttp
from pydantic import BaseModel

from models.exceptions import InexistentTypeError
from settings import ASSETS_URL

FORM_VARIANTS = tuple(str(i).zfill(3) for i in range(0, 20))
GENDER_VARIANTS = ('uk', 'mf', 'fd', 'md', 'fo', 'mo')
GIGANTAMAX_VARIANTS = ('n', 'g')
SHINY_VARIANTS = ('n', 'r')


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

    @property
    def images(self) -> list[str]:
        return asyncio.run(self.get_images())

    async def get_images(self) -> list[str]:
        image_urls = self.generate_image_urls()
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.check_image_existence(session, image_url)
                for image_url in image_urls
            ]
            results = await asyncio.gather(*tasks)
            return [url for url, exists in zip(image_urls, results) if exists]

    async def check_image_existence(
        self, session: aiohttp.ClientSession, url: str
    ) -> bool:
        with contextlib.suppress(TimeoutError):
            async with session.get(url, timeout=30) as response:
                if response.ok:
                    return True

        return False

    def generate_image_urls(self) -> list[str]:
        image_urls: list[str] = []
        for form, gender, gmax, shiny in itertools.product(
            FORM_VARIANTS, GENDER_VARIANTS, GIGANTAMAX_VARIANTS, SHINY_VARIANTS
        ):
            filename = (
                f'poke_capture_{str(self.dex_no).zfill(4)}_'
                f'{form}_{gender}_{gmax}_00000000_f_{shiny}.png'
            )
            image_url = f'{ASSETS_URL}/pokemon/{filename}'
            image_urls.append(image_url)

        return image_urls


def select_pokemon_type(type_str: str) -> PokemonType:
    for type_ in PokemonType:
        if type_str.lower() == type_.value:
            return type_

    raise InexistentTypeError(type_str)
