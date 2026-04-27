import { describe, it, expect, beforeEach, vi, afterEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { SummarizeForm } from "./SummarizeForm";
import type { SummarizeResponse } from "../types";

const successPayload: SummarizeResponse = {
  success: true,
  summary: "Great summary.",
  video_id: "abc123",
  metadata: { video_id: "abc123", title: "T", channel: "C" },
  transcript_stats: { word_count: 10, character_count: 50 },
  llm_stats: {
    model: "m",
    provider: "openrouter",
    input_tokens: 1,
    output_tokens: 2,
    total_tokens: 3,
  },
  processing_time: 0.1,
  timestamp: "2026-01-01T00:00:00Z",
};

describe("SummarizeForm", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders input and submit button", () => {
    render(<SummarizeForm onResult={() => {}} onError={() => {}} />);
    expect(screen.getByLabelText(/youtube url/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /summarize/i }),
    ).toBeInTheDocument();
  });

  it("blocks submit when URL is empty and surfaces a validation error", async () => {
    const onError = vi.fn();
    const onResult = vi.fn();
    render(<SummarizeForm onResult={onResult} onError={onError} />);
    await userEvent.click(screen.getByRole("button", { name: /summarize/i }));
    expect(fetch).not.toHaveBeenCalled();
    expect(onError).toHaveBeenCalledWith(
      expect.objectContaining({ code: "MISSING_URL" }),
    );
  });

  it("disables submit and shows loading indicator while request is in flight", async () => {
    let resolveFetch!: (v: unknown) => void;
    (fetch as unknown as ReturnType<typeof vi.fn>).mockImplementationOnce(
      () =>
        new Promise((resolve) => {
          resolveFetch = resolve;
        }),
    );
    render(<SummarizeForm onResult={() => {}} onError={() => {}} />);
    await userEvent.type(
      screen.getByLabelText(/youtube url/i),
      "https://youtu.be/abc123",
    );
    await userEvent.click(screen.getByRole("button", { name: /summarize/i }));

    const button = screen.getByRole("button", { name: /summarizing/i });
    expect(button).toBeDisabled();
    expect(screen.getByRole("status")).toHaveTextContent(/working/i);

    resolveFetch({ ok: true, status: 200, json: async () => successPayload });
    await waitFor(() =>
      expect(
        screen.getByRole("button", { name: /summarize/i }),
      ).not.toBeDisabled(),
    );
  });

  it("clears previous errors and results when a new submit starts", async () => {
    const onResult = vi.fn();
    const onError = vi.fn();
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => successPayload,
    });
    render(<SummarizeForm onResult={onResult} onError={onError} />);
    await userEvent.type(
      screen.getByLabelText(/youtube url/i),
      "https://youtu.be/abc123",
    );
    await userEvent.click(screen.getByRole("button", { name: /summarize/i }));

    await waitFor(() => expect(onResult).toHaveBeenCalledWith(successPayload));
    // Each submit should clear previous error/result via callbacks
    expect(onError).toHaveBeenCalledWith(null);
    expect(onResult).toHaveBeenNthCalledWith(1, null);
  });

  it("calls onResult with parsed response on success", async () => {
    const onResult = vi.fn();
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => successPayload,
    });
    render(<SummarizeForm onResult={onResult} onError={() => {}} />);
    await userEvent.type(
      screen.getByLabelText(/youtube url/i),
      "https://youtu.be/abc123",
    );
    await userEvent.click(screen.getByRole("button", { name: /summarize/i }));
    await waitFor(() => expect(onResult).toHaveBeenCalledWith(successPayload));
  });

  it("calls onError with ApiError on backend failure", async () => {
    const onError = vi.fn();
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: false,
      status: 422,
      json: async () => ({
        detail: { error: "no subs", error_code: "NO_SUBTITLES_AVAILABLE" },
      }),
    });
    render(<SummarizeForm onResult={() => {}} onError={onError} />);
    await userEvent.type(
      screen.getByLabelText(/youtube url/i),
      "https://youtu.be/x",
    );
    await userEvent.click(screen.getByRole("button", { name: /summarize/i }));
    await waitFor(() =>
      expect(onError).toHaveBeenCalledWith(
        expect.objectContaining({ code: "NO_SUBTITLES_AVAILABLE", status: 422 }),
      ),
    );
  });

  it("clears the input after a successful submit", async () => {
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => successPayload,
    });
    render(<SummarizeForm onResult={() => {}} onError={() => {}} />);
    const input = screen.getByLabelText(/youtube url/i) as HTMLInputElement;
    await userEvent.type(input, "https://youtu.be/abc123");
    await userEvent.click(screen.getByRole("button", { name: /summarize/i }));
    await waitFor(() => expect(input.value).toBe(""));
  });
});
