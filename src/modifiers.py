import math
from decimal import Decimal

from models.exceptions import InvalidCatchingPowerError
from models.poke_ball import PokeBall
from settings import (
    BADGE_THRESHOLDS,
    CATCHING_POWER_MODIFIERS,
    CRITICAL_CATCH_RANGES,
    CURRENT_HP,
    DARK_GRASS_RANGES,
    HEAVY_BALL_RANGES,
)


def get_hp_modifier(hp: int) -> int:
    return math.floor((3 * hp - 2 * CURRENT_HP) * 4096 + 0.5)


def get_dark_grass_modifier(registered_pokemon_on_dex: int) -> int:
    return 4096

    for (min_registered, max_registered), value in DARK_GRASS_RANGES.items():
        if min_registered <= registered_pokemon_on_dex <= max_registered:
            return value

    return 4096


def get_species_modifier(
    catch_rate: int, weight: Decimal, poke_ball: PokeBall
) -> int:
    if poke_ball == PokeBall.HEAVY_BALL:
        for (min_weight, max_weight), modifier in HEAVY_BALL_RANGES.items():
            if min_weight < weight <= max_weight:
                return catch_rate + modifier

        return catch_rate + 30

    return catch_rate


def get_badge_modifier(badges: int, level: int) -> float:
    for badges_required in range(len(BADGE_THRESHOLDS)):
        if level <= BADGE_THRESHOLDS[badges_required]:
            return (0.8 ** (max(0, badges_required - badges))) * 4096

    return 4096


def get_status_modifier(status: str) -> int:
    if status in ('asleep', 'frozen'):
        return 10240

    return 6144


def get_capture_value_coefficient_modifier(
    catching_power_level: int, backstrike: bool
) -> float:
    # if static_encounter (user input):
    #   catching_power_level = 0; backstrike = False
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

    # to-do: unclear if capped at 400 registered or not.
    return 10240
