import React from "react";

enum Status {
  CHECK_PENDING = "CHECK_PENDING",
  INCORRECT = "INCORRECT",
  CORRECT = "CORRECT",
}

interface CheckResultBadgeProps {
  status: Status;
  className?: string;
}

const CheckResultBadge: React.FC<CheckResultBadgeProps> = ({ status, className = "" }) => {
  const getBadgeConfig = (status: Status) => {
    switch (status) {
      case Status.CORRECT:
        return {
          label: "Correct",
          classes: "badge-success"
        };
      case Status.INCORRECT:
        return {
          label: "Incorrect",
          classes: "badge-error"
        };
      case Status.CHECK_PENDING:
        return {
          label: "Checking...",
          classes: "badge-neutral"
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
export { Status };

