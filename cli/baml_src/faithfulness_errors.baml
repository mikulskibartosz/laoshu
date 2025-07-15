enum FaithfulnessErrorType {
  CONTRADICTORY_FACTS @description("The claim states something that directly contradicts information in the source")
  EXAGGERATED_NUMBERS @description("Claim inflates or deflates numerical data from the source")
  WRONG_DATES_TIMELINE @description("Claim misrepresents when events occurred according to the source")
  INCORRECT_NAMES_IDENTIFIERS @description("Claim uses wrong names, titles, or identifiers for people, places, or things")
  MISATTRIBUTED_QUOTES @description("Claim attributes a statement to the wrong person or source")
  OUT_OF_CONTEXT_INFORMATION @description("Claim takes information from source but removes crucial context that changes meaning")
  WRONG_SOURCE_ATTRIBUTION @description("Claim cites a source that doesn't actually contain the stated information")
  FABRICATED_CITATIONS @description("Claim references a source that doesn't exist or doesn't contain the claimed content")
  PARTIAL_TRUTH_DISTORTION @description("Claim presents only part of the story from the source, omitting important qualifiers")
  SPECULATION_AS_FACT @description("Claim treats source's speculation or hypotheses as established facts")
  OUTDATED_INFORMATION @description("Claim uses information from source that has been superseded or corrected")
  MISSING_QUALIFICATIONS @description("Claim omits important caveats, limitations, or conditions mentioned in source")
  FALSE_CAUSATION @description("Claim suggests cause-and-effect relationship not supported by source")
  OVERGENERALIZATION @description("Claim extends source's specific findings to broader conclusions not justified")
  CHERRY_PICKING @description("Claim selectively uses only supporting evidence while ignoring contradictory information in source")
  MISINTERPRETATION_OF_STATISTICS @description("Claim misrepresents statistical findings or their significance from source")
}

class FaithfulnessError {
  reasoning string
  error_type FaithfulnessErrorType
}

function ClassifyFaithfulnessErrors(claim: string, source_content: string) -> FaithfulnessError[] {
  client "openai/gpt-4o-mini"
  prompt #"
    Analyze the relationship between the claim and the source content to identify any citation mistakes.

    Claim: {{ claim }}
    ---
    Source Content: {{ source_content }}
    ---

    Identify all types of faithfulness errors present in the claim when compared to the source content.
    Focus on how the claim misrepresents, distorts, or incorrectly attributes information from the source.

    Return a list of FaithfulnessError objects, each containing the reasoning and error_type.

    {{ ctx.output_format }}
  "#
}

test sample_faithfulness_check {
  functions [ClassifyFaithfulnessErrors]
  args {
    claim "The bridge required approximately 10,000 workers over four years to complete and cost around $8.5 billion."
    source_content "The Danyang–Kunshan Grand Bridge was completed in 2011 and spans 164.8 kilometers. Construction involved thousands of workers and cost billions of dollars, though exact figures vary by source."
  }
}
