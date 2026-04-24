import axios from "axios";

// ⚠️ FORCE LOCAL BACKEND (VERY IMPORTANT)
const API = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// =========================
// QUESTIONS (FIXED)
// =========================
export const getQuestions = (difficulty) => {
  return API.get(`/questions/${difficulty}`, {
    headers: {
      "Cache-Control": "no-cache",   // 🔥 prevent caching
    },
  });
};

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

export const submitCode = (code, questionTitle, difficulty) =>
  API.post("/evaluate", {
    code,
    question: questionTitle,
    difficulty,
  });

export const getAIFeedback = (code, questionTitle) =>
  API.post("/ai/feedback", {
    code,
    question: questionTitle,
  });

export default API;