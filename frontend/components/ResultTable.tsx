"use client";

import config from "@/config";
import React from "react";

interface Claim {
  claim: string;
  sources: string[];
  is_correct: boolean;
}

interface ResultTableProps {
  results: Claim[];
}

const ResultTable: React.FC<ResultTableProps> = ({ results }) => {
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
          onClick={() => { window.location.href = "/"; }}
        >
          Run another check
        </button>
        <button className="btn btn-outline" onClick={handlePrintPDF}>
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
            {results.map((result, index) => (
              <tr key={index}>
                <td className="max-w-md">
                  <div className="text-sm">{result.claim}</div>
                </td>
                <td className="max-w-md">
                  <div className="space-y-1">
                    {result.sources.map((source, sourceIndex) => (
                      <a
                        key={sourceIndex}
                        href={source}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="block text-xs text-blue-600 hover:text-blue-800 underline truncate"
                      >
                        {source}
                      </a>
                    ))}
                  </div>
                </td>
                <td>
                  <div className={`badge ${result.is_correct ? 'badge-success' : 'badge-error'}`}>
                    {result.is_correct ? 'Correct' : 'Incorrect'}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-4 text-sm text-base-content/70">
        <p>Incorrect means the claim isn&apos;t backed by the provided sources.<br/>It may be hallucinated, or it may still be true, but the AI provided the wrong source.</p>
      </div>
      <div className="mt-4 text-sm text-base-content/70">
        Did Lǎoshǔ miss something? <a href={config.repositoryUrlNewIssue} target="_blank" rel="noopener noreferrer" className="link link-hover font-semibold">Report an issue</a>
      </div>
    </div>
  );
};

export default ResultTable;
