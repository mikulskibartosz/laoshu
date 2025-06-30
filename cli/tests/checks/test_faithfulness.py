from asyncio import run
from laoshu.checks.faithfulness import FaithfulnessCheck
from laoshu.config import load_config
import pytest


@pytest.fixture
def api_key() -> str:
    config = load_config()
    if not config.openai_api_key:
        pytest.skip("OPENAI_API_KEY not set")
    return config.openai_api_key


@pytest.mark.cicd
def test_faithfulness_check(api_key: str) -> None:
    check = FaithfulnessCheck.instance(api_key=api_key)
    result = run(check.check(text="The sky is blue", context=["The sky is blue"]))
    assert result.is_hallucinated is False


@pytest.mark.cicd
def test_faithfulness_check_hallucinated(api_key: str) -> None:
    check = FaithfulnessCheck.instance(api_key=api_key)
    result = run(check.check(text="The sky is green", context=["The sky is blue"]))
    assert result.is_hallucinated is True
