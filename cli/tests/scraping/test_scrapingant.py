import pytest
import asyncio
from laoshu.scraping.scrapingant import ScrapingantScraper
from laoshu.config import load_config


@pytest.mark.cicd
def test_scrapingant_fetch_markdown() -> None:
    config = load_config()
    if not config.scrapingant_api_key:
        pytest.skip("SCRAPINGANT_API_KEY not set")

    scraper = ScrapingantScraper(config.scrapingant_api_key)
    result = asyncio.run(scraper.fetch_markdown("https://mikulskibartosz.name"))

    assert result is not None
    assert isinstance(result.markdown, str)
    assert len(result.markdown) > 0
