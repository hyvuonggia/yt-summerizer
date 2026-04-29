import { useState, type FormEvent } from "react";
import { summarizeUrl } from "../api";
import type { ApiError, SummarizeResponse, LanguageCode } from "../types";
import { SUPPORTED_LANGUAGES } from "../types";

interface SummarizeFormProps {
  onResult: (result: SummarizeResponse | null) => void;
  onError: (error: ApiError | null) => void;
}

export function SummarizeForm({ onResult, onError }: SummarizeFormProps) {
  const [url, setUrl] = useState("");
  const [summaryLanguage, setSummaryLanguage] = useState<LanguageCode>("en");
  const [loading, setLoading] = useState(false);

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
    try {
      const result = await summarizeUrl(trimmed, summaryLanguage);
      onResult(result);
      setUrl("");
    } catch (err) {
      onError(err as ApiError);
    } finally {
      setLoading(false);
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
          Working on it — fetching transcript and calling the AI…
        </div>
      )}
    </form>
  );
}
