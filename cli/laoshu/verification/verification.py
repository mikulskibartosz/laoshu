from dataclasses import dataclass
from laoshu.checks.freshness import FreshnessCheck, FreshnessCheckResult
from laoshu.checks.error_classification import ErrorClassificationCheck
from laoshu.baml_client.types import FaithfulnessError, FaithfulnessErrorType
from laoshu.checks.faithfulness import FaithfulnessCheck, FaithfulnessCheckResult
from typing import List, Optional, AsyncGenerator, Union
from laoshu.config import load_config
import os
from laoshu.scraping.interface import ScrapingResult
from laoshu.scraping.scrapingant import ScrapingantScraper
from laoshu.citations.extraction import get_citations_with_sources, Citation
import logging
import asyncio
from enum import Enum

log = logging.getLogger(__name__)


class VerificationStatus(Enum):
    INCORRECT = "INCORRECT"
    CORRECT = "CORRECT"
    CHECK_PENDING = "CHECK_PENDING"
    CANNOT_RETRIEVE = "CANNOT_RETRIEVE"
    BOT_TRAFFIC_DETECTED = "BOT_TRAFFIC_DETECTED"


@dataclass
class ErrorVerificationResult:
    error_type: FaithfulnessErrorType
    reasoning: str


@dataclass
class SourceVerificationResult:
    source: str
    status: VerificationStatus
    reasoning: str
    error_description: Optional[str]
    faithfulness_errors: List[ErrorVerificationResult]
    publication_date_iso8601: Optional[str]
    publication_date_relative_to_now: Optional[str]


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
        if all(s.status != VerificationStatus.CHECK_PENDING for s in result.sources):
            results.append(result)
    return results


def map_error_to_result(
    result: ScrapingResult, citation: Citation
) -> VerificationResult:
    if result.is_success:
        raise ValueError("Result is success, but error mapping was called.")

    if result.status_code == 423:
        return VerificationResult(
            claim=citation.text,
            sources=[
                SourceVerificationResult(
                    source=result.url,
                    status=VerificationStatus.BOT_TRAFFIC_DETECTED,
                    reasoning="",
                    error_description=f"Bot traffic detected. Cannot access the page.",
                    faithfulness_errors=[],
                    publication_date_iso8601=None,
                    publication_date_relative_to_now=None,
                )
            ],
        )
    else:
        return VerificationResult(
            claim=citation.text,
            sources=[
                SourceVerificationResult(
                    source=result.url,
                    status=VerificationStatus.CANNOT_RETRIEVE,
                    reasoning="",
                    error_description=f"{result.status_code}: {result.error_description}",
                    faithfulness_errors=[],
                    publication_date_iso8601=None,
                    publication_date_relative_to_now=None,
                )
            ],
        )


def map_check_result_to_result(
    result: FaithfulnessCheckResult,
    source_url: str,
    citation: Citation,
    errors: List[FaithfulnessError],
    freshness_result: FreshnessCheckResult,
) -> VerificationResult:
    return VerificationResult(
        claim=citation.text,
        sources=[
            SourceVerificationResult(
                source=source_url,
                status=(
                    VerificationStatus.CORRECT
                    if not result.is_hallucinated
                    else VerificationStatus.INCORRECT
                ),
                reasoning=result.reason,
                error_description=None,
                faithfulness_errors=[
                    ErrorVerificationResult(
                        error_type=error.error_type, reasoning=error.reasoning
                    )
                    for error in errors
                ],
                publication_date_iso8601=freshness_result.publication_date_iso8601,
                publication_date_relative_to_now=freshness_result.relative_to_now,
            )
        ],
    )


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
    error_classification_check = ErrorClassificationCheck()
    freshness_check = FreshnessCheck()

    semaphore = asyncio.Semaphore(max_concurrent_scrapes)
    queue: "asyncio.Queue[Union[VerificationResult, Exception]]" = asyncio.Queue()
    tasks = []

    async def verify_one(citation: Citation, source_url: str) -> None:
        try:
            async with semaphore:
                page = (await scraper.fetch_many_markdowns([source_url]))[0]

            if not page.is_success:
                await queue.put(map_error_to_result(page, citation))
                return

            markdown = page.markdown or ""
            result = await check.check(text=citation.text, context=[markdown])
            errors: List[FaithfulnessError] = []
            if result.is_hallucinated:
                errors = await error_classification_check.classify_errors(
                    citation.text, markdown
                )
            freshness_result = await freshness_check.check_freshness(markdown)
            await queue.put(
                map_check_result_to_result(
                    result, source_url, citation, errors, freshness_result
                )
            )
        except Exception as e:
            log.error(f"Error verifying  {source_url}: {e}")
            log.exception(e)
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
                        status=VerificationStatus.CHECK_PENDING,
                        reasoning="",
                        error_description=None,
                        faithfulness_errors=[],
                        publication_date_iso8601=None,
                        publication_date_relative_to_now=None,
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
