import asyncio
import logging
from typing import List, Dict, Any, AsyncGenerator, Optional
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from laoshu.verification.verification import stream_verify_citations, VerificationStatus


MOCK_RESPONSE: List[Dict[str, Any]] = [
    {
        "claim": "The Great Wall of China is visible from space with the naked eye.",
        "sources": [
            {
                "source": "https://www.nasa.gov/feature/goddard/2018/the-great-wall-of-china",
                "status": "CANNOT_RETRIEVE",
                "reasoning": "NASA has confirmed that the Great Wall of China is not visible from space with the naked eye. While it can be seen from low Earth orbit with the aid of cameras and lenses, it cannot be seen with unaided vision.",
                "error_description": "404: Not Found",
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
                "status": "CANNOT_RETRIEVE",
                "reasoning": "Scientific American debunks the 10% brain myth, explaining that humans use virtually all of their brain, with different regions active at different times for various functions.",
                "error_description": "404: Not Found",
            },
            {
                "source": "https://www.brainfacts.org/brain-anatomy-and-function/anatomy/2019/do-we-only-use-10-percent-of-our-brain-091219",
                "status": "CORRECT",
                "reasoning": "BrainFacts.org confirms that the 10% brain usage myth is false. Brain imaging shows that most of the brain is active throughout the day, even during sleep.",
            },
        ],
    },
    {
        "claim": "Lightning never strikes the same place twice.",
        "sources": [
            {
                "source": "https://www.weather.gov/safety/lightning-myths",
                "status": "INCORRECT",
                "reasoning": "The National Weather Service states that lightning can and does strike the same place more than once, especially tall, isolated objects.",
            },
            {
                "source": "https://www.nationalgeographic.com/science/article/lightning-strikes-same-place-twice",
                "status": "INCORRECT",
                "reasoning": "National Geographic explains that lightning often strikes the same place repeatedly, particularly tall structures like skyscrapers.",
            },
        ],
    },
    {
        "claim": "Bats are blind.",
        "sources": [
            {
                "source": "https://www.britannica.com/story/are-bats-really-blind",
                "status": "INCORRECT",
                "reasoning": "Britannica clarifies that bats are not blind; most species have good eyesight and use echolocation to navigate in the dark.",
            },
            {
                "source": "https://www.nationalgeographic.com/animals/mammals/facts/bats",
                "status": "CORRECT",
                "reasoning": "National Geographic confirms that bats can see and are not blind, debunking the common myth.",
            },
        ],
    },
    {
        "claim": "Goldfish have a three-second memory.",
        "sources": [
            {
                "source": "https://www.scientificamerican.com/article/fact-or-fiction-goldfish-have-a-three-second-memory/",
                "status": "CORRECT",
                "reasoning": "Scientific American reports that goldfish have a memory span of months, not seconds, and can be trained to respond to various signals.",
            },
            {
                "source": "https://www.bbc.com/news/magazine-24621394",
                "status": "INCORRECT",
                "reasoning": "BBC News explains that goldfish can remember things for weeks or months, disproving the three-second memory myth.",
            },
        ],
    },
]

USE_MOCK = True


class CheckRequest(BaseModel):
    text: str
    only_incorrect: bool = False


class SourceVerificationResult(BaseModel):
    source: str
    status: VerificationStatus
    reasoning: str
    error_description: Optional[str] = None


class CheckResponse(BaseModel):
    claim: str
    sources: List[SourceVerificationResult]


app = FastAPI()
log = logging.getLogger(__name__)


@app.post("/check")
async def check(request: CheckRequest) -> StreamingResponse:
    log.info(f"Received request: {request}")

    if USE_MOCK:

        async def stream_mock_response(
            log: logging.Logger,
        ) -> AsyncGenerator[str, None]:
            import random

            for result in MOCK_RESPONSE:
                for source in result["sources"]:
                    pending = result.copy()
                    pending["sources"] = [source.copy()]
                    pending["sources"][0]["status"] = VerificationStatus.CHECK_PENDING
                    log.info(
                        f"Yielding mock pending for claim: {pending['claim']}, source: {pending['sources'][0]['source']}"
                    )
                    yield CheckResponse(
                        claim=pending["claim"],
                        sources=[
                            SourceVerificationResult(
                                source=pending["sources"][0]["source"],
                                status=VerificationStatus.CHECK_PENDING,
                                reasoning=pending["sources"][0]["reasoning"],
                                error_description=pending["sources"][0].get(
                                    "error_description"
                                ),
                            )
                        ],
                    ).model_dump_json() + "\n"
                    await asyncio.sleep(0.1)
                    # Now yield the final result
                    final = result.copy()
                    final["sources"] = [source.copy()]
                    log.info(
                        f"Yielding mock final for claim: {final['claim']}, source: {final['sources'][0]['source']}"
                    )
                    yield CheckResponse(
                        claim=final["claim"],
                        sources=[
                            SourceVerificationResult(
                                source=final["sources"][0]["source"],
                                status=VerificationStatus(
                                    final["sources"][0]["status"]
                                ),
                                reasoning=final["sources"][0]["reasoning"],
                                error_description=final["sources"][0].get(
                                    "error_description"
                                ),
                            )
                        ],
                    ).model_dump_json() + "\n"
                    await asyncio.sleep(random.uniform(0.1, 0.5))

        stream_fn = stream_mock_response(log)
    else:

        async def stream_real(log: logging.Logger) -> AsyncGenerator[str, None]:
            try:
                async for result in stream_verify_citations(request.text):
                    # Map VerificationResult to CheckResponse
                    claim = result.claim
                    sources = [
                        SourceVerificationResult(
                            source=s.source,
                            status=(
                                VerificationStatus.CHECK_PENDING
                                if s.status == VerificationStatus.CHECK_PENDING
                                else (
                                    VerificationStatus.CORRECT
                                    if s.status == VerificationStatus.CORRECT
                                    else VerificationStatus.INCORRECT
                                )
                            ),
                            reasoning=s.reasoning,
                            error_description=s.error_description,
                        )
                        for s in result.sources
                    ]
                    log.info(
                        f"Yielding real result for claim: {claim}, sources: {[s.source for s in result.sources]}"
                    )
                    yield CheckResponse(
                        claim=claim, sources=sources
                    ).model_dump_json() + "\n"
            except Exception as e:
                log.error(f"Error in streaming: {e}")
                # Interrupt the stream with an error message
                yield '{"error": "Internal server error"}\n'

        stream_fn = stream_real(log)
    return StreamingResponse(stream_fn, media_type="application/json")
