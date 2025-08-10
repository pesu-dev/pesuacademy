"""This module provides functionality to scrape ESA results from the PESU Academy website."""

import httpx
from bs4 import BeautifulSoup

from pesuacademy import constants
from pesuacademy.models import Assessment, CourseResult, Credits, SemesterResult
from pesuacademy.util import _build_params


class _ResultsPageHandler:
    @staticmethod
    def _parse_assessments(container: BeautifulSoup) -> list[Assessment]:
        """Parses the assessments for a single course."""
        assessments = []
        assessment_bar = container.find("div", class_="dashboard-info-bar")
        if not assessment_bar:
            return []

        for assessment_div in assessment_bar.find_all("div", recursive=False):
            name_tag = assessment_div.find("h6")
            if not name_tag:
                continue
            name = name_tag.text.strip()

            marks, total = None, None
            marks_span = assessment_div.find("span", class_="dark-text")
            if marks_span:
                marks = marks_span.text.strip()
                if marks_span.next_sibling and isinstance(marks_span.next_sibling, str):
                    total_raw = marks_span.next_sibling.strip()
                    if total_raw.startswith("/"):
                        total = total_raw.replace("/", "").strip()
            elif grade_span := assessment_div.find("span", class_="f-size-2x-big"):
                marks = grade_span.text.strip()

            if name:
                assessments.append(Assessment(name=name, marks=marks, total=total))
        return assessments

    @staticmethod
    def _parse_single_course(container: BeautifulSoup) -> CourseResult | None:
        """Parses a single course container from the results page."""
        header = container.find("div", class_="header-info")
        if not header:
            return None

        header_text = header.find("h6").text.strip()
        code, title = (part.strip() for part in header_text.split("-", 1))

        credits_text = header.find("h6", class_="text-right").text.strip().split(":")[-1]
        s_credit_parts = credits_text.split("/")
        s_credits_earned = s_credit_parts[0].strip()
        s_credits_total = s_credit_parts[1].strip() if len(s_credit_parts) > 1 else s_credits_earned

        assessments = _ResultsPageHandler._parse_assessments(container)

        return CourseResult(
            code=code,
            title=title,
            credits=Credits(earned=s_credits_earned, total=s_credits_total),
            assessments=assessments,
        )

    @staticmethod
    def _parse_course_results(soup: BeautifulSoup) -> list[CourseResult]:
        """Parses all course results from the page."""
        wrapper = soup.find("div", class_="multiple-info-wrapper")
        if not wrapper:
            return []

        course_containers = wrapper.find_all("div", class_="clearfix")
        course_results = []
        for container in course_containers:
            if course_result := _ResultsPageHandler._parse_single_course(container):
                course_results.append(course_result)
        return course_results

    @staticmethod
    def _parse_summary(soup: BeautifulSoup) -> tuple[str, str, str]:
        """Parses the summary section (SGPA, credits) of the results page."""
        summary_divs = soup.select("div.dashboard-info-bar > div")
        summary_credits_raw = summary_divs[0].contents[-1].strip()

        credit_parts = summary_credits_raw.split("/")
        credits_earned = credit_parts[0].strip()
        credits_total = credit_parts[1].strip() if len(credit_parts) > 1 else credits_earned

        sgpa_raw = summary_divs[1].contents[-1].strip()
        return sgpa_raw, credits_earned, credits_total

    @staticmethod
    async def _get_page(session: httpx.AsyncClient, semester_id: str) -> SemesterResult:
        """Fetches the ESA results for a given semester ID.

        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.
            semester_id (str): The ID of the semester to fetch results for.

        Returns:
            SemesterResult: An object containing
            the semester results including SGPA, credits earned, and course results.

        Raises:
            httpx.HTTPStatusError: If the request to the results page fails.
        """
        params = _build_params(constants._PageURLParams.Results, semid=semester_id)
        response = await session.get(constants.PAGES_BASE_URL, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        sgpa, credits_earned, credits_total = _ResultsPageHandler._parse_summary(soup)
        course_results = _ResultsPageHandler._parse_course_results(soup)

        return SemesterResult(
            sgpa=sgpa,
            credits=Credits(earned=credits_earned, total=credits_total),
            courses=course_results,
        )
