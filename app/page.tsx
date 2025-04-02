import Head from 'next/head';
import TextEntry from './entrybox';
import React from 'react';

export const metadata = {
  title: "Differential Equations Solver",
  description: "solves differential equations",
}

export default function Home() {
  return (
    <>
      <Head>
        <title>Differential Equations Solver</title>
        <meta name="description" content="solves differential equations" />
        <meta property="og:image" content="https://images.icon-icons.com/2248/PNG/512/math_integral_box_icon_135416.png" />
      </Head>
        <main className="flex min-h-screen flex-col items-center justify-between p-5 bg-gray-900 text-white">
          <header className="text-center mb-10 transform translate-y-[-20px] opacity-0 animate-slideDown">
          <h1 className="text-4xl font-extrabold text-indigo-500 mb-3"><span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-white">Initial Value Problem Solver</span></h1>
          <p className="text-xl font-medium text-gray-300">By Nicholas Raal</p>
          <p className="text-sm mt-5 text-gray-400">Use prime notation for derivatives</p>
        </header>
        <div className=" w-full max-w-4xl min-h-[300px] flex flex-col justify-center">
          <TextEntry />
        </div>
      </main> 
    </>
  );
}
