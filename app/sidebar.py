import streamlit as st

from models.pokemon import PokemonStatus


def add_sidebar_widgets() -> None:
    with st.sidebar:
        st.header('Conditions')
        st.selectbox(
            label='Status',
            options=[
                f'{name.title()} ({enum.value/4096}x)'
                for name, enum in PokemonStatus.__members__.items()
            ]
            + ['No Status (1x)'],
            index=5,
            key='status',
        )

        st.selectbox(
            label='HP',
            options=[
                'Exactly 1 HP',
                '< 20% (red bar)',
                '< 50% (yellow bar)',
                '<= 100% (green bar)',
            ],
            index=3,
            key='hp',
        )

        st.checkbox('Backstrike', key='backstrike')
        st.checkbox('Catching Charm', key='catching_charm')

        st.slider(
            'Catching Power Level',
            min_value=0,
            max_value=3,
            value=0,
            key='catching_power_level',
        )

        st.number_input(
            'Badges',
            min_value=0,
            max_value=8,
            value=8,
            key='badges',
        )

        st.number_input(
            'Paldea Pokédex Progress',
            min_value=1,
            max_value=400,
            value=400,
            key='paldea_dex',
        )
        st.number_input(
            'Kitakami Pokédex Progress',
            min_value=0,
            max_value=200,
            value=200,
            key='kitakami_dex',
        )
        st.number_input(
            'Blueberry Pokédex Progress',
            min_value=0,
            max_value=243,
            value=243,
            key='blueberry_dex',
        )
        st.session_state['registered_pokemon'] = (
            st.session_state['paldea_dex']
            + st.session_state['kitakami_dex']
            + st.session_state['blueberry_dex']
        )
