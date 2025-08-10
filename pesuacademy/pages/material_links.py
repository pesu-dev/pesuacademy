"""This module handles the scraping of links for all materials from the PESU Academy website."""

import re

import httpx
from bs4 import BeautifulSoup

from pesuacademy import constants
from pesuacademy.models import MaterialLink, Topic
from pesuacademy.util import _build_params


class _MaterialLinksHandler:
    @staticmethod
    async def _get_page(session: httpx.AsyncClient, topic: Topic, material_type_id: str) -> list[MaterialLink]:
        """Fetches the material links for a given topic and material type ID.

        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.
            topic (Topic): The Topic object containing course and topic IDs.
            material_type_id (str): The ID of the material type to fetch links for.

        Returns:
            List[MaterialLink]: A list of MaterialLink objects containing the scraped data.

        Raises:
            httpx.HTTPStatusError: If the request to the material links page fails.
        """
        params = _build_params(
            constants._PageURLParams.MaterialLinks,
            selectedData=topic.course_id,
            id=material_type_id,
            unitid=topic.id,
            url="studentProfilePESUAdmin",
        )
        response = await session.get(constants.PAGES_BASE_URL, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        links = []

        # Find all link containers
        link_containers = soup.find_all("div", class_="link-preview")

        for container in link_containers:
            onclick_attr = container.get("onclick", "")

            # Non-PDF links (directly downloadable documents) which uses downloadcoursedoc
            if "downloadcoursedoc" in onclick_attr:
                match = re.search(r"downloadcoursedoc\('([^']*)'\)", onclick_attr)
                if match:
                    doc_id = match.group(1)
                    title = container.text.strip()
                    # Construct the full download URL
                    full_url = f"{constants.BASE_URL}/Academy/s/referenceMeterials/downloadcoursedoc/{doc_id}"
                    links.append(MaterialLink(title=title, url=full_url, is_pdf=False))

            # PDF links which are in the form of an Iframe
            else:
                link_tag = container.find("a")
                if link_tag:
                    onclick_attr = link_tag.get("onclick", "")
                    match = re.search(r"loadIframe\('([^']*)'", onclick_attr)
                    if match:
                        partial_url = match.group(1).split("#")[0]  # Get URL part before the '#'
                        title = link_tag.text.strip()
                        # Construct the full download URL
                        full_url = f"{constants.BASE_URL}{partial_url}"
                        links.append(MaterialLink(title=title, url=full_url, is_pdf=True))

        return links
