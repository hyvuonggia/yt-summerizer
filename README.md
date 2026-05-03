# YouTube Video Summarizer

AI-powered web application that generates summaries of YouTube videos using large language models.

## Tech Stack

- **Frontend:** React + TypeScript + Vite
- **Backend:** Python + FastAPI
- **LLM Provider:** OpenRouter (DeepSeek, OpenAI, etc.)

## Quick Start (Docker)

The easiest way to run the application:

```bash
# Start all services (Frontend, Backend)
docker compose --env-file .env.docker up -d

# View logs
docker compose --env-file .env.docker logs -f

# Stop all services
docker compose --env-file .env.docker down
```

### Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | React web app |
| Backend API | http://localhost:8000 | FastAPI server |
| API Docs | http://localhost:8000/docs | Swagger documentation |

### Environment Variables

Copy `.env.docker` to `.env` and update values:

```bash
# OpenRouter (REQUIRED)
OPENROUTER_API_KEY=your-api-key-here
```

## Development Setup

### Prerequisites

- Node.js 20+
- Python 3.13+

### Backend Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
python -m backend.main
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/summarize` | Summarize YouTube video |
| GET | `/health` | Health check |

## Features

- YouTube URL validation and video ID extraction
- Transcript retrieval from YouTube videos
- AI-powered summarization using LLM
- Dark/Light theme toggle
- Multi-language summary support

## Project Structure

```
yt-summerizer/
├── backend/              # FastAPI backend
│   ├── main.py          # Application entry point
│   ├── config.py        # Configuration
│   ├── models.py        # Pydantic models
│   └── services/        # Business logic
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── api.ts      # API client
│   │   └── App.tsx     # Main app
│   └── nginx.conf      # Nginx config for Docker
├── docker-compose.yml   # Docker orchestration
└── .env.docker         # Docker environment variables
```

## Testing

```bash
# Run backend tests
python -m pytest backend/tests/ -v

# Run frontend tests
cd frontend && npm test
```

## License

MIT