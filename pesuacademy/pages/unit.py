"""This module handles fetching and parsing Unit information from the PESU Academy website.."""

import re

import httpx
from bs4 import BeautifulSoup

from pesuacademy import constants
from pesuacademy.models import Topic
from pesuacademy.util import _build_params


class _UnitPageHandler:
    @staticmethod
    async def _get_page(session: httpx.AsyncClient, unit_id: str) -> list[Topic]:
        """Fetches the page for a specific unit and scrapes the list of topics and their required IDs.

        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.
            unit_id (str): The ID of the unit to fetch topics for.

        Returns:
            List[Topic]: A list of Topic objects containing the scraped data.

        Raises:
            httpx.HTTPStatusError: If the request to the unit page fails.
        """
        params = _build_params(constants._PageURLParams.UnitDetail, coursecontentid=unit_id)
        response = await session.get(constants.PAGES_BASE_URL, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Find the topics table
        table = soup.find("table", class_="table-bordered")
        if not table:
            return []

        topics = []
        for row in table.find("tbody").find_all("tr"):
            onclick_attr = row.get("onclick")
            if not onclick_attr:
                continue

            # handleclasscoursecontentunit('topic_id', 'course_id', 'unit_id', ...)
            match = re.search(
                r"handleclasscoursecontentunit\('([^']*)','([^']*)','([^']*)'",
                onclick_attr,
            )
            if not match:
                continue
            # Extract the first three critical arguments from the JS function
            # The MaterialLinksHandler needs only these 3 ids to fetch the material links
            topic_id, course_id, scraped_unit_id = match.groups()

            title_tag = row.find("span", class_="short-title")
            if not title_tag:
                continue
            # Get the title of the topic, defaulting to "Untitled Topic" if not found
            title = title_tag.get("title", "Untitled Topic")

            topics.append(
                Topic(
                    title=title,
                    id=topic_id,
                    course_id=course_id,
                    unit_id=scraped_unit_id,
                )
            )

        return topics
