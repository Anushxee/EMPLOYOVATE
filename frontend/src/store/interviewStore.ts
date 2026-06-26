import { create } from "zustand";
import { Interview, Question, Evaluation } from "../types";

interface InterviewStore {
  interview: Interview | null;
  transcript: string;
  isRecording: boolean;
  setInterview: (i: Interview) => void;
  setTranscript: (t: string) => void;
  setRecording: (r: boolean) => void;
  addEvaluation: (e: Evaluation) => void;
  setNextQuestion: (q: Question) => void;
  reset: () => void;
}

export const useInterviewStore = create<InterviewStore>((set) => ({
  interview: null,
  transcript: "",
  isRecording: false,
  setInterview: (interview) => set({ interview }),
  setTranscript: (transcript) => set({ transcript }),
  setRecording: (isRecording) => set({ isRecording }),
  addEvaluation: (e) =>
    set((s) => ({
      interview: s.interview
        ? { ...s.interview, answerEvaluations: [...s.interview.answerEvaluations, e] }
        : null,
    })),
  setNextQuestion: (q) =>
    set((s) => ({
      interview: s.interview ? { ...s.interview, currentQuestion: q } : null,
    })),
  reset: () => set({ interview: null, transcript: "", isRecording: false }),
}));
