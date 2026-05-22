import React, { useState, useEffect, useCallback } from "react";
import {
  runCode,
  runTests,
  getAIFeedback,
  saveAttempt,
  getStats,
  getLeaderboard,
  getQuestions,
  login,
  signup,
  getHistory,
} from "./api";

function App() {
  const [code, setCode] = useState("def solution():\n    pass");
  const [question, setQuestion] = useState(null);
  const [difficulty, setDifficulty] = useState("easy");

  const [output, setOutput] = useState("");
  const [tests, setTests] = useState([]);
  const [score, setScore] = useState(0);
  const [feedback, setFeedback] = useState("");

  const [stats, setStats] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [history, setHistory] = useState([]);

  const [timeLeft, setTimeLeft] = useState(300);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // FIX: token in state so effects re-run when it changes
  const [token, setToken] = useState(localStorage.getItem("token"));

  // =========================
  // LOAD QUESTION
  // =========================
  const loadQuestion = useCallback(async () => {
    try {
      const res = await getQuestions(difficulty);
      // Backend returns a single question object (not array)
      const q = res.data;
      setQuestion(q);
      setCode("def solution():\n    pass");
      setOutput("");
      setTests([]);
      setScore(0);
      setFeedback("");
      setTimeLeft(300);
    } catch (err) {
      console.error("Question load error:", err);
    }
  }, [difficulty]);

  // =========================
  // AUTH
  // =========================
  const handleLogin = async () => {
    try {
      const res = await login({ username, password });
      const accessToken = res.data.access_token;
      localStorage.setItem("token", accessToken);
      // FIX: update state so protected calls unblock immediately
      setToken(accessToken);
      alert("Login successful");
    } catch {
      alert("Login failed");
    }
  };

  const handleSignup = async () => {
    try {
      await signup({ username, password });
      alert("Signup success! Please log in.");
    } catch {
      alert("Signup failed");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setStats(null);
    setHistory([]);
  };

  // =========================
  // ACTIONS
  // =========================
  const handleRun = async () => {
    try {
      const res = await runCode(code);
      setOutput(res.data.output || "");
    } catch {
      setOutput("Error running code");
    }
  };

  const handleTest = async () => {
    if (!question) return;
    try {
      const res = await runTests(code, question.title);
      setTests(res.data.results || []);
      setScore(res.data.score || 0);
    } catch (err) {
      console.error("Test error:", err);
    }
  };

  const handleAI = async () => {
    if (!question) return;
    try {
      const res = await getAIFeedback(code, question.title);
      const d = res.data;
      let feedbackText =
        typeof d === "string"
          ? d
          : d.feedback || d.message || JSON.stringify(d);
      setFeedback(feedbackText);
    } catch {
      setFeedback("AI feedback failed");
    }
  };

  const handleSubmit = async () => {
    if (!token) {
      alert("Please log in first!");
      return;
    }
    try {
      await saveAttempt({ question: question.title, score });
      alert("Submitted!");
      fetchStats();
      fetchLeaderboard();
      fetchHistory();
    } catch {
      alert("Submit failed");
    }
  };

  // =========================
  // DATA FETCHING
  // FIX: no token param — api.js reads localStorage internally
  // =========================
  const fetchStats = useCallback(async () => {
    if (!token) return;
    try {
      const res = await getStats();
      setStats(res.data);
    } catch (err) {
      console.error("Stats error:", err);
    }
  }, [token]);

  const fetchLeaderboard = async () => {
    try {
      const res = await getLeaderboard();
      // FIX: res.data is the array directly (no manual wrapping in api.js)
      let data = res.data;
      if (!Array.isArray(data)) {
        data = Array.isArray(data.leaderboard) ? data.leaderboard : [];
      }
      setLeaderboard(data);
    } catch {
      setLeaderboard([]);
    }
  };

  const fetchHistory = useCallback(async () => {
    if (!token) return;
    try {
      const res = await getHistory();
      setHistory(res.data || []);
    } catch (err) {
      console.error("History error:", err);
    }
  }, [token]);

  // =========================
  // TIMER
  // =========================
  useEffect(() => {
    if (timeLeft <= 0) return;
    const t = setTimeout(() => setTimeLeft((prev) => prev - 1), 1000);
    return () => clearTimeout(t);
  }, [timeLeft]);

  // Load question + leaderboard whenever difficulty changes
  useEffect(() => {
    loadQuestion();
    fetchLeaderboard();
  }, [loadQuestion]);

  // FIX: re-fetch protected data whenever token changes (login/logout)
  useEffect(() => {
    fetchStats();
    fetchHistory();
  }, [fetchStats, fetchHistory]);

  // =========================
  // UI
  // =========================
  return (
    <div style={{ display: "flex", padding: 20, fontFamily: "monospace" }}>
      {/* LEFT PANEL */}
      <div style={{ width: "30%", paddingRight: 20 }}>

        {/* AUTH */}
        {!token ? (
          <>
            <h3>Login / Signup</h3>
            <input
              placeholder="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={{ display: "block", marginBottom: 4 }}
            />
            <input
              type="password"
              placeholder="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ display: "block", marginBottom: 4 }}
            />
            <button onClick={handleLogin}>Login</button>
            <button onClick={handleSignup} style={{ marginLeft: 4 }}>Signup</button>
          </>
        ) : (
          <>
            <p>✅ Logged in</p>
            <button onClick={handleLogout}>Logout</button>
          </>
        )}

        {/* DIFFICULTY */}
        <h3>Difficulty</h3>
        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>

        {/* QUESTION */}
        {question ? (
          <>
            <h2>{question.title}</h2>
            <p>{question.description}</p>
          </>
        ) : (
          <p>Loading question...</p>
        )}

        <h3>⏱ {timeLeft}s</h3>

        {/* STATS */}
        <h3>Stats</h3>
        {stats ? (
          <>
            <p>Attempts: {stats.total_attempts}</p>
            <p>Avg Score: {stats.avg_score}</p>
          </>
        ) : (
          <p>Login to see stats</p>
        )}

        {/* OUTPUT */}
        <h3>Output</h3>
        <pre style={{ background: "#111", color: "#0f0", padding: 8 }}>
          {output || "(no output)"}
        </pre>

        {/* TESTS */}
        <h3>Tests</h3>
        {tests.length === 0 ? (
          <p>No test results yet</p>
        ) : (
          tests.map((t, i) => (
            <p key={i}>
              {t.input ?? "Hidden"} → {t.passed ? "✅ PASS" : "❌ FAIL"}
            </p>
          ))
        )}

        <h3>Score: {score}</h3>

        {/* AI FEEDBACK */}
        <h3>AI Feedback</h3>
        <div style={{ whiteSpace: "pre-wrap", background: "#f5f5f5", padding: 8 }}>
          {feedback || "Click AI to get feedback"}
        </div>

        {/* HISTORY */}
        <h3>History</h3>
        {history.length === 0 ? (
          <p>No history</p>
        ) : (
          history.map((h, i) => (
            <p key={i}>
              {h.question} → {h.score}
            </p>
          ))
        )}

        {/* LEADERBOARD */}
        <h3>🏆 Leaderboard</h3>
        {leaderboard.length === 0 ? (
          <p>No entries yet</p>
        ) : (
          leaderboard.map((u, i) => (
            <p key={i}>
              {i + 1}. {u.username} — {u.score}
            </p>
          ))
        )}
      </div>

      {/* RIGHT PANEL */}
      <div style={{ width: "70%" }}>
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          style={{
            width: "100%",
            height: "400px",
            background: "#0d0d0d",
            color: "#00ff41",
            fontFamily: "monospace",
            fontSize: 14,
            padding: 12,
            border: "1px solid #333",
            boxSizing: "border-box",
          }}
        />

        <div style={{ marginTop: 10, display: "flex", gap: 8 }}>
          <button onClick={handleRun}>▶ Run</button>
          <button onClick={handleTest}>🧪 Test</button>
          <button onClick={handleAI}>🤖 AI</button>
          <button onClick={handleSubmit}>✅ Submit</button>
          <button onClick={loadQuestion}>⏭ Next</button>
        </div>
      </div>
    </div>
  );
}

export default App;