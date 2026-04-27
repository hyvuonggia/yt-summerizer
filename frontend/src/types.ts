/**
 * Shared API/domain types mirroring the backend response schema.
 * Source of truth: backend/models.py
 */

export interface VideoMetadata {
  video_id: string;
  title: string;
  channel: string;
  duration?: number;
  view_count?: number;
  upload_date?: string;
  thumbnail?: string;
}

export interface TranscriptStats {
  language?: string;
  language_code?: string;
  word_count: number;
  character_count: number;
  token_count?: number;
}

export interface LLMStats {
  model: string;
  provider: string;
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
  estimated_cost_usd?: string;
  api_time?: number;
}

export interface SummarizeResponse {
  success: true;
  summary: string;
  video_id: string;
  metadata: VideoMetadata;
  transcript_stats: TranscriptStats;
  llm_stats: LLMStats;
  processing_time: number;
  timestamp: string;
}

export interface ApiError {
  /** Machine-readable code, e.g. INVALID_URL, NO_SUBTITLES_AVAILABLE */
  code: string;
  /** Original message from the backend */
  message: string;
  /** HTTP status code, or 0 for network failures */
  status: number;
}
