export interface SourceVerificationResult {
  source: string;
  status: "CHECK_PENDING" | "INCORRECT" | "CORRECT";
  reasoning: string;
}

export interface Claim {
  claim: string;
  sources: SourceVerificationResult[];
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
          yield JSON.parse(trimmed);
        } catch (e) {
          // TODO: handle parse errors
        }
      }
    }
  }
  // Handle any remaining buffered line
  if (buffer.trim()) {
    try {
      yield JSON.parse(buffer.trim());
    } catch (e) {
      // TODO: handle parse errors
    }
  }
}
