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

// =========================
// TIMER LIMITS PER DIFFICULTY
// =========================
const TIMER_LIMITS = {
  easy: 5 * 60,    // 5 minutes
  medium: 10 * 60, // 10 minutes
  hard: 15 * 60,   // 15 minutes
};

// Format seconds → "MM:SS"
const formatTime = (seconds) => {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
};

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

  const [timeLeft, setTimeLeft] = useState(TIMER_LIMITS["easy"]);
  const [timedOut, setTimedOut] = useState(false);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [authError, setAuthError] = useState("");

  const [token, setToken] = useState(localStorage.getItem("token"));

  // "login" | "main"
  const [screen, setScreen] = useState(
    localStorage.getItem("token") ? "main" : "login"
  );

  const [backendStatus, setBackendStatus] = useState("idle");

  // =========================
  // LOAD QUESTION
  // =========================
  const loadQuestion = useCallback(async () => {
    setQuestion(null);
    setTimedOut(false);
    setTimeLeft(TIMER_LIMITS[difficulty]);
    try {
      const res = await getQuestions(difficulty);
      const q = res.data;
      setQuestion(q);
      setCode("def solution():\n    pass");
      setOutput("");
      setTests([]);
      setScore(0);
      setFeedback("");
    } catch (err) {
      console.error("Question load error:", err);
      setQuestion({
        title: "Failed to load",
        description: "Could not reach the server. Try clicking Next or refreshing.",
      });
    }
  }, [difficulty]);

  // =========================
  // AUTH
  // =========================
  const handleLogin = async () => {
    setAuthError("");
    try {
      const res = await login({ username, password });
      const accessToken = res.data.access_token;
      localStorage.setItem("token", accessToken);
      setToken(accessToken);
      setScreen("main");
    } catch {
      setAuthError("Invalid username or password.");
    }
  };

  const handleSignup = async () => {
    setAuthError("");
    if (!username || !password) {
      setAuthError("Username and password are required.");
      return;
    }
    try {
      await signup({ username, password });
      const res = await login({ username, password });
      const accessToken = res.data.access_token;
      localStorage.setItem("token", accessToken);
      setToken(accessToken);
      setScreen("main");
    } catch {
      setAuthError("Signup failed. Username may already exist.");
    }
  };

  const handleSkip = () => {
    setScreen("main");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setStats(null);
    setHistory([]);
    setScreen("login");
    setUsername("");
    setPassword("");
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
      alert("Please log in to submit!");
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
  // Counts down; locks editor at 00:00
  // =========================
  useEffect(() => {
    if (timedOut) return;
    if (timeLeft <= 0) {
      setTimedOut(true);
      return;
    }
    const t = setTimeout(() => setTimeLeft((prev) => prev - 1), 1000);
    return () => clearTimeout(t);
  }, [timeLeft, timedOut]);

  // Reset timer when difficulty changes
  useEffect(() => {
    setTimeLeft(TIMER_LIMITS[difficulty]);
    setTimedOut(false);
  }, [difficulty]);

  // =========================
  // BOOT SEQUENCE — runs when main screen appears
  // =========================
  useEffect(() => {
    if (screen !== "main") return;
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
  }, [screen]);

  // Re-load question when difficulty changes (backend already awake)
  useEffect(() => {
    if (backendStatus !== "ready") return;
    loadQuestion();
    fetchLeaderboard();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [difficulty]);

  useEffect(() => {
    fetchStats();
    fetchHistory();
  }, [fetchStats, fetchHistory]);

  // =========================
  // TIMER COLOR
  // =========================
  const timerColor = timedOut
    ? "#dc3545"
    : timeLeft < 60
    ? "#dc3545"
    : timeLeft < 120
    ? "#fd7e14"
    : "#28a745";

  const actionsDisabled = backendStatus === "waking" || timedOut;

  // =========================
  // LOGIN SCREEN
  // =========================
  if (screen === "login") {
    return (
      <div style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "#0d0d0d",
        fontFamily: "monospace",
      }}>
        <div style={{
          background: "#1a1a1a",
          border: "1px solid #333",
          borderRadius: 10,
          padding: "40px 48px",
          width: 360,
          boxShadow: "0 4px 24px rgba(0,0,0,0.5)",
        }}>
          <h1 style={{ color: "#00ff41", marginTop: 0, marginBottom: 4, fontSize: 22 }}>
            🧑‍💻 Interview Simulator
          </h1>
          <p style={{ color: "#666", fontSize: 13, marginBottom: 28 }}>
            Practice DSA with AI feedback
          </p>

          <input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleLogin()}
            style={{
              display: "block", width: "100%", marginBottom: 10,
              padding: "9px 12px", background: "#0d0d0d", color: "#fff",
              border: "1px solid #444", borderRadius: 5, fontFamily: "monospace",
              fontSize: 14, boxSizing: "border-box",
            }}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleLogin()}
            style={{
              display: "block", width: "100%", marginBottom: 14,
              padding: "9px 12px", background: "#0d0d0d", color: "#fff",
              border: "1px solid #444", borderRadius: 5, fontFamily: "monospace",
              fontSize: 14, boxSizing: "border-box",
            }}
          />

          {authError && (
            <p style={{ color: "#ff4d4d", fontSize: 13, marginBottom: 10, marginTop: -6 }}>
              {authError}
            </p>
          )}

          <div style={{ display: "flex", gap: 8, marginBottom: 14 }}>
            <button
              onClick={handleLogin}
              style={{
                flex: 1, padding: "9px 0", background: "#00ff41", color: "#000",
                border: "none", borderRadius: 5, fontFamily: "monospace",
                fontSize: 14, fontWeight: "bold", cursor: "pointer",
              }}
            >
              Login
            </button>
            <button
              onClick={handleSignup}
              style={{
                flex: 1, padding: "9px 0", background: "#1a1a1a", color: "#00ff41",
                border: "1px solid #00ff41", borderRadius: 5, fontFamily: "monospace",
                fontSize: 14, cursor: "pointer",
              }}
            >
              Sign Up
            </button>
          </div>

          <button
            onClick={handleSkip}
            style={{
              width: "100%", padding: "8px 0", background: "transparent",
              color: "#666", border: "1px solid #333", borderRadius: 5,
              fontFamily: "monospace", fontSize: 13, cursor: "pointer",
            }}
          >
            Skip — continue as guest
          </button>
        </div>
      </div>
    );
  }

  // =========================
  // MAIN SCREEN
  // =========================
  return (
    <div style={{ display: "flex", padding: 20, fontFamily: "monospace" }}>
      {/* LEFT PANEL */}
      <div style={{ width: "30%", paddingRight: 20 }}>

        {backendStatus === "waking" && (
          <div style={{
            background: "#fff3cd", border: "1px solid #ffc107",
            borderRadius: 6, padding: "10px 14px", marginBottom: 12, fontSize: 13,
          }}>
            ⏳ <strong>Server is waking up</strong> — ~30 seconds on first load.
            <br /><span style={{ color: "#666" }}>Render free tier sleeps after inactivity.</span>
          </div>
        )}
        {backendStatus === "failed" && (
          <div style={{
            background: "#f8d7da", border: "1px solid #f5c6cb",
            borderRadius: 6, padding: "10px 14px", marginBottom: 12, fontSize: 13,
          }}>
            ❌ <strong>Could not reach server.</strong>{" "}
            <button onClick={() => window.location.reload()} style={{ marginLeft: 8 }}>Retry</button>
          </div>
        )}

        {token ? (
          <div style={{ marginBottom: 12 }}>
            <span style={{ color: "#28a745", fontSize: 13 }}>✅ Logged in</span>
            {"  "}
            <button
              onClick={handleLogout}
              style={{
                fontSize: 12, padding: "2px 8px", cursor: "pointer",
                background: "transparent", border: "1px solid #ccc", borderRadius: 4,
              }}
            >
              Logout
            </button>
          </div>
        ) : (
          <div style={{ marginBottom: 12 }}>
            <span style={{ color: "#888", fontSize: 13 }}>👤 Guest — </span>
            <button
              onClick={() => setScreen("login")}
              style={{
                fontSize: 12, padding: "2px 8px", cursor: "pointer",
                background: "transparent", border: "1px solid #00ff41",
                borderRadius: 4, color: "#00ff41",
              }}
            >
              Log in
            </button>
          </div>
        )}

        <h3 style={{ marginBottom: 6 }}>Difficulty</h3>
        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          disabled={backendStatus === "waking"}
          style={{ marginBottom: 12 }}
        >
          <option value="easy">Easy (5 min)</option>
          <option value="medium">Medium (10 min)</option>
          <option value="hard">Hard (15 min)</option>
        </select>

        {backendStatus === "waking" ? (
          <p style={{ color: "#888", fontStyle: "italic" }}>⏳ Waiting for server...</p>
        ) : question ? (
          <>
            <h2 style={{ marginBottom: 4 }}>{question.title}</h2>
            <p style={{ marginTop: 0 }}>{question.description}</p>
          </>
        ) : (
          <p>Loading question...</p>
        )}

        {/* TIMER */}
        <h3 style={{ color: timerColor, fontSize: 20, marginBottom: 4 }}>
          ⏱ {formatTime(timeLeft)}
        </h3>
        {timedOut && (
          <p style={{
            color: "#dc3545", fontWeight: "bold", fontSize: 13,
            background: "#fff0f0", border: "1px solid #f5c6cb",
            borderRadius: 4, padding: "6px 10px", marginBottom: 8,
          }}>
            ⛔ Time's up! Click Next for a new question.
          </p>
        )}

        <h3>Stats</h3>
        {stats ? (
          <>
            <p>Attempts: {stats.total_attempts}</p>
            <p>Avg Score: {stats.avg_score}</p>
          </>
        ) : (
          <p style={{ color: "#888", fontSize: 13 }}>Login to see stats</p>
        )}

        <h3>Output</h3>
        <pre style={{ background: "#111", color: "#0f0", padding: 8 }}>
          {output || "(no output)"}
        </pre>

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

        <h3>AI Feedback</h3>
        <div style={{ whiteSpace: "pre-wrap", background: "#f5f5f5", padding: 8 }}>
          {feedback || "Click AI to get feedback"}
        </div>

        <h3>History</h3>
        {history.length === 0 ? (
          <p>No history</p>
        ) : (
          history.map((h, i) => (
            <p key={i}>{h.question} → {h.score}</p>
          ))
        )}

        <h3>🏆 Leaderboard</h3>
        {leaderboard.length === 0 ? (
          <p>No entries yet</p>
        ) : (
          leaderboard.map((u, i) => (
            <p key={i}>{i + 1}. {u.username} — {u.score}</p>
          ))
        )}
      </div>

      {/* RIGHT PANEL */}
      <div style={{ width: "70%", position: "relative" }}>
        <textarea
          value={code}
          onChange={(e) => !timedOut && setCode(e.target.value)}
          readOnly={timedOut}
          style={{
            width: "100%",
            height: "400px",
            background: timedOut ? "#1a0000" : "#0d0d0d",
            color: timedOut ? "#ff4d4d" : "#00ff41",
            fontFamily: "monospace",
            fontSize: 14,
            padding: 12,
            border: timedOut ? "1px solid #dc3545" : "1px solid #333",
            boxSizing: "border-box",
            cursor: timedOut ? "not-allowed" : "text",
            opacity: timedOut ? 0.7 : 1,
          }}
        />

        {timedOut && (
          <div style={{
            position: "absolute", top: 8, right: 12,
            background: "#dc3545", color: "#fff",
            padding: "3px 10px", borderRadius: 4, fontSize: 12, fontWeight: "bold",
          }}>
            TIME'S UP
          </div>
        )}

        <div style={{ marginTop: 10, display: "flex", gap: 8 }}>
          <button onClick={handleRun} disabled={actionsDisabled}>▶ Run</button>
          <button onClick={handleTest} disabled={actionsDisabled}>🧪 Test</button>
          <button onClick={handleAI} disabled={actionsDisabled}>🤖 AI</button>
          <button onClick={handleSubmit} disabled={actionsDisabled}>✅ Submit</button>
          <button
            onClick={loadQuestion}
            disabled={backendStatus === "waking"}
            style={timedOut ? { background: "#00ff41", color: "#000", fontWeight: "bold" } : {}}
          >
            ⏭ Next
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;