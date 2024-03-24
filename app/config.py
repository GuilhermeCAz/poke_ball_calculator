import math

import streamlit as st

from models.poke_ball import PokeBall
from models.pokemon import Pokemon, PokemonStatus
from settings import ROOT
from src.calc import BattleVariables, GameVariables


def set_basic_configuration() -> None:
    st.set_page_config(
        layout='wide',
        page_title='Pokémon Catch Rate Calculator',
        page_icon=PokeBall.LEVEL_BALL.image,
        initial_sidebar_state='expanded',
    )

    with open(ROOT / 'css' / 'styles.css') as css:
        st.markdown(
            '<style>' + css.read() + '</style>', unsafe_allow_html=True
        )

    st.title('Catch Rate Calculator')


def set_pokemon_by_dex_no() -> None:
    dex_no: int | None = st.session_state.get('dex_no')
    level: int = st.session_state.get('level', 1)
    if not dex_no:
        st.session_state['pokemon_name'] = None
        return

    pokemon = Pokemon(dex_no, level)
    if pokemon:
        st.session_state['pokemon'] = pokemon
        st.session_state['pokemon_name'] = pokemon.name.title()
    else:
        st.session_state['pokemon'] = None
        st.session_state['pokemon_name'] = None


def set_pokemon_by_name() -> None:
    pokemon_name: str | None = st.session_state.get('pokemon_name')
    level: int = st.session_state.get('level', 1)
    if not pokemon_name:
        st.session_state['dex_no'] = None
        return

    pokemon = Pokemon(pokemon_name.lower(), level)
    st.session_state['pokemon'] = pokemon
    st.session_state['dex_no'] = pokemon.dex_no


def set_pokemon_level() -> None:
    pokemon: Pokemon = st.session_state['pokemon']
    pokemon.level = st.session_state['level']
    st.session_state['pokemon'] = pokemon


def get_current_hp(pokemon_hp: int) -> int:
    selected_hp = st.session_state['hp']
    hp_selectbox_dict: dict[str, float] = {
        'Exactly 1 HP': 1,
        '< 20% (red bar)': 0.2 * pokemon_hp,
        '< 50% (yellow bar)': 0.5 * pokemon_hp,
        '<= 100% (green bar)': 1 * pokemon_hp,
    }

    return math.floor(hp_selectbox_dict[selected_hp])


def get_status() -> PokemonStatus | None:
    selected_status = st.session_state['status']
    status_selectbox_dict = {
        f'{name.title()} ({enum.value/4096}x)': enum
        for name, enum in PokemonStatus.__members__.items()
    }
    return status_selectbox_dict.get(selected_status)


def get_battle_variables(hp: int) -> BattleVariables:
    return BattleVariables(
        target_current_hp=get_current_hp(hp),
        target_status=get_status(),
        backstrike=st.session_state['backstrike'],
        catching_power_level=st.session_state['catching_power_level'],
    )


def get_game_variables() -> GameVariables:
    return GameVariables(
        badges=st.session_state['badges'],
        registered_pokemon=st.session_state['registered_pokemon'],
        catching_charm=st.session_state['catching_charm'],
    )
