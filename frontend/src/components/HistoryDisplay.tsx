import { useState, useEffect } from "react";
import { getUserHistory, deleteHistoryItem, getStoredToken, type HistoryItem } from "../api";

interface HistoryDisplayProps {
  refreshTrigger?: number;
}

/**
 * Display user's summary history.
 */
export function HistoryDisplay({ refreshTrigger }: HistoryDisplayProps) {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchHistory = async () => {
    if (!getStoredToken()) {
      setLoading(false);
      return;
    }

    setLoading(true);
    try {
      const history = await getUserHistory();
      setItems(history.items);
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch history");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [refreshTrigger]);

  const handleDelete = async (id: number) => {
    try {
      await deleteHistoryItem(id);
      setItems(items.filter((item) => item.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete");
    }
  };

  if (loading) {
    return <div className="history-loading">Loading history...</div>;
  }

  if (error) {
    return <div className="history-error">{error}</div>;
  }

  if (!getStoredToken()) {
    return null;
  }

  if (items.length === 0) {
    return <div className="history-empty">No summaries yet. Summarize a video to get started!</div>;
  }

  return (
    <div className="history-container">
      <h2>Your Summaries</h2>
      <div className="history-list">
        {items.map((item) => (
          <div key={item.id} className="history-item">
            <div className="history-item-header">
              <h3>{item.video_title}</h3>
              <button
                onClick={() => handleDelete(item.id)}
                className="btn btn-small"
                aria-label="Delete"
              >
                Delete
              </button>
            </div>
            <p className="video-id">Video ID: {item.video_id}</p>
            <p className="summary-text">{item.summary.slice(0, 200)}...</p>
            <p className="created-at">
              {new Date(item.created_at).toLocaleDateString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}