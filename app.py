import pathlib
import re

import pandas as pd
import streamlit as st

from models.poke_ball import PokeBall
from models.pokemon import Pokemon
from settings import ROOT
from src.calc import (
    calculate_modified_catch_rates,
    calculate_overall_catch_rate,
)
from src.misc import generate_pokemon_sav, get_all_pokemon, get_pokemon


def get_image_labels(pokemon_images: list[str]) -> dict[str, str]:
    pattern = r'poke_capture_\d{4}_(\d{3})_(\w{2})_(\w)_\d{8}_f_(\w).png'
    image_labels: dict[str, str] = {}
    for image_url in pokemon_images:
        match = re.search(pattern, image_url)
        if match:
            form, gender, gmax, shiny = match.groups()
            label = f'Form {int(form) + 1}'
            if gender == 'fd':
                label += ' | ♀'
            elif gender == 'md':
                label += ' | ♂'
            if gmax == 'g':
                label += ' | Gmax'
            if shiny == 'r':
                label += ' | Shiny'
            image_labels[label] = image_url

    return image_labels


def get_catch_rates(pokemon: Pokemon) -> pd.DataFrame:
    catch_rates_data: list[dict] = []
    for min_iv_scenario, min_iv_rate in calculate_modified_catch_rates(
        pokemon, pokemon.min_hp
    ):
        catch_rate = calculate_overall_catch_rate(min_iv_rate)

        catch_rates_data.append(
            {
                'Image': min_iv_scenario.poke_ball.image,
                'Poké Ball': min_iv_scenario.poke_ball.value,
                'Condition': min_iv_scenario.condition,
                'Catch Rate': catch_rate * 100,
            }
        )
    return pd.DataFrame(catch_rates_data)


def format_catch_rates(catch_rates: pd.DataFrame) -> pd.DataFrame:
    catch_rates['Turns'] = (
        catch_rates[catch_rates['Poké Ball'] == 'Timer Ball']['Condition']
        .str.extract(r'(\d+)')
        .astype(float)
    )

    min_turns: pd.DataFrame = catch_rates[
        (catch_rates['Poké Ball'] == 'Timer Ball')
        & (catch_rates['Catch Rate'] == 100)  # noqa: PLR2004
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
    )

    return sorted_catch_rates.drop(columns='Turns')


def main() -> None:
    st.set_page_config(
        layout='wide',
        page_title='Pokémon Catch Rate Calculator',
        page_icon=PokeBall.LEVEL_BALL.image,
    )

    st.title('Catch Rate Calculator')

    if not pathlib.Path.exists(ROOT / 'pokemon_list.sav'):
        generate_pokemon_sav()

    pokemon_list = get_all_pokemon()

    form_columns = st.columns([6, 5, 2, 5, 5, 1])
    labels = [f'{pokemon.dex_no} - {pokemon.name}' for pokemon in pokemon_list]

    form_columns[1].selectbox(
        label='Pokémon',
        options=labels,
        index=None,
        key='pokémon',
        placeholder='Select a Pokémon',
    )

    form_columns[2].number_input(
        label='Level',
        min_value=1,
        max_value=100,
        value=50,
        step=1,
        key='level',
    )

    form_box = form_columns[3].empty()
    form_box.selectbox(
        label='Form',
        options=[],
        disabled=True,
        help='You must select a Pokémon first.',
    )

    while not (
        st.session_state.get('pokémon') and st.session_state.get('level')
    ):
        pass

    dex_no = int(st.session_state['pokémon'].split(' - ')[0])
    pokemon = get_pokemon(dex_no, int(st.session_state['level']))

    image_labels = get_image_labels(pokemon.images)

    form_box.selectbox(
        label='Form',
        options=image_labels.keys(),
        key='form',
    )

    image_columns = st.columns([3, 1, 3])
    image_columns[1].image(image_labels[st.session_state['form']])

    catch_rates = get_catch_rates(pokemon)
    filtered_catch_rates = format_catch_rates(catch_rates)

    st.dataframe(
        filtered_catch_rates,
        hide_index=True,
        column_config={
            'Image': st.column_config.ImageColumn(),
            'Catch Rate': st.column_config.NumberColumn(format='%.2f%%'),
        },
        use_container_width=True,
    )


if __name__ == '__main__':
    main()
