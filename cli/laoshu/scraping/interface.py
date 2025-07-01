from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ScraperError(Exception):
    """
    Exception raised when there is an error during the scraping process.

    Attributes:
        http_status_code (Optional[int]): The HTTP status code if the error occurred during an HTTP request,
            None otherwise.
        is_internal_laoshu_error (bool): Whether the error originated from internal Laoshu code
            rather than an external source.
        error_description (str): A human-readable description of what went wrong.
    """

    http_status_code: Optional[int]
    is_internal_laoshu_error: bool
    error_description: str


class Scraper(ABC):
    """
    Retrieves the content of the given url as markdown.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The content of the URL in markdown format.

    Raises:
        ScraperError: If there is an error fetching or processing the content.
    """

    @abstractmethod
    async def fetch_markdown(self, url: str) -> str:
        pass

    @abstractmethod
    async def fetch_many_markdowns(self, urls: List[str]) -> List[str]:
        pass
