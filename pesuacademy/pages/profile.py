import datetime
import httpx
from bs4 import BeautifulSoup, Tag
import re
from ..models.profile import Profile, PersonalDetails, ParentDetails, ParentInformation, AddressDetails

class ProfilePageHandler:
    """ Handles fetching and parsing the user profile page in the PESU Academy system.
    This class provides methods to retrieve and parse the profile page to extract personal, parent, and address details.
    """
    @staticmethod
    def _find_value_for_label(soup: BeautifulSoup, text: str) -> str:
        """ Finds the value associated with a label in the profile page HTML.
        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the profile page HTML.
            text (str): The label text to search for.
        Returns:
            str: The value associated with the label, or "N/A" if not found.
        """
        label_tag = soup.find("label", string=re.compile(r'\s*' + text + r'\s*'))
        if not label_tag:
            return "N/A"
        
        # The value can be in the next sibling label or inside an input tag within the parent div
        next_sibling = label_tag.find_next_sibling()
        if next_sibling and next_sibling.name == 'label':
            return next_sibling.text.strip()
        
        input_tag = label_tag.find_next("input")
        if input_tag and input_tag.has_attr('value'):
            return input_tag['value'].strip()
            
        return "N/A"

    @staticmethod
    def _parse_profile_soup(soup: BeautifulSoup) -> Profile:
        """ Parses the profile page HTML and extracts personal, parent, and address details.
        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the profile page HTML.    
        Returns:
            Profile: A Profile object containing personal, parent, and address details.
        Raises:
            ValueError: If the profile page structure is not as expected.
        """
        
        # Extract personal details
        personal = PersonalDetails(
            name=ProfilePageHandler._find_value_for_label(soup, "Name"),
            pesu_id=ProfilePageHandler._find_value_for_label(soup, "PESU Id"),
            srn=ProfilePageHandler._find_value_for_label(soup, "SRN"),
            program=ProfilePageHandler._find_value_for_label(soup, "Program"),
            branch=ProfilePageHandler._find_value_for_label(soup, "Branch"),
            semester=ProfilePageHandler._find_value_for_label(soup, "Semester"),
            section=ProfilePageHandler._find_value_for_label(soup, "Section"),
            email_id=ProfilePageHandler._find_value_for_label(soup, "Email ID"),
            contact_no=ProfilePageHandler._find_value_for_label(soup, "Contact No"),
        )
        
        # Found an issue with the parent details extraction, it was not correctly identifying the parent labels.
        # The mobile, email, and occupation fields of both parents were being fetched from the same label.
        # TO-DO - Fix the parent details extraction logic to correctly identify each parent's fields.
        parents = ParentInformation(
            father=ParentDetails(
                name=ProfilePageHandler._find_value_for_label(soup, "Father Name"),
                mobile=ProfilePageHandler._find_value_for_label(soup, "Mobile"),
                email=ProfilePageHandler._find_value_for_label(soup, "Email"),
                occupation=ProfilePageHandler._find_value_for_label(soup, "Occupation"),
            ),
            mother=ParentDetails(
                name=ProfilePageHandler._find_value_for_label(soup, "Mother Name"),
                mobile=ProfilePageHandler._find_value_for_label(soup, "Mobile"),
                email=ProfilePageHandler._find_value_for_label(soup, "Email"),
                occupation=ProfilePageHandler._find_value_for_label(soup, "Occupation"),
            )
        )

        address = AddressDetails(
            present=ProfilePageHandler._find_value_for_label(soup, "Present Address"),
            permanent=ProfilePageHandler._find_value_for_label(soup, "Permanent Address"),
        )

        return Profile(personal=personal, parents=parents, address=address)

    @staticmethod
    async def get_page(session: httpx.AsyncClient) -> Profile:
        """ Fetches the profile page and parses the user's profile information.
        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.
        Returns:
            Profile: A Profile object containing personal, parent, and address details.
        Raises:
            httpx.HTTPStatusError: If the request to the profile page fails.
        """
        url = "/s/studentProfilePESUAdmin"
        params = {
            "menuId": "670", "controllerMode": "6414", "actionType": "5",
            "_": str(int(datetime.datetime.now().timestamp() * 1000)),
        }
        response = await session.get(url, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        return ProfilePageHandler._parse_profile_soup(soup)