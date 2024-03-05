"""Contains scraper exception definitions."""


class InexistentTypeError(ValueError):
    """Error raised when no PokemonType matches are found for string passed."""

    def __init__(self, type_str: str) -> None:
        super().__init__(f'{type_str} is not a recognized Pokémon Type.')


class InvalidLevelError(ValueError):
    """Error raised when the level surpasses the current level boundaries."""

    def __init__(self, level: int) -> None:
        super().__init__(f'{level} is not a valid level number.')


class InvalidCatchingPowerError(ValueError):
    """Error raised when the catching power level passed is invalid."""

    def __init__(self) -> None:
        super().__init__('Catching power level must be 1, 2, or 3.')


class NoMatchFoundError(Exception):
    """Error raised when no matches are found for RegEx pattern in string."""

    def __init__(self) -> None:
        """Alter standard exception message."""
        super().__init__(
            'The RegEx pattern returned no matches in the snippet.'
        )


class NoPaletteFoundError(Exception):
    """Error raised when no palette is found in quantized image."""

    def __init__(self, image_path: str) -> None:
        super().__init__(f'No palette found for image: {image_path}.')


class NoPokemonFoundError(Exception):
    """Error raised when no Pokemon matches are found for dex number passed."""

    def __init__(self, *args: str | int) -> None:
        super().__init__(f'No Pokémon found with {args}.')
