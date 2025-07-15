export interface FaithfulnessError {
  errorType: "MISINTERPRETATION_OF_STATISTICS" | "WRONG_DATES_TIMELINE" | "EXAGGERATED_NUMBERS" | "INCORRECT_NAMES_IDENTIFIERS" | "MISATTRIBUTED_QUOTES" | "OUT_OF_CONTEXT_INFORMATION" | "WRONG_SOURCE_ATTRIBUTION" | "FABRICATED_CITATIONS" | "PARTIAL_TRUTH_DISTORTION" | "SPECULATION_AS_FACT" | "OUTDATED_INFORMATION" | "MISSING_QUALIFICATIONS" | "FALSE_CAUSATION" | "OVERGENERALIZATION" | "CHERRY_PICKING" | "MISINTERPRETATION_OF_STATISTICS";
  reasoning: string;
}

export interface SourceVerificationResult {
  source: string;
  status: "CHECK_PENDING" | "INCORRECT" | "CORRECT" | "CANNOT_RETRIEVE" | "BOT_TRAFFIC_DETECTED";
  reasoning: string;
  errorDescription?: string;
  faithfulnessErrors: FaithfulnessError[];
}

export interface Claim {
  claim: string;
  sources: SourceVerificationResult[];
}

// Mapper function to map error_description to errorDescription in each source
function mapSourceErrorDescription(src: any) {
  if ('error_description' in src && !('errorDescription' in src)) {
    if (src.status === "CANNOT_RETRIEVE") {
      return {
        ...src,
        errorDescription: `Cannot retrieve page${src.error_description ? ` (${src.error_description})` : ""}`,
      };
    }
    return {
      ...src,
      errorDescription: src.error_description,
      faithfulnessErrors: src.faithfulness_errors,
    };
  }
  return src;
}

// Async generator to yield each claim as it arrives
export async function* verifyAI(text: string): AsyncGenerator<Claim, void, unknown> {
  const response = await fetch("/api/check", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: text,
      only_incorrect: false,
    }),
  });

  if (!response.body) {
    throw new Error("No response body");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    let lines = buffer.split("\n");
    buffer = lines.pop()!; // last line may be incomplete
    for (const line of lines) {
      const trimmed = line.trim();
      console.log(trimmed);
      if (trimmed) {
        try {
          // Parse the claim object
          const parsed = JSON.parse(trimmed);
          // Map error_description to errorDescription in each source
          if (parsed.sources && Array.isArray(parsed.sources)) {
            parsed.sources = parsed.sources.map(mapSourceErrorDescription);
          }
          yield parsed;
        } catch (e) {
          // TODO: handle parse errors
        }
      }
    }
  }
  // Handle any remaining buffered line
  if (buffer.trim()) {
    try {
      const parsed = JSON.parse(buffer.trim());
      if (parsed.sources && Array.isArray(parsed.sources)) {
        parsed.sources = parsed.sources.map(mapSourceErrorDescription);
      }
      yield parsed;
    } catch (e) {
      // TODO: handle parse errors
    }
  }
}
