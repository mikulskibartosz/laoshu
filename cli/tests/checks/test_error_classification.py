import asyncio
from laoshu.checks.error_classification import ErrorClassificationCheck

from laoshu.baml_client.types import FaithfulnessError, FaithfulnessErrorType
from typing import List


class ErrorClassificationCheckWithMocks(ErrorClassificationCheck):
    def __init__(self, returned_errors: List[FaithfulnessError]):
        self.returned_errors = returned_errors

    async def _classify_errors(self, _: str, _2: str) -> List[FaithfulnessError]:
        return self.returned_errors


def make_error(error_type: FaithfulnessErrorType) -> FaithfulnessError:
    return FaithfulnessError(error_type=error_type, reasoning="reasoning")


def test_return_no_errors() -> None:
    object_under_test = ErrorClassificationCheckWithMocks([])
    result = asyncio.run(object_under_test.classify_errors("claim", "source_content"))
    assert result == []


def test_return_one_error() -> None:
    object_under_test = ErrorClassificationCheckWithMocks(
        [make_error(FaithfulnessErrorType.CONTEXTUAL_OMISSION)]
    )
    result = asyncio.run(object_under_test.classify_errors("claim", "source_content"))
    assert result == [make_error(FaithfulnessErrorType.CONTEXTUAL_OMISSION)]


def test_return_two_different_errors() -> None:
    object_under_test = ErrorClassificationCheckWithMocks(
        [
            make_error(FaithfulnessErrorType.CONTEXTUAL_OMISSION),
            make_error(FaithfulnessErrorType.CONTRADICTORY_FACTS),
        ]
    )
    result = asyncio.run(object_under_test.classify_errors("claim", "source_content"))
    assert result == [
        make_error(FaithfulnessErrorType.CONTEXTUAL_OMISSION),
        make_error(FaithfulnessErrorType.CONTRADICTORY_FACTS),
    ]


def test_return_two_errors_with_same_type_should_be_merged() -> None:
    object_under_test = ErrorClassificationCheckWithMocks(
        [
            make_error(FaithfulnessErrorType.CONTEXTUAL_OMISSION),
            make_error(FaithfulnessErrorType.CONTEXTUAL_OMISSION),
        ]
    )
    result = asyncio.run(object_under_test.classify_errors("claim", "source_content"))
    assert len(result) == 1
    assert result[0].error_type == FaithfulnessErrorType.CONTEXTUAL_OMISSION
    assert result[0].reasoning == "reasoning\n\nreasoning"
