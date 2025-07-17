import React from "react";
import { Claim, FaithfulnessError } from "@/libs/verify_ai";

export class ModalContent {
  claim: Claim;
  errors: FaithfulnessError[];
  source: string;
}

interface ExplanationModalProps {
  content: ModalContent;
  isOpen: boolean;
  onClose: () => void;
}

const ExplanationModal: React.FC<ExplanationModalProps> = ({
  content,
  isOpen,
  onClose,
}) => {
  if (!isOpen || !content) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-4xl w-full mx-4 max-h-[80vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Hallucination Details</h3>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-xl"
            aria-label="Close modal"
          >
            ✕
          </button>
        </div>
        {/* Responsive layout: flex-row on md+, flex-col on mobile */}
        <div className="flex flex-col md:flex-row gap-6">
          {/* Left column: Claim and Source */}
          <div className="md:w-1/2 w-full mb-4 md:mb-0">
            <div className="mb-4">
              <div className="font-semibold text-sm text-gray-600 mb-1">Claim</div>
              <div className="text-base text-gray-900 break-words text-justify">{content.claim.claim}</div>
            </div>
            <div>
              <div className="font-semibold text-sm text-gray-600 mb-1">Source</div>
              <div className="text-base break-words text-justify">
                <a href={content.source} target="_blank" rel="noopener noreferrer" className="link link-hover text-blue-600 hover:text-blue-800">
                  {content.source}
                </a>
              </div>
            </div>
          </div>
          {/* Right column: Errors */}
          <div className="md:w-1/2 w-full">
            <div className="space-y-3">
              {content.errors.map((error: FaithfulnessError, index: number) => (
                <div key={index} className="border-l-4 border-red-500 pl-4 py-2 bg-red-50">
                  <div className="font-medium text-sm text-red-700 mb-1 text-center">
                    {error.errorType}
                  </div>
                  <div className="text-sm text-gray-700 text-justify">
                    {error.reasoning}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="btn btn-outline"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default ExplanationModal;
