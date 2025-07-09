from dataclasses import dataclass
from laoshu.checks.faithfulness import FaithfulnessCheck
from typing import List, Optional, AsyncGenerator, Union
from laoshu.config import load_config
import os
from laoshu.scraping.scrapingant import ScrapingantScraper
from laoshu.citations.extraction import get_citations_with_sources, Citation
import logging
import asyncio

log = logging.getLogger(__name__)


@dataclass
class SourceVerificationResult:
    source: str
    is_correct: Optional[bool]
    reasoning: str


@dataclass
class VerificationResult:
    claim: str
    sources: List[SourceVerificationResult]


async def verify_citations_in_file(file: str) -> List[VerificationResult]:
    if not os.path.exists(file):
        raise FileNotFoundError(f"File {file} not found")

    with open(file, "r") as f:
        text = f.read()

    results = []
    async for result in stream_verify_citations(text):
        # Only collect final results where all sources have is_correct set (i.e., not None)
        if all(s.is_correct is not None for s in result.sources):
            results.append(result)
    return results


async def stream_verify_citations(
    text: str, max_concurrent_scrapes: int = 1
) -> AsyncGenerator[VerificationResult, None]:
    """Async generator that streams verification results for each claim+source.

    Args:
        text: The input text to extract claims and sources from.
        max_concurrent_scrapes: Maximum number of concurrent scraping requests.

    Yields:
        VerificationResult objects with status CHECK_PENDING, then final status.

    Raises:
        Exception: If any background task fails, the stream is interrupted.
    """
    config = load_config()
    if not config.openai_api_key:
        raise ValueError("OPENAI_API_KEY not set")
    if not config.scrapingant_api_key:
        raise ValueError("SCRAPINGANT_API_KEY not set")

    scraper = ScrapingantScraper(api_key=config.scrapingant_api_key)
    check = FaithfulnessCheck.instance(api_key=config.openai_api_key)
    citations: List[Citation] = get_citations_with_sources(text)

    semaphore = asyncio.Semaphore(max_concurrent_scrapes)
    queue: "asyncio.Queue[Union[VerificationResult, Exception]]" = asyncio.Queue()
    tasks = []

    async def verify_one(citation: Citation, source_url: str) -> None:
        try:
            async with semaphore:
                page = (await scraper.fetch_many_markdowns([source_url]))[0]
            result = await check.check(text=citation.text, context=[page.markdown])
            await queue.put(
                VerificationResult(
                    claim=citation.text,
                    sources=[
                        SourceVerificationResult(
                            source=source_url,
                            is_correct=not result.is_hallucinated,
                            reasoning=result.reason,
                        )
                    ],
                )
            )
        except Exception as e:
            log.error(f"Error verifying {citation.text} / {source_url}: {e}")
            await queue.put(e)

    # 1. Immediately yield all pending statuses and start background tasks
    for citation in citations:
        for source_url in citation.sources:
            log.info(
                f"Yielding pending for claim: {citation.text}, source: {source_url}"
            )
            yield VerificationResult(
                claim=citation.text,
                sources=[
                    SourceVerificationResult(
                        source=source_url,
                        is_correct=None,
                        reasoning="",
                    )
                ],
            )
            tasks.append(asyncio.create_task(verify_one(citation, source_url)))

    # 2. Wait for all results, yield as they finish
    num_results = len(tasks)
    finished = 0
    errors = []
    while finished < num_results:
        result = await queue.get()
        if isinstance(result, Exception):
            errors.append(result)
            break
        log.info(
            f"Yielding final for claim: {result.claim}, source: {result.sources[0].source}"
        )
        yield result
        finished += 1

    # Cancel all tasks if error
    if errors:
        for t in tasks:
            t.cancel()
        raise errors[0]
    # Wait for all tasks to finish (handle cancellation)
    await asyncio.gather(*tasks, return_exceptions=True)
