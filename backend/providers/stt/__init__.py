from abc import ABC, abstractmethod

class BaseSTTProvider(ABC):
    async def transcribe_file(self, audio_bytes: bytes, mime_type: str) -> dict: ...
    # transcribe_stream() — Stage B
