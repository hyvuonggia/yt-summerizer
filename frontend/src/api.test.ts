import { describe, it, expect, beforeEach, vi, afterEach } from "vitest";
import { summarizeUrl } from "./api";

describe("summarizeUrl", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("POSTs JSON to /api/summarize and returns parsed response on success", async () => {
    const payload = {
      success: true,
      summary: "This is the summary.",
      video_id: "abc123",
      metadata: { video_id: "abc123", title: "T", channel: "C" },
      transcript_stats: { word_count: 100, character_count: 500 },
      llm_stats: {
        model: "m",
        provider: "openrouter",
        input_tokens: 10,
        output_tokens: 5,
        total_tokens: 15,
      },
      processing_time: 1.5,
      timestamp: "2026-01-01T00:00:00Z",
    };
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => payload,
    });

    const result = await summarizeUrl("https://youtu.be/abc123");

    expect(fetch).toHaveBeenCalledTimes(1);
    const [url, init] = (fetch as unknown as ReturnType<typeof vi.fn>).mock.calls[0];
    expect(url).toMatch(/\/api\/summarize$/);
    expect(init.method).toBe("POST");
    expect(init.headers["Content-Type"]).toBe("application/json");
    expect(JSON.parse(init.body)).toEqual({ url: "https://youtu.be/abc123", summary_language: "en" });
    expect(result).toEqual(payload);
  });

  it("throws ApiError with code from FastAPI detail on 400", async () => {
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: async () => ({
        detail: { error: "bad url", error_code: "INVALID_URL" },
      }),
    });

    await expect(summarizeUrl("not a url")).rejects.toMatchObject({
      code: "INVALID_URL",
      status: 400,
      message: "bad url",
    });
  });

  it("maps 422 NO_SUBTITLES_AVAILABLE", async () => {
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: false,
      status: 422,
      json: async () => ({
        detail: {
          error: "No subtitles available for this video",
          error_code: "NO_SUBTITLES_AVAILABLE",
        },
      }),
    });

    await expect(summarizeUrl("https://youtu.be/x")).rejects.toMatchObject({
      code: "NO_SUBTITLES_AVAILABLE",
      status: 422,
    });
  });

  it("throws ApiError with NETWORK_ERROR on fetch rejection", async () => {
    (fetch as unknown as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      new Error("offline"),
    );

    await expect(summarizeUrl("https://youtu.be/x")).rejects.toMatchObject({
      code: "NETWORK_ERROR",
      status: 0,
    });
  });

  it("falls back to UNKNOWN_ERROR when error body is unparseable", async () => {
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => {
        throw new Error("not json");
      },
    });

    await expect(summarizeUrl("https://youtu.be/x")).rejects.toMatchObject({
      code: "UNKNOWN_ERROR",
      status: 500,
    });
  });
});
