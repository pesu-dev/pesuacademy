"""This module initializes the page handlers for the PESU Academy package."""

from .announcements import _AnnouncementPageHandler
from .attendance import _AttendancePageHandler
from .course_detail import _CourseDetailPageHandler
from .courses import _CoursesPageHandler
from .esa_result import _ResultsPageHandler
from .material_links import _MaterialLinksHandler
from .profile import _ProfilePageHandler
from .seating_information import _SeatingInformationHandler
from .semester import _SemesterHandler
from .unit import _UnitPageHandler

__all__ = [
    "_AnnouncementPageHandler",
    "_AttendancePageHandler",
    "_CourseDetailPageHandler",
    "_CoursesPageHandler",
    "_ResultsPageHandler",
    "_MaterialLinksHandler",
    "_ProfilePageHandler",
    "_SeatingInformationHandler",
    "_SemesterHandler",
    "_UnitPageHandler",
]
