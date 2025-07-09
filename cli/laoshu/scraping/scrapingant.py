from typing import List
import httpx
from asyncio import gather
import logging
from .interface import Scraper, ScraperError, ScrapingResult
from .cache import ScrapingCache, InMemoryScrapingCache

log = logging.getLogger(__name__)


class ScrapingantScraper(Scraper):
    def __init__(
        self,
        api_key: str,
        timeout_seconds: int = 60,
        concurrent_requests: bool = False,
        use_headless_browser: bool = False,
        cache: ScrapingCache = InMemoryScrapingCache(),
    ):
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds
        self.concurrent_requests = concurrent_requests
        self.use_headless_browser = use_headless_browser
        self.cache = cache

    async def fetch_markdown(self, url: str) -> ScrapingResult:
        log.info(f"Fetching markdown from {url}.")
        try:
            async with httpx.AsyncClient() as client:
                cached_markdown = self.cache.get(url)
                if cached_markdown is not None:
                    log.info(f"Returning cached markdown for {url}.")
                    return ScrapingResult(
                        is_success=True,
                        url=url,
                        markdown=cached_markdown,
                        status_code=None,
                        error_description=None,
                    )

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
                response_text = response.text
                response_text_words_count = len(response_text.split())
                log.info(
                    f"Fetched markdown from {url} with {response_text_words_count} words."
                )
                self.cache.set(url, response_text)
                return ScrapingResult(
                    is_success=True,
                    url=url,
                    markdown=response_text,
                    status_code=response.status_code,
                    error_description=None,
                )
        except httpx.RequestError as e:
            # cannot even send the request, so we crash here.
            raise ScraperError(
                http_status_code=None,
                is_internal_laoshu_error=False,
                error_description=f"Failed to send the fetch markdown request to ScrapingAnt: {str(e)}",
            )
        except httpx.HTTPStatusError as e:
            # got a response, but it's not 200. We can work with that.
            return ScrapingResult(
                is_success=False,
                url=url,
                markdown=None,
                status_code=e.response.status_code,
                error_description=str(e),
            )

    async def fetch_many_markdowns(self, urls: List[str]) -> List[ScrapingResult]:
        deduplicated_urls = list(set(urls))
        log.info(
            f"Fetching {len(deduplicated_urls)} deduplicated markdown(s) from original {len(urls)} urls."
        )

        results = []
        if self.concurrent_requests:
            results = await gather(
                *[self.fetch_markdown(url) for url in deduplicated_urls]
            )
        else:
            results = [await self.fetch_markdown(url) for url in deduplicated_urls]

        url_to_content = dict(zip(deduplicated_urls, results))
        ordered_results = [url_to_content[url] for url in urls]
        return ordered_results
