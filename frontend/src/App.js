import React, { useEffect, useState } from "react";
import {
  getQuestions,
  runCode,
  runTests,
  getAIFeedback,
} from "./api";
import "./App.css";

function App() {
  const [question, setQuestion] = useState(null);
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [tests, setTests] = useState([]);
  const [score, setScore] = useState(0);
  const [verdict, setVerdict] = useState("");
  const [feedback, setFeedback] = useState("");
  const [difficulty, setDifficulty] = useState("easy");

  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);

  // ⏱️ TIMER
  const [timeLeft, setTimeLeft] = useState(300); // 5 min

  // =========================
  // LOAD QUESTION
  // =========================
  const loadQuestion = async () => {
    try {
      setLoading(true);

      const res = await getQuestions(difficulty);
      const q = Array.isArray(res.data) ? res.data[0] : res.data;

      setQuestion(q);

      setCode(`def solution():
    # Write your code here
    pass`);

      setOutput("");
      setTests([]);
      setScore(0);
      setVerdict("");
      setFeedback("");

      setTimeLeft(300); // 🔥 reset timer
    } catch (err) {
      console.error(err);
      alert("Failed to load question");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadQuestion();
  }, [difficulty]);

  // =========================
  // TIMER LOGIC
  // =========================
  useEffect(() => {
    if (timeLeft <= 0) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft]);

  useEffect(() => {
    if (timeLeft === 0) {
      handleSubmit();
      alert("⏱️ Time's up!");
    }
  }, [timeLeft]);

  // =========================
  // SAFE CALL
  // =========================
  const safeCall = async (fn) => {
    if (actionLoading) return;

    try {
      setActionLoading(true);
      await fn();
    } catch (err) {
      console.error(err);
      alert("Something went wrong");
    } finally {
      setActionLoading(false);
    }
  };

  // =========================
  // ACTIONS
  // =========================
  const handleRun = () =>
    safeCall(async () => {
      const res = await runCode(code);
      setOutput(res.data.output || res.data.stdout || "No output");
    });

  const handleRunTests = () =>
    safeCall(async () => {
      const res = await runTests(code, question?.title);

      setTests(res.data.results || []);
      setScore(res.data.score || 0);
      setVerdict(res.data.verdict || "");
    });

  const handleSubmit = () =>
    safeCall(async () => {
      const res = await runTests(code, question?.title);

      setTests(res.data.results || []);
      setScore(res.data.score || 0);
      setVerdict(res.data.verdict || "");
    });

  const handleAI = () =>
    safeCall(async () => {
      const res = await getAIFeedback(code, question?.title);
      setFeedback(res.data.feedback);
    });

  // =========================
  // UI
  // =========================
  if (loading || !question) {
    return <h2 style={{ padding: "20px" }}>Loading...</h2>;
  }

  return (
    <div className="app">
      <div className="left">
        <h2>{question.title}</h2>
        <p>{question.description}</p>

        {/* ⏱️ TIMER UI */}
        <div className="box">
          <h4>Time Left</h4>
          <p>
            {Math.floor(timeLeft / 60)}:
            {String(timeLeft % 60).padStart(2, "0")}
          </p>
        </div>

        <div className="box">
          <h4>Difficulty</h4>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
          >
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>

        <div className="box">
          <h4>Output</h4>
          <pre>{output || "Run code"}</pre>
        </div>

        <div className="box">
          <h4>Tests</h4>
          {tests.length === 0
            ? "Run tests"
            : tests.map((t, i) => (
                <div key={i}>
                  {t.input} → {t.passed ? "PASS" : "FAIL"}
                </div>
              ))}
        </div>

        <div className="box">
          <h4>Score</h4>
          {score} {verdict}
        </div>

        <div className="box">
          <h4>AI Feedback</h4>
          {feedback || "Click AI Review"}
        </div>
      </div>

      <div className="right">
        <textarea
          className="editor"
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />

        <div className="buttons">
          <button disabled={actionLoading} onClick={handleRun}>
            Run
          </button>
          <button disabled={actionLoading} onClick={handleRunTests}>
            Run Tests
          </button>
          <button disabled={actionLoading} onClick={handleSubmit}>
            Submit
          </button>
          <button disabled={actionLoading} onClick={handleAI}>
            AI Review
          </button>
          <button disabled={actionLoading} onClick={loadQuestion}>
            Next
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;