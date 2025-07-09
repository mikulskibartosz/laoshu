"use client";

import RichInput from "@/components/RichInput";
import ProgressIndicator from "@/components/ProgressIndicator";
import ResultTable from "@/components/ResultTable";
import { useRef, useState, useEffect, useCallback } from "react";
import { verifyAI, Claim } from "@/libs/verify_ai";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { toast } from "react-hot-toast";

export default function Page() {
  const richInputRef = useRef<any>();
  const [showProgress, setShowProgress] = useState(false);
  const [results, setResults] = useState<Claim[]>([]);
  const [lastUpdatedClaim, setLastUpdatedClaim] = useState<string | null>(null);
  const [autoScrollEnabled, setAutoScrollEnabled] = useState(true);
  const tableRef = useRef<HTMLDivElement>(null);

  // Handler to disable auto-scroll on user interaction
  const disableAutoScroll = useCallback(() => {
    setAutoScrollEnabled(false);
  }, []);

  // Attach listeners to disable auto-scroll on user scroll or click
  useEffect(() => {
    if (!autoScrollEnabled) return;

    const handleUserScroll = () => disableAutoScroll();
    const handleUserClick = () => disableAutoScroll();

    window.addEventListener("wheel", handleUserScroll, { passive: true });
    window.addEventListener("touchmove", handleUserScroll, { passive: true });
    window.addEventListener("keydown", handleUserScroll, { passive: true });
    window.addEventListener("mousedown", handleUserClick, { passive: true });

    return () => {
      window.removeEventListener("wheel", handleUserScroll);
      window.removeEventListener("touchmove", handleUserScroll);
      window.removeEventListener("keydown", handleUserScroll);
      window.removeEventListener("mousedown", handleUserClick);
    };
  }, [autoScrollEnabled, disableAutoScroll]);

  // Scroll to the last updated row if auto-scroll is enabled
  useEffect(() => {
    if (!autoScrollEnabled || !lastUpdatedClaim) return;

    // Try to find the row by a data attribute
    const row = document.querySelector(
      `[data-claim-row="${encodeURIComponent(lastUpdatedClaim)}"]`
    );
    if (row && typeof (row as HTMLElement).scrollIntoView === "function") {
      (row as HTMLElement).scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }, [results, lastUpdatedClaim, autoScrollEnabled]);

  const handleCheck = async () => {
    const markdown = richInputRef.current.getMarkdownValue();

    // Show toast if the text is empty (also strip spaces)
    if (!markdown || markdown.trim() === "") {
      toast.error("Please paste the Perplexity or ChatGPT Deep Research response");
      return;
    }

    setShowProgress(true);
    setResults([]); // Reset results for new check
    setAutoScrollEnabled(true); // Re-enable auto-scroll for new check
    setLastUpdatedClaim(null);

    try {
      for await (const claim of verifyAI(markdown)) {
        setResults(prev => {
          const merged = mergeClaimResult(prev, claim);
          setLastUpdatedClaim(claim.claim);
          return merged;
        });
        console.log(claim);
      }
    } catch (error) {
      toast.error("Error verifying AI content");
    } finally {
      setShowProgress(false);
    }
  };

  function mergeClaimResult(prev: Claim[], newClaim: Claim): Claim[] {
    // Find if claim exists
    const claimIndex = prev.findIndex(c => c.claim === newClaim.claim);
    if (claimIndex === -1) {
      // New claim, add it
      return [...prev, newClaim];
    } else {
      // Claim exists, update sources
      const existingClaim = prev[claimIndex];
      const updatedSources = [...existingClaim.sources];

      newClaim.sources.forEach(newSource => {
        const sourceIndex = updatedSources.findIndex(
          s => s.source === newSource.source
        );
        if (sourceIndex === -1) {
          // New source for this claim
          updatedSources.push(newSource);
        } else {
          // Replace existing source
          updatedSources[sourceIndex] = newSource;
        }
      });

      // Replace the claim in the array
      const updatedClaims = [...prev];
      updatedClaims[claimIndex] = {
        ...existingClaim,
        sources: updatedSources,
      };
      return updatedClaims;
    }
  }

  return (
    <>
      <main className="pb-32">
        <Header />
        <section
          className="flex flex-col items-center justify-center text-center gap-12 px-8 py-24"
          ref={tableRef}
        >
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
            <ResultTable
              results={results}
              disableButtons={showProgress}
              lastUpdatedClaim={lastUpdatedClaim}
            />
          )}
        </section>
      </main>
      <Footer />
    </>
  );
}
