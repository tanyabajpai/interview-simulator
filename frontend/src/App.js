import React, { useEffect, useState } from "react";
import {
  getQuestions,
  runCode,
  runTests,
  getAIFeedback,
  login,
  saveAttempt,
  getStats,
} from "./api";
import "./App.css";

function App() {
  const [question, setQuestion] = useState(null);
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [tests, setTests] = useState([]);
  const [score, setScore] = useState(0);
  const [feedback, setFeedback] = useState("");
  const [difficulty, setDifficulty] = useState("easy");

  const [token, setToken] = useState(localStorage.getItem("token"));
  const [stats, setStats] = useState(null);

  // =========================
  // LOGIN AUTO (TEMP)
  // =========================
  useEffect(() => {
    if (!token) {
      login({ username: "tanya", password: "123456" })
        .then((res) => {
          const t = res.data.access_token;
          localStorage.setItem("token", t);
          setToken(t);
        })
        .catch(console.error);
    }
  }, [token]);

  // =========================
  // LOAD QUESTION
  // =========================
  const loadQuestion = async () => {
    const res = await getQuestions(difficulty);
    const q = Array.isArray(res.data) ? res.data[0] : res.data;

    setQuestion(q);

    setCode(`def solution():
    pass`);

    setOutput("");
    setTests([]);
    setScore(0);
  };

  useEffect(() => {
    loadQuestion();
  }, [difficulty]);

  // =========================
  // ACTIONS
  // =========================
  const handleRun = async () => {
    const res = await runCode(code);
    setOutput(res.data.output || "No output");
  };

  const handleRunTests = async () => {
    const res = await runTests(code, question?.title);
    setTests(res.data.results || []);
    setScore(res.data.score || 0);
  };

  const handleSubmit = async () => {
    const res = await runTests(code, question?.title);

    const finalScore = res.data.score || 0;
    setScore(finalScore);

    // 🔥 SAVE TO BACKEND
    await saveAttempt(
      {
        question: question.title,
        score: finalScore,
      },
      token
    );

    // 🔥 FETCH STATS
    const statsRes = await getStats(token);
    setStats(statsRes.data);
  };

  const handleAI = async () => {
    const res = await getAIFeedback(code, question?.title);
    setFeedback(res.data.feedback);
  };

  if (!question) return <h2>Loading...</h2>;

  return (
    <div className="app">
      <div className="left">
        <h2>{question.title}</h2>
        <p>{question.description}</p>

        <div className="box">
          <h4>Stats</h4>
          {stats ? (
            <>
              Attempts: {stats.total_attempts} <br />
              Avg Score: {stats.avg_score}
            </>
          ) : (
            "Submit to see stats"
          )}
        </div>

        <div className="box">
          <h4>Output</h4>
          <pre>{output}</pre>
        </div>

        <div className="box">
          <h4>Tests</h4>
          {tests.map((t, i) => (
            <div key={i}>
              {t.input} → {t.passed ? "PASS" : "FAIL"}
            </div>
          ))}
        </div>

        <div className="box">
          <h4>Score</h4>
          {score}
        </div>

        <div className="box">
          <h4>AI Feedback</h4>
          {feedback}
        </div>
      </div>

      <div className="right">
        <textarea
          className="editor"
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />

        <div className="buttons">
          <button onClick={handleRun}>Run</button>
          <button onClick={handleRunTests}>Run Tests</button>
          <button onClick={handleSubmit}>Submit</button>
          <button onClick={handleAI}>AI Review</button>
          <button onClick={loadQuestion}>Next</button>
        </div>
      </div>
    </div>
  );
}

export default App;