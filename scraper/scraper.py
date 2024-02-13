"""Gets all Pokémon information from SciresM's GitHub Gist."""
import contextlib
import re
from decimal import Decimal

import requests

from models.exceptions import NoMatchFoundError
from models.pokemon import (
    Pokemon,
    PokemonEvolution,
    PokemonMove,
    PokemonStats,
    select_pokemon_type,
)

BASE_URL: str = 'https://gist.githubusercontent.com/'
GIST_USERNAME: str = 'SciresM'
GIST_ID: str = 'a1a0c2e48ae5ca58a0ecd131bb7f7845'
GIST_COMMIT_ID: str = 'f7d5d4fc4c0de9420030421aa8d8b64fc5dbca22'
GIST_FILE_NAME: str = 'personal.txt'

URL: str = (
    f'{BASE_URL}/{GIST_USERNAME}/{GIST_ID}/raw/'
    f'{GIST_COMMIT_ID}/{GIST_FILE_NAME}'
)


def get_txt() -> str:
    """Extract text from SciresM's GitHub Gist."""
    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    return response.text


def split_txt(input_str: str) -> list[str]:
    """
    Split text by Pokémon delimiter (======).

    Arguments:
    ---------
        input_str: string containing entire collection of Pokémon attributes.

    Returns:
    -------
        List of snippets with Pokémon attributes.

    """
    return re.split(r'\n\n======\n', input_str)[1:]


def parse_pokemon(snippet: str) -> Pokemon:
    """
    Extract and format data in the snippet.

    Arguments:
    ---------
        snippet: string containing attributes of only one Pokémon.

    Returns:
    -------
        Instance of Pokemon class, which contains all its attributes.

    """

    def extract_groups(pattern: str, split: bool = True) -> list[str]:
        """
        Search for attributes in snippet using RegEx.

        Arguments:
        ---------
            pattern: RegEx pattern to search in snippet.

        Raises:
        ------
            NoMatchFoundError: No matches found for RegEx pattern used.

        Returns:
        -------
            List of attributes that match the RegEx pattern.

        """
        matches = re.search(pattern, snippet)
        if not matches:
            raise NoMatchFoundError

        groups: list[str] = []
        for group in matches.groups():
            if split:
                split_groups = [
                    attr.strip()
                    for attr in re.split(
                        r'[\.|\/](?!\d{1,2}[a-zA-Z]{1,2})', group
                    )
                ]
                groups.extend(split_groups)
            else:
                groups.append(group)

        return groups

    dex_no_str, name, _stage = extract_groups(
        r'(\d{1,5}) - (.*?) (?:\w{0,1}#.*? ){0,1}\(Stage: (\d+)\)'
    )

    stats_str = extract_groups(r'Base Stats: (.+) \(BST: \d+\)')
    ev_yield_str = extract_groups(r'EV Yield: (.+)')
    (gender_ratio_str,) = extract_groups(r'Gender Ratio: (\d+)')
    (catch_rate_str,) = extract_groups(r'Catch Rate: (\d+)')
    abilities = extract_groups(r'Abilities: (.+)')
    types = [
        select_pokemon_type(type_) for type_ in extract_groups(r'Type: (.+)')
    ]
    (exp_group,) = extract_groups(r'EXP Group: (.+)')
    egg_group = extract_groups(r'Egg Group: (.+)')
    height_str, weight_str, color = extract_groups(
        r'Height: (\S+)m, Weight: (\S+)kg, Color: (.+)', split=False
    )
    dex_no = int(dex_no_str)
    stats = PokemonStats(*[int(attr) for attr in stats_str])
    ev_yield = PokemonStats(*[int(attr) for attr in ev_yield_str])
    gender_ratio = int(gender_ratio_str)
    catch_rate = int(catch_rate_str)
    height = Decimal(height_str)
    weight = Decimal(weight_str)

    level_up_moves = [
        PokemonMove(move) for move in re.findall(r'- \[\d+\] (.+)', snippet)
    ]
    # Level Up Moves:((?:\n- \[\d+\].+)+)

    tm_learn_moves = [
        PokemonMove(move, int(tm))
        for tm, move in re.findall(r'- \[TM(\d+)\] (.+)', snippet)
    ]

    _egg_moves = ...  # to-do: ends up on level_up_moves
    _reminder_moves = ...  # to-do: ends up on level_up_moves

    evolution = None
    with contextlib.suppress(NoMatchFoundError):
        method, level_str, species, item_str = extract_groups(
            r'Evolves into (.+) @ lv(\d{1,3}) \((.+)\) \[(.+)\]'
        )
        level = int(level_str) or None
        item = item_str if item_str != '0' else None
        if method and species and (level or item):
            evolution = PokemonEvolution(method, level, species, item)

    return Pokemon(
        dex_no=dex_no,
        name=name,
        stats=stats,
        ev_yield=ev_yield,
        gender_ratio=gender_ratio,
        catch_rate=catch_rate,
        abilities=abilities,
        types=types,
        exp_group=exp_group,
        egg_group=egg_group,
        height=height,
        weight=weight,
        color=color,
        level_up_moves=level_up_moves,
        tm_learn_moves=tm_learn_moves,
        evolution=evolution,
    )


def main() -> None:
    """Create list of Pokemon instances obtained from SciresM's GitHub Gist."""
    txt = get_txt()
    snippets = split_txt(txt)

    pokemon_list: list[Pokemon] = []
    for snippet in snippets:
        pokemon_list.append(parse_pokemon(snippet))

    import pickle

    with open('pokemon_list.sav', 'wb') as f:
        pickle.dump(pokemon_list, f)


if __name__ == '__main__':
    main()