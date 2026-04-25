import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// =========================
// 🔐 AUTO TOKEN HANDLER
// =========================
const getAuthHeader = () => {
  const token = localStorage.getItem("token");

  if (!token) {
    console.log("❌ No token found");
    return {};
  }

  return {
    Authorization: `Bearer ${token}`,
  };
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
// 🔐 PROTECTED ROUTES (SAFE)
// =========================
export const saveAttempt = async (data) => {
  return API.post("/user/save", data, {
    headers: getAuthHeader(),
  });
};

export const getStats = async () => {
  return API.get("/user/stats", {
    headers: getAuthHeader(),
  });
};

export const getHistory = async () => {
  return API.get("/attempts/history", {
    headers: getAuthHeader(),
  });
};

// =========================
// 🏆 LEADERBOARD (SAFE FIX)
// =========================
export const getLeaderboard = async () => {
  const res = await API.get("/leaderboard/leaderboard");

  // 🔥 normalize response
  if (Array.isArray(res.data)) return { data: res.data };
  if (Array.isArray(res.data.leaderboard)) return { data: res.data.leaderboard };

  return { data: [] };
};

export default API;