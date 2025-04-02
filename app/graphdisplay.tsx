"use client";
import React, { useState } from "react";

interface GraphProps {
    imageSrc: string | null;
}

const GraphComponent: React.FC<{ imgSource: string }> = ({ imgSource }) => {
    if (!imgSource || imgSource == "err") return <p>No graph available.</p>;

    return (
        <div className="mt-4">
            <img src={imgSource} alt="Graph Plot" className="border border-gray-300 rounded-lg" />
        </div>
    );
};
export default GraphComponent;