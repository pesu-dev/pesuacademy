"""PESU Academy API Client."""

import os

from dotenv import load_dotenv

# Import the core engine
from pesuacademy.client import _PesuScraper

# Import all Pydantic models to be used as return types for clarity
from pesuacademy.models import (
    Announcement,
    Course,
    MaterialLink,
    Profile,
    SeatingInformation,
    SemesterResult,
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
        """Asynchronously logs in and creates an authenticated session.

        Credentials can be passed as arguments or loaded from environment variables
        (PESU_USERNAME, PESU_PASSWORD) in a `.env` file.

        Args:
            username (Optional[str]): The user's login identifier. Defaults to
                the `PESU_USERNAME` environment variable.
            password (Optional[str]): The user's password. Defaults to the
                `PESU_PASSWORD` environment variable.

        Returns:
            PESUAcademy: An authenticated instance of the PESUAcademy class.

        Raises:
            ValueError: If credentials are not provided either as arguments
                or as environment variables.
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
        """Fetches and displays all details of the user's profile under PESU Academy in an organized manner.

        Args Required:
            None

        Returns:
            A Profile object containing user's personal details
            as well as parent details, qualifying examination, address and other information.
        """
        return await self._client.get_profile()

    async def get_seating_info(self) -> list[SeatingInformation]:
        """Fetches seating arrangement details of the user's upcoming examinations.

        Args Required:
            None

        Returns:
            User's examination seating details i.e course name, course code,
            examination date, time, location and block in the format of a list.
        """
        return await self._client.get_seating_info()

    async def get_courses(self, semester: int | None = None) -> dict[int, list[Course]]:
        """Fetches details of the courses that the user has registered for.

        Can view details of courses for a specific semester or all available
        semesters depending on the argument provided.

        Args Required:
            semester (Optional[int]): Optional user input is semester number
            to fetch course details from. If not provided, details of courses for
            all available semesters are returned.

        Returns:
            A dictionary with semester number/s as key/s and lists with course details i.e.
            code, title, type, status, attendance and id as its values.
        """
        return await self._client.get_courses(semester)

    async def get_attendance(self, semester: int | None = None) -> dict[int, list[Course]]:
        """Fetches details of the user's attendance records from PESU Academy.

        Args Required:
            semester (Optional[int]):  Optional user input is semester number
            to fetch attendance details from. If not provided, attendance details
            for all available semesters is returned.

        Returns:
            A dictionary with semester number/s as key/s and lists of course objects
            that contain user's attendance records in those courses respectively.
        """
        return await self._client.get_attendance(semester)

    async def get_results(self, semester: int) -> SemesterResult:
        """Fetches the final result as well as details of result for the semester entered by the user.

        Args:
            semester (int): The semester number for which final results
            are to be fetched.

        Returns:
            A SemesterResult object containing semester number, user's SGPA,
            credit details (if any), and course result details.

        Raises:
            ValueError: If the requested semester is invalid or has no results.
        """
        semester_id_str = self._client._semester_ids.get(semester)
        if not semester_id_str:
            raise ValueError(
                f"Invalid or unavailable semester: {semester}. Available: {list(self._client._semester_ids.keys())}"
            )
        return await self._client.get_results(semester_id_str)

    async def get_announcements(self) -> list[Announcement]:
        """Fetches the details of all recent announcements from the PESU Academy dashboard.

        Args:
            None

        Returns:
            A list of Announcement objects containing details of the latest announcements
            i.e. its title, date of announcement, content and attachments provided (if any).
        """
        return await self._client.get_announcements()

    # < Methods for the Materials Workflow >

    async def get_units_for_course(self, course_id: str) -> list[Unit]:
        """Fetches the list of units within the course_id provided by user.

        The course_id can be obtained from the Course model returned by `get_courses()`.

        Args Required:
            course_id (str): The unique internal ID for the course.

        Returns:
            A list of Unit objects containing title of the unit and unit_id.
        """
        return await self._client.get_units_for_course(course_id)

    async def get_topics_for_unit(self, unit_id: str) -> list[Topic]:
        """Fetches the list of topics within the unit_id provided by the user.

        The unit_id can be obtained from the Unit model.

        Args Required:
            unit_id (str): The unique internal ID for the required unit.

        Returns:
            A list of Topic objects containing IDs i.e. title, topic_id,
            course_id, unit_id needed for the final step (retrieving material links).
        """
        return await self._client.get_topics_for_unit(unit_id)

    async def get_material_links(self, topic: Topic, material_type_id: str) -> list[MaterialLink]:
        """Given a Topic object and a material type ID through user input, fetches the final required download links.

        Args Required:
            topic (Topic): The Topic object obtained from `get_topics_for_unit()`.
            material_type_id (str): A string representing the material type (e.g., "2" for Slides, "3" for Notes).

        Returns:
            A list of MaterialLink objects containing material title, URL, and a bool string
            indicating whether the URL provided is that of a PDF file.
        """
        return await self._client.get_material_links(topic, material_type_id)

    async def close(self) -> None:
        """Closes the network session gracefully.

        This should always be called when you are finished with the session to release resources.
        """
        await self._client.close()
