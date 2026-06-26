# Setup Guide

## Prerequisites
- Python 3.11+
- Node.js 20+
- A free [Supabase](https://supabase.com) project
- A free [Google AI Studio](https://aistudio.google.com) Gemini API key

---

## 1. Supabase Setup (free)

1. Create a new project at supabase.com
2. Enable pgvector: SQL Editor → run 
3. Create a storage bucket named **uploads** (public: false)
4. Copy your project URL and API keys

---

## 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scriptsctivate
pip install -r requirements.txt

cp .env.example .env
# Fill in SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_KEY, GEMINI_API_KEY, SECRET_KEY

uvicorn backend.main:app --reload
```

API docs at http://localhost:8000/docs

---

## 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env   # set VITE_API_URL=http://localhost:8000
npm run dev
```

App at http://localhost:5173

---

## 4. Deploy (free tier)

| Service | Where |
|---------|-------|
| Frontend | Vercel (connect GitHub repo, root = frontend/) |
| Backend  | Railway or Render free tier (Dockerfile or Python build) |
| DB/Auth/Storage | Supabase free |
| LLM | Gemini Developer Free Tier |
| STT | Local Whisper (runs on backend CPU) |

Set environment variables in the hosting dashboard matching .env.example

---

## Stage Roadmap

| Stage | What it adds |
|-------|-------------|
| **A (now)** | Text-based answers, upload-based transcription, adaptive follow-up, report |
| **B** | Browser mic recording, WebSocket audio streaming, local Whisper transcription |
| **C** | Full WebRTC realtime voice, TURN server, streaming STT |
