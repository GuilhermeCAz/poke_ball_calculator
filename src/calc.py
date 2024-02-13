import math

from models.catch_scenario import CatchScenario
from models.pokemon import Pokemon
from settings import LOW_LEVEL_BONUS_THRESHOLD
from src import modifiers
from src.scenarios import get_catch_scenarios


def special_round(value: float) -> int:
    return math.floor((value + 2048) / 4096)


def calculate_modified_catch_rates(
    pokemon: Pokemon,
    hp: int,
    catching_power_level: int = 0,
    backstrike: bool = False,
) -> list[tuple[CatchScenario, int]]:
    def _get_constant_modifiers() -> tuple[int, int, float, int, float]:
        return (
            modifiers.get_hp_modifier(hp),
            modifiers.get_dark_grass_modifier(601),
            modifiers.get_badge_modifier(8, pokemon.level),
            modifiers.get_status_modifier('asleep'),
            modifiers.get_capture_value_coefficient_modifier(
                catching_power_level, backstrike
            ),
        )

    def _calculate_modified_catch_rate_by_scenario(
        scenario: CatchScenario,
    ) -> int:
        species_modifier = modifiers.get_species_modifier(
            pokemon.catch_rate, pokemon.weight, scenario.poke_ball
        )
        c = _calculate_c(species_modifier, b)
        d = _calculate_d(scenario.catch_rate, c)
        e = _calculate_e(d)
        f = _calculate_f(e)
        g = _calculate_g(f)

        return min(special_round(cvc_modifier * g), 0xFF000)

    def _calculate_a() -> int:
        return hp_modifier

    def _calculate_b(a: int) -> int:
        return special_round(dark_grass_modifier * a)

    def _calculate_c(species_modifier: int, b: int) -> int:
        return species_modifier * b

    def _calculate_d(catch_rate: int, c: int) -> int:
        return special_round(catch_rate * c)

    def _calculate_e(d: int) -> float:
        return special_round(badge_modifier * d) / (3 * hp)

    def _calculate_f(e: float) -> float:
        return (
            math.floor((36 - 2 * pokemon.level) * e / 10)
            if pokemon.level <= LOW_LEVEL_BONUS_THRESHOLD
            else e
        )

    def _calculate_g(f: float) -> int:
        return special_round(status_modifier * f)

    (
        hp_modifier,
        dark_grass_modifier,
        badge_modifier,
        status_modifier,
        cvc_modifier,
    ) = _get_constant_modifiers()

    scenarios = get_catch_scenarios(pokemon)
    # scenarios = [
    #     scenario
    #     for scenario in scenarios
    #     if scenario.poke_ball == PokeBall.QUICK_BALL
    # ]

    a = _calculate_a()
    b = _calculate_b(a)

    return [
        (scenario, _calculate_modified_catch_rate_by_scenario(scenario))
        for scenario in scenarios
    ]


def calculate_critical_catch_value(
    registered_pokemon_on_dex: int, modified_catch_rate: int
) -> int:
    """Return value used to evaluate whether a catch is critical."""
    critical_catch_modifier = modifiers.get_critical_catch_modifier(
        registered_pokemon_on_dex
    )
    return math.floor(
        special_round(critical_catch_modifier * modified_catch_rate)
        * 715827883
        / (4294967296 * 4096)
    )


def calculate_critical_catch_odds(critical_catch_value: float) -> float:
    """Return the odds of a critical catch occurring."""
    return critical_catch_value / 256


def calculate_shake_value(modified_catch_rate: int) -> int:
    """Return value used to evaluate whether a shake is successful."""
    return 65536 / (((255 * 4096) / modified_catch_rate) ** (3 / 16))


def calculate_successful_shake_odds(shake_value: int) -> float:
    """Return the odds of a successful shake occurring."""
    return shake_value / 65536


def calculate_successful_catch_odds(
    is_critical_catch: bool, successful_shake_odds: float
) -> float:
    if is_critical_catch:
        return successful_shake_odds
    return (successful_shake_odds) ** 4