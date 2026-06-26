import { useState } from "react";
import { api } from "../../providers/api";

export default function UploadPanel({ onReady }: { onReady: (data: any) => void }) {
  const [resume, setResume] = useState<File | null>(null);
  const [jd, setJd] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!resume || !jd) return;
    setLoading(true);
    const [resumeData, jdData] = await Promise.all([api.uploadResume(resume), api.uploadJD(jd)]);
    setLoading(false);
    onReady({ resumeData, jdData });
  };

  return (
    <div className="flex flex-col gap-4 max-w-lg mx-auto mt-12">
      <h1 className="text-2xl font-bold">Adaptive AI Interviewer</h1>
      <label className="font-semibold">Resume (PDF or DOCX)</label>
      <input type="file" accept=".pdf,.docx" onChange={(e) => setResume(e.target.files?.[0] ?? null)} />
      <label className="font-semibold">Job Description (PDF, DOCX, or text)</label>
      <input type="file" accept=".pdf,.docx,.txt" onChange={(e) => setJd(e.target.files?.[0] ?? null)} />
      <button
        onClick={handleSubmit}
        disabled={!resume || !jd || loading}
        className="bg-blue-600 text-white py-2 rounded disabled:opacity-50"
      >
        {loading ? "Analysing..." : "Analyse & Start Interview"}
      </button>
    </div>
  );
}
