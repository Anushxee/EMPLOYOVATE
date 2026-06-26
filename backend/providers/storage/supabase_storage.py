from . import BaseStorageProvider
from backend.core.database import supabase

class SupabaseStorageAdapter(BaseStorageProvider):
    BUCKET = "uploads"

    async def put_resume(self, user_id: str, file_bytes: bytes, filename: str) -> str:
        path = f"resumes/{user_id}/{filename}"
        supabase.storage.from_(self.BUCKET).upload(path, file_bytes)
        return path

    async def put_recording(self, interview_id: str, audio_bytes: bytes) -> str:
        path = f"recordings/{interview_id}/answer.webm"
        supabase.storage.from_(self.BUCKET).upload(path, audio_bytes)
        return path

    async def get_signed_url(self, path: str, expires_in: int = 3600) -> str:
        resp = supabase.storage.from_(self.BUCKET).create_signed_url(path, expires_in)
        return resp["signedURL"]
