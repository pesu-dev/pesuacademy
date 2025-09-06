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
    Timetable,
    Topic,
    Unit,
)


class PESUAcademy:
    """The main, user-facing class to interact with PESU Academy.

    This class provides a high-level asynchronous interface for fetching academic
    data. An instance of this class represents a single, authenticated user
    session.
    """

    def __init__(self, client: _PesuScraper) -> None:
        """Initializes the PESUAcademy session.

        Note:
            This constructor is not meant to be called directly by the user.
            Please use the `PESUAcademy.login()` class method as a factory
            to create a properly authenticated instance.

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
            username (Optional[str]): The user's login identifier as used in  https://www.pesuacademy.com/Academy/.
            Defaults to the `PESU_USERNAME` environment variable.
            password (Optional[str]): The user's password. Defaults to the
                `PESU_PASSWORD` environment variable.

        Returns:
            PESUAcademy: An authenticated instance of the PESUAcademy class.

        Raises:
            ValueError: If credentials are not provided either as arguments
                or as environment variables.

        Example:
            >>> async def main():
            ...     pesu_session = await PESUAcademy.login("YOUR_PRN", "YOUR_PASSWORD")
            ...     profile = await pesu_session.get_profile()
            ...     print(f"Hello, {profile.personal.name}")
            ...     await pesu_session.close()
            >>>
            >>> if __name__ == "__main__":
            ...     asyncio.run(main())
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
        """Fetches all details of the user's profile under PESU Academy in an organized manner.

        Args:
            None

        Returns:
            Profile: A Profile object containing user's personal details
            as well as parent details, qualifying examination, address and other information.

        Example:
            >>> profile = await session.get_profile()
            >>> print(f"Name: {profile.personal.name}")
            >>> print(f"Qualifying examination: {profile.qualifying_exam.exam} : {profile.qualifying_exam.score}")
        """
        return await self._client.get_profile()

    async def get_seating_info(self) -> list[SeatingInformation]:
        """Fetches seating arrangement details of the user's examinations.

        Args:
            None

        Returns:
            list[SeatingInformation]: A list containing user's examination seating details i.e course name, course code,
            examination date, time, location and block.

        Example:
            >>> seating_info = await session.get_seating_info()
            >>> print(
            ...     f"{seating_info.name} on {seating_info.date} at {seating_info.time} in {seating_info.terminal}
            ...- {seating_info.block}")
        """
        return await self._client.get_seating_info()

    async def get_courses(self, semester: int | None = None) -> dict[int, list[Course]]:
        """Fetches details of the courses that the user has registered for.

        Can fetch details of courses for a specific semester or all available
        semesters depending on the argument provided.

        Args:
            semester (Optional[int]): The semester number for which courses are to
            be fetched. If not provided, details of courses for
            all available semesters are returned.

        Returns:
            dict[int, list[Course]]: A dictionary with semester number/s as key/s and lists with course details i.e.
            code, title, type, status, attendance and id as its value/s.

        Example:
            >>> sem_4_courses = await session.get_courses(semester=4)
            >>> for course in sem_4_courses.get(4, []):
            ...     print(f"Course: {course.title} ({course.code})")
        """
        return await self._client.get_courses(semester)

    async def get_attendance(self, semester: int | None = None) -> dict[int, list[Course]]:
        """Fetches details of the user's attendance records from PESU Academy.

        Args:
            semester (Optional[int]): The semester number for which attendance details are to
            be fetched. If not provided, attendance details for all available semesters is returned.

        Returns:
            dict[int, list[Course]]: A dictionary with semester number/s as key/s and lists of course objects
            that contain user's attendance records in those courses respectively.

        Example:
            >>> attendance_data = await session.get_attendance(semester=4)
            >>> courses_for_sem_4 = attendance_data.get(4, [])
            >>> for courses in courses_for_sem_4:
            ...     if courses.attendance:
            ...         print(f"{course.title}: {course.attendance.percentage}%")
            ...     else:
            ...         print(f"{course.title}: Attendance data not available")
        """
        return await self._client.get_attendance(semester)

    async def get_results(self, semester: int) -> SemesterResult:
        """Fetches the final result as well as details of result for the semester entered by the user.

        Args:
            semester (int): The semester number for which final results are to be fetched.

        Returns:
            SemesterResult: An object containing semester number, user's SGPA,
            credit details (if any), and course result details.

        Raises:
            ValueError: If the requested semester is invalid or has no results.

        Example:
            >>> try:
            ...     sem_3_result = await session.get_results(semester=3)
            ...     print(f"Semester 3 SGPA: {sem_3_result.sgpa}")
            ... except ValueError as e:
            ...     print(e)
        """
        semester_id_str = self._client._semester_ids.get(semester)
        if not semester_id_str:
            raise ValueError(
                f"Invalid or unavailable semester: {semester}. Available: {list(self._client._semester_ids.keys())}"
            )
        return await self._client.get_results(semester_id_str)

    async def get_announcements(self) -> list[Announcement]:
        """Fetches the details of all recent announcements from the PESU Academy.

        Args:
            None

        Returns:
            list[Announcement]: Announcement objects containing details of the latest announcements
            i.e. its title, date of announcement, content and attachments provided (if any).

        Example:
            >>> announcements = await session.get_announcements()
            >>> for announcement in announcements:
            ...     print(f"[{announcement.date}] {announcement.title}")
        """
        return await self._client.get_announcements()

    # < Methods for the Materials Workflow >

    async def get_units_for_course(self, course_id: str) -> list[Unit]:
        """Fetches the list of units within the course_id provided by user.

        The course_id can be obtained from the Course model returned by `get_courses()`.

        Args:
            course_id (str): The unique internal ID for the course.

        Returns:
            list[Unit]: A list of `Unit` objects containing title of the unit and unit_id.
        """
        return await self._client.get_units_for_course(course_id)

    async def get_topics_for_unit(self, unit_id: str) -> list[Topic]:
        """Fetches the list of topics within the unit_id provided by the user.

        The unit_id can be obtained from the Unit model.

        Args:
            unit_id (str): The unique internal ID for the required unit.

        Returns:
            list[Topic]: A list of `Topic` objects containing IDs i.e. title, topic_id,
            course_id, unit_id needed for the final step (retrieving material links).
        """
        return await self._client.get_topics_for_unit(unit_id)

    async def get_material_links(self, topic: Topic, material_type_id: str) -> list[MaterialLink]:
        """Given a `Topic` object and a material type ID through user input, fetches the final required download links.

        Args:
            topic (Topic): The `Topic` object obtained from `get_topics_for_unit()`.
            material_type_id (str): A string representing the material type (e.g., "2"
                for Slides, "3" for Notes).

        Returns:
            list[MaterialLink]: A list of `MaterialLink` objects containing material title, URL, and a bool string
            indicating whether the URL provided is that of a PDF file.

        Example:
            >>> # 1. Get courses to find a specific course_id
            >>> courses_data = await session.get_courses(semester=4)
            >>> my_course = courses_data.get(4, [])[0]
            >>>
            >>> # 2. Get units for that course
            >>> units = await session.get_units_for_course(my_course.course_id)
            >>> my_unit = units[0]
            >>>
            >>> # 3. Get topics for that unit
            >>> topics = await session.get_topics_for_unit(my_unit.unit_id)
            >>> my_topic = topics[0]
            >>>
            >>> # 4. Get material links
            >>> material_links = await session.get_material_links(my_topic, "2")
            >>> for link in material_links:
            ...     print(f"{'[PDF] ' if link.is_pdf else ''}{link.title}: {link.url}")
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
        """Closes the underlying network session gracefully. This method is crucial for proper resource management.

        To guarantee that the session is always closed, even if errors occur
        during its use, it is highly recommended to call this method within a
        `try...finally` block.

        Example:
            >>> session = None
            >>> try:
            ...     session = await PESUAcademy.login("YOUR_PRN", "YOUR_PASSWORD")
            ...     profile = await session.get_profile()
            ...     print(f"Hello, {profile.personal.name}")
            ... finally:
            ...     if session:
            ...         await session.close()
            ...         print("Session closed successfully.")
        """
        await self._client.close()
