import { SourceVerificationResult } from "@/libs/verify_ai";
import React from "react";

interface CheckResultBadgeProps {
  status: SourceVerificationResult["status"];
  className?: string;
}

const CheckResultBadge: React.FC<CheckResultBadgeProps> = ({ status, className = "" }) => {
  const getBadgeConfig = (status: SourceVerificationResult["status"]) => {
    switch (status) {
      case "CORRECT":
        return {
          label: "Correct",
          classes: "badge-success"
        };
      case "INCORRECT":
        return {
          label: "Incorrect",
          classes: "badge-error"
        };
      case "CHECK_PENDING":
        return {
          label: "Checking...",
          classes: "badge-neutral"
        };
      case "CANNOT_RETRIEVE":
        return {
          label: "Error",
          classes: "badge-error"
        };
      case "BOT_TRAFFIC_DETECTED":
        return {
          label: "Bot",
          classes: "badge-warning"
        };
      default:
        return {
          label: "Unknown",
          classes: "badge-neutral"
        };
    }
  };

  const config = getBadgeConfig(status);

  return (
    <div className={`badge ${config.classes} ${className}`}>
      {config.label}
    </div>
  );
};

export default CheckResultBadge;
