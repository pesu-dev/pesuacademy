from dataclasses import dataclass

BASE_URL = "https://www.pesuacademy.com"


@dataclass(frozen=True)
class PageURLParams:
    """
    Holds the static URL parameter values for various pages/actions within PESU Academy.
    """

    @dataclass(frozen=True)
    class Announcements:
        MENU_ID: str = "667"
        CONTROLLER_MODE: str = "6411"
        ACTION_TYPE: str = "5"

    @dataclass(frozen=True)
    class Attendance:
        MENU_ID: str = "660"
        CONTROLLER_MODE: str = "6407"
        ACTION_TYPE: str = "8"

    @dataclass(frozen=True)
    class Courses:
        MENU_ID: str = "653"
        CONTROLLER_MODE: str = "6403"
        ACTION_TYPE: str = "38"

    @dataclass(frozen=True)
    class CourseDetail:
        MENU_ID: str = "653"
        CONTROLLER_MODE: str = "6403"
        ACTION_TYPE: str = "42"

    @dataclass(frozen=True)
    class UnitDetail:
        MENU_ID: str = "653"
        CONTROLLER_MODE: str = "6403"
        ACTION_TYPE: str = "43"

    @dataclass(frozen=True)
    class MaterialLinks:
        URL: str = "studentProfilePESUAdmin"
        MENU_ID: str = "653"
        CONTROLLER_MODE: str = "6403"
        ACTION_TYPE: str = "60"

    @dataclass(frozen=True)
    class Profile:
        MENU_ID: str = "670"
        CONTROLLER_MODE: str = "6414"
        ACTION_TYPE: str = "5"

    @dataclass(frozen=True)
    class Results:
        MENU_ID: str = "652"
        CONTROLLER_MODE: str = "6402"
        ACTION_TYPE: str = "9"

    @dataclass(frozen=True)
    class SeatingInfo:
        MENU_ID: str = "655"
        CONTROLLER_MODE: str = "6404"
        ACTION_TYPE: str = "5"
