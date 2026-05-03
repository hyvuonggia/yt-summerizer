import { useState } from "react";
import { SummarizeForm } from "./components/SummarizeForm";
import { SummaryDisplay } from "./components/SummaryDisplay";
import { ErrorBanner } from "./components/ErrorBanner";
import { Header } from "./components/Header";
import { ThemeProvider } from "./ThemeContext";
import type { ApiError, SummarizeResponse } from "./types";

import "./App.css";

/**
 * Main App component
 * - No authentication required (open access)
 * - Theme toggle available
 * - YouTube summarization functionality
 */
function AppContent() {
  const [result, setResult] = useState<SummarizeResponse | null>(null);
  const [error, setError] = useState<ApiError | null>(null);

  return (
    <>
      <Header />
      <main className="app">
        <SummarizeForm onResult={setResult} onError={setError} />
        <ErrorBanner error={error} />
        <SummaryDisplay result={result} />
      </main>
    </>
  );
}

export function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}