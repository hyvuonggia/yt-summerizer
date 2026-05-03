/**
 * Header component with theme toggle.
 * No authentication - open access mode.
 */

import { ThemeToggle } from "./ThemeToggle";

export function Header() {
  return (
    <header className="header-bar">
      <div className="header-bar-content">
        <div className="header-brand">
          <h1>YouTube Video Summarizer</h1>
          <p>Paste a YouTube URL to get an AI-generated summary.</p>
        </div>
        <div className="header-actions">
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}