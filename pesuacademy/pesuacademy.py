from typing import Optional, List, Dict

# Import the core engine
from .client import PesuAcademyClient

# Import all Pydantic models to be used as return types for clarity
from .models import (
    Profile,
    Course,
    SeatingInformation,
    SemesterResult,
    Announcement,
    Unit,
    Topic,
    MaterialLink
)


class PESUAcademy:
    """
    The main, user-facing class to interact with PESU Academy.

    An instance of this class represents a single authenticated session and provides
    asynchronous methods to fetch academic data.
    """

    def __init__(self, client: PesuAcademyClient):
        """
        Initializes the PESUAcademy session. This method is not meant to be called directly.
        Please use the `PESUAcademy.login()` class method to create an instance.

        Args:
            client (PesuAcademyClient): An authenticated instance of the core client.
        """
        self._client = client

    @classmethod
    async def login(cls, username: str, password: str) -> "PESUAcademy":
        """
        Creates, authenticates, and returns an active PESUAcademy session.
        This is the primary way to start using the library.

        Args:
            username (str): The user's SRN, PRN, or other login identifier.
            password (str): The user's password.

        Returns:
            PESUAcademy: An authenticated instance ready to make requests.
        """
        client = PesuAcademyClient()
        await client.login(username, password)
        return cls(client)

    async def get_profile(self) -> Profile:
        """Fetches the student's detailed profile information.
        
        Args:
            None

        Returns:
            Profile: A Profile object containing personal, parent, and address details.
        """
        return await self._client.get_profile()

    async def get_seating_info(self) -> List[SeatingInformation]:
        """Fetches upcoming exam seating arrangements.
        
        Args:
            None
            
        Returns:
            A list of SeatingInformation objects containing seating details."""
        return await self._client.get_seating_info()

    async def get_courses(self, semester: Optional[int] = None) -> Dict[int, List[Course]]:
        """
        Fetches registered courses.

        Args:
            semester (Optional[int]): The semester number to fetch. If not provided,
                courses for all available semesters are returned.

        Returns:
            A dictionary mapping semester numbers to lists of Course objects.
        """
        return await self._client.get_courses(semester)

    async def get_attendance(self, semester: Optional[int] = None) -> Dict[int, List[Course]]:
        """
        Fetches attendance records.

        Args:
            semester (Optional[int]): The semester number to fetch. If not provided,
                attendance for all available semesters is returned.

        Returns:
            A dictionary mapping semester numbers to lists of Course objects with attendance data.
        """
        return await self._client.get_attendance(semester)

    async def get_results(self, semester: int) -> SemesterResult:
        """
        Fetches the final results for a specific semester.

        Args:
            semester (int): The semester number for which to fetch results.

        Returns:
            A SemesterResult object containing SGPA, credits, and subject details.
        
        Raises:
            ValueError: If the requested semester is invalid or has no results.
        """
        semester_id_str = self._client._semester_ids.get(semester)
        if not semester_id_str:
            raise ValueError(f"Invalid or unavailable semester: {semester}. Available: {list(self._client._semester_ids.keys())}")
        return await self._client.get_results(semester_id_str)

    async def get_announcements(self) -> List[Announcement]:
        """Fetches all recent announcements from the dashboard.
        
        Args:
            None    

        Returns:
            A list of Announcement objects containing the latest announcements.
        """
        return await self._client.get_announcements()
    
    # < Methods for the Materials Workflow >

    async def get_units_for_course(self, course_id: str) -> List[Unit]:
        """
        Given a course_id, fetches the list of units within it.
        The course_id can be obtained from the Course model returned by `get_courses()`.

        Args:
            course_id (str): The unique internal ID for the course.

        Returns:
            A list of Unit objects.
        """
        return await self._client.get_units_for_course(course_id)

    async def get_topics_for_unit(self, unit_id: str) -> List[Topic]:
        """
        Given a unit_id, fetches the list of topics within it.
        The unit_id can be obtained from the Unit model.

        Args:
            unit_id (str): The unique internal ID for the unit.

        Returns:
            A list of Topic objects, containing IDs needed for the final step.
        """
        return await self._client.get_topics_for_unit(unit_id)

    async def get_material_links(self, topic: Topic, material_type_id: str) -> List[MaterialLink]:
        """
        Given a Topic object and a material type ID, fetches the final download links.

        Args:
            topic (Topic): The Topic object obtained from `get_topics_for_unit()`.
            material_type_id (str): A string representing the material type (e.g., "2" for Slides, "3" for Notes).

        Returns:
            A list of MaterialLink objects.
        """
        return await self._client.get_material_links(topic, material_type_id)

    async def close(self):
        """
        Closes the network session gracefully. This should always be called when
        you are finished with the session to release resources.
        """
        await self._client.close()