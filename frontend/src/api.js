import axios from "axios";

const API = axios.create({
  baseURL: "https://interview-simulator-backend-6ne6.onrender.com",
  
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
// AUTH
// =========================
export const signup = (data) =>
  API.post("/user/signup", data);

export const login = (data) =>
  API.post("/user/login", data);

// =========================
// QUESTIONS
// =========================
// Returns axios response: res.data = single question object
export const getQuestions = (difficulty) =>
  API.get(`/questions/${difficulty}`);

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
// PROTECTED ROUTES
// All use getAuthHeader() internally — no token param needed
// =========================
export const saveAttempt = (data) =>
  API.post("/user/save", data, {
    headers: getAuthHeader(),
  });

export const getStats = () =>
  API.get("/user/stats", {
    headers: getAuthHeader(),
  });

export const getHistory = () =>
  API.get("/attempts/history", {
    headers: getAuthHeader(),
  });

// =========================
// LEADERBOARD
// Returns standard axios response — no manual wrapping
// =========================
export const getLeaderboard = () =>
  API.get("/leaderboard/leaderboard");

export default API;