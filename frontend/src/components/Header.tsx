/**
 * Header component with logout and theme toggle.
 */

import { useAuth } from "../AuthContext";
import { ThemeToggle } from "./ThemeToggle";

export function Header() {
  const { logout } = useAuth();

  return (
    <header className="header-bar">
      <div className="header-bar-content">
        <div className="header-brand">
          <h1>YouTube Video Summarizer</h1>
          <p>Paste a YouTube URL to get an AI-generated summary.</p>
        </div>
        <div className="header-actions">
          <button onClick={logout} className="btn btn-secondary">
            Logout
          </button>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}