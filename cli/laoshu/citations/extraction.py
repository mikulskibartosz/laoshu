import re
from typing import List, Optional
from dataclasses import dataclass
import logging


log = logging.getLogger(__name__)


@dataclass
class ParagraphLink:
    paragraph: str
    link: str


@dataclass
class Citation:
    text: str
    sources: List[str]


def _strip_last_link(paragraph: str) -> Optional[ParagraphLink]:
    """
    Extracts the last markdown link from the end of a paragraph and returns both the preceding text and the link URL.

    Args:
        paragraph (str): The paragraph text to process

    Returns:
        Optional[ParagraphLink]: A ParagraphLink object containing the paragraph text without the link
            and the extracted URL. Returns None if no link is found at the end of the paragraph.
    """
    match = re.search(r"(.*?)\s*\[([^\]]+)\]\(([^)]+)\)(?:\s*[.\n]?\s*$)", paragraph)
    if match:
        return ParagraphLink(paragraph=match.group(1), link=match.group(3))
    return None


def _split_paragraphs(article: str) -> List[str]:
    match = re.search(r"\[[^\]]*\]\([^)]+\)(?:\.)\s*", article.strip())
    if not match:
        return [article.strip()]
    end_pos = match.end()

    matched, rest = article[:end_pos], article[end_pos:]

    from_rest = _split_paragraphs(rest)

    return [matched.strip()] + from_rest


def get_citations_with_sources(article: str) -> List[Citation]:
    citations: List[Citation] = []

    paragraphs = _split_paragraphs(article)

    for paragraph in paragraphs:
        citation_text = None
        sources = []
        while paragraph_link := _strip_last_link(paragraph):
            citation_text = paragraph_link.paragraph
            sources.append(paragraph_link.link)
            paragraph = paragraph_link.paragraph
        if citation_text:
            citations.append(Citation(text=citation_text, sources=sources[::-1]))

    log.info(f"Extracted {len(citations)} citations.")
    return citations
