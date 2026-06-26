from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.services.interview_orchestrator.state_machine import InterviewState, transition
from backend.services.interview_orchestrator.concept_graph import ConceptGraph
from backend.services.interview_orchestrator.next_question_policy import NextQuestionPolicy
from backend.services.evaluation.evaluator import AnswerEvaluator
from backend.services.reporting.report_generator import ReportGenerator
from backend.providers.llm.gemini import GeminiAdapter
from backend.providers.stt.whisper_local import LocalWhisperAdapter
import uuid, json

router = APIRouter(prefix="/v1/interviews", tags=["interviews"])

# In-memory session store for MVP (replace with Supabase/Redis in production)
SESSIONS: dict = {}

@router.post("/")
async def create_interview(body: dict):
    interview_id = str(uuid.uuid4())
    SESSIONS[interview_id] = {
        "id": interview_id,
        "state": InterviewState.PREPARED,
        "concept_graph": ConceptGraph(),
        "question_history": [],
        "answer_evaluations": [],
        "blueprint": body.get("blueprint", {}),
        "role_profile": body.get("role_profile", {}),
        "time_remaining": body.get("duration_seconds", 2400),
    }
    return {"interview_id": interview_id}

@router.post("/{interview_id}/start")
async def start_interview(interview_id: str):
    session = SESSIONS[interview_id]
    session["state"] = transition(session["state"], InterviewState.LOBBY_READY)
    session["state"] = transition(session["state"], InterviewState.ASKING)
    llm = GeminiAdapter()
    questions = await llm.generate_questions(session["blueprint"])
    first_q = questions[0] if questions else {"question": "Tell me about yourself.", "topic": "intro", "difficulty": 1}
    session["current_question"] = first_q
    session["question_history"].append(first_q)
    return {"question": first_q}

@router.post("/{interview_id}/answer")
async def submit_answer(interview_id: str, body: dict):
    """Stage A: candidate submits text transcript directly."""
    session = SESSIONS[interview_id]
    transcript = body.get("transcript", "")
    current_q = session["current_question"]

    llm = GeminiAdapter()
    evaluator = AnswerEvaluator(llm)
    evaluation = await evaluator.evaluate(current_q, transcript, session["role_profile"])
    session["answer_evaluations"].append(evaluation)

    # Update concept graph
    cg = session["concept_graph"]
    concept = current_q.get("topic", "general")
    cg.add(concept)
    cg.update(concept, evaluation.get("correctness", 0))

    # Decide next question
    policy = NextQuestionPolicy(llm)
    next_q = await policy.decide(current_q, evaluation, cg, session["blueprint"], session["time_remaining"])
    session["current_question"] = next_q
    session["question_history"].append(next_q)

    return {"evaluation": evaluation, "next_question": next_q}

@router.post("/{interview_id}/end")
async def end_interview(interview_id: str):
    session = SESSIONS[interview_id]
    session["state"] = InterviewState.COMPLETED
    session["concept_graph_snapshot"] = session["concept_graph"].to_dict()
    return {"status": "completed"}

@router.get("/{interview_id}/report")
async def get_report(interview_id: str):
    session = SESSIONS[interview_id]
    session_data = {
        "answer_evaluations": session["answer_evaluations"],
        "concept_graph": session.get("concept_graph_snapshot", session["concept_graph"].to_dict()),
        "role_profile": session["role_profile"],
    }
    llm = GeminiAdapter()
    reporter = ReportGenerator(llm)
    report = await reporter.generate(session_data)
    return report

@router.websocket("/{interview_id}/ws")
async def interview_websocket(websocket: WebSocket, interview_id: str):
    """Stage B: real-time audio channel (voice upload per answer)."""
    await websocket.accept()
    stt = LocalWhisperAdapter()
    try:
        while True:
            data = await websocket.receive_bytes()
            result = await stt.transcribe_file(data, "audio/webm")
            await websocket.send_json({"type": "transcript.final", "text": result["text"]})
    except WebSocketDisconnect:
        pass
