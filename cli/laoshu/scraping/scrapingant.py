from typing import List
import httpx
from asyncio import gather
from .interface import Scraper, ScraperError


class ScrapingantScraper(Scraper):
    def __init__(
        self,
        api_key: str,
        timeout_seconds: int = 60,
        use_headless_browser: bool = False,
    ):
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds
        self.use_headless_browser = use_headless_browser

    async def fetch_markdown(self, url: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.scrapingant.com/v2/markdown",
                    params={
                        "url": url,
                        "x-api-key": self.api_key,
                        "browser": self.use_headless_browser,
                    },
                    timeout=self.timeout_seconds,
                )
                response.raise_for_status()
                return response.text
        except httpx.RequestError as e:
            raise ScraperError(
                http_status_code=None,
                is_internal_laoshu_error=False,
                error_description=f"Failed to send the fetch markdown request to ScrapingAnt: {str(e)}",
            )
        except httpx.HTTPStatusError as e:
            raise ScraperError(
                http_status_code=e.response.status_code,
                is_internal_laoshu_error=False,
                error_description=f"Failed to fetch markdown from ScrapingAnt: {str(e)}",
            )

    async def fetch_many_markdowns(self, urls: List[str]) -> List[str]:
        return await gather(*[self.fetch_markdown(url) for url in urls])
