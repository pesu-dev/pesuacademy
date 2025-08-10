"""Utility functions for PESU Academy package."""

import datetime
from typing import Protocol


class _PageURLParams(Protocol):
    """A protocol for objects that have the required parameters."""

    MENU_ID: str
    CONTROLLER_MODE: str
    ACTION_TYPE: str


def _build_params(params_obj: _PageURLParams, **kwargs: str) -> dict[str, str]:
    """Builds and returns the common parameter dictionary for PESU Academy requests.

    Args:
        params_obj: The dataclass object from constants.PageURLParams (e.g., PageURLParams.Results).
        **kwargs: Additional key-value pairs (e.g., semid="1234").

    Returns:
        Dict[str, str]: The complete dictionary of parameters for the request.
    """
    params = {
        "menuId": params_obj.MENU_ID,
        "controllerMode": params_obj.CONTROLLER_MODE,
        "actionType": params_obj.ACTION_TYPE,
    }

    params.update(kwargs)

    params["_"] = str(int(datetime.datetime.now().timestamp() * 1000))

    return params
