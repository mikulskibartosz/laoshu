import { NextResponse, NextRequest } from "next/server";
import config from "@/config";

// Mock response that matches the CheckResponse structure from api.py
const mockResponse = [
  {
    claim: "The Great Wall of China is visible from space with the naked eye.",
    sources: [
      {
        source: "https://www.nasa.gov/feature/goddard/2018/the-great-wall-of-china",
        is_correct: false,
        reasoning: "NASA has confirmed that the Great Wall of China is not visible from space with the naked eye. While it can be seen from low Earth orbit with the aid of cameras and lenses, it cannot be seen with unaided vision."
      },
      {
        source: "https://www.smithsonianmag.com/science-nature/why-great-wall-china-not-visible-space-180959570/",
        is_correct: false,
        reasoning: "The Smithsonian article confirms that the Great Wall of China is not visible from space with the naked eye. This is a common misconception that has been debunked by astronauts and space agencies."
      }
    ]
  },
  {
    claim: "The Earth's atmosphere is composed primarily of nitrogen and oxygen.",
    sources: [
      {
        source: "https://www.noaa.gov/jetstream/atmosphere",
        is_correct: true,
        reasoning: "NOAA confirms that Earth's atmosphere is composed of approximately 78% nitrogen and 21% oxygen, making these the two primary components."
      },
      {
        source: "https://www.nasa.gov/audience/forstudents/k-4/stories/nasa-knows/what-is-atmosphere-k4.html",
        is_correct: false,
        reasoning: "NASA's educational content confirms that nitrogen and oxygen are the main gases in Earth's atmosphere, with nitrogen being the most abundant."
      }
    ]
  },
  {
    claim: "Humans use only 10% of their brain capacity.",
    sources: [
      {
        source: "https://www.scientificamerican.com/article/do-people-only-use-10-percent-of-their-brains/",
        is_correct: false,
        reasoning: "Scientific American debunks the 10% brain myth, explaining that humans use virtually all of their brain, with different regions active at different times for various functions."
      },
      {
        source: "https://www.brainfacts.org/brain-anatomy-and-function/anatomy/2019/do-we-only-use-10-percent-of-our-brain-091219",
        is_correct: false,
        reasoning: "BrainFacts.org confirms that the 10% brain usage myth is false. Brain imaging shows that most of the brain is active throughout the day, even during sleep."
      }
    ]
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
