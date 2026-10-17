"""PESU Academy package initialization.

Deprecated: this package no longer works. Use PESU OAuth2 (https://github.com/pesu-dev/oauth2) instead.
"""

import warnings

__version__ = "1.0.1"

warnings.warn(
    "pesuacademy is deprecated and no longer works. "
    "All access to PESU Academy now goes through PESU OAuth2: https://github.com/pesu-dev/oauth2",
    FutureWarning,
    stacklevel=2,
)

from .pesuacademy import PESUAcademy  # noqa: E402

__all__ = ["PESUAcademy"]
