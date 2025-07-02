"use client";

import React from "react";

const ProgressIndicator: React.FC = () => {
  return (
    <div className="flex items-center justify-center gap-2">
      {[0, 1, 2, 3, 4].map((index) => (
        <div
          key={index}
          className="w-2 h-2 bg-primary rounded-sm animate-pulse"
          style={{
            animationDelay: `${index * 0.2}s`,
            animationDuration: "1s",
            animationIterationCount: "infinite",
          }}
        />
      ))}
    </div>
  );
};

export default ProgressIndicator;
