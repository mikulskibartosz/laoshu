import asyncio
import logging
from enum import Enum
from typing import List, Dict, Any, AsyncGenerator
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from laoshu.verification.verification import stream_verify_citations


MOCK_RESPONSE: List[Dict[str, Any]] = [
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
    use_mock = False

    if use_mock:

        async def stream_mock_response(
            log: logging.Logger,
        ) -> AsyncGenerator[str, None]:
            for result in MOCK_RESPONSE:
                for source in result["sources"]:
                    pending = result.copy()
                    pending["sources"] = [source.copy()]
                    pending["sources"][0]["status"] = Status.CHECK_PENDING
                    log.info(
                        f"Yielding mock pending for claim: {pending['claim']}, source: {pending['sources'][0]['source']}"
                    )
                    yield CheckResponse(
                        claim=pending["claim"],
                        sources=[
                            SourceVerificationResult(
                                source=pending["sources"][0]["source"],
                                status=Status.CHECK_PENDING,
                                reasoning=pending["sources"][0]["reasoning"],
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
                                status=Status(final["sources"][0]["status"]),
                                reasoning=final["sources"][0]["reasoning"],
                            )
                        ],
                    ).model_dump_json() + "\n"
                    await asyncio.sleep(0.1)

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
                                Status.CHECK_PENDING
                                if s.is_correct is None
                                else (
                                    Status.CORRECT if s.is_correct else Status.INCORRECT
                                )
                            ),
                            reasoning=s.reasoning,
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
