import datetime
import re

import httpx
from bs4 import BeautifulSoup


class _SemesterHandler:
    @staticmethod
    async def _get_semester_ids(session: httpx.AsyncClient) -> dict[int, str]:
        """Fetches semester IDs by calling the dynamic endpoint and cleaning the extracted values.

        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.

        Returns:
            dict[int, str]: A dictionary mapping semester numbers to their corresponding IDs.

        Raises:
            httpx.HTTPStatusError: If the request to the semester endpoint fails.
            Exception: If the semester data cannot be fetched or parsed correctly.
        """
        url = "/a/studentProfilePESU/getStudentSemestersPESU"
        params = {"_": str(int(datetime.datetime.now().timestamp() * 1000))}

        response = await session.get(url, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        options = soup.find_all("option")

        if not options:
            raise Exception("Failed to fetch semester data from the endpoint.")

        semester_ids = {}

        # Too many fixes done, need to refactor this later
        for option in options:
            raw_value = option.get("value")  # Fetches a wierd formatted value (eg.'\"2763\"')
            text = option.text.strip()

            # Find the sem number from text (e.g. the '2' in 'Sem-2')
            text_match = re.search(r"\d+", text)

            if raw_value and text_match:
                # Imp Fix: Clean the raw value to extract the numeric part
                # Finds each numeric part of the raw value (e.g. '2763') and joins it to form a clean numeric string
                clean_value = "".join(re.findall(r"\d+", raw_value))

                if clean_value:  # Make sure we actually found a number
                    semester_number = int(
                        text_match.group(0)
                    )  # Extract the semester number from the text
                    # Store the clean numeric string (e.g., "2763") as the ID
                    semester_ids[semester_number] = clean_value

        return semester_ids
