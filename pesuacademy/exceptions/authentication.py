"""This module defines custom exceptions related to authentication errors in the PESU Academy application."""


class AuthenticationError(Exception):
    """Custom exception for authentication errors in the PESU Academy application."""

    def __init__(self, message: str) -> None:
        """Initializes the AuthenticationError with a custom message."""
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Returns the string representation of the error message."""
        return f"{self.message}"
