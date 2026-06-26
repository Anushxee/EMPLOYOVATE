from enum import Enum

class ConceptStatus(str, Enum):
    UNEXPLORED = "unexplored"
    PARTIALLY_VALIDATED = "partially_validated"
    VALIDATED = "validated"
    WEAK = "weak"
    FAILED = "failed"

class ConceptGraph:
    def __init__(self):
        self.nodes: dict = {}

    def add(self, concept: str):
        self.nodes.setdefault(concept, ConceptStatus.UNEXPLORED)

    def update(self, concept: str, score: float):
        if score >= 7:   self.nodes[concept] = ConceptStatus.VALIDATED
        elif score >= 4: self.nodes[concept] = ConceptStatus.PARTIALLY_VALIDATED
        elif score >= 2: self.nodes[concept] = ConceptStatus.WEAK
        else:            self.nodes[concept] = ConceptStatus.FAILED

    def weak_concepts(self) -> list:
        return [c for c, s in self.nodes.items() if s in (ConceptStatus.WEAK, ConceptStatus.FAILED)]

    def to_dict(self) -> dict:
        return {k: v.value for k, v in self.nodes.items()}
