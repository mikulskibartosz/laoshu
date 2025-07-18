from typing import List
from laoshu.baml_client.types import FaithfulnessError
from laoshu.baml_client import b


class ErrorClassificationCheck:
    async def classify_errors(
        self, claim: str, source_content: str
    ) -> List[FaithfulnessError]:
        return await b.ClassifyFaithfulnessErrors(claim, source_content)
