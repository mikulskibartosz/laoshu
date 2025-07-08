"use client";

import React, { forwardRef, useImperativeHandle, useRef, useEffect, useState } from "react";

interface RichInputProps {
  value?: string;
  onChange?: (value: string) => void;
  placeholder?: string;
  className?: string;
  disabled?: boolean;
}

const RichInput = forwardRef<{ getMarkdownValue: () => string }, RichInputProps>(({
  onChange,
  placeholder = "Type or paste content here...",
  className = "",
  disabled = false,
}, ref) => {
  const contentRef = useRef<HTMLDivElement>(null);
  const [isComposing, setIsComposing] = useState(false);

  const handleInput = () => {
    if (contentRef.current && !isComposing && onChange) {
      onChange(contentRef.current.innerHTML);
    }
  };

  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault();

    const clipboardData = e.clipboardData;
    const pastedText = clipboardData.getData("text/html") || clipboardData.getData("text");

    // If we have HTML content, insert it directly
    if (clipboardData.getData("text/html")) {
      document.execCommand("insertHTML", false, pastedText);
    } else {
      // For plain text, preserve line breaks
      const formattedText = pastedText
        .replace(/\n/g, "<br>")
        .replace(/\r/g, "")
        .replace(/\t/g, "&nbsp;&nbsp;&nbsp;&nbsp;");
      document.execCommand("insertHTML", false, formattedText);
    }

    handleInput();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      document.execCommand("insertHTML", false, "<br>");
      handleInput();
    }
  };

  const handleCompositionStart = () => {
    setIsComposing(true);
  };

  const handleCompositionEnd = () => {
    setIsComposing(false);
    handleInput();
  };

  const getMarkdownValue = (): string => {
    if (!contentRef.current) return "";

    const html = contentRef.current.innerHTML;

    // Convert HTML to markdown
    let markdown = html
      // Convert <br> tags to newlines
      .replace(/<br\s*\/?>/gi, '\n')
      // Convert <p> tags to newlines
      .replace(/<\/p>/gi, '\n\n')
      .replace(/<p[^>]*>/gi, '')
      // Convert <strong> and <b> tags to **
      .replace(/<\/?(strong|b)>/gi, '**')
      // Convert <em> and <i> tags to *
      .replace(/<\/?(em|i)>/gi, '*')
      // Convert <h1> tags to #
      .replace(/<h1[^>]*>(.*?)<\/h1>/gi, '# $1\n\n')
      // Convert <h2> tags to ##
      .replace(/<h2[^>]*>(.*?)<\/h2>/gi, '## $1\n\n')
      // Convert <h3> tags to ###
      .replace(/<h3[^>]*>(.*?)<\/h3>/gi, '### $1\n\n')
      // Convert <h4> tags to ####
      .replace(/<h4[^>]*>(.*?)<\/h4>/gi, '#### $1\n\n')
      // Convert <h5> tags to #####
      .replace(/<h5[^>]*>(.*?)<\/h5>/gi, '##### $1\n\n')
      // Convert <h6> tags to ######
      .replace(/<h6[^>]*>(.*?)<\/h6>/gi, '###### $1\n\n')
      // Convert <ul> and <ol> tags
      .replace(/<ul[^>]*>(.*?)<\/ul>/gi, (match, content) => {
        return content.replace(/<li[^>]*>(.*?)<\/li>/gi, '- $1\n') + '\n';
      })
      .replace(/<ol[^>]*>(.*?)<\/ol>/gi, (match, content) => {
        let counter = 1;
        return content.replace(/<li[^>]*>(.*?)<\/li>/gi, () => `${counter++}. $1\n`) + '\n';
      })
      // Convert <code> tags to backticks
      .replace(/<code[^>]*>(.*?)<\/code>/gi, '`$1`')
      // Convert <pre> tags to code blocks
      .replace(/<pre[^>]*>(.*?)<\/pre>/gi, '```\n$1\n```\n')
      // Convert <a> tags to markdown links
      .replace(/<a[^>]*href="([^"]*)"[^>]*>(.*?)<\/a>/gi, '[$2]($1)')
      // Remove any remaining HTML tags
      .replace(/<[^>]*>/g, '')
      // Decode HTML entities
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      // Clean up multiple newlines
      .replace(/\n\s*\n\s*\n/g, '\n\n')
      // Trim whitespace
      .trim();

    return markdown;
  };

  // Expose methods to parent via ref
  useImperativeHandle(ref, () => ({
    getMarkdownValue: () => {
      return getMarkdownValue();
    },
  }));

  return (
    <>
      <div className="text-sm text-gray-600 mb-2">
        Paste the result from Perplexity or ChatGPT Deep Research
      </div>
      <div
        ref={contentRef}
        contentEditable={!disabled}
        onInput={handleInput}
        onPaste={handlePaste}
        onKeyDown={handleKeyDown}
        onCompositionStart={handleCompositionStart}
        onCompositionEnd={handleCompositionEnd}
        className={`w-full min-h-[200px] p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
          disabled ? "bg-gray-100 cursor-not-allowed" : "bg-white"
        } ${className}`}
        style={{
          whiteSpace: "pre-wrap",
          wordWrap: "break-word",
        }}
        data-placeholder={placeholder}
        suppressContentEditableWarning={true}
      />
    </>
  );
});

RichInput.displayName = "RichInput";

export default RichInput;
