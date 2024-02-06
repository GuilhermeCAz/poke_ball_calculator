"""Contains scraper exception definitions."""


class NoMatchFoundError(Exception):
    """Error raised when no matches are found for RegEx pattern in string."""

    def __init__(self) -> None:
        """Alter standard exception message."""
        super().__init__(
            'The RegEx pattern returned no matches in the snippet.'
        )
