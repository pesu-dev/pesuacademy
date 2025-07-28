import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Optional


from .pages import (
    SeatingInformationHandler,
    CoursesPageHandler,
    CourseDetailPageHandler, 
    UnitPageHandler,         
    MaterialLinksHandler,
    AttendancePageHandler,
    ProfilePageHandler,
    SemesterHandler,
    AnnouncementPageHandler,
    ResultsPageHandler
)
from .models import (
    SeatingInformation, 
    Course, 
    Profile, 
    Announcement, 
    Unit,                 
    Topic,                
    MaterialLink,
    SemesterResult        
)

class PesuAcademyClient:
    def __init__(self):
        self._base_url = "https://www.pesuacademy.com/Academy"
        self._session = httpx.AsyncClient(base_url=self._base_url, follow_redirects=True, timeout=30.0)
        self._csrf_token: Optional[str] = None
        self._semester_ids: Dict[int, str] = {}
        self.is_authenticated = False

    async def login(self, username: str, password: str):
        """ Logs in to the PESU Academy portal and initializes the session.
        Args:
            username (str): The user's SRN, PRN, or other login identifier.
            password (str): The user's password.
        Raises:
            Exception: If the login fails or the credentials are invalid.
        Returns:
            None
        """
        response = await self._session.get("/")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        # Extract the CSRF token from the initial page
        initial_csrf = soup.find("meta", attrs={"name": "csrf-token"})["content"]

        login_data = {"_csrf": initial_csrf, "j_username": username, "j_password": password}
        response = await self._session.post("/j_spring_security_check", data=login_data)
        response.raise_for_status()

        if "Invalid credentials" in response.text: # Check if login failed
            raise Exception("Authentication failed. Please check your credentials.")
        
        # After login, fetch the CSRF token again
        soup = BeautifulSoup(response.text, "lxml")
        final_csrf = soup.find("meta", attrs={"name": "csrf-token"})["content"]
        self._csrf_token = final_csrf
        self.is_authenticated = True
        # Always Fetch semester IDs after successful login
        # Improve this by making it a separate method later
        self._semester_ids = await SemesterHandler.get_semester_ids(self._session)

    async def get_seating_info(self) -> List[SeatingInformation]:
        if not self.is_authenticated: raise Exception("Not authenticated.")
        return await SeatingInformationHandler.get_page(self._session)

    async def get_profile(self) -> Profile: 
        if not self.is_authenticated: raise Exception("Not authenticated.")
        return await ProfilePageHandler.get_page(self._session)

    async def get_courses(self, semester: Optional[int] = None) -> Dict[int, List[Course]]:
        if not self.is_authenticated: raise Exception("Not authenticated.")
        # Fetch courses for a specific semester or all semesters if none specified
        semesters_to_fetch = {semester: self._semester_ids[semester]} if semester and semester in self._semester_ids else self._semester_ids
        courses_data = {}
        for sem_num, sem_id in semesters_to_fetch.items():
            courses_data[sem_num] = await CoursesPageHandler.get_courses_in_semester(self._session, sem_id)
        return courses_data

    async def get_attendance(self, semester: Optional[int] = None) -> Dict[int, List[Course]]:
        if not self.is_authenticated: raise Exception("Not authenticated.")
        attendance_data = {}
        # Fetch attendance for a specific semester or all semesters if none specified
        semesters_to_fetch = {semester: self._semester_ids[semester]} if semester and semester in self._semester_ids else self._semester_ids
        for sem_num, sem_id in semesters_to_fetch.items():
            attendance_data[sem_num] = await AttendancePageHandler.get_attendance_in_semester(self._session, sem_id)
        return attendance_data
    
    async def get_announcements(self) -> List[Announcement]:
        if not self.is_authenticated: raise Exception("Not authenticated.")
        return await AnnouncementPageHandler.get_page(self._session)

    async def get_units_for_course(self, course_id: str) -> List[Unit]:
        if not self.is_authenticated: raise Exception("Not authenticated.")
        return await CourseDetailPageHandler.get_page(self._session, course_id)

    async def get_topics_for_unit(self, unit_id: str) -> List[Topic]:
        if not self.is_authenticated: raise Exception("Not authenticated.")
        return await UnitPageHandler.get_page(self._session, unit_id)

    async def get_material_links(self, topic: Topic, material_type_id: str) -> List[MaterialLink]:
        if not self.is_authenticated: raise Exception("Not authenticated.")
        return await MaterialLinksHandler.get_page(self._session, topic, material_type_id)
    
    async def get_results(self, semester_id: str) -> SemesterResult:
        if not self.is_authenticated: raise Exception("Not authenticated.")
        return await ResultsPageHandler.get_page(self._session, semester_id)

    async def close(self):
        await self._session.aclose()