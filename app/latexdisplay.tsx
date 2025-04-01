import { MathJax, MathJaxContext } from "better-react-mathjax";
import { useState } from "react";

export default function LatexComponent({ latex }: { latex: string }) {
  const [tooltipVisible, setTooltipVisible] = useState(false);

  const handleCopy = async () => {
    try {
      // Copy the LaTeX text to clipboard
      await navigator.clipboard.writeText(latex);
      setTooltipVisible(true);  // Show tooltip when copied
      setTimeout(() => setTooltipVisible(false), 2000);  // Hide after 2 seconds
    } catch (err) {
      alert("Failed to copy LaTeX.");
    }
  };

  return (
    <MathJaxContext>
      <div
        className="mt-6 transition delay-150 duration-300 ease-in-out hover:-translate-y-1 hover:scale-110 hover:bg-indigo-500 text-lg text-white bg-gray-800 p-10 rounded p-10 cursor-pointer group relative"
        onClick={handleCopy} // Trigger copy on click
      >
        <MathJax>{`\\(${latex}\\)`}</MathJax>
        {/* Tooltip */}
        {tooltipVisible && (
          <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 p-2 bg-black text-white rounded text-xs shadow-lg">
            Copied to clipboard!
          </div>
        )}
      </div>
    </MathJaxContext>
  );
}
