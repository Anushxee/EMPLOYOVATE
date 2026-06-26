import google.generativeai as genai
import json
from . import BaseLLMProvider
from backend.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

class GeminiAdapter(BaseLLMProvider):
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")  # free tier

    async def _chat(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

    async def generate_questions(self, context: dict) -> list[dict]:
        prompt = f"""Generate interview questions as a JSON array.
Context: {json.dumps(context)}
Return ONLY valid JSON: array of {{topic, subtopic, difficulty(1-5), question, expected_concepts[], purpose}}"""
        raw = await self._chat(prompt)
        return json.loads(raw.strip().strip("```json").strip("```"))

    async def evaluate_answer(self, question: dict, transcript: str, context: dict) -> dict:
        prompt = f"""Evaluate this interview answer. Return ONLY valid JSON.
Question: {question['question']}
Answer: {transcript}
Return: {{correctness, communication, confidence, completeness, keyword_coverage}} (0-10 each),
strengths[], misconceptions[], missing_concepts[], follow_up_type, rationale"""
        raw = await self._chat(prompt)
        return json.loads(raw.strip().strip("```json").strip("```"))

    async def extract_skills(self, text: str, doc_type: str) -> dict:
        prompt = f"""Extract skills from this {doc_type}. Return ONLY valid JSON.
Text: {text[:4000]}
Return: {{extracted_skills: [{{label, category, confidence, source_span}}], domain_signals[]}}"""
        raw = await self._chat(prompt)
        return json.loads(raw.strip().strip("```json").strip("```"))

    async def generate_roadmap(self, weak_concepts: list[str], role: str) -> dict:
        prompt = f"""Study roadmap for {role} role targeting: {weak_concepts}.
Return ONLY valid JSON: {{weeks: [{{week, title, topics[], resources_placeholder[]}}]}}"""
        raw = await self._chat(prompt)
        return json.loads(raw.strip().strip("```json").strip("```"))
