import axios from "axios";

// ==========================
// 🌐 BASE CONFIG
// ==========================
const API = axios.create({
  baseURL: "https://interview-simulator-q3hl.onrender.com",
  headers: {
    "Content-Type": "application/json",
  },
});

// ==========================
// ⚠️ ERROR HANDLER
// ==========================
API.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API ERROR:", error?.response || error.message);

    if (error.response) {
      alert(`Backend Error: ${error.response.status}`);
    } else {
      alert("Server not reachable");
    }

    return Promise.reject(error);
  }
);

// ==========================
// 📡 API CALLS
// ==========================
export const runCode = (code) =>
  API.post("/code/run", { code });

export const runTests = (code, question) =>
  API.post("/code/test", { code, question });

export const submitCode = (code, question, difficulty) =>
  API.post("/evaluate", { code, question, difficulty });

export const getQuestions = (difficulty) =>
  API.get(`/questions/${difficulty}`);

export const getAIFeedback = (code, question) =>
  API.post("/ai/feedback", { code, question });

export default API;