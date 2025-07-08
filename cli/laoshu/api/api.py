from enum import Enum
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from laoshu.verification.verification import verify_citations



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


@app.post("/check")
async def check(request: CheckRequest) -> List[CheckResponse]:
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

    return response
