"""Model for announcements in the PESU Academy system."""

import datetime

from pydantic import BaseModel


class Announcement(BaseModel):
    """Represents an announcement in the PESU Academy system.

    Attributes:
        title (str): The title of the announcement.
        date (datetime.date): The date of the announcement.
        content (str): The content of the announcement.
        attachments (Optional[List[str]]): Optional list of attachment links related to the announcement.
    """

    title: str
    date: datetime.date
    content: str
    attachments: list[str] | None = None
