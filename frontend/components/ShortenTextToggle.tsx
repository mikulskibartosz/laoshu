import React from "react";

interface ShortenTextToggleProps {
  text: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
}

const ShortenTextToggle: React.FC<ShortenTextToggleProps> = ({
  text,
  checked,
  onChange,
  disabled = false,
}) => {
  return (
    <div className="flex items-center gap-2">
      <label className="label cursor-pointer">
        <input
          type="checkbox"
          className="toggle toggle-neutral toggle-md"
          checked={checked}
          onChange={(e) => onChange(e.target.checked)}
          disabled={disabled}
        />
      </label>
      <span className="label-text text-sm">{text}</span>
    </div>
  );
};

export default ShortenTextToggle;