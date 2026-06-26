import { useEffect, useState } from "react";
import { api } from "../../providers/api";
import { Report } from "../../types";

export default function ReportViewer({ interviewId }: { interviewId: string }) {
  const [report, setReport] = useState<Report | null>(null);

  useEffect(() => {
    api.getReport(interviewId).then((r: any) => setReport(r));
  }, [interviewId]);

  if (!report) return <p className="text-center mt-12">Generating your report...</p>;

  return (
    <div className="max-w-2xl mx-auto mt-8 flex flex-col gap-6">
      <h2 className="text-2xl font-bold">Interview Report</h2>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-blue-50 rounded p-4 text-center">
          <p className="text-4xl font-bold">{report.overall_score}</p>
          <p className="text-sm text-gray-500">Overall Score</p>
        </div>
        <div className="bg-purple-50 rounded p-4 text-center">
          <p className="text-lg font-semibold capitalize">{report.hiring_readiness.replace(/_/g, " ")}</p>
          <p className="text-sm text-gray-500">Hiring Readiness</p>
        </div>
      </div>
      <div>
        <h3 className="font-semibold mb-2">Dimension Scores</h3>
        {Object.entries(report.dimension_scores).map(([k, v]) => (
          <div key={k} className="flex items-center gap-3 mb-1">
            <span className="w-40 text-sm capitalize">{k.replace(/_/g, " ")}</span>
            <div className="flex-1 bg-gray-200 rounded h-2">
              <div className="bg-blue-500 h-2 rounded" style={{ width:  }} />
            </div>
            <span className="text-sm w-8">{v}</span>
          </div>
        ))}
      </div>
      {report.weak_concepts.length > 0 && (
        <div>
          <h3 className="font-semibold mb-2">Weak Concepts</h3>
          <div className="flex flex-wrap gap-2">
            {report.weak_concepts.map((c) => (
              <span key={c} className="bg-red-100 text-red-700 px-2 py-1 rounded text-sm">{c}</span>
            ))}
          </div>
        </div>
      )}
      <div>
        <h3 className="font-semibold mb-2">Study Roadmap</h3>
        {report.roadmap?.weeks?.map((w) => (
          <div key={w.week} className="border rounded p-3 mb-2">
            <p className="font-medium">Week {w.week}: {w.title}</p>
            <ul className="list-disc list-inside text-sm text-gray-600 mt-1">
              {w.topics.map((t) => <li key={t}>{t}</li>)}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
