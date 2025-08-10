"""This module initializes the models for the PESU Academy package."""

from .announcement import Announcement
from .course import Attendance, Course
from .materials import MaterialLink, Topic, Unit
from .profile import (
    AddressDetails,
    OtherInformation,
    ParentDetails,
    ParentInformation,
    PersonalDetails,
    Profile,
    QualifyingExamination,
)
from .results import Assessment, CourseResult, Credits, SemesterResult
from .seating_information import SeatingInformation

__all__ = [
    "Announcement",
    "Attendance",
    "Course",
    "MaterialLink",
    "Profile",
    "SeatingInformation",
    "SemesterResult",
    "Topic",
    "Unit",
    "AddressDetails",
    "OtherInformation",
    "ParentDetails",
    "ParentInformation",
    "PersonalDetails",
    "QualifyingExamination",
    "Assessment",
    "CourseResult",
    "Credits",
]
