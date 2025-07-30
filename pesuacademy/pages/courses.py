import datetime
import httpx
from bs4 import BeautifulSoup
from typing import List
from ..models import Course
from .. import constants

class CoursesPageHandler:
    @staticmethod
    async def get_courses_in_semester(session: httpx.AsyncClient, semester_id: str) -> List[Course]:
        """ Fetches the courses for a single given semester ID.
        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.
            semester_id (str): The ID of the semester to fetch courses for.
        Returns:
            List[Course]: A list of Course objects containing course information.
        Raises:
            httpx.HTTPStatusError: If the request to the courses page fails.
        """
        url = "/s/studentProfilePESUAdmin"
        params = {
            "menuId": constants.PageURLParams.Courses.MENU_ID,
            "controllerMode": constants.PageURLParams.Courses.CONTROLLER_MODE,
            "actionType": constants.PageURLParams.Courses.ACTION_TYPE,
            "id": semester_id, # Some wierd formating error in semester id, made a temp fix but will have to find a better way later
            "_": str(int(datetime.datetime.now().timestamp() * 1000)),
        }

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
                course_id = row_id.split('_')[-1]
            except IndexError:
                continue

            cols = [c.text.strip() for c in row.find_all("td")]

            if len(cols) >= 4: # Temp fix to ensure we have enough columns
                courses.append(
                    Course(
                        code=cols[0],
                        title=cols[1],
                        type=cols[2],
                        status=cols[3],
                        course_id=course_id
                    )
                )
        return courses