import asyncio
import random
import logging
from enum import Enum
from typing import List
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from laoshu.verification.verification import verify_citations


MOCK_RESPONSE = [
    {
        "claim": "The Great Wall of China is visible from space with the naked eye.",
        "sources": [
            {
                "source": "https://www.nasa.gov/feature/goddard/2018/the-great-wall-of-china",
                "status": "INCORRECT",
                "reasoning": "NASA has confirmed that the Great Wall of China is not visible from space with the naked eye. While it can be seen from low Earth orbit with the aid of cameras and lenses, it cannot be seen with unaided vision.",
            },
            {
                "source": "https://www.smithsonianmag.com/science-nature/why-great-wall-china-not-visible-space-180959570/",
                "status": "INCORRECT",
                "reasoning": "The Smithsonian article confirms that the Great Wall of China is not visible from space with the naked eye. This is a common misconception that has been debunked by astronauts and space agencies.",
            },
        ],
    },
    {
        "claim": "The Earth's atmosphere is composed primarily of nitrogen and oxygen.",
        "sources": [
            {
                "source": "https://www.noaa.gov/jetstream/atmosphere",
                "status": "CORRECT",
                "reasoning": "NOAA confirms that Earth's atmosphere is composed of approximately 78% nitrogen and 21% oxygen, making these the two primary components.",
            },
            {
                "source": "https://www.nasa.gov/audience/forstudents/k-4/stories/nasa-knows/what-is-atmosphere-k4.html",
                "status": "CORRECT",
                "reasoning": "NASA's educational content confirms that nitrogen and oxygen are the main gases in Earth's atmosphere, with nitrogen being the most abundant.",
            },
        ],
    },
    {
        "claim": "Humans use only 10% of their brain capacity.",
        "sources": [
            {
                "source": "https://www.scientificamerican.com/article/do-people-only-use-10-percent-of-their-brains/",
                "status": "INCORRECT",
                "reasoning": "Scientific American debunks the 10% brain myth, explaining that humans use virtually all of their brain, with different regions active at different times for various functions.",
            },
            {
                "source": "https://www.brainfacts.org/brain-anatomy-and-function/anatomy/2019/do-we-only-use-10-percent-of-our-brain-091219",
                "status": "CORRECT",
                "reasoning": "BrainFacts.org confirms that the 10% brain usage myth is false. Brain imaging shows that most of the brain is active throughout the day, even during sleep.",
            },
        ],
    },
]


async def stream_mock_response(log):
    log.info("Streaming mock response")
    response = []
    for result in MOCK_RESPONSE:
        result_copy = result.copy()
        result_copy["sources"] = []
        for source in result["sources"]:
            source_copy = source.copy()
            source_copy["status"] = Status.CHECK_PENDING
            result_copy["sources"].append(source_copy)
        response.append(result_copy)

    log.info(f"Preapared {len(response)} check pending responses")

    for obj in MOCK_RESPONSE:
        response.append(obj)

    log.info(f"Preapared {len(response)} final responses")

    for index, obj in enumerate(response):
        log.info(f"Sending response {index+1}/{len(response)}")
        pydantic_obj = CheckResponse(**obj)
        yield pydantic_obj.model_dump_json() + "\n"
        await asyncio.sleep(
            random.uniform(
                0.1 + (index / len(response)) * 2, 1.5 + (index / len(response)) * 3
            )
        )


class Status(Enum):
    CHECK_PENDING = "CHECK_PENDING"
    INCORRECT = "INCORRECT"
    CORRECT = "CORRECT"


class CheckRequest(BaseModel):
    text: str
    only_incorrect: bool = False


class SourceVerificationResult(BaseModel):
    source: str
    status: Status
    reasoning: str


class CheckResponse(BaseModel):
    claim: str
    sources: List[SourceVerificationResult]


app = FastAPI()
log = logging.getLogger(__name__)


@app.post("/check")
async def check(request: CheckRequest) -> StreamingResponse:
    log.info(f"Received request: {request}")
    results = await verify_citations(request.text)

    response = []
    for result in results:
        if request.only_incorrect and all(
            source.is_correct for source in result.sources
        ):
            continue

        claim_results = []
        for source in result.sources:
            claim_results.append(
                SourceVerificationResult(
                    source=source.source,
                    status=Status.CORRECT if source.is_correct else Status.INCORRECT,
                    reasoning=source.reasoning,
                )
            )
        response.append(
            CheckResponse(
                claim=result.claim,
                sources=claim_results,
            )
        )

    # pretend to be streaming, so the frontend can handle a change of API
    log.info(f"Pretending to be streaming {len(response)} responses")
    in_progress_responses = []
    for obj in response:
        in_progress = obj.copy()
        in_progress.sources = []
        for source in obj.sources:
            source_copy = source.copy()
            source_copy.status = Status.CHECK_PENDING
            in_progress.sources.append(source_copy)
        in_progress_responses.append(in_progress)

    log.info(f"Prepared {len(in_progress_responses)} in progress responses")

    async def stream_response(log):
        everything = in_progress_responses.copy()
        everything.extend(response)
        log.info(f"Sending {len(everything)} responses")
        for index, obj in enumerate(everything):
            log.info(f"Sending response {index+1}/{len(everything)}")
            yield obj.model_dump_json() + "\n"
            await asyncio.sleep(random.uniform(0.1 + (index / len(everything)) * 2, 1.5 + (index / len(everything)) * 3))

    return StreamingResponse(stream_response(log), media_type="application/json")
