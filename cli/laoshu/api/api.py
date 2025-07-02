from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from laoshu.verification.verification import verify_citations


class CheckRequest(BaseModel):
    text: str
    only_incorrect: bool = False


class CheckResponse(BaseModel):
    claim: str
    sources: List[str]
    is_correct: bool


app = FastAPI()


@app.post("/check")
async def check(
    request: CheckRequest
) -> List[CheckResponse]:
    results = await verify_citations(request.text)

    response = []
    for result in results:
        if request.only_incorrect and result.is_correct:
            continue
        response.append(
            CheckResponse(
                claim=result.claim,
                sources=result.sources,
                is_correct=result.is_correct,
            )
        )

    return response
