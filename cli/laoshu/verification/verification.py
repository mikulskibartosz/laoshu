from dataclasses import dataclass
from laoshu.checks.faithfulness import FaithfulnessCheck
from typing import List
from laoshu.config import load_config
import os
from laoshu.scraping.scrapingant import ScrapingantScraper
from laoshu.citations.extraction import get_citations_with_sources, Citation
import logging

log = logging.getLogger(__name__)


@dataclass
class VerificationResult:
    claim: str
    sources: List[str]
    is_correct: bool
    reasoning: str


async def verify_citations_in_file(file: str) -> List[VerificationResult]:
    if not os.path.exists(file):
        raise FileNotFoundError(f"File {file} not found")

    with open(file, "r") as f:
        text = f.read()

    return await verify_citations(text)


async def verify_citations(text: str) -> List[VerificationResult]:
    config = load_config()
    if not config.openai_api_key:
        raise ValueError("OPENAI_API_KEY not set")

    if not config.scrapingant_api_key:
        raise ValueError("SCRAPINGANT_API_KEY not set")

    scraper = ScrapingantScraper(api_key=config.scrapingant_api_key)
    check = FaithfulnessCheck.instance(api_key=config.openai_api_key)

    citations: List[Citation] = get_citations_with_sources(text)

    # TODO do it async, but synchronize the number of requests to the server with the scraper (it also has async processing)
    retrieved_pages = [
        await scraper.fetch_many_markdowns(citation.sources) for citation in citations
    ]

    claims_with_sources = zip(citations, retrieved_pages)

    results = []
    for citation, pages in claims_with_sources:
        result = await check.check(text=citation.text, context=pages)
        results.append(
            VerificationResult(
                claim=citation.text,
                sources=citation.sources,
                is_correct=not result.is_hallucinated,
                reasoning=result.reason,
            )
        )
    log.info(f"Verified {len(results)} citations.")
    return results
