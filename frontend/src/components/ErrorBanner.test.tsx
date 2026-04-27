import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { ErrorBanner } from "./ErrorBanner";

describe("ErrorBanner", () => {
  it("renders nothing when error is null", () => {
    const { container } = render(<ErrorBanner error={null} />);
    expect(container.firstChild).toBeNull();
  });

  it("shows friendly INVALID_URL message", () => {
    render(
      <ErrorBanner
        error={{ code: "INVALID_URL", message: "bad", status: 400 }}
      />,
    );
    expect(screen.getByRole("alert")).toHaveTextContent(/invalid youtube url/i);
  });

  it("shows friendly NO_SUBTITLES_AVAILABLE message", () => {
    render(
      <ErrorBanner
        error={{
          code: "NO_SUBTITLES_AVAILABLE",
          message: "x",
          status: 422,
        }}
      />,
    );
    expect(screen.getByRole("alert")).toHaveTextContent(/no subtitles/i);
  });

  it("shows friendly TRANSCRIPTS_DISABLED message", () => {
    render(
      <ErrorBanner
        error={{ code: "TRANSCRIPTS_DISABLED", message: "x", status: 422 }}
      />,
    );
    expect(screen.getByRole("alert")).toHaveTextContent(/transcripts.*disabled/i);
  });

  it("shows friendly NETWORK_ERROR message", () => {
    render(
      <ErrorBanner
        error={{ code: "NETWORK_ERROR", message: "offline", status: 0 }}
      />,
    );
    expect(screen.getByRole("alert")).toHaveTextContent(
      /could not reach the server/i,
    );
  });

  it("falls back to backend message for unknown codes when provided", () => {
    render(
      <ErrorBanner
        error={{ code: "WEIRD", message: "Something specific", status: 500 }}
      />,
    );
    expect(screen.getByRole("alert")).toHaveTextContent(/something specific/i);
  });

  it("shows generic 5xx message when no specific message", () => {
    render(
      <ErrorBanner
        error={{ code: "UNKNOWN_ERROR", message: "", status: 500 }}
      />,
    );
    expect(screen.getByRole("alert")).toHaveTextContent(
      /server error.*try again/i,
    );
  });
});
