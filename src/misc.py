import pickle

from models.exceptions import InvalidLevelError, NoPokemonFoundError
from models.pokemon import Pokemon
from scraper import scraper
from settings import CURRENT_LAST_DEX_NUMBER, POKEMON_LEVEL_CAP


def generate_pokemon_sav() -> None:
    """Create list of Pokemon instances obtained from SciresM's GitHub Gist."""
    txt = scraper.get_txt()
    snippets = scraper.split_txt(txt)

    pokemon_list: list[Pokemon] = []
    for snippet in snippets:
        pokemon_list.append(scraper.parse_pokemon(snippet))

    with open('pokemon_list.sav', 'wb') as f:
        pickle.dump(pokemon_list, f)


def get_pokemon(dex_no: int, level: int) -> Pokemon:
    with open('pokemon_list.sav', 'rb') as f:
        pokemon_list = pickle.load(f)  # noqa: S301

    if not 1 <= level <= POKEMON_LEVEL_CAP:
        raise InvalidLevelError(level)

    if 1 <= dex_no <= CURRENT_LAST_DEX_NUMBER:
        for pokemon in pokemon_list:
            if pokemon.dex_no == dex_no:
                pokemon.level = level  # user input
                return pokemon

    raise NoPokemonFoundError(dex_no)


def get_all_pokemon() -> list[Pokemon]:
    with open('pokemon_list.sav', 'rb') as f:
        pokemon_list = pickle.load(f)  # noqa: S301

    return [
        pokemon
        for pokemon in pokemon_list
        if pokemon.dex_no <= CURRENT_LAST_DEX_NUMBER
    ]
