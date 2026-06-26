

# Adaptive AI Interviewer

> Resume + JD → Adaptive voice/text interview → AI scoring → Personalized study roadmap

Built with **100% free software** for MVP. See  to get running.

## Stack

| Layer | Technology | Cost |
|-------|-----------|------|
| Frontend | React + Vite + TypeScript + Tailwind | Free |
| API | FastAPI (Python) | Free (open source) |
| Auth + DB + Storage | Supabase free tier | Free |
| LLM | Gemini 1.5 Flash (Google AI Studio) | Free tier |
| STT | OpenAI Whisper (local, CPU) | Free |
| Vector search | pgvector (inside Supabase Postgres) | Free |
| Hosting | Vercel (frontend) + Railway/Render (backend) | Free tier |

## Project Structure

```
adaptive-interviewer/
├── frontend/                   # React + Vite app
│   └── src/
│       ├── components/
│       │   ├── upload/         # Resume + JD upload
│       │   ├── interview/      # Live interview screen
│       │   └── report/         # Final report viewer
│       ├── store/              # Zustand interview state
│       ├── providers/          # API client
│       └── types/              # TypeScript types
└── backend/                    # FastAPI app
    ├── main.py
    ├── api/routes/             # HTTP + WebSocket routes
    ├── services/
    │   ├── skill_extraction/   # Skill entity extraction
    │   ├── match_engine/       # Resume-JD gap analysis
    │   ├── interview_orchestrator/  # State machine + concept graph
    │   ├── evaluation/         # Answer scoring
    │   └── reporting/          # Final report + roadmap
    └── providers/
        ├── llm/                # GeminiAdapter (swap to OpenAI later)
        ├── stt/                # LocalWhisperAdapter (swap to cloud later)
        └── storage/            # SupabaseStorageAdapter
```

## MVP Stage Plan

- **Stage A** (now): Text answers + upload-then-transcribe + adaptive follow-up + report
- **Stage B**: Browser mic + WebSocket audio + delayed transcript
- **Stage C**: Full WebRTC realtime voice

