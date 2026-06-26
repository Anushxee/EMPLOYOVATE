import { useState } from "react";
import UploadPanel from "../components/upload/UploadPanel";
import InterviewScreen from "../components/interview/InterviewScreen";
import ReportViewer from "../components/report/ReportViewer";
import { useInterviewStore } from "../store/interviewStore";
import { api } from "../providers/api";

type Page = "upload" | "interview" | "report";

export default function App() {
  const [page, setPage] = useState<Page>("upload");
  const [interviewId, setInterviewId] = useState("");
  const { setInterview } = useInterviewStore();

  const handleReady = async (data: any) => {
    const res: any = await api.createInterview({
      blueprint: { skills: data.jdData?.skills, remaining_topics: [] },
      role_profile: data.jdData,
    });
    const startRes: any = await api.startInterview(res.interview_id);
    setInterview({
      id: res.interview_id,
      state: "ASKING",
      currentQuestion: startRes.question,
      questionHistory: [startRes.question],
      answerEvaluations: [],
    });
    setInterviewId(res.interview_id);
    setPage("interview");
  };

  return (
    <div className="min-h-screen bg-white p-4">
      {page === "upload" && <UploadPanel onReady={handleReady} />}
      {page === "interview" && (
        <InterviewScreen
          interviewId={interviewId}
          onComplete={() => setPage("report")}
        />
      )}
      {page === "report" && <ReportViewer interviewId={interviewId} />}
    </div>
  );
}
