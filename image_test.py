import math
import pathlib
from typing import NamedTuple

from PIL import Image

from models.exceptions import NoPaletteFoundError
from src.calc import calculate_modified_catch_rates
from src.misc import get_pokemon


class RGBA(NamedTuple):
    r: int
    g: int
    b: int
    a: int


class Color(NamedTuple):
    count_: int
    rgba: RGBA


def euclidean_distance(rgba1: RGBA, rgba2: RGBA) -> float:
    """Calculate the Euclidean distance between two colors RGBs."""
    return math.sqrt(
        (rgba1.r - rgba2.r) ** 2
        + (rgba1.g - rgba2.g) ** 2
        + (rgba1.b - rgba2.b) ** 2
    )


def get_weighted_color_similarity(
    colors1: list[Color], colors2: list[Color]
) -> float:
    total_diff = 0.0
    used_indices: set[int] = set()
    color_combos: list[tuple[Color, Color]] = []

    for color1 in colors1:
        matching_index = None
        lowest_diff = float('inf')

        for index, color2 in enumerate(colors2):
            if index in used_indices:
                continue

            diff = euclidean_distance(color1.rgba, color2.rgba)

            if diff <= lowest_diff:
                lowest_diff = diff
                matching_index = index

        if matching_index is None:
            raise Exception  # noqa: TRY002

        color_combos.append((color1, colors2[matching_index]))
        used_indices.add(matching_index)
        total_diff += lowest_diff

    return total_diff / len(color_combos)


def get_predominant_colors(
    image_path: pathlib.Path,
) -> list[Color]:
    """
    Get list of most predominant colors on image, excluding transparent ones.

    Arguments:
        image_path: path to the image.

    Raises:
        NoPaletteFoundError: Error raised to avoid images without palettes.
    """
    with Image.open(image_path) as image:
        quantized_image = image.quantize(colors=6)

        colors_rank = quantized_image.getcolors()
        palette = quantized_image.getpalette(rawmode='RGBA')

        if not palette:
            raise NoPaletteFoundError(image_path)

        colors_rgba = [
            RGBA(*palette[i : i + 4]) for i in range(0, len(palette), 4)
        ]

        return [
            Color(amount, colors_rgba[index])
            for amount, index in colors_rank
            if colors_rgba[index].a != 0
        ]


def main() -> None:
    pokemon = get_pokemon(dex_no=443, level=100)
    pokemon_colors = get_predominant_colors(pokemon.images[0])
    print(f'Best scenarios for {pokemon.name} at level {pokemon.level}:')
    min_weight = float('inf')
    min_ball = None
    for min_iv_scenario, _min_iv_rate in calculate_modified_catch_rates(
        pokemon, pokemon.min_hp
    ):
        pokeball_colors = get_predominant_colors(
            min_iv_scenario.poke_ball.image
        )

        weight = get_weighted_color_similarity(pokemon_colors, pokeball_colors)
        if weight < min_weight:
            min_weight = weight
            min_ball = min_iv_scenario.poke_ball.value

    print(min_weight, min_ball)


if __name__ == '__main__':
    main()
