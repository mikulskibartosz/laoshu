class PublicationTime {
  Reasoning string
  is_in_the_text bool
  year int
  month int
  day int
}

function GetPublicationTime(markdown: string) -> PublicationTime {
  client "openai/gpt-4o"
  prompt #"
    Find the publication time of the source from the markdown.

    Return the publication time in the format of "YYYY-MM-DD" by filling out the year, month, and day.
    January 1, 2024 should be returned as year 2024, month 1, and day 1.
    If the publication date is not in the text, set is_in_the_text to false and return 0 as the date components.

    Markdown: {{ markdown }}

    {{ ctx.output_format }}
  "#
}

test real_article {
  functions [GetPublicationTime]
  args {
    markdown "**[MOTIVE](https://www.motivewith.com/en?hsLang=en)**\n\n  * [Get motivated](/en/get-motivated?hsLang=en)\n  * with MOTIVATORS’\n\n[Who is MOTIVATOR](/en/who-is-motivator?hsLang=en)\n[MOTIVATORS](/en/motivators?hsLang=en)\n\n  * [Insights](/en/insights?hsLang=en)\n  * [About us](/en/about-us?hsLang=en)\n\n[Subscribe](/en/subscribe?hsLang=en) [Be a MOTIVATOR](/en/join-\nmotive?hsLang=en)\n\n[English](https://www.motivewith.com/en?hsLang=en)\n[한국어](https://www.motivewith.com/ko?hsLang=en)\n\n#  **World's Longest Bridge Spans (by Type)**\n\n__Jan 25, 2024\n\n2 minute read\n\nThe world's longest bridge spans are not just about length; they are about engineering, design, and innovation. In this article, we will explore the world's longest bridges by type, from arch bridges to cable-stayed bridges and suspension bridges. We will also look at the engineering challenges and innovations that make these bridges possible."
  }
}

test no_publication_date {
  functions [GetPublicationTime]
  args {
    markdown "The world's longest bridge spans are not just about length; they are about engineering, design, and innovation. In this article, we will explore the world's longest bridges by type, from arch bridges to cable-stayed bridges and suspension bridges. We will also look at the engineering challenges and innovations that make these bridges possible."
  }
}