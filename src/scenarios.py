import math

from models.catch_scenario import CatchScenario
from models.poke_ball import PokeBall
from models.pokemon import Pokemon, PokemonType
from settings import (
    FAST_BALL_SPEED_MIN,
    GENDER_UNKNOWN_VALUE,
    NEST_BALL_LEVEL_MIN,
    POKEMON_LEVEL_CAP,
    UB_DEX_NUMBERS,
)


def get_catch_scenarios(target_pokemon: Pokemon) -> list[CatchScenario]:
    catch_scenarios: list[CatchScenario] = []

    def _get_base_catch_rates() -> None:
        base_catch_rate_balls = [
            PokeBall.POKÉ_BALL,
            PokeBall.SAFARI_BALL,
            PokeBall.LEVEL_BALL,
            PokeBall.LURE_BALL,
            PokeBall.HEAVY_BALL,
            PokeBall.LOVE_BALL,
            PokeBall.FRIEND_BALL,
            PokeBall.SPORT_BALL,
            PokeBall.DIVE_BALL,
            PokeBall.NEST_BALL,
            PokeBall.REPEAT_BALL,
            PokeBall.TIMER_BALL,
            PokeBall.LUXURY_BALL,
            PokeBall.PREMIER_BALL,
            PokeBall.DUSK_BALL,
            PokeBall.HEAL_BALL,
            PokeBall.QUICK_BALL,
        ]

        catch_scenarios.extend(
            [
                CatchScenario(base_catch_rate_ball, 0x1000)
                for base_catch_rate_ball in base_catch_rate_balls
            ]
        )

    def _get_timer_ball_rates() -> None:
        for turns in range(0, 11):
            catch_scenarios.append(
                CatchScenario(
                    poke_ball=PokeBall.TIMER_BALL,
                    catch_rate=min(turns * 1229 + 0x1000, 0x4000),
                    condition=f'{turns} {'turn' if turns == 1 else 'turns'}'
                    ' since battle started',
                    # is_condition_true=user information required
                )
            )

    _get_base_catch_rates()
    _get_timer_ball_rates()

    catch_scenarios.extend(
        [
            CatchScenario(
                poke_ball=PokeBall.GREAT_BALL,
                catch_rate=0x1800,
            ),
            CatchScenario(
                poke_ball=PokeBall.ULTRA_BALL,
                catch_rate=0x2000,
            ),
            CatchScenario(
                poke_ball=PokeBall.FAST_BALL,
                catch_rate=0x4000,
                condition=f'Target Pokémon Speed >= {FAST_BALL_SPEED_MIN}',
                is_possible=target_pokemon.stats.speed >= FAST_BALL_SPEED_MIN,
            ),
            CatchScenario(
                poke_ball=PokeBall.FAST_BALL,
                catch_rate=0x1000,
                condition=f'Target Pokémon Speed < {FAST_BALL_SPEED_MIN}',
                is_possible=target_pokemon.stats.speed < FAST_BALL_SPEED_MIN,
            ),
            CatchScenario(
                poke_ball=PokeBall.LEVEL_BALL,
                catch_rate=0x8000,
                condition='User Pokémon Level '
                + f'{"=" if 4 * target_pokemon.level == POKEMON_LEVEL_CAP
                    else ">="}'
                + f' {4 * target_pokemon.level}',
                is_possible=4 * target_pokemon.level <= POKEMON_LEVEL_CAP,
            ),
            CatchScenario(
                poke_ball=PokeBall.LEVEL_BALL,
                catch_rate=0x4000,
                condition='User Pokémon Level '
                + f'{"=" if 2 * target_pokemon.level == POKEMON_LEVEL_CAP
                    else ">="}'
                + f' {2 * target_pokemon.level}',
                is_possible=2 * target_pokemon.level <= POKEMON_LEVEL_CAP,
            ),
            CatchScenario(
                poke_ball=PokeBall.LEVEL_BALL,
                catch_rate=0x2000,
                condition=f'User Pokémon Level > {target_pokemon.level}',
                is_possible=target_pokemon.level < POKEMON_LEVEL_CAP,
            ),
            CatchScenario(
                poke_ball=PokeBall.LURE_BALL,
                catch_rate=0x4000,
                condition='Target Pokémon is in water or just above water',
                # is_condition_true=user information required
            ),
            CatchScenario(
                poke_ball=PokeBall.LOVE_BALL,
                catch_rate=0x8000,
                condition='User Pokémon Species is the same as Target,'
                ' but opposite gender',
                is_possible=target_pokemon.gender_ratio
                != GENDER_UNKNOWN_VALUE,
            ),
            CatchScenario(
                poke_ball=PokeBall.MOON_BALL,
                catch_rate=0x4000,
                condition='Target Pokémon evolves with Moon Stone',
                is_possible=target_pokemon.evolution is not None
                and target_pokemon.evolution.item == 'Moon Stone',
            ),
            CatchScenario(
                poke_ball=PokeBall.MOON_BALL,
                catch_rate=0x1000,
                condition='Target Pokémon does not evolve with Moon Stone',
                is_possible=not (
                    target_pokemon.evolution is not None
                    and target_pokemon.evolution.item == 'Moon Stone'
                ),
            ),
            CatchScenario(
                poke_ball=PokeBall.NET_BALL,
                catch_rate=0x3800,
                condition='Target Pokémon is either Bug or Water type',
                is_possible=any(
                    type_ in (PokemonType.BUG, PokemonType.WATER)
                    for type_ in target_pokemon.types
                ),
            ),
            CatchScenario(
                poke_ball=PokeBall.NET_BALL,
                catch_rate=0x1000,
                condition='Target Pokémon is neither Bug nor Water type',
                is_possible=not any(
                    type_ in (PokemonType.BUG, PokemonType.WATER)
                    for type_ in target_pokemon.types
                ),
            ),
            CatchScenario(
                poke_ball=PokeBall.DIVE_BALL,
                catch_rate=0x3800,
                condition='Target Pokémon is in water',
                # is_condition_true=user information required
            ),
            CatchScenario(
                poke_ball=PokeBall.NEST_BALL,
                catch_rate=math.floor(
                    ((41 - target_pokemon.level) * 0x1000 + 0.5) / 10
                ),
                condition='Target Pokémon Level < 30',
                is_possible=target_pokemon.level < NEST_BALL_LEVEL_MIN,
            ),
            CatchScenario(
                poke_ball=PokeBall.NEST_BALL,
                catch_rate=0x1000,
                condition='Target Pokémon Level >= 30',
                is_possible=target_pokemon.level >= NEST_BALL_LEVEL_MIN,
            ),
            CatchScenario(
                poke_ball=PokeBall.REPEAT_BALL,
                catch_rate=0x3800,
                condition='Target Pokémon has been registered',
                # is_possible=user information required
            ),
            CatchScenario(
                poke_ball=PokeBall.DUSK_BALL,
                catch_rate=0x3000,
                condition='Catch inside caves or during nighttime',
                # is_possible=user information required
            ),
            CatchScenario(
                poke_ball=PokeBall.QUICK_BALL,
                catch_rate=0x5000,
                condition='0 turns since battle started',
                # is_possible=user information required
            ),
            CatchScenario(
                poke_ball=PokeBall.DREAM_BALL,
                catch_rate=0x4000,
                condition='Target Pokémon is asleep',
                # is_possible=user information required
            ),
            CatchScenario(
                poke_ball=PokeBall.BEAST_BALL,
                catch_rate=0x5000,
                condition='Target Pokémon is an Ultra Beast',
                is_possible=target_pokemon.dex_no in UB_DEX_NUMBERS,
            ),
            CatchScenario(
                poke_ball=PokeBall.BEAST_BALL,
                catch_rate=0x19A,
                condition='Target Pokémon is not an Ultra Beast',
                is_possible=target_pokemon.dex_no not in UB_DEX_NUMBERS,
            ),
        ]
    )

    return [scenario for scenario in catch_scenarios if scenario.is_possible]
