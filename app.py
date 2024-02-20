import pathlib

import pandas as pd
import streamlit as st

from settings import ROOT
from src.calc import (
    calculate_modified_catch_rates,
    calculate_overall_catch_rate,
)
from src.misc import generate_pokemon_sav, get_all_pokemon, get_pokemon


def display_image(image_path: str) -> None:
    st.image(
        image_path,
        width=19,
        output_format='PNG',
    )


def main() -> None:
    if not pathlib.Path.exists(ROOT / 'pokemon_list.sav'):
        generate_pokemon_sav()

    pokemon_list = get_all_pokemon()

    labels = [''] + [
        f'{pokemon.dex_no} - {pokemon.name}' for pokemon in pokemon_list
    ]

    st.title('Catch Rate Calculator')

    pokemon_input_col, level_input_col = st.columns([3, 1])

    pokemon_input_text = pokemon_input_col.selectbox(
        label='Pokémon',
        options=labels,
        placeholder='Select a Pokémon',
    )
    level_input_text = int(
        level_input_col.number_input(
            label='Level',
            min_value=1,
            max_value=100,
            value=50,
            step=1,
        )
    )

    if pokemon_input_text and level_input_text:
        dex_no = int(pokemon_input_text.split(' - ')[0])

        pokemon = get_pokemon(dex_no, level_input_text)

        st.write(  # type: ignore
            f'Best catch rates for {pokemon.name} at level {pokemon.level}:'
        )

        stats = pd.DataFrame(
            columns=[
                'Image',
                'Poké Ball',
                'Condition',
                'Catch Rate',
            ]
        )

        for min_iv_scenario, min_iv_rate in calculate_modified_catch_rates(
            pokemon, pokemon.min_hp
        ):
            catch_rate = calculate_overall_catch_rate(min_iv_rate)

            stats.loc[len(stats)] = [
                f'<img src="{min_iv_scenario.poke_ball.image}" height="30" width="30" > ',
                min_iv_scenario.poke_ball.value,
                min_iv_scenario.condition,
                catch_rate * 100,
            ]

        stats = stats.sort_values(  # type: ignore
            by=['Catch Rate', 'Poké Ball', 'Condition'], ascending=False
        )

        st.markdown(stats.to_markdown(index=False, numalign='center', stralign='center'), unsafe_allow_html=True)


if __name__ == '__main__':
    main()
