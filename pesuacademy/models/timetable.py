"""Model for TimeTable in the PESU Academy system."""

from datetime import time
from enum import Enum

from pydantic import BaseModel


class ClassSession(BaseModel):
    """Represents a single class session at a specific time.

    Attributes:
        code (str): The code of the course.
        name (str): The name of the course.
        faculty (str): The name(s) of the faculty for the class.
    """

    code: str
    name: str
    faculty: str


class Time(BaseModel):
    """Represents the start, end, and duration of a class session.

    Attributes:
        start (datetime): The start time of the session.
        end (datetime): The end time of the session.
        duration (int): The duration of the session in minutes.
    """

    start: time
    end: time
    duration: int


class Slot(BaseModel):
    """Represents a single Slot in the timetable (e.g., 8:00 AM - 8:45 AM).

    Attributes:
        time (Time): The time info for the class.
        is_break (bool): True if this is a break slot, False otherwise.
        session (Optional[ClassSession]): The class session for this slot, if any.
    """

    time: Time
    is_break: bool = False
    session: ClassSession | None = ClassSession(code="N/A", name="N/A", faculty="N/A")


class Weekday(str, Enum):
    """Enumeration for the days of the week."""

    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"


class Timetable(BaseModel):
    """The main model to hold the entire weekly schedule, organized by day."""

    days: dict[Weekday, list[Slot]]

    def __getattr__(self, item: str) -> list[Slot]:
        """Allows for convenient dot-access to days (e.g., timetable.monday)."""
        try:
            return self.days[Weekday(item)]
        except (ValueError, KeyError):
            raise AttributeError(f"Timetable has no attribute or day named '{item}'")
