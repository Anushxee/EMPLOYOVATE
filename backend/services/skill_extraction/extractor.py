import re
from backend.providers.llm import BaseLLMProvider

class SkillExtractor:
    def __init__(self, llm: BaseLLMProvider):
        self.llm = llm

    async def extract(self, text: str, doc_type: str) -> dict:
        cleaned = re.sub(r"\s+", " ", text).strip()
        return await self.llm.extract_skills(cleaned, doc_type)
