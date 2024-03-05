"""Settings."""

import pathlib

import dotenv

dotenv.load_dotenv()

ROOT = pathlib.Path(__file__).resolve().parent
ASSETS_URL = (
    'https://raw.githubusercontent.com/marcelogcardozo/pokeballs/main/assets'
)

CURRENT_LAST_DEX_NUMBER = 1025
POKEMON_LEVEL_CAP = 100
BADGE_THRESHOLDS = [25, 30, 35, 40, 45, 50, 55, 60, 100]
LOW_LEVEL_BONUS_THRESHOLD = 13

FAST_BALL_SPEED_MIN = 100
NEST_BALL_LEVEL_MIN = 30

GENDER_UNKNOWN_RATIO = 255

UB_DEX_NUMBERS = (793, 794, 795, 796, 797, 798, 799, 803, 804, 805, 806)

CURRENT_HP = 1

DARK_GRASS_RANGES = {
    (0, 30): 1229,
    (31, 150): 2048,
    (151, 300): 2867,
    (301, 450): 3277,
    (451, 600): 3686,
}

HEAVY_BALL_RANGES = {
    (0.0, 99.9): -20,
    (100.0, 199.9): 0,
    (200.0, 299.9): 20,
}

CRITICAL_CATCH_RANGES = {
    (0, 30): 0,
    (31, 150): 2048,
    (151, 300): 4096,
    (301, 450): 6144,
    (451, 600): 8192,
}

CATCHING_POWER_MODIFIERS = {0: 1, 1: 1.1, 2: 1.25, 3: 2.0}
