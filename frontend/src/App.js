import { useEffect, useState } from "react";
import API from "./api";
import "./App.css";

function App() {
  const [question, setQuestion] = useState(null);
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [testResults, setTestResults] = useState([]);
  const [score, setScore] = useState(0);
  const [verdict, setVerdict] = useState("");
  const [feedback, setFeedback] = useState("");
  const [aiFeedback, setAIFeedback] = useState("");
  const [followups, setFollowups] = useState([]);
  const [submitted, setSubmitted] = useState(false);
  const [difficulty, setDifficulty] = useState("easy");
  const [loading, setLoading] = useState(false);

  // ⏱ TIMER
  const [timeLeft, setTimeLeft] = useState(600);

  useEffect(() => {
    if (timeLeft <= 0 || submitted) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, submitted]);

  const formatTime = () => {
    const m = Math.floor(timeLeft / 60);
    const s = timeLeft % 60;
    return `${m}:${s < 10 ? "0" : ""}${s}`;
  };

  // =========================
  // 📥 LOAD QUESTION
  // =========================
  const loadQuestion = async () => {
    setLoading(true);
    try {
      console.log("API:", API.defaults.baseURL);

      const res = await API.get(`/questions/${difficulty}`);

      if (!res.data || res.data.length === 0) {
        alert("No questions found from backend");
        return;
      }

      const q = res.data[Math.floor(Math.random() * res.data.length)];

      setQuestion(q);
      setCode("");
      setOutput("");
      setTestResults([]);
      setScore(0);
      setVerdict("");
      setFeedback("");
      setFollowups([]);
      setAIFeedback("");
      setTimeLeft(600);
      setSubmitted(false);
    } catch (err) {
      console.error(err);
      alert("Backend not responding (Render may be sleeping)");
    }
    setLoading(false);
  };

  useEffect(() => {
    if (!submitted) {
      loadQuestion();
    }
  }, [difficulty, submitted]);

  // =========================
  // ▶ RUN CODE
  // =========================
  const handleRun = async () => {
    if (!code.trim()) return alert("Write code first");

    setLoading(true);
    try {
      const res = await API.post("/code/run", { code });

      setOutput(
        res.data.stdout ||
          res.data.stderr ||
          "⚠️ No output (did you forget print?)"
      );
    } catch {
      setOutput("Error running code");
    }
    setLoading(false);
  };

  // =========================
  // 🧪 RUN TESTS
  // =========================
  const handleTest = async () => {
    if (!code.trim()) return alert("Write code first");

    setLoading(true);
    try {
      const res = await API.post("/code/test", {
        code,
        question: question?.title?.toLowerCase(),
      });

      setTestResults(res.data.results || []);
    } catch {
      alert("Test failed");
    }
    setLoading(false);
  };

  // =========================
  // 🚀 SUBMIT
  // =========================
  const handleSubmit = async () => {
    if (!code.trim()) return alert("Write code first");

    setLoading(true);
    try {
      const res = await API.post("/evaluate", {
        code,
        question: question?.title,
        difficulty,
      });

      setScore(res.data.score);
      setVerdict(res.data.verdict);
      setFeedback(res.data.feedback);
      setFollowups(res.data.followups || []);

      if (res.data.plagiarism) {
        alert(`Plagiarism: ${res.data.plagiarism.similarity}%`);
      }

      if (res.data.next_difficulty) {
        setDifficulty(res.data.next_difficulty);
      }

      setSubmitted(true);
    } catch (err) {
      console.error(err);
      alert("Submit failed");
    }
    setLoading(false);
  };

  // =========================
  // 🤖 AI FEEDBACK
  // =========================
  const handleAIFeedback = async () => {
    if (!code.trim()) return alert("Write code first");

    setLoading(true);
    try {
      const res = await API.post("/ai/feedback", {
        code,
        question: question?.title,
      });

      setAIFeedback(res.data.feedback);
    } catch {
      alert("AI feedback failed");
    }
    setLoading(false);
  };

  if (loading && !question) return <h2>Loading question...</h2>;
  if (!question) return <h2>No question loaded</h2>;

  return (
    <div className="app">
      <div className="left">
        <h2>{question.title}</h2>
        <p className="desc">{question.description}</p>

        <div className="meta">
          <span className="difficulty">{difficulty.toUpperCase()}</span>
          <span className="timer">⏱ {formatTime()}</span>
        </div>

        <div className="box">
          <h4>Difficulty</h4>
          <select
            value={difficulty}
            onChange={(e) => {
              setSubmitted(false);
              setDifficulty(e.target.value);
            }}
          >
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>

        <div className="box">
          <h4>Output</h4>
          <pre>{output || "Run code to see output"}</pre>
        </div>

        <div className="box">
          <h4>Tests</h4>
          {testResults.length === 0 ? (
            <p>No tests run yet</p>
          ) : (
            testResults.map((t, i) => (
              <div key={i} className="test-row">
                <span>{String(t.input)}</span>
                <span className={t.status === "PASS" ? "pass" : "fail"}>
                  {t.status}
                </span>
              </div>
            ))
          )}
        </div>

        <div className="box">
          <h4>Score</h4>
          <p>{feedback}</p>
          <p>
            <b>{score}</b> | {verdict}
          </p>
        </div>

        {aiFeedback && (
          <div className="box">
            <h4>🤖 AI Feedback</h4>
            <p>{aiFeedback}</p>
          </div>
        )}

        {followups.length > 0 && (
          <div className="box">
            <h4>Follow-up Questions</h4>
            {followups.map((q, i) => (
              <div key={i}>• {q}</div>
            ))}
          </div>
        )}
      </div>

      <div className="right">
        <textarea
          className="editor"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Write your code here..."
        />

        <div className="buttons">
          <button onClick={handleRun} disabled={loading}>
            Run
          </button>
          <button onClick={handleTest} disabled={loading}>
            Run Tests
          </button>
          <button onClick={handleSubmit} disabled={loading}>
            Submit
          </button>
          <button onClick={handleAIFeedback} disabled={loading}>
            AI Review
          </button>

          <button
            onClick={() => {
              setSubmitted(false);
              loadQuestion();
            }}
          >
            Next →
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;