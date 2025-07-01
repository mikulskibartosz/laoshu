import yaml
from pathlib import Path
from typing import List, Tuple, Dict

from laoshu.citations.extraction import Citation, get_citations_with_sources


def get_claims(test_data_directory: Path) -> List[Tuple[Citation, bool]]:
    """
    Retrieves citations from the given test data directory and returns them with the expected is_hallucinated value.
    """
    answer_file = test_data_directory / "answer.md"

    with open(answer_file, "r", encoding="utf-8") as f:
        answer_content = f.read()

    metadata, main_content = answer_content.split("---")

    metadata_dict = yaml.safe_load(metadata)

    is_hallucinated = []
    for claim in metadata_dict.get("claims", []):
        is_hallucinated.append(claim.get("is_hallucinated", False))

    citations = get_citations_with_sources(main_content)

    claims = list(zip(citations, is_hallucinated))

    return claims


def get_sources(test_data_directory: Path) -> Dict[str, str]:
    """
    Retrieves sources from the given test data directory and returns them as a dictionary.
    Where the key is the source url and the value is the source text.
    """
    sources = {}
    for file_path in test_data_directory.glob("source_*"):
        with open(file_path, "r", encoding="utf-8") as f:
            source_text = f.read()
            metadata, main_content = source_text.split("---")
            metadata_dict = yaml.safe_load(metadata)
            sources[metadata_dict.get("source_url", "")] = main_content
    return sources
