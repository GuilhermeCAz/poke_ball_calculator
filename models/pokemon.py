"""Defines a Pokémon class and its attributes."""

import asyncio
import contextlib
import itertools
import math
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, StrEnum, auto

import aiohttp
from pydantic import BaseModel

from models.exceptions import InexistentTypeError
from settings import ASSETS_URL, CURRENT_LAST_DEX_NUMBER

FORM_VARIANTS = tuple(str(i).zfill(3) for i in range(0, 18))
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

    @property
    def url(self) -> str:
        return f'{ASSETS_URL}/types/{self.value}.png'


def select_pokemon_type(type_str: str) -> PokemonType:
    for type_ in PokemonType:
        if type_str.lower() == type_.name.lower():
            return type_

    raise InexistentTypeError(type_str)


@dataclass
class PokemonEvolution:
    """Represents the data of a Pokémon evolution."""

    method: str
    level: int | None
    species: str
    item: str | None


@dataclass
class PokemonForm:
    dex_no: int
    number: str
    gender: str
    gmax: str
    shiny: str

    @property
    def url(self) -> str:
        return (
            f'{ASSETS_URL}/pokemon/poke_capture_{str(self.dex_no).zfill(4)}_'
            f'{self.number}_{self.gender}_{self.gmax}_'
            f'00000000_f_{self.shiny}.png'
        )

    @property
    def label(self) -> str:
        _label = f'Form {int(self.number) + 1}'
        if self.gender == 'fd':
            _label += ' | ♀'
        elif self.gender == 'md':
            _label += ' | ♂'
        if self.gmax == 'g':
            _label += ' | Gmax'
        if self.shiny == 'r':
            _label += ' | Shiny'

        return _label


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
    forms: list[PokemonForm]
    images: dict[str, str] = {}

    def model_post_init(self, __context) -> None:  # noqa: ANN001
        self.images = {form.label: form.url for form in self.forms}

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


async def check_image_existence(
    session: aiohttp.ClientSession, url: str
) -> bool:
    with contextlib.suppress(TimeoutError):
        async with session.get(url, timeout=10) as response:
            return response.ok

    return False


async def get_existing_forms_by_dex_no(dex_no: int) -> list[PokemonForm]:
    existing_forms: list[PokemonForm] = []

    for number in FORM_VARIANTS:
        forms: list[PokemonForm] = []
        for gender, gmax, shiny in itertools.product(
            GENDER_VARIANTS, GIGANTAMAX_VARIANTS, SHINY_VARIANTS
        ):
            form = PokemonForm(dex_no, number, gender, gmax, shiny)
            forms.append(form)

        async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(
                *[check_image_existence(session, form.url) for form in forms]
            )

        if not any(results):
            break

        existing_forms.extend(
            [
                form
                for form, exists in zip(forms, results, strict=False)
                if exists
            ]
        )

    return existing_forms


async def get_all_existing_forms() -> dict[int, list[PokemonForm]]:
    forms_dict = defaultdict(list)
    forms: list[PokemonForm] = []
    for dex_no in range(1, CURRENT_LAST_DEX_NUMBER + 1):
        for number in FORM_VARIANTS:
            for gender, gmax, shiny in itertools.product(
                GENDER_VARIANTS, GIGANTAMAX_VARIANTS, SHINY_VARIANTS
            ):
                form = PokemonForm(dex_no, number, gender, gmax, shiny)
                forms.append(form)

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[check_image_existence(session, form.url) for form in forms],
            return_exceptions=True,
        )

    for form, exists in zip(forms, results, strict=False):
        if exists:
            forms_dict[form.dex_no].append(form)

    return dict(forms_dict)
