from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.uploads import router as uploads_router
from backend.api.routes.interviews import router as interviews_router

app = FastAPI(title="Adaptive AI Interviewer", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://your-vercel-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(uploads_router)
app.include_router(interviews_router)

@app.get("/health")
def health(): return {"status": "ok"}
