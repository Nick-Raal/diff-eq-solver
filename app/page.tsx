import Head from 'next/head';
import TextEntry from './entrybox';
import React from 'react';

export default function Home() {
  return (
    <>
      <Head>
        <title>Main Page</title>
        <meta name="description" content="Main page heading here" />
      </Head>
      <main className="flex min-h-screen flex-col items-center justify-between p-5 bg-gray-900 text-white">
        <header className="text-center">
          <h1 className="text-3xl font-bold">Initial Value Problem Solver</h1>
          <p className="text-lg">By Nicholas Raal</p>
        </header>
      <TextEntry></TextEntry>
      </main> 
    </>
  );
}
