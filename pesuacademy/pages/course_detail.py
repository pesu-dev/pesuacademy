"""This module handles the scraping of course details from the PESU Academy website."""

import re

import httpx
from bs4 import BeautifulSoup

from pesuacademy import constants
from pesuacademy.models import Unit
from pesuacademy.util import _build_params


class _CourseDetailPageHandler:
    @staticmethod
    async def _get_page(session: httpx.AsyncClient, course_id: str) -> list[Unit]:
        """Fetches the main page for a course and scrapes the list of units.

        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.
            course_id (str): The ID of the course to fetch units for.

        Returns:
            List[Unit]: A list of Unit objects containing the scraped data.

        Raises:
            httpx.HTTPStatusError: If the request to the course page fails.
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
