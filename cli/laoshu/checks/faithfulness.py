from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from llama_index.llms.openai import OpenAI
from llama_index.core.evaluation.faithfulness import FaithfulnessEvaluator


@dataclass
class FaithfulnessCheckResult:
    is_hallucinated: bool
    reason: str


class FaithfulnessCheck(ABC):
    """
    Base class for faithfulness checks.

    Faithfulness checks are used to determine if a piece of text is hallucinated.

    A hallucination is a piece of text that is not supported by the evidence.

    The `check` method returns a `FaithfulnessCheckResult` object which indicates whether the text is hallucinated and the reason for the check result.
    """

    @abstractmethod
    async def check(self, text: str, context: List[str]) -> FaithfulnessCheckResult:
        """
        Checks if the text is hallucinated.

        It's expected that the text is based on the provided context. If not, the is_hallucinated flag should be set to True.

        Args:
            text (str): The text to check.
            context (List[str]): The context to use for the check.

        Returns:
            FaithfulnessCheckResult: The result of the faithfulness check.
        """
        pass

    @classmethod
    def instance(cls, api_key: str) -> FaithfulnessCheck:
        """
        Returns the default implementation of the faithfulness check.

        Args:
            api_key (str): The API key for the faithfulness check.

        Returns:
            FaithfulnessCheck: The default implementation of the faithfulness check.
        """
        return LlamaIndexFaithfulnessCheck(api_key)


class LlamaIndexFaithfulnessCheck(FaithfulnessCheck):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", temperature: float = 0.0):
        self.llm = OpenAI(api_key=api_key, model=model, temperature=temperature)

    async def check(self, text: str, context: List[str]) -> FaithfulnessCheckResult:
        evaluator = FaithfulnessEvaluator(self.llm)
        result = await evaluator.aevaluate(response=text, contexts=context)
        return FaithfulnessCheckResult(
            is_hallucinated=not result.passing,
            reason=result.feedback or "No feedback provided",
        )
