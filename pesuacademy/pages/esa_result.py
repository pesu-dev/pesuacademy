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

        credits_elem = header.find("h6", class_="text-right")
        if credits_elem:
            credits_text = credits_elem.text.strip().split(":")[-1]
            s_credit_parts = credits_text.split("/")
            s_credits_earned = s_credit_parts[0].strip()
            s_credits_total = s_credit_parts[1].strip() if len(s_credit_parts) > 1 else s_credits_earned
        else:
            s_credits_earned = "0"
            s_credits_total = "0"

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
    def _parse_provisional_summary(soup: BeautifulSoup, semester: int) -> tuple[str, str, str, dict[str, str]]:
        """Parses the summary section (SGPA, credits) and grades of the provisional results page."""
        sgpa_raw, credits_earned, credits_total = "N/A", "N/A", "N/A"
        grades = {}

        containers = soup.find_all("div", id="isaEsaResult_3")
        for container in containers:
            sem_label = container.find("label", class_="control-label")
            if sem_label and f"{semester} Sem" in sem_label.text:
                summary_divs = container.select("div.dashboard-info-bar > div")
                if len(summary_divs) >= 2:
                    summary_credits_raw = summary_divs[0].contents[-1].strip()
                    credit_parts = summary_credits_raw.split("/")
                    credits_earned = credit_parts[0].strip()
                    credits_total = credit_parts[1].strip() if len(credit_parts) > 1 else credits_earned

                    sgpa_raw = summary_divs[1].contents[-1].strip()

                table = container.find("table")
                if table:
                    tbody = table.find("tbody")
                    if tbody:
                        for tr in tbody.find_all("tr"):
                            tds = tr.find_all("td")
                            if len(tds) >= 4:
                                code = tds[1].text.strip()
                                grade_td = tds[3]
                                grade = grade_td.contents[0].strip() if grade_td.contents else grade_td.text.strip()
                                grades[code] = grade
                break

        return sgpa_raw, credits_earned, credits_total, grades

    @staticmethod
    async def _get(session: httpx.AsyncClient, semester_id: str, semester: int) -> SemesterResult:  # noqa: C901
        """Fetches the ESA results for a given semester ID.

        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.
            semester_id (str): The ID of the semester to fetch results for.
            semester (int): The semester number for which to fetch results.

        Returns:
            SemesterResult: An object containing
            the semester results including SGPA, credits earned, and course results.

        Raises:
            httpx.HTTPStatusError: If the request to the results page fails.
        """
        # Fetch detailed course results (assessments breakdown)
        params_9 = _build_params(constants._PageURLParams.Results, semid=semester_id)
        response_9 = await session.get(constants.PAGES_BASE_URL, params=params_9)
        response_9.raise_for_status()

        soup_9 = BeautifulSoup(response_9.text, "lxml")
        course_results = _ResultsPageHandler._parse_course_results(soup_9)

        # First try extracting SGPA from the final results page (actionType=9)
        sgpa, credits_earned, credits_total = "N/A", "N/A", "N/A"
        bars = soup_9.select("div.dashboard-info-bar")
        if bars and "SGPA" in bars[0].text:
            summary_divs = bars[0].find_all("div", recursive=False)
            if len(summary_divs) >= 2:
                summary_credits_raw = summary_divs[0].contents[-1].strip()
                credit_parts = summary_credits_raw.split("/")
                credits_earned = credit_parts[0].strip()
                credits_total = credit_parts[1].strip() if len(credit_parts) > 1 else credits_earned
                sgpa = summary_divs[1].contents[-1].strip()

        # Check if we need to fetch provisional results
        needs_provisional = False
        is_ongoing = False

        # Check if ISA 1 or ISA 2 is NA (meaning semester is ongoing and ESA won't be available)
        for course in course_results:
            for assessment in course.assessments:
                if assessment.name in ("ISA 1", "ISA 2") and assessment.marks in ("NA", None):
                    is_ongoing = True
                    break
            if is_ongoing:
                break

        if not is_ongoing:
            if sgpa == "N/A":
                needs_provisional = True
            else:
                for course in course_results:
                    for assessment in course.assessments:
                        if assessment.name == "ESA" and assessment.marks in ("NA", None):
                            needs_provisional = True
                            break
                    if needs_provisional:
                        break

        if needs_provisional:
            # Fetch provisional results (SGPA and credits and grades)
            params_53 = _build_params(constants._PageURLParams.ProvisionalResults, semid=semester_id)
            response_53 = await session.get(constants.PAGES_BASE_URL, params=params_53)
            response_53.raise_for_status()

            soup_53 = BeautifulSoup(response_53.text, "lxml")
            prov_parsed = _ResultsPageHandler._parse_provisional_summary(soup_53, semester)
            prov_sgpa, prov_credits_earned, prov_credits_total, provisional_grades = prov_parsed

            # If SGPA is N/A in final results, fallback to provisional results
            if sgpa == "N/A":
                sgpa = prov_sgpa
                credits_earned = prov_credits_earned
                credits_total = prov_credits_total

            # Replace 'NA' or None ESA marks with provisional grades if available
            for course in course_results:
                for assessment in course.assessments:
                    if assessment.name == "ESA" and assessment.marks in ("NA", None):
                        if course.code in provisional_grades:
                            assessment.marks = provisional_grades[course.code]

        return SemesterResult(
            sgpa=sgpa,
            credits=Credits(earned=credits_earned, total=credits_total),
            courses=course_results,
        )

    @staticmethod
    async def _get_sgpa_and_credits(session: httpx.AsyncClient, semester_id: str, semester: int) -> tuple[str, Credits]:
        """Fetches only the SGPA and credits for a given semester ID."""
        params_9 = _build_params(constants._PageURLParams.Results, semid=semester_id)
        response_9 = await session.get(constants.PAGES_BASE_URL, params=params_9)
        response_9.raise_for_status()

        soup_9 = BeautifulSoup(response_9.text, "lxml")

        # Extract SGPA from the final results page (actionType=9)
        sgpa, credits_earned, credits_total = "N/A", "N/A", "N/A"
        bars = soup_9.select("div.dashboard-info-bar")
        if bars and "SGPA" in bars[0].text:
            summary_divs = bars[0].find_all("div", recursive=False)
            if len(summary_divs) >= 2:
                summary_credits_raw = summary_divs[0].contents[-1].strip()
                credit_parts = summary_credits_raw.split("/")
                credits_earned = credit_parts[0].strip()
                credits_total = credit_parts[1].strip() if len(credit_parts) > 1 else credits_earned
                sgpa = summary_divs[1].contents[-1].strip()

        # If SGPA is already found in Final Results, we are done
        if sgpa != "N/A":
            return sgpa, Credits(earned=credits_earned, total=credits_total)

        # SGPA is N/A. We must check if the semester is ongoing by looking at ISA marks.
        course_results = _ResultsPageHandler._parse_course_results(soup_9)
        is_ongoing = False

        for course in course_results:
            for assessment in course.assessments:
                if assessment.name in ("ISA 1", "ISA 2") and assessment.marks in ("NA", None):
                    is_ongoing = True
                    break
            if is_ongoing:
                break

        # If the semester is not ongoing, fetch provisional results for the SGPA
        if not is_ongoing:
            params_53 = _build_params(constants._PageURLParams.ProvisionalResults, semid=semester_id)
            response_53 = await session.get(constants.PAGES_BASE_URL, params=params_53)
            response_53.raise_for_status()

            soup_53 = BeautifulSoup(response_53.text, "lxml")
            prov_parsed = _ResultsPageHandler._parse_provisional_summary(soup_53, semester)
            prov_sgpa, prov_credits_earned, prov_credits_total, _ = prov_parsed

            if prov_sgpa != "N/A":
                sgpa = prov_sgpa
                credits_earned = prov_credits_earned
                credits_total = prov_credits_total

        return sgpa, Credits(earned=credits_earned, total=credits_total)
