'use client'
import { useState, useEffect } from "react";
import InputList from "./inputlist";
import LatexDisplay from "./latexdisplay";

export default function TextEntry() {
    const [text, setText] = useState('');
    const [result, setResult] = useState('');
    const [solution, setSolution] = useState('');
    const [inputs, setInputs] = useState<string[]>([]);
    const [inputs1, setInputs1] = useState<string[]>([]);

    // Function to handle fetching degree from backend
    const fetchDegree = async () => {
        if (!text.trim()) return;  // Avoid unnecessary requests for empty input

        try {
            const response = await fetch('http://localhost:5328/degrees', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ equation: text }),
            });

            const data = await response.json();
            if (response.ok) {
              setResult(data.solution);
            }
        } catch (error) {
            console.error("Error fetching degree:", error);
        }
    };

    // Call `fetchDegree` when `text` changes, but debounce it to prevent excessive calls
    useEffect(() => {
        const timeoutId = setTimeout(() => {
            fetchDegree();
        }, 200); // 200ms debounce

        return () => clearTimeout(timeoutId); // Cleanup
    }, [text]);

    const handleInputsChange = (newInputs: string[]) => {
        setInputs(newInputs);
    };

    const handleInputs1Change = (newInputs1: string[]) => {
        setInputs1(newInputs1);
    };

    // Function to send equation + inputs to backend
    const handleClick = async () => {
        const dataToSend = {
            equation: text,
            inputs: inputs,
            inputs1: inputs1
        };

        try {
            const response = await fetch('http://localhost:5328/solve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dataToSend),
            });

            const data = await response.json();
            if (response.ok) {
                setSolution(data.solution);
            }else{
              alert(data.error)
            }
        } catch (error) {
            console.error("Error solving equation:", error);
            alert(error);
        }
    };

    return (
        <main className="flex min-h-screen flex-col items-center mt-3 bg-gray-900 text-white gap-1">
            {/* Text Entry Box */}
            <div className="flex space-x-5">
                <input
                    type="text"
                    placeholder="Enter a differential equation..."
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    className="outline-none p-2 caret-indigo-500 focus:border-40 focus:border-indigo-500 rounded-lg border border-gray-300 text-black"
                />
                <button 
                    className="bg-blue-500 transition delay-150 duration-300 ease-in-out 
                       hover:-translate-y-1 hover:scale-110 hover:bg-indigo-500 px-4 py-2 rounded-lg"
                    onClick={handleClick}
                >
                Solve
                </button>
            </div>

            

            {/* Render InputList if result is a valid number */}
            {parseInt(result) != 0 && !isNaN(parseInt(result)) && (
                <InputList
                    numInputs={parseInt(result)}
                    inputs={inputs}
                    setInputs={handleInputsChange}
                    inputs1={inputs1}
                    setInputs1={handleInputs1Change}
                />
            )}

            {/* Display Result */}
            {solution && <LatexDisplay latex = {solution}></LatexDisplay>}
        </main>
    );
}
