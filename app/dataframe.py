import pandas as pd

from app.config import get_battle_variables, get_game_variables
from models.pokemon import Pokemon
from src.calc import (
    calculate_modified_catch_rates,
    calculate_overall_catch_rate,
)


def get_catch_rates(pokemon: Pokemon) -> pd.DataFrame:
    # add max_iv catch rates  # to-do
    battle_variables = get_battle_variables(pokemon.min_hp)
    game_variables = get_game_variables()
    catch_rates_data: list[dict] = []
    for min_iv_scenario, min_iv_rate in calculate_modified_catch_rates(
        pokemon=pokemon,
        hp=pokemon.min_hp,
        battle_variables=battle_variables,
        game_variables=game_variables,
    ):
        catch_rate = calculate_overall_catch_rate(
            modified_catch_rate=min_iv_rate,
            registered_pokemon=game_variables.registered_pokemon,
            catching_charm=game_variables.catching_charm,
        )

        catch_rates_data.append(
            {
                'Image': f'<img src="{min_iv_scenario.poke_ball.image}"',
                'Poké Ball': min_iv_scenario.poke_ball.value,
                'Condition': min_iv_scenario.condition or '',
                'Catch Rate': catch_rate,
            }
        )
    return pd.DataFrame(catch_rates_data)


def format_catch_rates(catch_rates: pd.DataFrame) -> str:
    catch_rates['Turns'] = (
        catch_rates[catch_rates['Poké Ball'] == 'Timer Ball']['Condition']
        .str.extract(r'(\d+)')
        .astype(float)
    )

    min_turns: pd.DataFrame = catch_rates[
        (catch_rates['Poké Ball'] == 'Timer Ball')
        & (catch_rates['Catch Rate'] == 1)
    ]['Turns'].min()

    filtered_catch_rates = catch_rates[
        (catch_rates['Poké Ball'] != 'Timer Ball')
        | (
            (catch_rates['Poké Ball'] == 'Timer Ball')
            & (catch_rates['Turns'] <= min_turns)
        )
    ]

    sorted_catch_rates = filtered_catch_rates.sort_values(
        by=['Catch Rate', 'Poké Ball', 'Turns', 'Condition'], ascending=False
    ).drop(columns='Turns')

    return sorted_catch_rates.to_html(
        index=False,
        float_format=lambda x: f'{x:.2%}',
        justify='center',
        escape=False,
    )
