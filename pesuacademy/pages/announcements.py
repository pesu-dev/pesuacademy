"""This module handles the scraping of announcements from the PESU Academy website."""

import copy
import datetime
import re

import httpx
from bs4 import BeautifulSoup

from pesuacademy import constants
from pesuacademy.models import Announcement
from pesuacademy.util import _build_params


class _AnnouncementPageHandler:
    @staticmethod
    async def _get_page(session: httpx.AsyncClient) -> list[Announcement]:
        """Fetches the main announcements page and scrapes all announcements.

        Args:
            session (httpx.AsyncClient): The HTTP client session to use for requests.

        Returns:
            List[Announcement]: A list of Announcement objects containing the scraped data.

        Raises:
            httpx.HTTPStatusError: If the request to the announcements page fails.
        """
        params = _build_params(constants._PageURLParams.Announcements, url="studentProfilePESUAdmin")
        response = await session.get(constants.PAGES_BASE_URL, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        announcements = []

        # Find all announcement wrappers
        announcement_wrappers = soup.find_all("div", class_="elem-info-wrapper")

        for wrapper in announcement_wrappers:
            try:
                # Title
                title_tag = wrapper.find("h4", class_="text-info")
                title = title_tag.text.strip() if title_tag else "No Title"

                # Date
                date_tag = wrapper.find("span", class_="text-muted")
                date_str = date_tag.text.strip() if date_tag else ""
                date = datetime.datetime.strptime(date_str, "%d-%B-%Y").date()

                content_div = wrapper.find("div", class_="col-md-12")
                if not content_div:
                    continue

                # Content attachments
                attachments = []
                link_tags = content_div.find_all("a", href=re.compile(r"handleDownloadAnoncemntdoc"))
                for link_tag in link_tags:
                    href_attr = link_tag.get("href", "")
                    match = re.search(r"handleDownloadAnoncemntdoc\('(\d+)'\)", href_attr)
                    if match:
                        doc_id = match.group(1)
                        # Construct the full download URL
                        partial_url = f"{constants.BASE_URL}/Academy/s/studentProfilePESUAdmin/downloadAnoncemntdoc/"
                        full_url = f"{partial_url}{doc_id}"
                        attachments.append(full_url)

                # Content without "Read more" attachments and download attachments
                # To get clean content, we make a copy and remove the elements we don't want
                content_clone = copy.copy(content_div)
                if read_more := content_clone.find("a", class_="readmorelink"):
                    read_more.decompose()
                for link_div in content_clone.find_all("div"):
                    if link_div.find("a", href=re.compile(r"handleDownloadAnoncemntdoc")):
                        link_div.decompose()
                content = content_clone.text.strip()

                announcements.append(
                    Announcement(
                        title=title,
                        date=date,
                        content=content,
                        attachments=attachments or None,
                    )
                )

            except (AttributeError, ValueError) as e:
                # Skip any panels that have parsing errors
                print(f"Skipping a panel due to parsing error: {e}")
                continue

        return announcements
