import datetime
import httpx
from bs4 import BeautifulSoup
from typing import List
from models import Course, Attendance

class AttendancePageHandler:
    @staticmethod
    async def get_attendance_in_semester(session: httpx.AsyncClient, semester_id: str) -> List[Course]:
        """ Fetches the attendance for a single given semester ID.
        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.
            semester_id (str): The ID of the semester to fetch attendance for.
        Returns:
            List[Course]: A list of Course objects containing attendance information.
        Raises:
            httpx.HTTPStatusError: If the request to the attendance page fails.
        """
        url = "/s/studentProfilePESUAdmin"
        params = {
            "menuId": "660", "controllerMode": "6407", "actionType": "8", "batchClassId": semester_id,
            "_": str(int(datetime.datetime.now().timestamp() * 1000)),
        }
        response = await session.get(url, params=params)
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
                attended_classes, total_classes = None, None
                if "/" in cols[2]:
                    try:
                        attended, total = cols[2].split("/")
                        attended_classes, total_classes = int(attended), int(total)
                    except ValueError:
                        pass # Keep them as None if conversion fails
                
                percentage = None
                try:
                    percentage = float(cols[3])
                except ValueError:
                    pass # Keep as None if "NA"

                course_attendance = Attendance(
                    attended_classes=attended_classes,
                    total_classes=total_classes,
                    percentage=percentage
                )
                course = Course(
                    code=cols[0], title=cols[1], attendance=course_attendance
                )
                attendance_data.append(course)
        return attendance_data