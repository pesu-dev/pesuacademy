"""This module handles the scraping of course details from the PESU Academy website."""

import re

import httpx
from bs4 import BeautifulSoup

from pesuacademy import constants
from pesuacademy.models import Unit
from pesuacademy.util import _build_params


class _CourseDetailPageHandler:
    @staticmethod
    async def _get(session: httpx.AsyncClient, course_id: str) -> list[Unit]:
        """Fetches the main page for a course and scrapes the list of units.

        This method is tightly coupled to the HTML structure of `Course Detail` page in PESUAcademy.
        The unit identifier is extracted by parsing the JS `handleclassUnit()` function call
        from the `onclick` attribute of each unit's link.
        The unit title is extracted from the link's `title` attribute.

        Args:
            session (httpx.AsyncClient): An active HTTP Client session used to make the request
                                        to the `Course Detail` page.
            course_id (str): The identifier of the course to fetch units for.

        Returns:
            List[Unit]: A list of `Unit` objects scraped from the page. Returns an
                        empty list if no units are found.

        Raises:
            httpx.HTTPStatusError: If the request to the course page fails. [ Non-2xx status code ]
        """
        params = _build_params(constants._PageURLParams.CourseDetail, id=course_id)
        response = await session.get(constants.PAGES_BASE_URL, params=params)
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
                units.append(Unit(title=title, id=unit_id))

        return units
