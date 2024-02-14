from src.misc import generate_pokemon_sav, get_all_pokemon, get_pokemon
from settings import ROOT
import streamlit as st
import pathlib
from src.calc import (
    calculate_critical_catch_odds,
    calculate_critical_catch_value,
    calculate_modified_catch_rates,
    calculate_shake_value,
    calculate_successful_catch_odds,
    calculate_successful_shake_odds,
)
import pandas as pd

if not pathlib.Path.exists(ROOT / 'pokemon_list.sav'):
    generate_pokemon_sav()

st.title('Calculadora Pokémon')

pokemons = get_all_pokemon()

labels = [''] + [f'{str(pokemon.dex_no).zfill(4)} - {pokemon.name}' for pokemon in pokemons]

col1, col2 = st.columns([3, 1])

input_pokemon = col1.selectbox('Pokémon', options=labels, placeholder='Selecione um Pokémon')
input_level = col2.number_input('Nível', min_value=1, max_value=100, value=50)

if input_pokemon and input_level:

    dex_no = int(input_pokemon.split(' - ')[0])

    pokemon = get_pokemon(dex_no, input_level)

    st.write(f'Best scenarios for {pokemon.name} at level {pokemon.level}:')

    stats = pd.DataFrame(
        columns=['Pokéball', 'Condition', 'Critical Odds', 'Critical Catch Odds', 'Non Critical Catch Odds', 'Not Caught Odds', 'ordering'])

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

        stats.loc[len(stats)] = [
            min_iv_scenario.poke_ball.value, 
            min_iv_scenario.condition, 
            f'{critical_catch_odds*100:.4f}%', 
            f'{successful_crit_catch_odds*100:.4f}%', 
            f'{successful_non_crit_catch_odds*100:.4f}%', 
            f'{(1-successful_crit_catch_odds-successful_non_crit_catch_odds)*100:.4f}%',
            successful_non_crit_catch_odds]

    stats = stats.sort_values(by='ordering', ascending=False).drop(columns='ordering')    
    st.markdown(stats.to_markdown(index=False), unsafe_allow_html=True)



















