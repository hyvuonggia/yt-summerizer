import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { SummaryDisplay } from "./SummaryDisplay";
import type { SummarizeResponse } from "../types";

const baseResponse: SummarizeResponse = {
  success: true,
  summary: "First line.\n\nSecond paragraph with more text.",
  video_id: "abc123",
  metadata: {
    video_id: "abc123",
    title: "Example Title",
    channel: "Example Channel",
    duration: 300,
    view_count: 1234,
  },
  transcript_stats: {
    word_count: 1500,
    character_count: 7500,
    token_count: 2000,
    language: "English",
  },
  llm_stats: {
    model: "deepseek/deepseek-v3.2",
    provider: "openrouter",
    input_tokens: 1200,
    output_tokens: 250,
    total_tokens: 1450,
    estimated_cost_usd: "$0.0004",
    api_time: 3.5,
  },
  processing_time: 8.2,
  timestamp: "2026-01-01T00:00:00Z",
};

describe("SummaryDisplay", () => {
  it("renders nothing when no result", () => {
    const { container } = render(<SummaryDisplay result={null} />);
    expect(container.firstChild).toBeNull();
  });

  it("renders title and channel", () => {
    render(<SummaryDisplay result={baseResponse} />);
    expect(screen.getByRole("heading", { name: /example title/i })).toBeInTheDocument();
    expect(screen.getByText(/example channel/i)).toBeInTheDocument();
  });

  it("renders summary paragraphs (split on blank lines)", () => {
    render(<SummaryDisplay result={baseResponse} />);
    expect(screen.getByText(/first line/i)).toBeInTheDocument();
    expect(screen.getByText(/second paragraph/i)).toBeInTheDocument();
  });

  it("shows provider, model, and token stats", () => {
    render(<SummaryDisplay result={baseResponse} />);
    expect(screen.getByText(/openrouter/i)).toBeInTheDocument();
    expect(screen.getByText(/deepseek\/deepseek-v3\.2/i)).toBeInTheDocument();
    expect(screen.getByText(/1450/)).toBeInTheDocument();
    expect(screen.getByText(/1500/)).toBeInTheDocument();
  });
});
