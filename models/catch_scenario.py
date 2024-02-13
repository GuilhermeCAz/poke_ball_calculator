from dataclasses import dataclass

from models.poke_ball import PokeBall


@dataclass
class CatchScenario:
    poke_ball: PokeBall
    catch_rate: int
    condition: str | None = None
    is_possible: bool = True
