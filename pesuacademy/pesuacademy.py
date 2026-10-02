"""PESU Academy API Client."""

import os

from dotenv import load_dotenv

# Import the core engine
from pesuacademy.client import _PesuScraper

# Import all Pydantic models to be used as return types for clarity
from pesuacademy.models import (
    Announcement,
    CGPAResult,
    Course,
    Credits,
    MaterialLink,
    Profile,
    SeatingInformation,
    SemesterResult,
    SemesterSGPA,
    Timetable,
    Topic,
    Unit,
)


class PESUAcademy:
    """The main, user-facing class to interact with PESU Academy.

    An instance of this class represents a single authenticated session and provides
    asynchronous methods to fetch academic data.
    """

    def __init__(self, client: _PesuScraper) -> None:
        """Initializes the PESUAcademy session.

        This method is not meant to be called directly.
        Please use the `PESUAcademy.login()` class method to create an instance.

        Args:
            client (_PesuScraper): An authenticated instance of the core client.
        """
        self._client = client

    @classmethod
    async def login(cls, username: str | None = None, password: str | None = None) -> "PESUAcademy":
        """Creates and returns an authenticated PESUAcademy session.

        Credentials can be passed as arguments or loaded from environment variables
        (PESU_USERNAME, PESU_PASSWORD).

        Args:
            username (Optional[str]): The user's login identifier.
            password (Optional[str]): The user's password.
        """
        load_dotenv()  # Load environment variables from .env file
        uname = username or os.environ.get("PESU_USERNAME")
        pword = password or os.environ.get("PESU_PASSWORD")

        if not uname or not pword:
            raise ValueError(
                "Credentials not provided. "
                "Pass them as arguments or set PESU_USERNAME and PESU_PASSWORD environment variables."
            )

        client = _PesuScraper()
        await client.login(uname, pword)
        return cls(client)

    async def get_profile(self) -> Profile:
        """Fetches the student's detailed profile information.

        Args:
            None

        Returns:
            Profile: A Profile object containing personal, parent, and address details.
        """
        return await self._client.get_profile()

    async def get_seating_info(self) -> list[SeatingInformation]:
        """Fetches upcoming exam seating arrangements.

        Args:
            None

        Returns:
            A list of SeatingInformation objects containing seating details.
        """
        return await self._client.get_seating_info()

    async def get_courses(self, semester: int | None = None) -> dict[int, list[Course]]:
        """Fetches registered courses.

        Args:
            semester (Optional[int]): The semester number to fetch. If not provided,
                courses for all available semesters are returned.

        Returns:
            A dictionary mapping semester numbers to lists of Course objects.
        """
        return await self._client.get_courses(semester)

    async def get_attendance(self, semester: int | None = None) -> dict[int, list[Course]]:
        """Fetches attendance records.

        Args:
            semester (Optional[int]): The semester number to fetch. If not provided,
                attendance for all available semesters is returned.

        Returns:
            A dictionary mapping semester numbers to lists of Course objects with attendance data.
        """
        return await self._client.get_attendance(semester)

    async def get_results(self, semester: int) -> SemesterResult:
        """Fetches the final results for a specific semester.

        Args:
            semester (int): The semester number for which to fetch results.

        Returns:
            A SemesterResult object containing SGPA, credits, and subject details.

        Raises:
            ValueError: If the requested semester is invalid or has no results.
        """
        semester_id_str = self._client._semester_ids.get(semester)
        if not semester_id_str:
            raise ValueError(
                f"Invalid or unavailable semester: {semester}. Available: {list(self._client._semester_ids.keys())}"
            )
        return await self._client.get_results(semester_id_str, semester)

    async def get_sgpa(self, semester: int) -> tuple[str, Credits]:
        """Fetches only the SGPA and credits for a specific semester.

        Args:
            semester (int): The semester number.

        Returns:
            tuple[str, Credits]: A tuple containing the SGPA string and a Credits object.

        Raises:
            ValueError: If the requested semester is invalid or has no results.
        """
        semester_id_str = self._client._semester_ids.get(semester)
        if not semester_id_str:
            raise ValueError(
                f"Invalid or unavailable semester: {semester}. Available: {list(self._client._semester_ids.keys())}"
            )
        return await self._client.get_sgpa(semester_id_str, semester)

    async def get_cgpa(self) -> CGPAResult:
        """Calculates the cumulative CGPA by fetching all SGPAs for the student.

        Returns:
            CGPAResult: An object containing the overall CGPA, total credits, and a breakdown of all semesters.
        """
        semester_list = []
        total_earned_credits = 0.0
        total_grade_points = 0.0

        for sem in sorted(self._client._semester_ids.keys()):
            sgpa_str, credits = await self.get_sgpa(semester=sem)
            semester_list.append(SemesterSGPA(semester=sem, sgpa=sgpa_str, credits=credits))

            # Add to CGPA calculation if SGPA is a valid number
            if sgpa_str != "N/A":
                try:
                    sem_sgpa = float(sgpa_str)
                    sem_credits_earned = float(credits.earned)
                    total_grade_points += sem_sgpa * sem_credits_earned
                    total_earned_credits += sem_credits_earned
                except ValueError:
                    pass

        if total_earned_credits > 0:
            cgpa_val = round(total_grade_points / total_earned_credits, 2)
            cgpa_str = f"{cgpa_val:.2f}"
        else:
            cgpa_str = "N/A"

        earned_credits_str = str(total_earned_credits).rstrip("0").rstrip(".")
        total_credits = Credits(earned=earned_credits_str, total=earned_credits_str)

        return CGPAResult(cgpa=cgpa_str, credits=total_credits, semesters=semester_list)

    async def get_announcements(self) -> list[Announcement]:
        """Fetches all recent announcements from the dashboard.

        Args:
            None

        Returns:
            A list of Announcement objects containing the latest announcements.
        """
        return await self._client.get_announcements()

    # < Methods for the Materials Workflow >

    async def get_units_for_course(self, course_id: str) -> list[Unit]:
        """Given a course_id, fetches the list of units within it.

        The course_id can be obtained from the Course model returned by `get_courses()`.

        Args:
            course_id (str): The unique internal ID for the course.

        Returns:
            A list of Unit objects.
        """
        return await self._client.get_units_for_course(course_id)

    async def get_topics_for_unit(self, unit_id: str) -> list[Topic]:
        """Given a unit_id, fetches the list of topics within it.

        The unit_id can be obtained from the Unit model.

        Args:
            unit_id (str): The unique internal ID for the unit.

        Returns:
            A list of Topic objects, containing IDs needed for the final step.
        """
        return await self._client.get_topics_for_unit(unit_id)

    async def get_material_links(self, topic: Topic, material_type_id: str) -> list[MaterialLink]:
        """Given a Topic object and a material type ID, fetches the final download links.

        Args:
            topic (Topic): The Topic object obtained from `get_topics_for_unit()`.
            material_type_id (str): A string representing the material type (e.g., "2" for Slides, "3" for Notes).

        Returns:
            A list of MaterialLink objects.
        """
        return await self._client.get_material_links(topic, material_type_id)

    async def get_timetable(self) -> Timetable:
        """Fetches the student's timetable.

        Args:
            None

        Returns:
            Timetable: A Timetable object containing the student's timetable details.
        """
        return await self._client.get_timetable()

    async def close(self) -> None:
        """Closes the network session gracefully.

        This should always be called when you are finished with the session to release resources.
        """
        await self._client.close()
