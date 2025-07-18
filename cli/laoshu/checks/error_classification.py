from typing import Dict, List
from laoshu.baml_client.types import FaithfulnessError, FaithfulnessErrorType
from laoshu.baml_client import b


class ErrorClassificationCheck:
    async def classify_errors(
        self, claim: str, source_content: str
    ) -> List[FaithfulnessError]:
        errors = await b.ClassifyFaithfulnessErrors(claim, source_content)

        merged: Dict[FaithfulnessErrorType, FaithfulnessError] = {}
        for error in errors:
            key = error.error_type
            if key in merged:
                merged[key].reasoning += "\n\n" + error.reasoning
            else:
                merged[key] = error
        return list(merged.values())
