"""Fully free local STT via openai-whisper (runs on CPU)."""
import whisper, tempfile, os
from . import BaseSTTProvider

class LocalWhisperAdapter(BaseSTTProvider):
    def __init__(self, model_size: str = "base"):
        self.model = whisper.load_model(model_size)

    async def transcribe_file(self, audio_bytes: bytes, mime_type: str) -> dict:
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
            f.write(audio_bytes)
            tmp = f.name
        try:
            result = self.model.transcribe(tmp)
            return {"text": result["text"], "segments": result.get("segments", [])}
        finally:
            os.unlink(tmp)
