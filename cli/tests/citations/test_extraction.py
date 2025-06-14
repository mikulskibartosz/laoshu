from typing import List
from laoshu.citations.extraction import get_citations_with_sources, Citation


def cat_article_no_links() -> str:
    article = """
# The Fascinating World of Cats

Cats have been companions to humans for thousands of years, with evidence suggesting they were first domesticated in ancient Egypt around 7500 BCE. These graceful creatures have evolved from wild hunters to beloved pets while maintaining their natural instincts. Cats were initially attracted to human settlements due to the abundance of rodents attracted to stored grain.

The domestic cat's scientific name, Felis catus, reflects its classification within the Felidae family. There are over 70 recognized cat breeds worldwide, each with unique characteristics and personalities. From the majestic Maine Coon to the elegant Siamese, these breeds showcase the remarkable diversity within the species.
"""
    return article


def cat_article() -> str:
    article = """
# The Fascinating World of Cats

Cats have been companions to humans for thousands of years, with evidence suggesting they were first domesticated in ancient Egypt around 7500 BCE. These graceful creatures have evolved from wild hunters to beloved pets while maintaining their natural instincts. Cats were initially attracted to human settlements due to the abundance of rodents attracted to stored grain.

The domestic cat's scientific name, Felis catus, reflects its classification within the Felidae family. There are over 70 recognized cat breeds worldwide, each with unique characteristics and personalities. From the majestic Maine Coon to the elegant Siamese, these breeds showcase the remarkable diversity within the species. [National Geographic](https://www.nationalgeographic.com/animals/mammals/facts/domestic-cat) [American Association of Feline Practitioners](https://catvets.com/)

Cats possess remarkable physical abilities that have fascinated scientists and cat lovers alike. Their flexible spines allow them to twist and turn mid-air, while their retractable claws provide excellent grip and hunting capabilities. Cats have a unique "righting reflex" that enables them to land on their feet when falling from heights. [1](https://www.scientificamerican.com/article/how-do-cats-land-on-their-feet/).

According to [Psychology Today](https://www.psychologytoday.com/us/blog/the-modern-mind/201908/are-cats-social-animals), the social behavior of cats is complex and often misunderstood. While they are often portrayed as solitary animals, cats can form strong social bonds with both humans and other cats. They communicate through various vocalizations, body language, and scent marking, creating intricate social networks within their communities.

Modern cat care has evolved significantly with advances in veterinary medicine and nutrition. Organizations provide valuable resources for cat owners and veterinarians. From specialized diets to environmental enrichment, understanding cat behavior and needs has led to improved welfare and longer lifespans for our feline companions."""
    return article


def expected_cat_citations() -> List[Citation]:
    return [
        Citation(
            text="The domestic cat's scientific name, Felis catus, reflects its classification within the Felidae family. There are over 70 recognized cat breeds worldwide, each with unique characteristics and personalities. From the majestic Maine Coon to the elegant Siamese, these breeds showcase the remarkable diversity within the species.",
            sources=[
                "https://www.nationalgeographic.com/animals/mammals/facts/domestic-cat",
                "https://catvets.com/",
            ],
        ),
        Citation(
            text='Cats possess remarkable physical abilities that have fascinated scientists and cat lovers alike. Their flexible spines allow them to twist and turn mid-air, while their retractable claws provide excellent grip and hunting capabilities. Cats have a unique "righting reflex" that enables them to land on their feet when falling from heights.',
            sources=[
                "https://www.scientificamerican.com/article/how-do-cats-land-on-their-feet/"
            ],
        ),
    ]


def test_return_empty_list_if_no_citations() -> None:
    article = cat_article_no_links()
    expected_citations: List[Citation] = []
    citations = get_citations_with_sources(article)
    assert citations == expected_citations


def test_get_citations_with_sources() -> None:
    article = cat_article()
    expected_citations = expected_cat_citations()
    citations = get_citations_with_sources(article)
    assert len(citations) == len(expected_citations)
    assert citations == expected_citations
