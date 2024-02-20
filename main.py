import pathlib

from settings import ROOT
from src.calc import (
    calculate_modified_catch_rates,
    calculate_overall_catch_rate,
)
from src.misc import generate_pokemon_sav, get_pokemon


def main() -> None:
    if not pathlib.Path.exists(ROOT / 'pokemon_list.sav'):
        generate_pokemon_sav()

    pokemon = get_pokemon(dex_no=23, level=100)
    print(f'Best scenarios for {pokemon.name} at level {pokemon.level}:')

    for min_iv_scenario, min_iv_rate in calculate_modified_catch_rates(
        pokemon, pokemon.min_hp
    ):
        catch_rate = calculate_overall_catch_rate(min_iv_rate)

        print(
            min_iv_scenario.poke_ball.value,
            min_iv_scenario.condition,
            f'Catch Rate: {catch_rate*100:.4f}%',
        )

    # sorted_catch_rates = sorted(
    #     zip(min_catch_rate_scenarios, max_catch_rates_scenarios),
    #     key=lambda x: x[1].modified_catch_rate,
    #     reverse=True,
    # )


if __name__ == '__main__':
    main()
