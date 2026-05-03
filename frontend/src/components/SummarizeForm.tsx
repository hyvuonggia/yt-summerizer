import { useState, useEffect, type FormEvent } from "react";
import { summarizeUrl } from "../api";
import type { ApiError, SummarizeResponse, LanguageCode } from "../types";
import { SUPPORTED_LANGUAGES } from "../types";

interface SummarizeFormProps {
  onResult: (result: SummarizeResponse | null) => void;
  onError: (error: ApiError | null) => void;
}

/** Progress stages for the loading indicator */
type ProgressStage = "starting" | "transcript" | "summary";

export function SummarizeForm({ onResult, onError }: SummarizeFormProps) {
  const [url, setUrl] = useState("");
  const [summaryLanguage, setSummaryLanguage] = useState<LanguageCode>("en");
  const [loading, setLoading] = useState(false);
  const [progressStage, setProgressStage] = useState<ProgressStage>("starting");
  const [startTime, setStartTime] = useState<number | null>(null);

  // Progress message based on stage
  const progressMessages: Record<ProgressStage, string> = {
    starting: "Starting up...",
    transcript: "Fetching video transcript...",
    summary: "Generating summary with AI...",
  };

  // Update progress stage periodically to give user feedback
  useEffect(() => {
    if (!loading) return;

    const elapsed = startTime ? Date.now() - startTime : 0;

    // Progress through stages based on elapsed time
    if (elapsed < 2000) {
      setProgressStage("starting");
    } else if (elapsed < 5000) {
      setProgressStage("transcript");
    } else {
      setProgressStage("summary");
    }
  }, [loading, startTime]);

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (loading) return; // prevent double-submit

    const trimmed = url.trim();
    if (!trimmed) {
      onError({
        code: "MISSING_URL",
        message: "Please enter a YouTube URL.",
        status: 0,
      });
      return;
    }

    // Clear previous state on new submit
    onError(null);
    onResult(null);

    setLoading(true);
    setStartTime(Date.now());
    setProgressStage("starting");
    try {
      const result = await summarizeUrl(trimmed, summaryLanguage);
      onResult(result);
      setUrl("");
    } catch (err) {
      onError(err as ApiError);
    } finally {
      setLoading(false);
      setStartTime(null);
    }
  }

  return (
    <form className="summarize-form" onSubmit={handleSubmit} noValidate>
      <label htmlFor="yt-url">YouTube URL</label>
      <input
        id="yt-url"
        name="url"
        type="url"
        placeholder="https://www.youtube.com/watch?v=..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        disabled={loading}
        autoComplete="off"
      />
      <label htmlFor="summary-language">Summary Language</label>
      <select
        id="summary-language"
        name="summary_language"
        value={summaryLanguage}
        onChange={(e) => setSummaryLanguage(e.target.value as LanguageCode)}
        disabled={loading}
      >
        {SUPPORTED_LANGUAGES.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </select>
      <button type="submit" disabled={loading}>
        {loading ? "Summarizing…" : "Summarize"}
      </button>
      {loading && (
        <div role="status" aria-live="polite" className="loading-indicator">
          <span className="spinner" aria-hidden="true" />
          <div className="loading-message">
            <span className="progress-stage">{progressMessages[progressStage]}</span>
            <span className="progress-hint">This usually takes 10-30 seconds</span>
          </div>
        </div>
      )}
    </form>
  );
}
