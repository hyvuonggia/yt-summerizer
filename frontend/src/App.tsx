import { useState } from "react";
import { SummarizeForm } from "./components/SummarizeForm";
import { SummaryDisplay } from "./components/SummaryDisplay";
import { ErrorBanner } from "./components/ErrorBanner";
import type { ApiError, SummarizeResponse } from "./types";

export function App() {
  const [result, setResult] = useState<SummarizeResponse | null>(null);
  const [error, setError] = useState<ApiError | null>(null);

  return (
    <main className="app">
      <header className="app-header">
        <h1>YouTube Video Summarizer</h1>
        <p>Paste a YouTube URL to get an AI-generated summary.</p>
      </header>

      <SummarizeForm onResult={setResult} onError={setError} />
      <ErrorBanner error={error} />
      <SummaryDisplay result={result} />
    </main>
  );
}
