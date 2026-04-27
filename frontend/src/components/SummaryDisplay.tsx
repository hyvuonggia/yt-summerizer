import type { SummarizeResponse } from "../types";

interface SummaryDisplayProps {
  result: SummarizeResponse | null;
}

function renderSummary(summary: string) {
  // Split on blank lines into paragraphs; preserve bullet-like lines.
  return summary
    .split(/\n\s*\n/)
    .map((para) => para.trim())
    .filter(Boolean)
    .map((para, i) => {
      const lines = para.split("\n");
      const isBulletList = lines.every((l) => /^\s*[-*•]\s+/.test(l));
      if (isBulletList) {
        return (
          <ul key={i} className="summary-list">
            {lines.map((l, j) => (
              <li key={j}>{l.replace(/^\s*[-*•]\s+/, "")}</li>
            ))}
          </ul>
        );
      }
      return <p key={i}>{para}</p>;
    });
}

export function SummaryDisplay({ result }: SummaryDisplayProps) {
  if (!result) return null;
  const { summary, metadata, llm_stats, transcript_stats, processing_time } =
    result;
  return (
    <section className="summary-display" aria-label="Video summary">
      <header>
        <h2>{metadata.title}</h2>
        <p className="channel">{metadata.channel}</p>
      </header>

      <div className="summary-body">{renderSummary(summary)}</div>

      <footer className="summary-stats">
        <dl>
          <div>
            <dt>Provider</dt>
            <dd>{llm_stats.provider}</dd>
          </div>
          <div>
            <dt>Model</dt>
            <dd>{llm_stats.model}</dd>
          </div>
          <div>
            <dt>Tokens</dt>
            <dd>
              {llm_stats.total_tokens} ({llm_stats.input_tokens} in /{" "}
              {llm_stats.output_tokens} out)
            </dd>
          </div>
          <div>
            <dt>Transcript</dt>
            <dd>{transcript_stats.word_count} words</dd>
          </div>
          <div>
            <dt>Time</dt>
            <dd>{processing_time.toFixed(1)}s</dd>
          </div>
        </dl>
      </footer>
    </section>
  );
}
