import { useState, useRef } from "react";
import { useInterviewStore } from "../../store/interviewStore";
import { api } from "../../providers/api";

export default function InterviewScreen({ interviewId, onComplete }: { interviewId: string; onComplete: () => void }) {
  const { interview, setNextQuestion, addEvaluation } = useInterviewStore();
  const [transcript, setTranscript] = useState("");
  const [loading, setLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const mediaRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mr = new MediaRecorder(stream, { mimeType: "audio/webm" });
    chunksRef.current = [];
    mr.ondataavailable = (e) => chunksRef.current.push(e.data);
    mr.onstop = () => {
      // Stage B: send audio via WebSocket for transcription
      // For Stage A just use the text textarea below
    };
    mr.start();
    mediaRef.current = mr;
    setIsRecording(true);
  };

  const stopRecording = () => {
    mediaRef.current?.stop();
    setIsRecording(false);
  };

  const submitAnswer = async () => {
    if (!transcript.trim()) return;
    setLoading(true);
    const result: any = await api.submitAnswer(interviewId, transcript);
    addEvaluation(result.evaluation);
    setNextQuestion(result.next_question);
    setTranscript("");
    setLoading(false);
  };

  const endInterview = async () => {
    await api.endInterview(interviewId);
    onComplete();
  };

  const q = interview?.currentQuestion;

  return (
    <div className="max-w-2xl mx-auto mt-8 flex flex-col gap-6">
      <div className="bg-gray-50 rounded p-4">
        <p className="text-xs text-gray-400 uppercase">{q?.topic} · difficulty {q?.difficulty}/5</p>
        <p className="text-xl font-semibold mt-1">{q?.question ?? "Loading question..."}</p>
      </div>

      <textarea
        className="border rounded p-3 h-32 resize-none"
        placeholder="Type your answer here (or use the mic button below)..."
        value={transcript}
        onChange={(e) => setTranscript(e.target.value)}
      />

      <div className="flex gap-3">
        <button
          onClick={isRecording ? stopRecording : startRecording}
          className={}
        >
          {isRecording ? "Stop Recording" : "🎤 Record"}
        </button>
        <button
          onClick={submitAnswer}
          disabled={loading || !transcript.trim()}
          className="bg-blue-600 text-white px-6 py-2 rounded disabled:opacity-50 flex-1"
        >
          {loading ? "Evaluating..." : "Submit Answer"}
        </button>
        <button onClick={endInterview} className="text-red-500 px-4 py-2">End</button>
      </div>

      {interview?.answerEvaluations.length ? (
        <div className="bg-green-50 rounded p-4 text-sm">
          <p className="font-semibold mb-1">Last evaluation</p>
          {Object.entries(interview.answerEvaluations.at(-1) ?? {})
            .filter(([k]) => typeof interview.answerEvaluations.at(-1)?.[k as keyof any] === "number")
            .map(([k, v]) => (
              <div key={k} className="flex justify-between"><span>{k}</span><span>{v}/10</span></div>
            ))}
        </div>
      ) : null}
    </div>
  );
}
