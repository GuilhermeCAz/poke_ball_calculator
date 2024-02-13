import pathlib

from settings import ROOT
from src.calc import (
    calculate_critical_catch_odds,
    calculate_critical_catch_value,
    calculate_modified_catch_rates,
    calculate_shake_value,
    calculate_successful_catch_odds,
    calculate_successful_shake_odds,
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
        ccv = calculate_critical_catch_value(601, min_iv_rate)
        critical_catch_odds = calculate_critical_catch_odds(ccv)

        shake_value = calculate_shake_value(min_iv_rate)
        successful_shake_odds = calculate_successful_shake_odds(shake_value)

        successful_crit_catch_odds = (
            critical_catch_odds
            * calculate_successful_catch_odds(True, successful_shake_odds)
        )
        successful_non_crit_catch_odds = (
            1 - critical_catch_odds
        ) * calculate_successful_catch_odds(False, successful_shake_odds)

        print(
            min_iv_scenario.poke_ball.value,
            min_iv_scenario.condition,
            f'Crit: {critical_catch_odds*100:.4f}%',
            f'Caught with crit: {successful_crit_catch_odds*100:.4f}%',
            f'Caught without crit: {successful_non_crit_catch_odds*100:.4f}%',
            f'Not caught: '
            f'{(1-successful_crit_catch_odds-successful_non_crit_catch_odds)*100:.4f}%',
            sep=' | ',
        )

    # sorted_catch_rates = sorted(
    #     zip(min_catch_rate_scenarios, max_catch_rates_scenarios),
    #     key=lambda x: x[1].modified_catch_rate,
    #     reverse=True,
    # )


if __name__ == '__main__':
    main()
