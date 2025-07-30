class PageURLParams:
    """
    Holds the static URL parameter values for various pages/actions within PESU Academy.
    """

    class Announcements:
        MENU_ID = "667"
        CONTROLLER_MODE = "6411"
        ACTION_TYPE = "5"

    class Attendance:
        MENU_ID = "660"
        CONTROLLER_MODE = "6407"
        ACTION_TYPE = "8"
    
    class Courses:
        MENU_ID = "653"
        CONTROLLER_MODE = "6403"
        ACTION_TYPE = "38"

    class CourseDetail:
        MENU_ID = "653"
        CONTROLLER_MODE = "6403"
        ACTION_TYPE = "42"
    
    class UnitDetail:
        MENU_ID = "653"
        CONTROLLER_MODE = "6403"
        ACTION_TYPE = "43"
        
    class MaterialLinks:
        URL = "studentProfilePESUAdmin"
        MENU_ID = "653"
        CONTROLLER_MODE = "6403"
        ACTION_TYPE = "60"
        
    class Profile:
        MENU_ID = "670"
        CONTROLLER_MODE = "6414"
        ACTION_TYPE = "5"
        
    class Results:
        MENU_ID = "652"
        CONTROLLER_MODE = "6402"
        ACTION_TYPE = "9"
        
    class SeatingInfo:
        MENU_ID = "655"
        CONTROLLER_MODE = "6404"
        ACTION_TYPE = "5"
