"""This module handles the scraping of courses from the PESU Academy website."""

import httpx
from bs4 import BeautifulSoup

from pesuacademy import constants
from pesuacademy.models import Course
from pesuacademy.util import _build_params


class _CoursesPageHandler:
    @staticmethod
    async def _get(session: httpx.AsyncClient, semester_id: str) -> list[Course]:
        """Fetches the courses for a single given semester identifier.

        This method is tightly coupled to the HTML structure of `Courses` page in PESUAcademy.
        The course identifier is extracted from the `id` attribute of the table row `<tr>` tag
        (e.g., `'rowWiseCourseContent_...'`).

        Args:
            session (httpx.AsyncClient): An active HTTP Client session used to make the request
                                        to the `Courses` page.
            semester_id (str): The identifier of the semester to fetch courses for.

        Returns:
            List[Course]: A list of `Course` objects parsed from the page. Returns
                        an empty list if no courses are found.

        Raises:
            httpx.HTTPStatusError: If the request to the courses page fails. [ Non-2xx status code ]
        """
        params = _build_params(constants._PageURLParams.Courses, id=semester_id)

        response = await session.get(constants.PAGES_BASE_URL, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("table", class_="table-hover")
        if not table or "No subjects found" in table.text:
            return []

        courses = []
        # Iterate through each Course row
        for row in table.find("tbody").find_all("tr"):
            row_id = row.get("id")
            # Ensure the row ID is valid and contains the expected prefix
            if not row_id or "rowWiseCourseContent_" not in row_id:
                continue
            # Split and extract the course ID from the row ID
            try:
                course_id = row_id.split("_")[-1]
            except IndexError:
                continue

            cols = [c.text.strip() for c in row.find_all("td")]

            if len(cols) >= 4:
                courses.append(
                    Course(
                        code=cols[0],
                        title=cols[1],
                        type=cols[2],
                        status=cols[3],
                        id=course_id,
                    )
                )
        return courses
