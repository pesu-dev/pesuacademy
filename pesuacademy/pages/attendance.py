"""This module handles the scraping of attendance data from the PESU Academy website."""

import httpx
from bs4 import BeautifulSoup

from pesuacademy import constants
from pesuacademy.models import Attendance, Course
from pesuacademy.util import _build_params


class _AttendancePageHandler:
    @staticmethod
    async def _get_page(session: httpx.AsyncClient, semester_id: str) -> list[Course]:
        """Fetches the attendance for a single given semester ID.

        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.
            semester_id (str): The ID of the semester to fetch attendance for.

        Returns:
            List[Course]: A list of Course objects containing attendance information.

        Raises:
            httpx.HTTPStatusError: If the request to the attendance page fails.
        """
        params = _build_params(constants._PageURLParams.Attendance, batchClassId=semester_id)
        response = await session.get(constants.PAGES_BASE_URL, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("table", class_="box-shadow")
        if not table or "Data Not Available" in table.text:
            return []

        # Parse the attendance data
        # The table structure is assumed to have columns: Code, Title, Attended/Total, Percentage
        attendance_data = []
        for row in table.find("tbody").find_all("tr"):
            cols = [c.text.strip() for c in row.find_all("td")]
            if len(cols) >= 4:
                attended, total = None, None
                if "/" in cols[2]:
                    try:
                        attended, total = cols[2].split("/")
                        attended, total = int(attended), int(total)
                    except ValueError:
                        pass  # Keep them as None if conversion fails

                percentage = None
                try:
                    percentage = float(cols[3])
                except ValueError:
                    pass  # Keep as None if "NA"

                course_attendance = Attendance(attended=attended, total=total, percentage=percentage)
                course = Course(code=cols[0], title=cols[1], attendance=course_attendance)
                attendance_data.append(course)
        return attendance_data
