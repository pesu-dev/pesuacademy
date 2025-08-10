"""PESU Academy constants module."""

from dataclasses import dataclass

BASE_URL = "https://www.pesuacademy.com"
PAGES_BASE_URL = "/s/studentProfilePESUAdmin"
SEMESTER_BASE_URL = "/a/studentProfilePESU/getStudentSemestersPESU"


@dataclass(frozen=True)
class _PageURLParams:
    """Holds the static URL parameter values for various pages/actions within PESU Academy."""

    @dataclass(frozen=True)
    class Announcements:
        """Static parameters for the Announcements page."""

        MENU_ID: str = "667"
        CONTROLLER_MODE: str = "6411"
        ACTION_TYPE: str = "5"

    @dataclass(frozen=True)
    class Attendance:
        """Static parameters for the Attendance page."""

        MENU_ID: str = "660"
        CONTROLLER_MODE: str = "6407"
        ACTION_TYPE: str = "8"

    @dataclass(frozen=True)
    class Courses:
        """Static parameters for the Courses page."""

        MENU_ID: str = "653"
        CONTROLLER_MODE: str = "6403"
        ACTION_TYPE: str = "38"

    @dataclass(frozen=True)
    class CourseDetail:
        """Static parameters for the Course Detail page."""

        MENU_ID: str = "653"
        CONTROLLER_MODE: str = "6403"
        ACTION_TYPE: str = "42"

    @dataclass(frozen=True)
    class UnitDetail:
        """Static parameters for the Unit Detail page."""

        MENU_ID: str = "653"
        CONTROLLER_MODE: str = "6403"
        ACTION_TYPE: str = "43"

    @dataclass(frozen=True)
    class MaterialLinks:
        """Static parameters for the Materials page."""

        URL: str = "studentProfilePESUAdmin"
        MENU_ID: str = "653"
        CONTROLLER_MODE: str = "6403"
        ACTION_TYPE: str = "60"

    @dataclass(frozen=True)
    class Profile:
        """Static parameters for the Profile page."""

        MENU_ID: str = "670"
        CONTROLLER_MODE: str = "6414"
        ACTION_TYPE: str = "5"

    @dataclass(frozen=True)
    class Results:
        """Static parameters for the ESA / ISA Results page."""

        MENU_ID: str = "652"
        CONTROLLER_MODE: str = "6402"
        ACTION_TYPE: str = "9"

    @dataclass(frozen=True)
    class SeatingInfo:
        """Static parameters for the Seating Information page."""

        MENU_ID: str = "655"
        CONTROLLER_MODE: str = "6404"
        ACTION_TYPE: str = "5"
