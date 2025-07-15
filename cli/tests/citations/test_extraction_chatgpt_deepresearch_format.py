from typing import List
from laoshu.citations.extraction import get_citations_with_sources, Citation


def article() -> str:
    article = """
Introduce the idea that the model can be asked to critique and improve its own answer. For instance, after getting a response, you can prompt: “Analyze the above answer. Is there any error or something important missing? If yes, please improve the answer.” This method, known as self-refinement, has been shown to boost performance by iteratively letting the model correct itself[learnprompting.org](https://learnprompting.org/docs/advanced/self_criticism/self_refine?srsltid=AfmBOop4qBmMGpcGH3ivQtrRMhKz_Q52kuywl0-C0A8qCiK1ir8HpwfV#:~:text=%2A%20Refining%20through%20feedback%3A%20Self,results%20based%20on%20model%20feedback)[learnprompting.org](https://learnprompting.org/docs/advanced/self_criticism/self_refine?srsltid=AfmBOop4qBmMGpcGH3ivQtrRMhKz_Q52kuywl0-C0A8qCiK1ir8HpwfV#:~:text=Inspired%20by%20humans%27%20ability%20to,a%203%20step%20approach%20involving). It's like having the AI double-check its work. Quick caution: not all errors will be caught, but it’s a helpful strategy especially with GPT-4 which can critique more effectively."""
    return article


def expected_citations() -> List[Citation]:
    return [
        Citation(
            text="Introduce the idea that the model can be asked to critique and improve its own answer. For instance, after getting a response, you can prompt: “Analyze the above answer. Is there any error or something important missing? If yes, please improve the answer.” This method, known as self-refinement, has been shown to boost performance by iteratively letting the model correct itself",
            sources=[
                "https://learnprompting.org/docs/advanced/self_criticism/self_refine?srsltid=AfmBOop4qBmMGpcGH3ivQtrRMhKz_Q52kuywl0-C0A8qCiK1ir8HpwfV",
                "https://learnprompting.org/docs/advanced/self_criticism/self_refine?srsltid=AfmBOop4qBmMGpcGH3ivQtrRMhKz_Q52kuywl0-C0A8qCiK1ir8HpwfV",
            ],
        ),
    ]


def test_get_citations_with_sources() -> None:
    citations = get_citations_with_sources(article())
    assert len(citations) == len(expected_citations())
    assert citations == expected_citations()
