import React, { useState, useEffect } from "react";
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

  const token = localStorage.getItem("token");

  // =========================
  // LOAD QUESTION
  // =========================
  const loadQuestion = async () => {
    try {
      const res = await getQuestions(difficulty);
      let q = res.data;

      if (Array.isArray(q)) {
        q = q[Math.floor(Math.random() * q.length)];
      }

      setQuestion(q);
      setCode("def solution():\n    pass");
      setOutput("");
      setTests([]);
      setScore(0);
      setFeedback("");
      setTimeLeft(300);
    } catch {
      console.log("Question error");
    }
  };

  // =========================
  // AUTH
  // =========================
  const handleLogin = async () => {
    try {
      const res = await login({ username, password });

      localStorage.setItem("token", res.data.access_token);

      alert("Login successful");

      fetchStats();
      fetchLeaderboard();
      fetchHistory();
    } catch {
      alert("Login failed");
    }
  };

  const handleSignup = async () => {
    try {
      await signup({ username, password });
      alert("Signup success!");
    } catch {
      alert("Signup failed");
    }
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
    } catch {
      console.log("Test error");
    }
  };

  const handleAI = async () => {
    if (!question) return;

    try {
      const res = await getAIFeedback(code, question.title);

      let feedbackText = "";

      if (typeof res.data === "string") {
        feedbackText = res.data;
      } else if (res.data.feedback) {
        feedbackText = res.data.feedback;
      } else if (res.data.message) {
        feedbackText = res.data.message;
      } else {
        feedbackText = JSON.stringify(res.data);
      }

      setFeedback(feedbackText);
    } catch {
      setFeedback("❌ AI failed");
    }
  };

  const handleSubmit = async () => {
    if (!token) {
      alert("Login first!");
      return;
    }

    try {
      await saveAttempt(
        {
          question: question.title,
          score,
        },
        token
      );

      alert("Submitted");

      fetchStats();
      fetchLeaderboard();
      fetchHistory();
    } catch {
      alert("Submit failed");
    }
  };

  // =========================
  // DATA
  // =========================
  const fetchStats = async () => {
    if (!token) return;

    try {
      const res = await getStats(token);
      setStats(res.data);
    } catch {}
  };

  const fetchLeaderboard = async () => {
    try {
      const res = await getLeaderboard();

      let data = res.data;
      if (!Array.isArray(data)) {
        if (Array.isArray(data.leaderboard)) data = data.leaderboard;
        else data = [];
      }

      setLeaderboard(data);
    } catch {
      setLeaderboard([]);
    }
  };

  const fetchHistory = async () => {
    if (!token) return;

    try {
      const res = await getHistory(token);
      setHistory(res.data || []);
    } catch {}
  };

  // =========================
  // TIMER
  // =========================
  useEffect(() => {
    if (timeLeft <= 0) return;

    const t = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
    return () => clearTimeout(t);
  }, [timeLeft]);

  useEffect(() => {
    loadQuestion();
    fetchLeaderboard();
    fetchStats();
    fetchHistory();
  }, [difficulty]);

  // =========================
  // UI
  // =========================
  return (
    <div style={{ display: "flex", padding: 20 }}>
      {/* LEFT PANEL */}
      <div style={{ width: "30%" }}>
        <h3>Login</h3>
        <input placeholder="username" onChange={(e) => setUsername(e.target.value)} />
        <input type="password" placeholder="password" onChange={(e) => setPassword(e.target.value)} />
        <button onClick={handleLogin}>Login</button>
        <button onClick={handleSignup}>Signup</button>

        <h3>Difficulty</h3>
        <select onChange={(e) => setDifficulty(e.target.value)}>
          <option>easy</option>
          <option>medium</option>
          <option>hard</option>
        </select>

        <h2>{question?.title}</h2>
        <p>{question?.description}</p>

        <h3>⏱ {timeLeft}s</h3>

        <h3>Stats</h3>
        {stats ? (
          <>
            <p>Attempts: {stats.total_attempts}</p>
            <p>Avg: {stats.avg_score}</p>
          </>
        ) : (
          <p>Login to see stats</p>
        )}

        <h3>Output</h3>
        <pre>{output}</pre>

        <h3>Tests</h3>
        {tests.map((t, i) => (
          <p key={i}>
            {t.input || "Hidden"} → {t.passed ? "PASS" : "FAIL"}
          </p>
        ))}

        <h3>Score</h3>
        <p>{score}</p>

        <h3>AI Feedback</h3>
        <div style={{ whiteSpace: "pre-wrap" }}>
          {feedback || "Click AI"}
        </div>

        <h3>History</h3>
        {history.map((h, i) => (
          <p key={i}>
            {h.question} → {h.score}
          </p>
        ))}

        <h3>Leaderboard</h3>
        {leaderboard.map((u, i) => (
          <p key={i}>
            {i + 1}. {u.username} - {u.score}
          </p>
        ))}
      </div>

      {/* RIGHT PANEL */}
      <div style={{ width: "70%" }}>
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          style={{
            width: "100%",
            height: "400px",
            background: "black",
            color: "lime",
          }}
        />

        <div style={{ marginTop: 10 }}>
          <button onClick={handleRun}>Run</button>
          <button onClick={handleTest}>Test</button>
          <button onClick={handleAI}>AI</button>
          <button onClick={handleSubmit}>Submit</button>
          <button onClick={loadQuestion}>Next</button>
        </div>
      </div>
    </div>
  );
}

export default App;