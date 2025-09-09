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
    def _parse_profile_soup(soup: BeautifulSoup, high_privacy: bool = False) -> Profile:
        """Parses the profile page HTML into a structured Profile object.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML of the profile page.
            high_privacy (bool): If True, sensitive information will be masked or omitted.

        Returns:
            Profile: A Profile object containing personal, parent, and address details.

        Raises:
            ValueError: If the profile page structure is not as expected.
        """

        # Define a helper function to handle privacy-sensitive values
        # This function returns None for sensitive information if high privacy mode is enabled
        def privacy_value(label: str, container: Tag, high_privacy: bool) -> str | None:
            """Returns the value for a label, or None if high privacy mode is enabled.

            Args:
                label (str): The label to search for.
                container (Tag): The BeautifulSoup Tag object containing the profile information.
                high_privacy (bool): If True, sensitive information will be masked or omitted.

            Returns:
                str | None: The value associated with the label, or None if high privacy mode is enabled.
            """
            return None if high_privacy else _ProfilePageHandler._find_value_for_label(container, label)

        # Personal Details
        personal_container = soup.find("div", class_="media-body")

        if high_privacy:
            img_tag = soup.find("img", class_="media-object")
            profile_image_base64 = img_tag["src"] if img_tag else None
            profile_image_base64 = profile_image_base64.split("data:image/jpeg;base64,")[1]
        else:
            profile_image_base64 = None

        personal = PersonalDetails(
            name=_ProfilePageHandler._find_value_for_label(personal_container, "Name"),
            pesu_id=_ProfilePageHandler._find_value_for_label(personal_container, "PESU Id"),
            srn=_ProfilePageHandler._find_value_for_label(personal_container, "SRN"),
            program=_ProfilePageHandler._find_value_for_label(personal_container, "Program"),
            branch=_ProfilePageHandler._find_value_for_label(personal_container, "Branch"),
            semester=_ProfilePageHandler._find_value_for_label(personal_container, "Semester"),
            section=_ProfilePageHandler._find_value_for_label(personal_container, "Section"),
            email_id=privacy_value("Email ID", personal_container, high_privacy),
            contact_no=privacy_value("Contact No", personal_container, high_privacy),
            aadhar_no=privacy_value("Aadhar No", personal_container, high_privacy),
            name_as_in_aadhar=privacy_value("Name as in aadhar", personal_container, high_privacy),
            image=profile_image_base64,
        )

        # Other Information and Qualifying Examination
        other_info_container = soup.find("h4", string="Other Information").find_next("div", class_="info-contents")
        qualifying_exam_container = soup.find("h4", string="Qualifying examination").find_next(
            "div", class_="info-contents"
        )

        other_info = OtherInformation(
            sslc_marks=privacy_value("SSLC Marks", other_info_container, high_privacy),
            puc_marks=privacy_value("PUC Marks", other_info_container, high_privacy),
            date_of_birth=privacy_value("Date of birth", other_info_container, high_privacy),
            blood_group=privacy_value("Blood Group", other_info_container, high_privacy),
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
                name=privacy_value("Father Name", father_container, high_privacy),
                mobile=privacy_value("Mobile", father_container, high_privacy),
                email=privacy_value("Email", father_container, high_privacy),
                occupation=privacy_value("Occupation", father_container, high_privacy),
                qualification=privacy_value("Qualification", father_container, high_privacy),
                designation=privacy_value("Designation", father_container, high_privacy),
                employer=privacy_value("Employer", father_container, high_privacy),
            ),
            mother=ParentDetails(
                name=privacy_value("Mother Name", mother_container, high_privacy),
                mobile=privacy_value("Mobile", mother_container, high_privacy),
                email=privacy_value("Email", mother_container, high_privacy),
                occupation=privacy_value("Occupation", mother_container, high_privacy),
                qualification=privacy_value("Qualification", mother_container, high_privacy),
                designation=privacy_value("Designation", mother_container, high_privacy),
                employer=privacy_value("Employer", mother_container, high_privacy),
            ),
        )

        # Address Details
        address_container = soup.find("h4", string="Address").find_next("div")
        address = AddressDetails(
            present=privacy_value("Present Address", address_container, high_privacy),
            permanent=privacy_value("Permanent Address", address_container, high_privacy),
        )

        return Profile(
            personal=personal,
            other_info=other_info,
            qualifying_exam=qualifying_exam,
            parents=parents,
            address=address,
        )

    @staticmethod
    async def _get(session: httpx.AsyncClient) -> Profile:
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
