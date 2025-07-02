"use client";

import RichInput from "@/components/RichInput";
import ProgressIndicator from "@/components/ProgressIndicator";
import ResultTable from "@/components/ResultTable";
import { useRef, useState } from "react";
import { verifyAI } from "@/libs/verify_ai";
import { Claim } from "@/libs/verify_ai";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { toast } from "react-hot-toast";

export default function Page() {
  const richInputRef = useRef<any>();
  const [showProgress, setShowProgress] = useState(false);
  const [results, setResults] = useState<Claim[]>([]);

  const handleCheck = async () => {
    const markdown = richInputRef.current.getMarkdownValue();

    // Show toast if the text is empty (also strip spaces)
    if (!markdown || markdown.trim() === "") {
      toast.error("Please paste the Perplexity or ChatGPT Deep Research response");
      return;
    }

    setShowProgress(true);
    const results = await verifyAI(markdown);
    setResults(results);

    richInputRef.current.setMarkdownValue(markdown);
    setShowProgress(false);
  }

  return (
    <>
      <main className="pb-32">
        <Header />
        <section className="flex flex-col items-center justify-center text-center gap-12 px-8 py-24">

          {results.length === 0 && (
            <>
              <RichInput ref={richInputRef} />

              <button className="btn btn-primary" onClick={handleCheck} disabled={showProgress}>
                {showProgress ? "Checking..." : "Check for hallucinations"}
              </button>
            </>
          )}

          {showProgress && <ProgressIndicator />}
          {results.length > 0 && (
            <ResultTable results={results} />
          )}
        </section>
      </main>
      <Footer />
    </>
  );
}
