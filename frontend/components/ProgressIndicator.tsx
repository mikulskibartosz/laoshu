"use client";

import React from "react";

const ProgressIndicator: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <div className="text-lg font-medium text-gray-700">
        Citation verification in progress...
      </div>
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
    </div>
  );
};

export default ProgressIndicator;
