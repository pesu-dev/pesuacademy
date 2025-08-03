"""This module contains custom exceptions for the PESU Academy application."""

from .authentication import AuthenticationError
from .csrf import CSRFTokenError

__all__ = [
    "AuthenticationError",
    "CSRFTokenError",
]
