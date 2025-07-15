import React from "react";
import { FaithfulnessError } from "@/libs/verify_ai";

interface HallucinationLinkProps {
  errors: FaithfulnessError[];
  disabled?: boolean;
  onShowModal: (errors: FaithfulnessError[]) => void;
}

const HallucinationLink: React.FC<HallucinationLinkProps> = ({
  errors,
  disabled = false,
  onShowModal,
}) => {
  const count = errors.length;

  if (count === 0) return null;

  const text = count === 1 ? "1 hallucination" : `${count} hallucinations`;

  return (
    <button
      className="text-blue-600 hover:text-blue-800 underline text-xs disabled:opacity-50 disabled:cursor-not-allowed"
      onClick={() => onShowModal(errors)}
      disabled={disabled}
      aria-label={`${text} - click to show details`}
    >
      {text}
    </button>
  );
};

export default HallucinationLink;
