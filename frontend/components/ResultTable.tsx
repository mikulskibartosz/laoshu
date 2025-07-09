"use client";

import config from "@/config";
import React from "react";
import CheckResultBadge from "./CheckResultBadge";
import { Claim } from "@/libs/verify_ai";

interface ResultTableProps {
  results: Claim[];
  disableButtons?: boolean;
  lastUpdatedClaim?: string | null;
}

const ResultTable: React.FC<ResultTableProps> = ({
  results,
  disableButtons = false,
  lastUpdatedClaim = null,
}) => {
  if (!results || results.length === 0) {
    return null;
  }

  const handlePrintPDF = () => {
    window.print();
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="w-full flex justify-between items-center mb-4">
        <button
          className="btn btn-outline"
          onClick={() => {
            window.location.href = "/";
          }}
          disabled={disableButtons}
        >
          Run another check
        </button>
        <button
          className="btn btn-outline"
          onClick={handlePrintPDF}
          disabled={disableButtons}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            className="w-5 h-5"
          >
            <path
              fillRule="evenodd"
              d="M5 4v3H4a2 2 0 00-2 2v3a2 2 0 002 2h1v2a2 2 0 002 2h6a2 2 0 002-2v-2h1a2 2 0 002-2V9a2 2 0 00-2-2h-1V4a2 2 0 00-2-2H7a2 2 0 00-2 2zm8 0H7v3h6V4zm0 8H7v4h6v-4z"
              clipRule="evenodd"
            />
          </svg>
          Print to PDF
        </button>
      </div>
      <div className="overflow-x-auto">
        <table className="table table-zebra w-full">
          <thead>
            <tr>
              <th className="text-left">Claim</th>
              <th className="text-left">Sources</th>
              <th className="text-left">Status</th>
            </tr>
          </thead>
          <tbody>
            {results.map((result, index) => {
              // Determine if this claim is the last updated one
              const isLastUpdated =
                lastUpdatedClaim &&
                result.claim === lastUpdatedClaim;
              return (
                <React.Fragment key={index}>
                  {result.sources.map((source, sourceIndex) => (
                    <tr
                      key={`${index}-${sourceIndex}`}
                      // Only add the data attribute to the first row of the claim
                      {...(sourceIndex === 0 && isLastUpdated
                        ? {
                            "data-claim-row": encodeURIComponent(result.claim),
                          }
                        : {})}
                    >
                      {sourceIndex === 0 && (
                        <td
                          className="max-w-md"
                          rowSpan={result.sources.length}
                        >
                          <div className="text-sm">{result.claim}</div>
                        </td>
                      )}
                      <td className="max-w-md">
                        <a
                          href={source.source}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block text-xs text-blue-600 hover:text-blue-800 underline truncate"
                        >
                          {source.source}
                        </a>
                      </td>
                      <td>
                        <CheckResultBadge status={source.status} />
                      </td>
                    </tr>
                  ))}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
      <div className="mt-4 text-sm text-base-content/70">
        <p>
          Incorrect means the claim isn&apos;t backed by the provided sources.
          <br />
          It may be hallucinated, or it may still be true, but the AI provided
          the wrong source.
        </p>
      </div>
      <div className="mt-4 text-sm text-base-content/70">
        Did Lǎoshǔ miss something?{" "}
        <a
          href={config.repositoryUrlNewIssue}
          target="_blank"
          rel="noopener noreferrer"
          className="link link-hover font-semibold"
        >
          Report an issue
        </a>
      </div>
    </div>
  );
};

export default ResultTable;
