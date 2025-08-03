"""Model for seating information in the PESU Academy system."""

from pydantic import BaseModel


class SeatingInformation(BaseModel):
    """Represents seating information in the PESU Academy system.

    Attributes:
        name (str): Name of the course/assessment.
        course_code (str): Code of the course for which seating information is provided.
        date (str): Date of the examination or event.
        time (str): Time of the examination or event.
        terminal (str): Terminal or location where the student is seated.
        block (str): Block or section of the seating arrangement.
    """

    name: str
    course_code: str
    date: str
    time: str
    terminal: str
    block: str
