"""Model for materials in the PESU Academy system."""

from pydantic import BaseModel


class Unit(BaseModel):
    """Represents a unit of a course in the PESU Academy system.

    Attributes:
        title (str): The title of the unit.
        unit_id (str): Unique identifier for the unit.
    """

    title: str
    id: str


class Topic(BaseModel):
    """Represents a topic within a unit in the PESU Academy system.

    Attributes:
        title (str): The title of the topic.
        topic_id (str): Unique identifier for the topic.
        course_id (str): Identifier for the course this topic belongs to.
        unit_id (str): Identifier for the unit this topic belongs to.
    """

    title: str
    id: str
    course_id: str
    unit_id: str


class MaterialLink(BaseModel):
    """Represents a link to a material in the PESU Academy system.

    Attributes:
        title (str): The title of the material link.
        url (str): The URL of the material.
        is_pdf (bool): Indicates if the link points to a PDF document.
    """

    title: str
    url: str
    is_pdf: bool
