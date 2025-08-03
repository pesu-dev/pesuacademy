"""This module defines a custom exception for CSRF token errors in the PESU Academy application."""


class CSRFTokenError(Exception):
    """Custom exception for CSRF token errors in the PESU Academy application."""

    def __init__(self, message: str) -> None:
        """Custom exception for CSRF token errors."""
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return a string representation of the error."""
        return f"{self.message}"
