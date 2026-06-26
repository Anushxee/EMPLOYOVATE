export interface Interview {
  id: string;
  state: string;
  currentQuestion?: Question;
  questionHistory: Question[];
  answerEvaluations: Evaluation[];
}

export interface Question {
  topic: string;
  subtopic?: string;
  difficulty: number;
  question: string;
  expected_concepts?: string[];
  purpose?: string;
}

export interface Evaluation {
  correctness: number;
  communication: number;
  confidence: number;
  completeness: number;
  keyword_coverage: number;
  strengths: string[];
  misconceptions: string[];
  missing_concepts: string[];
  rationale: string;
}

export interface Report {
  overall_score: number;
  dimension_scores: Record<string, number>;
  weak_concepts: string[];
  roadmap: { weeks: { week: number; title: string; topics: string[] }[] };
  hiring_readiness: string;
}
