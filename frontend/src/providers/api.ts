const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, opts?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export const api = {
  uploadResume: (file: File) => {
    const fd = new FormData();
    fd.append("file", file);

    return fetch(`${BASE}/v1/uploads/resume`, {
      method: "POST",
      body: fd,
    }).then((r) => r.json());
  },

  uploadJD: (file: File) => {
    const fd = new FormData();
    fd.append("file", file);

    return fetch(`${BASE}/v1/uploads/job-description`, {
      method: "POST",
      body: fd,
    }).then((r) => r.json());
  },

  createInterview: (body: object) =>
    request("/v1/interviews", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  startInterview: (id: string) =>
    request(`/v1/interviews/${id}/start`, {
      method: "POST",
    }),

  submitAnswer: (id: string, transcript: string) =>
    request(`/v1/interviews/${id}/answer`, {
      method: "POST",
      body: JSON.stringify({ transcript }),
    }),

  endInterview: (id: string) =>
    request(`/v1/interviews/${id}/end`, {
      method: "POST",
    }),

  getReport: (id: string) =>
    request(`/v1/interviews/${id}/report`),
};