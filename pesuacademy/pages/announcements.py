"""This module handles the scraping of announcements from the PESU Academy website."""

import copy
import datetime
import re

import httpx
from bs4 import BeautifulSoup

from .. import constants
from ..models.announcement import Announcement
from ..util import build_params


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
        url = "/s/studentProfilePESUAdmin"
        params = build_params(constants.PageURLParams.Announcements, url="studentProfilePESUAdmin")
        response = await session.get(url, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        announcements = []
        base_url = "https://www.pesuacademy.com"

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

                # Content Links
                links = []
                link_tags = content_div.find_all("a", href=re.compile(r"handleDownloadAnoncemntdoc"))
                for link_tag in link_tags:
                    href_attr = link_tag.get("href", "")
                    match = re.search(r"handleDownloadAnoncemntdoc\('(\d+)'\)", href_attr)
                    if match:
                        doc_id = match.group(1)
                        # Construct the full download URL
                        full_url = f"{base_url}/Academy/s/studentProfilePESUAdmin/downloadAnoncemntdoc/{doc_id}"
                        links.append(full_url)

                # Content without "Read more" links and download links
                # To get clean content, we make a copy and remove the elements we don't want
                content_clone = copy.copy(content_div)
                if read_more := content_clone.find("a", class_="readmorelink"):
                    read_more.decompose()
                # temp fix to remove download links which have
                for link_div in content_clone.find_all("div"):
                    if link_div.find("a", href=re.compile(r"handleDownloadAnoncemntdoc")):
                        link_div.decompose()
                content = content_clone.text.strip()

                announcements.append(Announcement(title=title, date=date, content=content, links=links or None))

            except (AttributeError, ValueError) as e:
                # Skip any panels that have parsing errors
                print(f"Skipping a panel due to parsing error: {e}")
                continue

        return announcements
