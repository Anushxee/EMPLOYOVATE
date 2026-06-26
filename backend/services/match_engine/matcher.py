WEIGHT = {"required": 1.0, "preferred": 0.5}

class MatchEngine:
    def compute(self, candidate_skills: list, role_skills: dict) -> dict:
        required = {s["label"].lower() for s in role_skills.get("required_skills", [])}
        preferred = {s["label"].lower() for s in role_skills.get("preferred_skills", [])}
        candidate_set = {s["label"].lower(): s["confidence"] for s in candidate_skills}

        gaps, matches = [], []
        for skill in required | preferred:
            conf = candidate_set.get(skill, 0.0)
            weight = WEIGHT["required"] if skill in required else WEIGHT["preferred"]
            bucket = self._bucket(conf)
            entry = {"skill": skill, "bucket": bucket, "confidence": conf, "weight": weight}
            (matches if bucket in ("strong_match", "moderate_exposure") else gaps).append(entry)

        total_weight = sum(e["weight"] for e in matches + gaps) or 1
        score = sum(e["weight"] * e["confidence"] for e in matches) / total_weight
        return {"match_score": round(score, 2), "matches": matches, "gaps": gaps}

    def _bucket(self, confidence: float) -> str:
        if confidence >= 0.8: return "strong_match"
        if confidence >= 0.5: return "moderate_exposure"
        if confidence > 0:   return "weak_exposure"
        return "missing"
