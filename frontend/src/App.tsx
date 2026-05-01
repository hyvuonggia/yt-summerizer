import { useState } from "react";
import { SummarizeForm } from "./components/SummarizeForm";
import { SummaryDisplay } from "./components/SummaryDisplay";
import { ErrorBanner } from "./components/ErrorBanner";
import { ThemeToggle } from "./components/ThemeToggle";
import { ThemeProvider } from "./ThemeContext";
import type { ApiError, SummarizeResponse } from "./types";

function AppContent() {
  const [result, setResult] = useState<SummarizeResponse | null>(null);
  const [error, setError] = useState<ApiError | null>(null);

  return (
    <main className="app">
      <header className="app-header">
        <div>
          <h1>YouTube Video Summarizer</h1>
          <p>Paste a YouTube URL to get an AI-generated summary.</p>
        </div>
        <ThemeToggle />
      </header>

      <SummarizeForm onResult={setResult} onError={setError} />
      <ErrorBanner error={error} />
      <SummaryDisplay result={result} />
    </main>
  );
}

export function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}
