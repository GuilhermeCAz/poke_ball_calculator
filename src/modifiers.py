import math

from models.exceptions import InvalidCatchingPowerError
from models.poke_ball import PokeBall
from models.pokemon import PokemonStatus
from settings import (
    BADGE_THRESHOLDS,
    CATCHING_POWER_MODIFIERS,
    CRITICAL_CATCH_RANGES,
    DARK_GRASS_RANGES,
    HEAVY_BALL_RANGES,
)


def get_hp_modifier(hp: int, current_hp: int = 1) -> int:
    return math.floor((3 * hp - 2 * current_hp) * 4096 + 0.5)


def get_dark_grass_modifier(registered_pokemon_on_dex: int) -> int:
    return 4096

    for (min_registered, max_registered), value in DARK_GRASS_RANGES.items():
        if min_registered <= registered_pokemon_on_dex <= max_registered:
            return value

    return 4096


def get_species_modifier(
    catch_rate: int,
    weight: float,
    poke_ball: PokeBall,
) -> int:
    if poke_ball == PokeBall.HEAVY_BALL:
        for (min_weight, max_weight), modifier in HEAVY_BALL_RANGES.items():
            if min_weight < weight <= max_weight:
                return max(catch_rate + modifier, 1)

        return catch_rate + 30

    return catch_rate


def get_badge_modifier(badges: int, level: int) -> float:
    for badges_required in range(len(BADGE_THRESHOLDS)):
        if level <= BADGE_THRESHOLDS[badges_required]:
            return (0.8 ** (max(0, badges_required - badges))) * 4096

    return 4096


def get_status_modifier(status: PokemonStatus | None) -> int:
    if status:
        return status.value
    return 4096


def get_capture_value_coefficient_modifier(
    catching_power_level: int,
    *,
    backstrike: bool,
) -> float:
    backstrike_modifier = 2 if backstrike else 1
    if catching_power_level in CATCHING_POWER_MODIFIERS:
        return (
            backstrike_modifier
            * CATCHING_POWER_MODIFIERS[catching_power_level]
        ) * 4096
    raise InvalidCatchingPowerError


def get_critical_catch_modifier(registered_pokemon_on_dex: int) -> int:
    for (
        min_registered,
        max_registered,
    ), value in CRITICAL_CATCH_RANGES.items():
        if min_registered <= registered_pokemon_on_dex <= max_registered:
            return value

    return 10240
