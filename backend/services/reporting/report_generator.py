from backend.providers.llm import BaseLLMProvider

class ReportGenerator:
    def __init__(self, llm: BaseLLMProvider):
        self.llm = llm

    async def generate(self, session: dict) -> dict:
        evaluations = session.get("answer_evaluations", [])
        concept_graph = session.get("concept_graph", {})
        role = session.get("role_profile", {}).get("title", "Software Engineer")

        weak_concepts = [c for c, s in concept_graph.items() if s in ("weak", "failed")]
        roadmap = await self.llm.generate_roadmap(weak_concepts, role)

        dims = ["correctness","communication","confidence","completeness","keyword_coverage"]
        avg = {}
        for d in dims:
            vals = [e.get(d, 0) for e in evaluations]
            avg[d] = round(sum(vals)/len(vals), 1) if vals else 0

        overall = round(sum(avg.values())/len(avg), 1) if avg else 0
        band = "hire_ready" if overall>=8 else "borderline" if overall>=6 else "needs_development" if overall>=4 else "not_ready"
        return {
            "overall_score": overall,
            "dimension_scores": avg,
            "concept_graph": concept_graph,
            "weak_concepts": weak_concepts,
            "roadmap": roadmap,
            "hiring_readiness": band,
        }
