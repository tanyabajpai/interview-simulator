import axios from "axios";

const BASE_URL = "https://interview-simulator-backend-6ne6.onrender.com";

const API = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// =========================
// AUTO TOKEN HANDLER
// =========================
const getAuthHeader = () => {
  const token = localStorage.getItem("token");
  if (!token) return {};
  return { Authorization: `Bearer ${token}` };
};

// =========================
// WAKE-UP + RETRY UTILITY
// Render free tier sleeps after 15 min inactivity.
// This pings /health first, then retries failed requests.
// =========================
export const wakeUpBackend = async () => {
  const MAX_WAIT_MS = 60000; // wait up to 60s for backend to wake
  const PING_INTERVAL = 3000;
  const start = Date.now();

  while (Date.now() - start < MAX_WAIT_MS) {
    try {
      await axios.get(`${BASE_URL}/health`, { timeout: 5000 });
      return true; // backend is up
    } catch {
      await new Promise((r) => setTimeout(r, PING_INTERVAL));
    }
  }
  return false; // gave up
};

// Wraps any API call with automatic retry on network/5xx errors
export const withRetry = async (apiFn, retries = 4, delayMs = 4000) => {
  for (let i = 0; i < retries; i++) {
    try {
      return await apiFn();
    } catch (err) {
      const isLastAttempt = i === retries - 1;
      const status = err?.response?.status;
      // Don't retry on auth errors (401/403) or bad requests (400)
      if (status === 401 || status === 403 || status === 400) throw err;
      if (isLastAttempt) throw err;
      console.log(`Retry ${i + 1}/${retries} in ${delayMs}ms...`);
      await new Promise((r) => setTimeout(r, delayMs));
    }
  }
};

// =========================
// AUTH
// =========================
export const signup = (data) => API.post("/user/signup", data);

export const login = (data) => API.post("/user/login", data);

// =========================
// QUESTIONS
// =========================
export const getQuestions = (difficulty) =>
  withRetry(() => API.get(`/questions/${difficulty}`));

// =========================
// CODE
// =========================
export const runCode = (code) => API.post("/code/run", { code });

export const runTests = (code, questionTitle) =>
  API.post("/code/test", { code, question: questionTitle });

export const getAIFeedback = (code, questionTitle) =>
  API.post("/ai/feedback", { code, question: questionTitle });

// =========================
// PROTECTED ROUTES
// =========================
export const saveAttempt = (data) =>
  API.post("/user/save", data, { headers: getAuthHeader() });

export const getStats = () =>
  API.get("/user/stats", { headers: getAuthHeader() });

export const getHistory = () =>
  API.get("/attempts/history", { headers: getAuthHeader() });

// =========================
// LEADERBOARD
// =========================
export const getLeaderboard = () => API.get("/leaderboard/leaderboard");

export default API;