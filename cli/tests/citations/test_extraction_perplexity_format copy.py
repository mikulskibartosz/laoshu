from typing import List
from laoshu.citations.extraction import get_citations_with_sources, Citation


def cat_article_no_links() -> str:
    article = """
# The Fascinating World of Cats

Cats have been companions to humans for thousands of years, with evidence suggesting they were first domesticated in ancient Egypt around 7500 BCE. These graceful creatures have evolved from wild hunters to beloved pets while maintaining their natural instincts. Cats were initially attracted to human settlements due to the abundance of rodents attracted to stored grain.

The domestic cat's scientific name, Felis catus, reflects its classification within the Felidae family. There are over 70 recognized cat breeds worldwide, each with unique characteristics and personalities. From the majestic Maine Coon to the elegant Siamese, these breeds showcase the remarkable diversity within the species.
"""
    return article


def bridges_article() -> str:
    article = """
The Undisputed Champion: Danyang–Kunshan Grand Bridge
The Danyang–Kunshan Grand Bridge in China held the title as the world's longest bridge in 2015, stretching an impressive 164.8 kilometers (102.4 miles) [1](https://www.civitatis.com/blog/en/longest-bridges-in-the-world/) [2](https://www.thortech.co.uk/bridges/5-of-the-worlds-longest-bridges/). This massive viaduct, completed in 2011, formed a crucial part of the Beijing–Shanghai High-Speed Railway and was officially recognized by Guinness World Records as the longest bridge in the world in any category [2](https://www.thortech.co.uk/bridges/5-of-the-worlds-longest-bridges/) [3](https://www.motivewith.com/en/get-motivated/world-longest-bridge-span-by-types). The bridge required approximately 10,000 workers over four years to complete and cost around $8.5 billion [3](https://www.motivewith.com/en/get-motivated/world-longest-bridge-span-by-types)."""
    return article


def expected_bridges_citations() -> List[Citation]:
    return [
        Citation(
            text="The Danyang–Kunshan Grand Bridge in China held the title as the world's longest bridge in 2015, stretching an impressive 164.8 kilometers (102.4 miles)",
            sources=[
                "https://www.civitatis.com/blog/en/longest-bridges-in-the-world/",
                "https://www.thortech.co.uk/bridges/5-of-the-worlds-longest-bridges/",
            ],
        ),
        Citation(
            text="This massive viaduct, completed in 2011, formed a crucial part of the Beijing–Shanghai High-Speed Railway and was officially recognized by Guinness World Records as the longest bridge in the world in any category",
            sources=[
                "https://www.thortech.co.uk/bridges/5-of-the-worlds-longest-bridges/",
                "https://www.motivewith.com/en/get-motivated/world-longest-bridge-span-by-types",
            ],
        ),
        Citation(
            text="The bridge required approximately 10,000 workers over four years to complete and cost around $8.5 billion",
            sources=[
                "https://www.motivewith.com/en/get-motivated/world-longest-bridge-span-by-types",
            ],
        ),
    ]


def test_return_empty_list_if_no_citations() -> None:
    article = cat_article_no_links()
    expected_citations: List[Citation] = []
    citations = get_citations_with_sources(article)
    assert citations == expected_citations


def test_get_citations_with_sources() -> None:
    article = bridges_article()
    expected_citations = expected_bridges_citations()
    citations = get_citations_with_sources(article)
    assert len(citations) == len(expected_citations)
    assert citations == expected_citations
