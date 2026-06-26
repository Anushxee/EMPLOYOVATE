from backend.providers.llm import BaseLLMProvider

class AnswerEvaluator:
    def __init__(self, llm: BaseLLMProvider):
        self.llm = llm

    async def evaluate(self, question: dict, transcript: str, context: dict) -> dict:
        return await self.llm.evaluate_answer(question, transcript, context)
