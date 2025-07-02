import { NextResponse, NextRequest } from "next/server";
import config from "@/config";

// Mock response that matches the CheckResponse structure from api.py
const mockResponse = [
  {
    claim: "The Great Wall of China is visible from space with the naked eye.",
    sources: [
      "https://www.nasa.gov/feature/goddard/2018/the-great-wall-of-china",
      "https://www.smithsonianmag.com/science-nature/why-great-wall-china-not-visible-space-180959570/"
    ],
    is_correct: false
  },
  {
    claim: "The Earth's atmosphere is composed primarily of nitrogen and oxygen.",
    sources: [
      "https://www.noaa.gov/jetstream/atmosphere",
      "https://www.nasa.gov/audience/forstudents/k-4/stories/nasa-knows/what-is-atmosphere-k4.html"
    ],
    is_correct: true
  },
  {
    claim: "Humans use only 10% of their brain capacity.",
    sources: [
      "https://www.scientificamerican.com/article/do-people-only-use-10-percent-of-their-brains/",
      "https://www.brainfacts.org/brain-anatomy-and-function/anatomy/2019/do-we-only-use-10-percent-of-our-brain-091219"
    ],
    is_correct: false
  }
];


export async function POST(req: NextRequest) {
  const body = await req.json();

  if (!body.text) {
    return NextResponse.json({ error: "Text is required" }, { status: 400 });
  }

  try {
    const response = await fetch(`${config.backendUrl}/check`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: body.text,
        only_incorrect: body.only_incorrect || false,
      }),
    });

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.statusText}`);
    }

    const data = await response.json();
    // const data = mockResponse;
    return NextResponse.json(data);
  } catch (e) {
    console.error(e);
    return NextResponse.json({ error: e.message }, { status: 500 });
  }
}
