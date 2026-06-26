from .concept_graph import ConceptGraph
from backend.providers.llm import BaseLLMProvider

class NextQuestionPolicy:
    def __init__(self, llm: BaseLLMProvider):
        self.llm = llm

    async def decide(self, current_question: dict, evaluation: dict, concept_graph: ConceptGraph, blueprint: dict, time_remaining_seconds: int) -> dict:
        score = (evaluation.get("correctness", 0) + evaluation.get("completeness", 0)) / 2
        is_core = current_question.get("purpose") == "core"

        if score < 5 and is_core:          mode = "deep_followup"
        elif score < 5:                    mode = "simplify_or_pivot"
        elif time_remaining_seconds < 120: mode = "high_info"
        else:                              mode = "advance"

        context = {
            "mode": mode,
            "last_question": current_question,
            "weak_concepts": concept_graph.weak_concepts(),
            "blueprint_remaining": blueprint.get("remaining_topics", []),
            "score": score,
        }
        questions = await self.llm.generate_questions(context)
        return questions[0] if questions else {
            "question": "Walk me through your overall approach to this problem.",
            "topic": "general", "difficulty": 2, "purpose": "general"
        }
