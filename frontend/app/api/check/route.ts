import { NextRequest } from "next/server";
import config from "@/config";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  const body = await req.json();

  if (!body.text) {
    return new Response(JSON.stringify({ error: "Text is required" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  const backendResponse = await fetch(`${config.backendUrl}/check`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: body.text,
      only_incorrect: body.only_incorrect || false,
    }),
  });

  if (!backendResponse.body) {
    return new Response(JSON.stringify({ error: "No response body from backend" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }

  const stream = new ReadableStream({
    async start(controller) {
      const reader = backendResponse.body.getReader();
      let { value, done } = await reader.read();
      while (!done) {
        controller.enqueue(value);
        ({ value, done } = await reader.read());
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "application/json",
      "Transfer-Encoding": "chunked",
    },
  });
}
