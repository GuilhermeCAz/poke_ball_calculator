# Poké Ball Calculator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FGuilhermeCAz%2Fpoke_ball_calculator%2Fmain%2Fpyproject.toml&logo=python&label=Python)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-%23FF4B4B?logo=streamlit&labelColor=black)](https://streamlit.io/)
[![Make](https://img.shields.io/badge/Make-%236D00CC?logo=make)](https://www.gnu.org/software/make/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

## About

Poké Ball Calculator was built on Python using Streamlit. It scrapes many resources from [PokéAPI](https://pokeapi.co/) and combines it with the Pokémon Scarlet and Violet (Gen IX) catch rate formula to return all the possible catching scenarios a trainer has when trying to catch a Pokémon.

## Description

Poké Ball Calculator is a Python website that lists the catch rates of all Poké Balls for the selected Pokémon in the selected level.

All the user has to do is select the wild Pokémon desired, either by name or by dex number, and its current level.

With this tool, you can figure out what is the most efficient Poké Ball to use.

For now, this application only calculates the catch rates of Scarlet and Violet Pokémon.

![Poké Ball Calculator](https://raw.githubusercontent.com/GuilhermeCAz/poke_ball_calculator/main/assets/images/preview.png)

## Sidebar: Conditions

The user can also use the sidebar to manipulate certain battle or game conditions which affect the catch rate.

### Battle Conditions

- [Status](https://bulbapedia.bulbagarden.net/wiki/Status_condition): Asleep, Frozen, Burned, Paralyzed, Poisoned, or No Status
- [HP](https://bulbapedia.bulbagarden.net/wiki/HP): Exactly 1 Health Point, < 20%, < 50%, or <= 100%
- [Backstrike](<https://bulbapedia.bulbagarden.net/wiki/Catch_rate#Capture_method_(Generation_IX)>): whether the battle started with a backstrike

### Game Conditions

- [Catching Charm](https://bulbapedia.bulbagarden.net/wiki/Catching_Charm): whether the user has the Catching Charm
- [Catching Power Level](https://m.bulbapedia.bulbagarden.net/wiki/Sandwich#Meal_Powers): the level of the user's catching power, temporarily obtained by making sandwiches.
- [Badges](https://bulbapedia.bulbagarden.net/wiki/Badge): amount of Badges obtained by the user

#### Pokédex Progress

- [Paldea Pokédex](https://www.serebii.net/scarletviolet/paldeapokedex.shtml): 0-400
- [Kitakami Pokédex](https://www.serebii.net/scarletviolet/kitakamipokedex.shtml): 0-200
- [Blueberry Pokedex](https://www.serebii.net/scarletviolet/blueberrypokedex.shtml): 0-243

## Resources

- [PokéAPI](https://github.com/PokeAPI/pokeapi)
- [Anubis formula breakdown](https://x.com/Sibuna_Switch/status/1610341810655608833)
- [Datamine compilation roundup | Reddit](https://www.reddit.com/r/PokeLeaks/comments/ys27pn/datamine_compilation_roundup/)
- [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Catch_rate)
- [Serebii](https://www.serebii.net/pokedex-sv/)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Pokémon and Pokémon character names are trademarks of Nintendo.
