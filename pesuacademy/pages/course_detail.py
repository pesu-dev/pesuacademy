import datetime
import httpx
import re
from bs4 import BeautifulSoup
from typing import List
from ..models.materials import Unit
from .. import constants


class CourseDetailPageHandler:
    @staticmethod
    async def get_page(session: httpx.AsyncClient, course_id: str) -> List[Unit]:
        """ Fetches the main page for a course and scrapes the list of units.
        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.
            course_id (str): The ID of the course to fetch units for.   
        Returns:
            List[Unit]: A list of Unit objects containing the scraped data.
        Raises:
            httpx.HTTPStatusError: If the request to the course page fails.
        """
        url = "/s/studentProfilePESUAdmin"
        params = {
            "controllerMode": constants.PageURLParams.CourseDetail.CONTROLLER_MODE,
            "actionType": constants.PageURLParams.CourseDetail.ACTION_TYPE,
            "id": course_id,
            "menuId": constants.PageURLParams.CourseDetail.MENU_ID,
            "_": str(int(datetime.datetime.now().timestamp() * 1000)),
        }
        response = await session.get(url, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Find the units container
        units_container = soup.find("ul", id="courselistunit")
        if not units_container:
            return []

        units = []
        unit_links = units_container.find_all("a")

        for link in unit_links:
            # Title
            title = link.get("title")
            onclick_attr = link.get("onclick")
            
            # Skip if title or onclick attribute is missing
            if not title or not onclick_attr:
                continue

            # Get the unit ID from the onclick attribute
            match = re.search(r"handleclassUnit\('(\d+)'\)", onclick_attr)
            if match:
                unit_id = match.group(1)
                units.append(Unit(title=title, unit_id=unit_id))
        
        return units