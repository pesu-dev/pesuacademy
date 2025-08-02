import httpx
from bs4 import BeautifulSoup

from .. import constants
from ..models.results import Assessment, CourseResult, SemesterResult
from ..util import build_params


class _ResultsPageHandler:
    @staticmethod
    async def _get_page(session: httpx.AsyncClient, semester_id: str) -> SemesterResult:
        """Fetches the ESA results for a given semester ID.

        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.
            semester_id (str): The ID of the semester to fetch results for.

        Returns:
            SemesterResult: An object containing the semester results including SGPA, credits earned, and course results.

        Raises:
            httpx.HTTPStatusError: If the request to the results page fails.
        """
        url = "/s/studentProfilePESUAdmin"
        params = build_params(constants.PageURLParams.Results, semid=semester_id)
        response = await session.get(url, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Fetch the summary section
        summary_divs = soup.select("div.dashboard-info-bar > div")
        summary_credits_raw = summary_divs[0].contents[-1].strip()

        credit_parts = summary_credits_raw.split("/")
        credits_earned = credit_parts[0].strip()
        credits_total = (
            credit_parts[1].strip() if len(credit_parts) > 1 else credits_earned
        )  # Fix for cases where total credits are not provided

        # Fetch the SGPA
        sgpa_raw = summary_divs[1].contents[-1].strip()
        # Not fetching CGPA as it is not a part of ESA results for a particular semester
        # Will Fetch it separately if needed later

        course_results = []

        # Ensure the main wrapper exists
        wrapper = soup.find("div", class_="multiple-info-wrapper")
        if not wrapper:
            # Fallback if the wrapper is not found
            return SemesterResult(
                sgpa=sgpa_raw,
                credits_earned=credits_earned,
                credits_total=credits_total,
                courses=[],
            )

        # Find all course containers
        course_containers = wrapper.find_all("div", class_="clearfix")

        for container in course_containers:
            header = container.find("div", class_="header-info")
            if not header:
                continue

            header_text = header.find("h6").text.strip()
            # Extract code and title from the header text
            code, title = (part.strip() for part in header_text.split("-", 1))
            # Extract credits from the header
            credits_text = header.find("h6", class_="text-right").text.strip().split(":")[-1]
            s_credit_parts = credits_text.split("/")
            s_credits_earned = s_credit_parts[0].strip()
            s_credits_total = (
                s_credit_parts[1].strip() if len(s_credit_parts) > 1 else s_credits_earned
            )

            # Extract Assessments or Exams like ISA, ESA, etc.
            assessments = []
            assessment_bar = container.find("div", class_="dashboard-info-bar")
            if not assessment_bar:
                continue

            for assessment_div in assessment_bar.find_all("div", recursive=False):
                name_tag = assessment_div.find("h6")
                if not name_tag:
                    continue
                name = name_tag.text.strip()

                marks, total = None, None

                # Some bizzare method used to find marks
                # The marks are either in a span with class 'dark-text' or in a span
                # with class 'f-size-2x-big' for letter grades
                # The earned marks are inside the 'dark-text' span
                marks_span = assessment_div.find("span", class_="dark-text")
                if marks_span:
                    marks = marks_span.text.strip()
                    # The total marks are the text node after this span
                    if marks_span.next_sibling and isinstance(marks_span.next_sibling, str):
                        total_raw = marks_span.next_sibling.strip()
                        if total_raw.startswith(
                            "/"
                        ):  # If it starts with '/', it means it's a total marks value
                            total = total_raw.replace("/", "").strip()  # Remove the '/'

                # Handle letter grades for ESA
                elif grade_span := assessment_div.find("span", class_="f-size-2x-big"):
                    marks = grade_span.text.strip()

                if name:
                    assessments.append(Assessment(name=name, marks=marks, total=total))

            course_results.append(
                CourseResult(
                    code=code,
                    title=title,
                    credits_earned=s_credits_earned,
                    credits_total=s_credits_total,
                    assessments=assessments,
                )
            )

        return SemesterResult(
            sgpa=sgpa_raw,
            credits_earned=credits_earned,
            credits_total=credits_total,
            courses=course_results,
        )
