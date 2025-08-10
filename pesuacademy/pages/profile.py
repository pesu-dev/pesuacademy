"""This module handles fetching and parsing the student Profile page from the PESU Academy website."""

import re

import httpx
from bs4 import BeautifulSoup, Tag

from pesuacademy import constants
from pesuacademy.models import (
    AddressDetails,
    OtherInformation,
    ParentDetails,
    ParentInformation,
    PersonalDetails,
    Profile,
    QualifyingExamination,
)
from pesuacademy.util import _build_params


class _ProfilePageHandler:
    """Handles fetching and parsing the user profile page in the PESU Academy system.

    This class provides methods to retrieve and parse the profile page to extract personal, parent, and address details.
    """

    @staticmethod
    def _find_value_for_label(container: Tag, text: str) -> str:
        """Finds a value associated with a label within a specific container.

        Args:
            container (Tag): The BeautifulSoup Tag object containing the profile information.
            text (str): The label text to search for.

        Returns:
            str: The value associated with the label, or "N/A" if not found.
        """
        label_tag = container.find("label", string=re.compile(r"\s*" + text + r"\s*"))
        if not label_tag:
            return "N/A"
        # Find the next sibling label or input to get the value
        value_tag = label_tag.find_next_sibling("label")
        if value_tag:
            return value_tag.text.strip()
        # If the next sibling is not a label, check for an input field
        input_tag = label_tag.find_next("input")
        if input_tag and input_tag.has_attr("value"):
            return input_tag["value"].strip()

        return "N/A"

    @staticmethod
    def _parse_profile_soup(soup: BeautifulSoup) -> Profile:
        """Parses the profile page HTML into a structured Profile object.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML of the profile page.

        Returns:
            Profile: A Profile object containing personal, parent, and address details.

        Raises:
            ValueError: If the profile page structure is not as expected.
        """
        # Personal Details
        personal_container = soup.find("div", class_="media-body")
        img_tag = soup.find("img", class_="media-object")
        profile_image_base64 = img_tag["src"] if img_tag else None
        profile_image_base64 = profile_image_base64.split("data:image/jpeg;base64,")[1]

        personal = PersonalDetails(
            name=_ProfilePageHandler._find_value_for_label(personal_container, "Name"),
            pesu_id=_ProfilePageHandler._find_value_for_label(personal_container, "PESU Id"),
            srn=_ProfilePageHandler._find_value_for_label(personal_container, "SRN"),
            program=_ProfilePageHandler._find_value_for_label(personal_container, "Program"),
            branch=_ProfilePageHandler._find_value_for_label(personal_container, "Branch"),
            semester=_ProfilePageHandler._find_value_for_label(personal_container, "Semester"),
            section=_ProfilePageHandler._find_value_for_label(personal_container, "Section"),
            email_id=_ProfilePageHandler._find_value_for_label(personal_container, "Email ID"),
            contact_no=_ProfilePageHandler._find_value_for_label(personal_container, "Contact No"),
            aadhar_no=_ProfilePageHandler._find_value_for_label(personal_container, "Aadhar No"),
            name_as_in_aadhar=_ProfilePageHandler._find_value_for_label(personal_container, "Name as in aadhar"),
            image=profile_image_base64,
        )

        # Other Information and Qualifying Examination
        other_info_container = soup.find("h4", string="Other Information").find_next("div", class_="info-contents")
        qualifying_exam_container = soup.find("h4", string="Qualifying examination").find_next(
            "div", class_="info-contents"
        )

        other_info = OtherInformation(
            sslc_marks=_ProfilePageHandler._find_value_for_label(other_info_container, "SSLC Marks"),
            puc_marks=_ProfilePageHandler._find_value_for_label(other_info_container, "PUC Marks"),
            date_of_birth=_ProfilePageHandler._find_value_for_label(other_info_container, "Date of birth"),
            blood_group=_ProfilePageHandler._find_value_for_label(other_info_container, "Blood Group"),
        )
        qualifying_exam = QualifyingExamination(
            exam=_ProfilePageHandler._find_value_for_label(qualifying_exam_container, "Exam"),
            rank=_ProfilePageHandler._find_value_for_label(qualifying_exam_container, "Rank"),
            score=_ProfilePageHandler._find_value_for_label(qualifying_exam_container, "Score"),
        )

        # Parent Details
        # Correctly handles the parent details section by just spltting the containers
        # Assumes Father is always first and Mother is always second (just in this context, lol)
        parent_containers = soup.find("h4", string="Parent Details").find_next("div").find_all("div", class_="col-md-6")
        father_container = parent_containers[0]
        mother_container = parent_containers[1]

        parents = ParentInformation(
            father=ParentDetails(
                name=_ProfilePageHandler._find_value_for_label(father_container, "Father Name"),
                mobile=_ProfilePageHandler._find_value_for_label(father_container, "Mobile"),
                email=_ProfilePageHandler._find_value_for_label(father_container, "Email"),
                occupation=_ProfilePageHandler._find_value_for_label(father_container, "Occupation"),
                qualification=_ProfilePageHandler._find_value_for_label(father_container, "Qualification"),
                designation=_ProfilePageHandler._find_value_for_label(father_container, "Designation"),
                employer=_ProfilePageHandler._find_value_for_label(father_container, "Employer"),
            ),
            mother=ParentDetails(
                name=_ProfilePageHandler._find_value_for_label(mother_container, "Mother Name"),
                mobile=_ProfilePageHandler._find_value_for_label(mother_container, "Mobile"),
                email=_ProfilePageHandler._find_value_for_label(mother_container, "Email"),
                occupation=_ProfilePageHandler._find_value_for_label(mother_container, "Occupation"),
                qualification=_ProfilePageHandler._find_value_for_label(mother_container, "Qualification"),
                designation=_ProfilePageHandler._find_value_for_label(mother_container, "Designation"),
                employer=_ProfilePageHandler._find_value_for_label(mother_container, "Employer"),
            ),
        )

        # Address Details
        address_container = soup.find("h4", string="Address").find_next("div")
        address = AddressDetails(
            present=_ProfilePageHandler._find_value_for_label(address_container, "Present Address"),
            permanent=_ProfilePageHandler._find_value_for_label(address_container, "Permanent Address"),
        )

        return Profile(
            personal=personal,
            other_info=other_info,
            qualifying_exam=qualifying_exam,
            parents=parents,
            address=address,
        )

    @staticmethod
    async def _get_page(session: httpx.AsyncClient) -> Profile:
        """Fetches and parses the user's profile page.

        Args:
            session (httpx.AsyncClient): An authenticated HTTP client session.

        Returns:
            Profile: A Profile object containing the user's profile information.

        Raises:
            httpx.HTTPStatusError: If the request to fetch the profile page fails.
        """
        params = _build_params(
            constants._PageURLParams.Profile,
        )
        response = await session.get(constants.PAGES_BASE_URL, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        return _ProfilePageHandler._parse_profile_soup(soup)
