import httpx
from bs4 import BeautifulSoup

from .. import constants
from ..models import Course
from ..util import build_params


class _CoursesPageHandler:
    @staticmethod
    async def _get_page(session: httpx.AsyncClient, semester_id: str) -> list[Course]:
        """Fetches the courses for a single given semester ID.

        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.
            semester_id (str): The ID of the semester to fetch courses for.

        Returns:
            List[Course]: A list of Course objects containing course information.

        Raises:
            httpx.HTTPStatusError: If the request to the courses page fails.
        """
        url = "/s/studentProfilePESUAdmin"
        params = build_params(constants.PageURLParams.Courses, id=semester_id)

        response = await session.get(url, params=params)
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
                        course_id=course_id,
                    )
                )
        return courses
