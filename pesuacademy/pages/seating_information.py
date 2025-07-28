import datetime
import httpx
from bs4 import BeautifulSoup
from typing import List
from models import SeatingInformation

class SeatingInformationHandler:
    @staticmethod
    async def get_page(session: httpx.AsyncClient) -> List[SeatingInformation]:
        """ Fetches and parses the seating information page.
        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.
        Returns:
            List[SeatingInformation]: A list of SeatingInformation objects containing the seating details.
        Raises:
            httpx.HTTPStatusError: If the request to the seating information page fails.
        """
        url = "/s/studentProfilePESUAdmin"
        params = {
            "menuId": "655", "controllerMode": "6404", "actionType": "5",
            "_": str(int(datetime.datetime.now().timestamp() * 1000)),
        }
        response = await session.get(url, params=params)
        response.raise_for_status()
        
        if "No Test Seating Info is available" in response.text: # Check if no seating info is available
            return []

        soup = BeautifulSoup(response.text, "lxml")
        info_table = soup.find("table", id="seatinginfo")
        if not info_table:
            return []

        # Parse the seating information data
        # The table structure is assumed to have columns: Name, Course Code, Date, Time, Terminal, Block
        seating_info = []
        for row in info_table.find("tbody").find_all("tr"):
            cols = [c.text.strip() for c in row.find_all("td")]
            if len(cols) >= 6:
                seating_info.append(
                    SeatingInformation(
                        name=cols[0], course_code=cols[1], date=cols[2],
                        time=cols[3], terminal=cols[4], block=cols[5]
                    )
                )
        return seating_info