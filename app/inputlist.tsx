import React, { useState } from 'react';

const InputList: React.FC<{
  numInputs: number;
  inputs: string[];
  setInputs: (newInputs: string[]) => void;
  inputs1: string[];
  setInputs1: (newInputs1: string[]) => void;
}> = ({ numInputs, inputs, setInputs, inputs1, setInputs1 }) => {
    // Handle input change for inputs
    const handleChange = (index: number, event: React.ChangeEvent<HTMLInputElement>) => {
        const newInputs = [...inputs];
        newInputs[index] = event.target.value;
        setInputs(newInputs);
    };

    // Handle input change for inputs1
    const handleChange1 = (index: number, event: React.ChangeEvent<HTMLInputElement>) => {
        const newInputs1 = [...inputs1];
        newInputs1[index] = event.target.value;
        setInputs1(newInputs1);
    };

    return (
        <div className="flex flex-col gap-2  mt-6">
            {Array.from({ length: numInputs }).map((_, index) => (
                <div key={index} className="flex items-center justify-end">
                    <p className="mr-2">y{'\''.repeat(index)}(</p>
                    <input
                        type="text"
                        className="p-1 border border-gray-300 rounded text-black w-10"
                        value={inputs[index]}  // Controlled component
                        onChange={(e) => handleChange(index, e)}
                    />
                    <p className="ml-2">)</p> {/* Add text after input */}
                    <p className="mr-2">=</p> {/* Add text before input */}
                    <input
                        type="text"
                        value={inputs1[index]} 
                        onChange={(e) => handleChange1(index, e)}
                        className="p-1 border border-gray-300 rounded text-black w-10"
                    />
                    <p className="ml-2"></p> {/* Add text after input */}
                </div>
            ))}
        </div>
    );
};
export default InputList