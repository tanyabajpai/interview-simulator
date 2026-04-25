import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// =========================
// AUTH
// =========================
export const signup = (data) =>
  API.post("/user/signup", data);

export const login = (data) =>
  API.post("/user/login", data);

// =========================
// QUESTIONS
// =========================
export const getQuestions = (difficulty) =>
  API.get(`/questions/${difficulty}`, {
    headers: { "Cache-Control": "no-cache" },
  });

// =========================
// CODE
// =========================
export const runCode = (code) =>
  API.post("/code/run", { code });

export const runTests = (code, questionTitle) =>
  API.post("/code/test", {
    code,
    question: questionTitle,
  });

export const getAIFeedback = (code, questionTitle) =>
  API.post("/ai/feedback", {
    code,
    question: questionTitle,
  });

// =========================
// 🔐 PROTECTED ROUTES
// =========================
export const saveAttempt = (data, token) =>
  API.post("/user/save", data, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

export const getStats = (token) =>
  API.get("/user/stats", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

export const getLeaderboard = () =>
  API.get("/leaderboard/leaderboard");

export default API;