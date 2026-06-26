from enum import Enum

class InterviewState(str, Enum):
    PREPARED = "PREPARED"
    LOBBY_READY = "LOBBY_READY"
    ASKING = "ASKING"
    LISTENING = "LISTENING"
    TRANSCRIBING = "TRANSCRIBING"
    EVALUATING = "EVALUATING"
    FOLLOWUP_DECISION = "FOLLOWUP_DECISION"
    SPEAKING_NEXT_QUESTION = "SPEAKING_NEXT_QUESTION"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

TRANSITIONS = {
    InterviewState.PREPARED: [InterviewState.LOBBY_READY],
    InterviewState.LOBBY_READY: [InterviewState.ASKING],
    InterviewState.ASKING: [InterviewState.LISTENING],
    InterviewState.LISTENING: [InterviewState.TRANSCRIBING],
    InterviewState.TRANSCRIBING: [InterviewState.EVALUATING],
    InterviewState.EVALUATING: [InterviewState.FOLLOWUP_DECISION],
    InterviewState.FOLLOWUP_DECISION: [InterviewState.SPEAKING_NEXT_QUESTION, InterviewState.COMPLETED],
    InterviewState.SPEAKING_NEXT_QUESTION: [InterviewState.ASKING],
}

def transition(current: InterviewState, next_state: InterviewState) -> InterviewState:
    allowed = TRANSITIONS.get(current, [])
    if next_state not in allowed:
        raise ValueError(f"Invalid transition {current} -> {next_state}")
    return next_state
