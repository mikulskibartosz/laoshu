import pytest
from pathlib import Path
from asyncio import run

from laoshu.config import load_config
from laoshu.checks.faithfulness import LlamaIndexFaithfulnessCheck

from . import get_claims, get_sources


@pytest.fixture
def get_test_data_directory() -> Path:
    return Path.cwd().parent / "test_data" / "bridges_2015"


@pytest.fixture
def get_faithfulness_check() -> LlamaIndexFaithfulnessCheck:
    config = load_config()
    if not config.openai_api_key:
        pytest.skip("OPENAI_API_KEY not set")
    return LlamaIndexFaithfulnessCheck(api_key=config.openai_api_key)


def test_should_get_all_claims_for_bridges_2015(get_test_data_directory: Path) -> None:
    claims = get_claims(get_test_data_directory)
    assert len(claims) == 3

    first_claim = claims[0]
    first_claim_citation, first_claim_is_hallucinated = first_claim
    assert len(first_claim_citation.sources) == 2
    assert first_claim_is_hallucinated is False

    second_claim = claims[1]
    second_claim_citation, second_claim_is_hallucinated = second_claim
    assert len(second_claim_citation.sources) == 2
    assert second_claim_is_hallucinated is False

    third_claim = claims[2]
    third_claim_citation, third_claim_is_hallucinated = third_claim
    assert len(third_claim_citation.sources) == 1
    assert third_claim_is_hallucinated is True


@pytest.mark.cicd
def test_ai_evaluation_for_bridges_2015(
    get_test_data_directory: Path, get_faithfulness_check: LlamaIndexFaithfulnessCheck
) -> None:
    claims = get_claims(get_test_data_directory)
    sources = get_sources(get_test_data_directory)

    expected_is_hallucinated = []
    received_is_hallucinated = []

    for claim, is_hallucinated in claims:
        sources_for_claim = [sources[source_url] for source_url in claim.sources]
        expected_is_hallucinated.append(is_hallucinated)

        result = run(get_faithfulness_check.check(claim.text, sources_for_claim))
        received_is_hallucinated.append(result.is_hallucinated)

        print(
            f"Expected: {is_hallucinated}, Received: {result.is_hallucinated}. Reason: {result.reason}"
        )

    assert expected_is_hallucinated == received_is_hallucinated
