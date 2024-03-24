from typing import TYPE_CHECKING

import streamlit as st

from app.config import (
    set_basic_configuration,
    set_pokemon_by_dex_no,
    set_pokemon_by_name,
    set_pokemon_level,
)
from app.dataframe import format_catch_rates, get_catch_rates
from app.sidebar import add_sidebar_widgets
from settings import CURRENT_LAST_DEX_NUMBER
from src.api import get_pokemon_names

if TYPE_CHECKING:
    from models.pokemon import Pokemon


def main() -> None:
    set_basic_configuration()
    add_sidebar_widgets()

    image_columns = st.columns([1, 1, 1, 1, 1])
    image_box = image_columns[2].empty()

    type_columns = st.columns([5, 1, 5])
    type_box = type_columns[1].empty()

    form_columns = st.columns([1, 4, 1])

    form_columns[1].number_input(
        label='National Dex Number',
        min_value=1,
        max_value=CURRENT_LAST_DEX_NUMBER,
        value=None,
        step=1,
        key='dex_no',
        help='Some Pokémon are not available to catch on Scarlet/Violet. '
        'Their catch rates are only hypothetical, based on previous games.',
        on_change=set_pokemon_by_dex_no,
    )

    form_columns[1].selectbox(
        label='Pokémon Name',
        options=get_pokemon_names(),
        index=None,
        key='pokemon_name',
        on_change=set_pokemon_by_name,
        placeholder='Select a Pokémon',
    )

    form_columns[1].number_input(
        label='Level',
        min_value=1,
        max_value=100,
        value=50,
        step=1,
        key='level',
        on_change=set_pokemon_level,
    )
    button_box = form_columns[1].empty()
    button_box.button(
        label='Calculate',
        help='You must select a Pokémon first.',
        disabled=True,
        use_container_width=True,
    )

    pokemon: Pokemon | None = st.session_state.get('pokemon')

    if pokemon:
        image_box.image(pokemon.sprites.official_artwork.default)
        type_box.image([type_.url for type_ in pokemon.types])

        button_box.button(
            label='Calculate',
            key='calculate',
            use_container_width=True,
        )

        if st.session_state.get('calculate'):
            catch_rates = get_catch_rates(pokemon)
            filtered_catch_rates = format_catch_rates(catch_rates)

            form_columns[1].markdown(
                filtered_catch_rates, unsafe_allow_html=True
            )


if __name__ == '__main__':
    main()
