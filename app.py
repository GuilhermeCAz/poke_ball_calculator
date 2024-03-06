import asyncio
import pathlib

import pandas as pd
import streamlit as st

from models.poke_ball import PokeBall
from models.pokemon import Pokemon, PokemonStatus
from settings import CURRENT_LAST_DEX_NUMBER, ROOT
from src.calc import (
    calculate_modified_catch_rates,
    calculate_overall_catch_rate,
)
from src.misc import (
    generate_pokemon_sav,
    get_all_pokemon,
    get_pokemon_by_dex_no,
    get_pokemon_by_name,
)


def get_catch_rates(pokemon: Pokemon) -> pd.DataFrame:
    # add max_iv catch rates?
    catch_rates_data: list[dict] = []
    for min_iv_scenario, min_iv_rate in calculate_modified_catch_rates(
        pokemon, pokemon.min_hp
    ):
        catch_rate = calculate_overall_catch_rate(min_iv_rate)

        catch_rates_data.append(
            {
                'Image': f'<img src="{min_iv_scenario.poke_ball.image}"',
                'Poké Ball': min_iv_scenario.poke_ball.value,
                'Condition': min_iv_scenario.condition or '',
                'Catch Rate': catch_rate,
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
    )

    return sorted_catch_rates.drop(columns='Turns')


def style_catch_rates(catch_rates: pd.DataFrame) -> str:
    return catch_rates.to_html(
        index=False,
        float_format=lambda x: f'{x:.2%}',
        justify='center',
        classes='styled-table',
        escape=False,
    )


def set_basic_configuration() -> None:
    st.set_page_config(
        layout='wide',
        page_title='Pokémon Catch Rate Calculator',
        page_icon=PokeBall.LEVEL_BALL.image,
        initial_sidebar_state='collapsed',
    )

    with open(ROOT / 'css' / 'styles.css') as css:
        st.markdown(
            '<style>' + css.read() + '</style>', unsafe_allow_html=True
        )

    st.title('Catch Rate Calculator')

    if not pathlib.Path.exists(ROOT / 'data' / 'pokemon_list.sav'):
        asyncio.run(generate_pokemon_sav())


def set_pokemon_by_dex_no() -> None:
    dex_no = st.session_state.get('dex_no')
    if not dex_no:
        st.session_state['pokemon_name'] = None
        return

    pokemon = get_pokemon_by_dex_no(
        dex_no,
        int(st.session_state['level']),
    )
    st.session_state['pokemon'] = pokemon
    st.session_state['pokemon_name'] = pokemon.name


def set_pokemon_by_name() -> None:
    pokemon_name = st.session_state.get('pokemon_name')
    if not pokemon_name:
        st.session_state['dex_no'] = None
        return

    pokemon = get_pokemon_by_name(
        pokemon_name,
        int(st.session_state['level']),
    )
    st.session_state['pokemon'] = pokemon
    st.session_state['dex_no'] = pokemon.dex_no


def add_sidebar_widgets() -> None:
    st.sidebar.selectbox(
        label='Status',
        options=[
            f'{name.title()} ({enum.value/4096}x)'
            for name, enum in PokemonStatus.__members__.items()
        ],
        key='status',
        disabled=True,
    )
    st.sidebar.slider(
        label='HP',
        min_value=1,
        max_value=100,
        step=1,
        format=None,
        key='hp',
        help=None,
    )


def main() -> None:
    set_basic_configuration()
    pokemon_list = get_all_pokemon()

    image_columns = st.columns([3, 1, 3])
    image_box = image_columns[1].empty()

    form_columns = st.columns([4, 3, 5, 2, 5, 5])
    pokemon_names = [pokemon.name for pokemon in pokemon_list]

    form_columns[1].number_input(
        label='National Dex Number',
        min_value=1,
        max_value=CURRENT_LAST_DEX_NUMBER,
        value=None,
        step=1,
        key='dex_no',
        on_change=set_pokemon_by_dex_no,
    )

    form_columns[2].selectbox(
        label='Pokémon',
        options=[pokemon.name for pokemon in pokemon_list],
        index=None,
        key='pokemon_name',
        on_change=set_pokemon_by_name,
        placeholder='Select a Pokémon',
    )

    form_columns[3].number_input(
        label='Level',
        min_value=1,
        max_value=100,
        value=50,
        step=1,
        key='level',
    )

    form_box = form_columns[4].empty()
    form_box.selectbox(
        label='Form',
        options=[],
        disabled=True,
        help='You must select a Pokémon first.',
    )

    add_sidebar_widgets()

    pokemon: Pokemon | None = st.session_state.get('pokemon')

    if pokemon:
        form_box.selectbox(
            label='Form',
            options=[form.label for form in pokemon.forms],
            key='form',
        )

        image_box.image(pokemon.images[st.session_state['form']])

        catch_rates = get_catch_rates(pokemon)
        filtered_catch_rates = format_catch_rates(catch_rates)
        styled_catch_rates = style_catch_rates(filtered_catch_rates)

        data_columns = st.columns([1, 3, 1])

        data_columns[1].markdown(styled_catch_rates, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
