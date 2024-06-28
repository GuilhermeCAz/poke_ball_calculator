from typing import Any, cast
from urllib.parse import urljoin

import requests

PAYLOAD = {'limit': 10000}
BASE_API_URL = 'https://pokeapi.co/api/v2/'


def get_pages() -> dict[str, str]:
    response = requests.get(BASE_API_URL, timeout=1)
    return cast(dict[str, str], response.json())


def get_endpoint(endpoint: str) -> list[dict[str, str]]:
    pages = get_pages()
    response = requests.get(pages[endpoint], params=PAYLOAD, timeout=10)
    return cast(list[dict[str, str]], response.json()['results'])


def get_resource(endpoint: str, resource: int | str) -> dict[str, Any]:
    pages = get_pages()
    response = requests.get(
        urljoin(pages[endpoint], str(resource)),
        params=PAYLOAD,
        timeout=10,
    )
    return cast(dict[str, Any], response.json())


def get_pokemon_names() -> tuple[str, ...]:
    pokemon_species = get_endpoint('pokemon-species')
    return tuple(species['name'].title() for species in pokemon_species)
