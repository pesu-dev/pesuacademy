"""This module handles fetching and parsing the seating information page from the PESU Academy website.."""

import httpx
from bs4 import BeautifulSoup

from pesuacademy import constants
from pesuacademy.models import SeatingInformation
from pesuacademy.util import _build_params


class _SeatingInformationHandler:
    @staticmethod
    async def _get(session: httpx.AsyncClient) -> list[SeatingInformation]:
        """Fetches and parses the seating information page.

        This method is tightly coupled to the HTML structure of `Seating Information` page in PESUAcademy.
        If no test seating information is found, an empty list is returned.

        Args:
            session (httpx.AsyncClient): An active HTTP Client session used to make the request
                                        to the `Seating Information` page.

        Returns:
            List[SeatingInformation]: A list of `SeatingInformation` objects parsed from the page.

        Raises:
            httpx.HTTPStatusError: If the request to the seating information page fails. [ Non-2xx status code ]
        """
        params = _build_params(
            constants._PageURLParams.SeatingInformation,
        )
        response = await session.get(constants.PAGES_BASE_URL, params=params)
        response.raise_for_status()

        if "No Test Seating Info is available" in response.text:  # Check if no seating info is available
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
            if len(cols) >= constants.SEATING_INFO_EXPECTED_COLUMNS:
                seating_info.append(
                    SeatingInformation(
                        name=cols[0],
                        course_code=cols[1],
                        date=cols[2],
                        time=cols[3],
                        terminal=cols[4],
                        block=cols[5],
                    )
                )
        return seating_info
