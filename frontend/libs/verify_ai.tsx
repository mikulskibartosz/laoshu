export interface FaithfulnessError {
  errorType:
    | "CONTRADICTORY_FACTS"
    | "NUMERIC_STATISTICAL_DISTORTION"
    | "WRONG_DATES_TIMELINE"
    | "INCORRECT_ATTRIBUTION_IDENTIFIER"
    | "CONTEXTUAL_OMISSION"
    | "BAD_OR_NONEXISTENT_SOURCE"
    | "SPECULATION_AS_FACT"
    | "OUTDATED_INFORMATION"
    | "FALSE_CAUSATION"
    | "OVERGENERALIZATION";
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

function mapErrorTypeToHumanReadable(errorType: string) {
  return errorType
    .toLowerCase()
    .split("_")
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

// Mapper function to map error_description to errorDescription in each source
function mapSourceErrorDescription(src: any) {
  // Helper to map error_type to errorType in faithfulness errors
  function mapFaithfulnessErrors(errors: any[]) {
    if (!Array.isArray(errors)) return errors;
    return errors.map((err) => {
      if (err && typeof err === "object" && "error_type" in err && !("errorType" in err)) {
        // Map error_type to errorType, preserve other properties
        const { error_type, ...rest } = err;
        return { ...rest, errorType: mapErrorTypeToHumanReadable(error_type) };
      }
      return err;
    });
  }

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
      faithfulnessErrors: mapFaithfulnessErrors(src.faithfulness_errors),
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
