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
  wakeUpBackend,
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

  const [token, setToken] = useState(localStorage.getItem("token"));

  // =========================
  // WAKE-UP STATE
  // Tracks whether backend is cold-starting
  // =========================
  const [backendStatus, setBackendStatus] = useState("idle");
  // "idle" | "waking" | "ready" | "failed"

  // =========================
  // LOAD QUESTION
  // =========================
  const loadQuestion = useCallback(async () => {
    setQuestion(null); // show loading state while fetching
    try {
      const res = await getQuestions(difficulty);
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
      setQuestion({ title: "Failed to load", description: "Could not reach the server. Try clicking Next or refreshing." });
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
      const feedbackText =
        typeof d === "string" ? d : d.feedback || d.message || JSON.stringify(d);
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

  // =========================
  // BOOT SEQUENCE
  // On first load: wake backend → then load question + leaderboard
  // This replaces the old useEffect that called loadQuestion directly,
  // which raced against a cold-starting backend and got nothing.
  // =========================
  useEffect(() => {
    const boot = async () => {
      setBackendStatus("waking");
      const isUp = await wakeUpBackend();
      if (!isUp) {
        setBackendStatus("failed");
        setQuestion({
          title: "Server unavailable",
          description: "The backend could not be reached. Please try again in a minute.",
        });
        return;
      }
      setBackendStatus("ready");
      await loadQuestion();
      fetchLeaderboard();
    };
    boot();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // runs ONCE on mount

  // Re-load question when difficulty changes (backend already awake by then)
  useEffect(() => {
    // Skip the very first render — boot() handles it
    if (backendStatus !== "ready") return;
    loadQuestion();
    fetchLeaderboard();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [difficulty]);

  // Re-fetch protected data on login/logout
  useEffect(() => {
    fetchStats();
    fetchHistory();
  }, [fetchStats, fetchHistory]);

  // =========================
  // WAKE-UP BANNER
  // =========================
  const WakingBanner = () => {
    if (backendStatus === "waking") {
      return (
        <div style={{
          background: "#fff3cd",
          border: "1px solid #ffc107",
          borderRadius: 6,
          padding: "10px 14px",
          marginBottom: 12,
          fontSize: 13,
        }}>
          ⏳ <strong>Server is waking up</strong> — this takes ~30 seconds on first load.
          <br />
          <span style={{ color: "#666" }}>Render free tier sleeps after inactivity.</span>
        </div>
      );
    }
    if (backendStatus === "failed") {
      return (
        <div style={{
          background: "#f8d7da",
          border: "1px solid #f5c6cb",
          borderRadius: 6,
          padding: "10px 14px",
          marginBottom: 12,
          fontSize: 13,
        }}>
          ❌ <strong>Could not reach server.</strong>{" "}
          <button onClick={() => window.location.reload()} style={{ marginLeft: 8 }}>
            Retry
          </button>
        </div>
      );
    }
    return null;
  };

  // =========================
  // UI
  // =========================
  return (
    <div style={{ display: "flex", padding: 20, fontFamily: "monospace" }}>
      {/* LEFT PANEL */}
      <div style={{ width: "30%", paddingRight: 20 }}>

        <WakingBanner />

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
          disabled={backendStatus === "waking"}
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>

        {/* QUESTION */}
        {backendStatus === "waking" ? (
          <p style={{ color: "#888", fontStyle: "italic" }}>⏳ Waiting for server...</p>
        ) : question ? (
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
          <button onClick={handleRun} disabled={backendStatus === "waking"}>▶ Run</button>
          <button onClick={handleTest} disabled={backendStatus === "waking"}>🧪 Test</button>
          <button onClick={handleAI} disabled={backendStatus === "waking"}>🤖 AI</button>
          <button onClick={handleSubmit} disabled={backendStatus === "waking"}>✅ Submit</button>
          <button onClick={loadQuestion} disabled={backendStatus === "waking"}>⏭ Next</button>
        </div>
      </div>
    </div>
  );
}

export default App;