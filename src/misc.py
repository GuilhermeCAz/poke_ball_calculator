import pickle

import streamlit as st

from models.exceptions import InvalidLevelError, NoPokemonFoundError
from models.pokemon import Pokemon, PokemonForm, get_existing_forms_by_dex_no
from scraper import scraper
from settings import CURRENT_LAST_DEX_NUMBER, POKEMON_LEVEL_CAP, ROOT


async def generate_forms_sav() -> None:
    import pathlib

    if not pathlib.Path.exists(ROOT / 'data' / 'forms.sav'):
        forms_dict: dict[int, list[PokemonForm]] = {}
        for dex_no in range(1, CURRENT_LAST_DEX_NUMBER + 1):
            forms_dict[dex_no] = await get_existing_forms_by_dex_no(dex_no)

        with open(ROOT / 'data' / 'forms.sav', 'wb') as f:
            pickle.dump(forms_dict, f)


async def generate_pokemon_sav() -> None:
    """Create list of Pokemon instances obtained from SciresM's GitHub Gist."""

    with open(ROOT / 'data' / 'forms.sav', 'rb') as f:
        forms_dict = pickle.load(f)  # noqa: S301

    text = scraper.get_text()
    snippets = scraper.split_text(text)

    pokemon_list: list[Pokemon] = []
    for snippet in snippets[: len(forms_dict)]:
        pokemon = scraper.parse_pokemon(snippet, forms_dict)
        pokemon_list.append(pokemon)

    with open(ROOT / 'data' / 'pokemon_list.sav', 'wb') as f:
        pickle.dump(pokemon_list, f)


def get_pokemon_by_dex_no(dex_no: int, level: int) -> Pokemon | None:
    with open(ROOT / 'data' / 'pokemon_list.sav', 'rb') as f:
        pokemon_list = pickle.load(f)  # noqa: S301

    if not 1 <= level <= POKEMON_LEVEL_CAP:
        raise InvalidLevelError(level)

    if 1 <= dex_no <= CURRENT_LAST_DEX_NUMBER:
        for pokemon in pokemon_list:
            if pokemon.dex_no == dex_no:
                pokemon.level = level
                return pokemon

    return None
    # raise NoPokemonFoundError(dex_no)


def get_pokemon_by_name(name: str, level: int) -> Pokemon:
    with open(ROOT / 'data' / 'pokemon_list.sav', 'rb') as f:
        pokemon_list = pickle.load(f)  # noqa: S301

    if not 1 <= level <= POKEMON_LEVEL_CAP:
        raise InvalidLevelError(level)

    for pokemon in pokemon_list:
        if pokemon.name == name:
            pokemon.level = level
            return pokemon

    raise NoPokemonFoundError(name)


@st.cache_data
def get_all_pokemon() -> list[Pokemon]:
    with open(ROOT / 'data' / 'pokemon_list.sav', 'rb') as f:
        pokemon_list = pickle.load(f)  # noqa: S301

    return [
        pokemon
        for pokemon in pokemon_list
        if pokemon.dex_no <= CURRENT_LAST_DEX_NUMBER
    ]
