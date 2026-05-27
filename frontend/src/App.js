import React, { useState, useEffect, useCallback, useRef } from "react";
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
  easy: 5 * 60,
  medium: 10 * 60,
  hard: 15 * 60,
};

const formatTime = (seconds) => {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
};

// =========================
// SIMPLE SYNTAX HIGHLIGHTER
// Highlights Python keywords in the textarea overlay
// =========================
const KEYWORDS = ["def","return","if","elif","else","for","while","in","not","and","or","True","False","None","import","from","class","pass","break","continue","lambda","try","except","finally","with","as","raise","yield","len","range","print","int","str","list","dict","set","tuple","sorted","min","max","sum","abs","enumerate","zip","map","filter","append","extend","pop","items","keys","values","self","__init__"];

function highlight(code) {
  const escaped = code
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Strings
  let result = escaped.replace(/("""[\s\S]*?"""|'''[\s\S]*?'''|"[^"\n]*"|'[^'\n]*')/g,
    '<span style="color:#f1fa8c">$1</span>');

  // Comments
  result = result.replace(/(#[^\n]*)/g,
    '<span style="color:#6272a4;font-style:italic">$1</span>');

  // Numbers
  result = result.replace(/\b(\d+\.?\d*)\b/g,
    '<span style="color:#bd93f9">$1</span>');

  // Keywords
  KEYWORDS.forEach(kw => {
    result = result.replace(
      new RegExp(`\\b(${kw})\\b`, 'g'),
      '<span style="color:#ff79c6;font-weight:600">$1</span>'
    );
  });

  return result;
}

// =========================
// HIGHLIGHTED EDITOR COMPONENT
// Textarea layered over a pre for syntax highlighting
// =========================
function CodeEditor({ value, onChange, disabled, timedOut }) {
  const taRef = useRef(null);
  const preRef = useRef(null);

  const syncScroll = () => {
    if (preRef.current && taRef.current) {
      preRef.current.scrollTop = taRef.current.scrollTop;
      preRef.current.scrollLeft = taRef.current.scrollLeft;
    }
  };

  const sharedStyle = {
    position: "absolute", top: 0, left: 0,
    width: "100%", height: "100%",
    margin: 0, padding: "14px 16px",
    fontFamily: "'Fira Code', 'Cascadia Code', monospace",
    fontSize: 14, lineHeight: "1.7",
    tabSize: 4, whiteSpace: "pre",
    overflowWrap: "normal", overflow: "auto",
    boxSizing: "border-box",
    letterSpacing: "0.02em",
  };

  return (
    <div style={{
      position: "relative",
      width: "100%", height: "100%",
      borderRadius: 10,
      border: timedOut ? "1.5px solid #dc3545" : "1.5px solid #2a2a3a",
      overflow: "hidden",
      background: timedOut ? "#1a0008" : "#0d0d14",
    }}>
      {/* Syntax-highlighted display layer */}
      <pre
        ref={preRef}
        aria-hidden="true"
        style={{
          ...sharedStyle,
          color: timedOut ? "#ff6b6b" : "#00ff41",
          background: "transparent",
          pointerEvents: "none",
          zIndex: 1,
          overflowY: "scroll",
        }}
        dangerouslySetInnerHTML={{ __html: highlight(value) + "\n" }}
      />
      {/* Transparent textarea on top */}
      <textarea
        ref={taRef}
        value={value}
        onChange={(e) => !timedOut && onChange(e.target.value)}
        onScroll={syncScroll}
        readOnly={timedOut || disabled}
        spellCheck={false}
        autoCorrect="off"
        autoCapitalize="off"
        style={{
          ...sharedStyle,
          color: "transparent",
          caretColor: timedOut ? "#ff6b6b" : "#00ff41",
          background: "transparent",
          zIndex: 2,
          resize: "none",
          outline: "none",
          border: "none",
          cursor: timedOut ? "not-allowed" : "text",
        }}
        onKeyDown={(e) => {
          if (e.key === "Tab") {
            e.preventDefault();
            const s = e.target.selectionStart;
            const en = e.target.selectionEnd;
            const newVal = value.substring(0, s) + "    " + value.substring(en);
            onChange(newVal);
            setTimeout(() => { e.target.selectionStart = e.target.selectionEnd = s + 4; }, 0);
          }
        }}
      />
      {timedOut && (
        <div style={{
          position: "absolute", top: 10, right: 12, zIndex: 3,
          background: "#dc3545", color: "#fff",
          padding: "3px 10px", borderRadius: 4, fontSize: 11,
          fontWeight: "bold", letterSpacing: "0.08em",
        }}>TIME'S UP</div>
      )}
    </div>
  );
}

// =========================
// MAIN APP
// =========================
function App() {
  const [code, setCode] = useState("def solution():\n    pass");
  const [question, setQuestion] = useState(null);
  const [difficulty, setDifficulty] = useState("easy");

  const [output, setOutput] = useState("");
  const [outputLoading, setOutputLoading] = useState(false);
  const [tests, setTests] = useState([]);
  const [testsLoading, setTestsLoading] = useState(false);
  const [score, setScore] = useState(null);
  const [feedback, setFeedback] = useState("");
  const [feedbackLoading, setFeedbackLoading] = useState(false);

  const [stats, setStats] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [history, setHistory] = useState([]);

  const [timeLeft, setTimeLeft] = useState(TIMER_LIMITS["easy"]);
  const [timedOut, setTimedOut] = useState(false);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [authError, setAuthError] = useState("");
  const [authLoading, setAuthLoading] = useState(false);

  const [token, setToken] = useState(localStorage.getItem("token"));
  const [loggedInUser, setLoggedInUser] = useState(localStorage.getItem("username") || "");

  const [screen, setScreen] = useState(
    localStorage.getItem("token") ? "main" : "landing"
  );

  const [backendStatus, setBackendStatus] = useState("idle");
  const [activeTab, setActiveTab] = useState("output"); // "output" | "tests" | "feedback"
  const [mobilePanel, setMobilePanel] = useState("left"); // "left" | "right"
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 768);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  // =========================
  // LOAD QUESTION
  // =========================
  const loadQuestion = useCallback(async () => {
    setQuestion(null);
    setTimedOut(false);
    setTimeLeft(TIMER_LIMITS[difficulty]);
    setOutput("");
    setTests([]);
    setScore(null);
    setFeedback("");
    setSubmitSuccess(false);
    try {
      const res = await getQuestions(difficulty);
      const q = res.data;
      setQuestion(q);
      const starterMap = {
        "Reverse String": "def solution(s):\n    pass",
        "Palindrome Check": "def solution(s):\n    pass",
        "Factorial": "def solution(n):\n    pass",
        "Fibonacci Number": "def solution(n):\n    pass",
        "Count Vowels": "def solution(s):\n    pass",
        "Sum of List": "def solution(nums):\n    pass",
        "Check Prime": "def solution(n):\n    pass",
        "Max in List": "def solution(nums):\n    pass",
        "Min in List": "def solution(nums):\n    pass",
        "Even or Odd": "def solution(n):\n    pass",
        "Remove Spaces": "def solution(s):\n    pass",
        "Remove Duplicates": "def solution(nums):\n    pass",
        "Count Words": "def solution(s):\n    pass",
        "Square Number": "def solution(n):\n    pass",
        "Cube Number": "def solution(n):\n    pass",
        "Find Length": "def solution(s):\n    pass",
        "Uppercase String": "def solution(s):\n    pass",
        "Lowercase String": "def solution(s):\n    pass",
        "Average of List": "def solution(nums):\n    pass",
        "Find Index": "def solution(nums, target):\n    pass",
        "FizzBuzz": "def solution(n):\n    pass",
        "Sum of Digits": "def solution(n):\n    pass",
        "Flatten List": "def solution(lst):\n    pass",
        "Count Occurrences": "def solution(lst, val):\n    pass",
        "Power Function": "def solution(base, exp):\n    pass",
        "Merge Two Sorted Lists": "def solution(l1, l2):\n    pass",
        "Missing Number": "def solution(nums):\n    pass",
        "Is Anagram": "def solution(s, t):\n    pass",
        "Two Sum": "def solution(nums, target):\n    pass",
        "Valid Parentheses": "def solution(s):\n    pass",
        "Longest Substring Without Repeating": "def solution(s):\n    pass",
        "Second Largest": "def solution(nums):\n    pass",
        "Rotate Array": "def solution(nums, k):\n    pass",
        "Product Except Self": "def solution(nums):\n    pass",
        "Group Anagrams": "def solution(strs):\n    pass",
        "Top K Frequent Elements": "def solution(nums, k):\n    pass",
        "Kth Largest Element": "def solution(nums, k):\n    pass",
        "Container With Most Water": "def solution(height):\n    pass",
        "Longest Palindromic Substring": "def solution(s):\n    pass",
        "Subarray Sum Equals K": "def solution(nums, k):\n    pass",
        "Sort Colors": "def solution(nums):\n    pass",
        "Spiral Matrix": "def solution(matrix):\n    pass",
        "Combination Sum": "def solution(candidates, target):\n    pass",
        "Permutations": "def solution(nums):\n    pass",
        "Search in Rotated Sorted Array": "def solution(nums, target):\n    pass",
        "Word Search": "def solution(board, word):\n    pass",
        "Set Matrix Zeroes": "def solution(matrix):\n    pass",
        "Jump Game": "def solution(nums):\n    pass",
        "Anagram Check": "def solution(s, t):\n    pass",
        "Trapping Rain Water": "def solution(height):\n    pass",
        "Median of Two Sorted Arrays": "def solution(nums1, nums2):\n    pass",
        "Merge Intervals": "def solution(intervals):\n    pass",
        "Minimum Window Substring": "def solution(s, t):\n    pass",
        "N Queens": "def solution(n):\n    pass",
        "Edit Distance": "def solution(word1, word2):\n    pass",
        "Word Break": "def solution(s, wordDict):\n    pass",
        "Course Schedule": "def solution(numCourses, prerequisites):\n    pass",
        "Sliding Window Maximum": "def solution(nums, k):\n    pass",
        "Regular Expression Matching": "def solution(s, p):\n    pass",
        "Palindrome Partitioning": "def solution(s):\n    pass",
        "Burst Balloons": "def solution(nums):\n    pass",
        "Distinct Subsequences": "def solution(s, t):\n    pass",
        "Word Ladder": "def solution(beginWord, endWord, wordList):\n    pass",
      };
      setCode(starterMap[q.title] || "def solution(*args):\n    pass");
    } catch {
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
    setAuthError(""); setAuthLoading(true);
    try {
      const res = await login({ username, password });
      const accessToken = res.data.access_token;
      localStorage.setItem("token", accessToken);
      localStorage.setItem("username", username);
      setToken(accessToken);
      setLoggedInUser(username);
      setScreen("main");
    } catch {
      setAuthError("Invalid username or password.");
    } finally { setAuthLoading(false); }
  };

  const handleSignup = async () => {
    setAuthError(""); setAuthLoading(true);
    if (!username || !password) { setAuthError("Both fields required."); setAuthLoading(false); return; }
    if (password.length < 4) { setAuthError("Password must be at least 4 characters."); setAuthLoading(false); return; }
    try {
      await signup({ username, password });
      const res = await login({ username, password });
      const accessToken = res.data.access_token;
      localStorage.setItem("token", accessToken);
      localStorage.setItem("username", username);
      setToken(accessToken);
      setLoggedInUser(username);
      setScreen("main");
    } catch {
      setAuthError("Signup failed. Username may already exist.");
    } finally { setAuthLoading(false); }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setToken(null); setLoggedInUser("");
    setStats(null); setHistory([]);
    setScreen("landing");
    setUsername(""); setPassword("");
  };

  // =========================
  // ACTIONS
  // =========================
  const handleRun = async () => {
    setOutputLoading(true);
    setActiveTab("output");
    // On mobile: switch to info panel so user sees the result
    if (isMobile) setMobilePanel("left");
    try {
      const res = await runCode(code);
      setOutput(res.data.output || "(no output)");
    } catch (err) {
      const msg = err?.response?.data?.detail || err?.response?.data?.error || "Error running code.";
      setOutput(msg);
    } finally { setOutputLoading(false); }
  };

  const handleTest = async () => {
    if (!question) return;
    setTestsLoading(true);
    setActiveTab("tests");
    // On mobile: switch to info panel so user sees test results
    if (isMobile) setMobilePanel("left");
    try {
      const res = await runTests(code, question.title);
      setTests(res.data.results || []);
      setScore(res.data.score ?? 0);
    } catch (err) {
      console.error("Test error:", err);
      const msg = err?.response?.data?.detail || "Tests failed to run.";
      setTests([{ passed: false, input: "Error", expected: "", got: msg }]);
      setScore(0);
    } finally { setTestsLoading(false); }
  };

  const handleAI = async () => {
    if (!question) return;
    setFeedbackLoading(true);
    setActiveTab("feedback");
    // On mobile: switch to info panel so user sees AI feedback
    if (isMobile) setMobilePanel("left");
    try {
      const res = await getAIFeedback(code, question.title);
      const d = res.data;
      setFeedback(typeof d === "string" ? d : d.feedback || d.message || JSON.stringify(d));
    } catch {
      setFeedback("AI feedback failed. Please try again.");
    } finally { setFeedbackLoading(false); }
  };

  const handleSubmit = async () => {
    if (!token) { alert("Please log in to submit!"); return; }
    if (!question) { alert("No question loaded."); return; }
    try {
      // Run tests first if score is not yet available
      let finalScore = score;
      if (finalScore === null) {
        try {
          const res = await runTests(code, question.title);
          setTests(res.data.results || []);
          finalScore = res.data.score ?? 0;
          setScore(finalScore);
          setActiveTab("tests");
        } catch {
          finalScore = 0;
        }
      }
      await saveAttempt({ question: question.title, score: finalScore });
      setSubmitSuccess(true);
      setTimeout(() => setSubmitSuccess(false), 3000);
      fetchStats(); fetchLeaderboard(); fetchHistory();
    } catch (err) {
      const msg = err?.response?.data?.detail || "Submit failed. Please try again.";
      alert(msg);
    }
  };

  // =========================
  // DATA FETCHING
  // =========================
  const fetchStats = useCallback(async () => {
    if (!token) return;
    try { const res = await getStats(); setStats(res.data); } catch {}
  }, [token]);

  const fetchLeaderboard = async () => {
    try {
      const res = await getLeaderboard();
      let data = res.data;
      if (!Array.isArray(data)) data = Array.isArray(data.leaderboard) ? data.leaderboard : [];
      setLeaderboard(data);
    } catch { setLeaderboard([]); }
  };

  const fetchHistory = useCallback(async () => {
    if (!token) return;
    try { const res = await getHistory(); setHistory(res.data || []); } catch {}
  }, [token]);

  // =========================
  // TIMER
  // =========================
  useEffect(() => {
    if (timedOut || timeLeft <= 0) { if (timeLeft <= 0) setTimedOut(true); return; }
    const t = setTimeout(() => setTimeLeft((p) => p - 1), 1000);
    return () => clearTimeout(t);
  }, [timeLeft, timedOut]);

  useEffect(() => {
    setTimeLeft(TIMER_LIMITS[difficulty]);
    setTimedOut(false);
  }, [difficulty]);

  // =========================
  // BOOT
  // =========================
  useEffect(() => {
    if (screen !== "main") return;
    const boot = async () => {
      setBackendStatus("waking");
      const isUp = await wakeUpBackend();
      if (!isUp) {
        setBackendStatus("failed");
        setQuestion({ title: "Server unavailable", description: "The backend could not be reached. Please try again." });
        return;
      }
      setBackendStatus("ready");
      await loadQuestion();
      fetchLeaderboard();
    };
    boot();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [screen]);

  useEffect(() => {
    if (backendStatus !== "ready") return;
    loadQuestion();
    fetchLeaderboard();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [difficulty]);

  useEffect(() => { fetchStats(); fetchHistory(); }, [fetchStats, fetchHistory]);

  const timerColor = timedOut ? "#dc3545" : timeLeft < 60 ? "#dc3545" : timeLeft < 120 ? "#fd7e14" : "#00ff41";
  const actionsDisabled = backendStatus === "waking" || timedOut;

  // =========================
  // SHARED STYLES
  // =========================
  const S = {
    panelBg: "#0a0a12",
    border: "1.5px solid #1a1a2e",
    accent: "#00ff41",
    accentDim: "#00cc33",
    font: "'Fira Code', 'Cascadia Code', monospace",
    text: "#c8d6e5",
    muted: "#5a6a7a",
    cardBg: "#0f0f1e",
  };

  // =========================
  // LANDING SCREEN
  // =========================
  if (screen === "landing") {
    return (
      <div style={{
        minHeight: "100vh", background: "#050508",
        fontFamily: S.font, color: S.text,
        overflowX: "hidden",
      }}>
        {/* Grid background */}
        <div style={{
          position: "fixed", inset: 0, zIndex: 0,
          backgroundImage: `
            linear-gradient(rgba(0,255,65,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,255,65,0.03) 1px, transparent 1px)
          `,
          backgroundSize: "40px 40px",
          pointerEvents: "none",
        }} />

        {/* Glow orb */}
        <div style={{
          position: "fixed", top: "-20vh", left: "50%", transform: "translateX(-50%)",
          width: "80vw", height: "60vh", borderRadius: "50%",
          background: "radial-gradient(ellipse, rgba(0,255,65,0.07) 0%, transparent 70%)",
          pointerEvents: "none", zIndex: 0,
        }} />

        {/* NAV */}
        <nav style={{
          position: "relative", zIndex: 10,
          display: "flex", alignItems: "center", justifyContent: "space-between",
          padding: "20px 40px",
          borderBottom: "1px solid rgba(0,255,65,0.1)",
        }}>
          <span style={{ color: S.accent, fontSize: 18, fontWeight: 700, letterSpacing: "0.05em" }}>
            {"<"} InterviewSim {"/>"}
          </span>
          <div style={{ display: "flex", gap: 12 }}>
            <button onClick={() => setScreen("login")} style={{
              background: "transparent", border: "1px solid rgba(0,255,65,0.4)",
              color: S.accent, padding: "8px 20px", borderRadius: 6,
              fontFamily: S.font, fontSize: 13, cursor: "pointer",
              transition: "all 0.2s",
            }}
              onMouseEnter={e => { e.target.style.background = "rgba(0,255,65,0.1)"; }}
              onMouseLeave={e => { e.target.style.background = "transparent"; }}
            >Login</button>
            <button onClick={() => setScreen("login")} style={{
              background: S.accent, border: "none",
              color: "#000", padding: "8px 20px", borderRadius: 6,
              fontFamily: S.font, fontSize: 13, fontWeight: 700, cursor: "pointer",
            }}>Get Started</button>
          </div>
        </nav>

        {/* HERO */}
        <div style={{
          position: "relative", zIndex: 1,
          textAlign: "center", padding: "100px 20px 60px",
        }}>
          <div style={{
            display: "inline-block",
            background: "rgba(0,255,65,0.08)", border: "1px solid rgba(0,255,65,0.2)",
            color: S.accent, fontSize: 12, padding: "4px 14px", borderRadius: 20,
            marginBottom: 28, letterSpacing: "0.12em", textTransform: "uppercase",
          }}>
            AI-Powered Coding Practice
          </div>
          <h1 style={{
            fontSize: "clamp(36px, 7vw, 80px)",
            fontWeight: 800, lineHeight: 1.1, margin: "0 0 24px",
            color: "#fff",
            textShadow: "0 0 60px rgba(0,255,65,0.2)",
          }}>
            Ace Your Next<br />
            <span style={{ color: S.accent }}>Coding Interview</span>
          </h1>
          <p style={{
            fontSize: "clamp(14px, 2vw, 18px)", color: S.muted,
            maxWidth: 560, margin: "0 auto 44px", lineHeight: 1.7,
          }}>
            Timed DSA challenges with real test cases, AI code feedback, and a global leaderboard.
            Practice like it's the real thing.
          </p>
          <div style={{ display: "flex", gap: 14, justifyContent: "center", flexWrap: "wrap" }}>
            <button onClick={() => setScreen("login")} style={{
              background: S.accent, color: "#000", border: "none",
              padding: "14px 36px", borderRadius: 8, fontFamily: S.font,
              fontSize: 15, fontWeight: 700, cursor: "pointer",
              boxShadow: "0 0 30px rgba(0,255,65,0.3)",
            }}>Start Practicing →</button>
            <button onClick={() => { setScreen("main"); }} style={{
              background: "transparent", color: S.text,
              border: "1px solid rgba(255,255,255,0.15)",
              padding: "14px 36px", borderRadius: 8, fontFamily: S.font,
              fontSize: 15, cursor: "pointer",
            }}>Try as Guest</button>
          </div>
        </div>

        {/* STATS BAR */}
        <div style={{
          position: "relative", zIndex: 1,
          display: "flex", justifyContent: "center", gap: "60px",
          padding: "40px 20px", flexWrap: "wrap",
        }}>
          {[["60+", "Challenges"], ["3", "Difficulty Levels"], ["AI", "Code Feedback"], ["⚡", "Real-time Judge"]].map(([val, label]) => (
            <div key={label} style={{ textAlign: "center" }}>
              <div style={{ fontSize: 32, fontWeight: 800, color: S.accent }}>{val}</div>
              <div style={{ fontSize: 12, color: S.muted, letterSpacing: "0.1em", textTransform: "uppercase", marginTop: 4 }}>{label}</div>
            </div>
          ))}
        </div>

        {/* FEATURES */}
        <div style={{
          position: "relative", zIndex: 1,
          display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
          gap: 20, maxWidth: 1000, margin: "0 auto", padding: "20px 30px 80px",
        }}>
          {[
            { icon: "⏱", title: "Timed Challenges", desc: "Real interview pressure. 5, 10, or 15 minute limits that count down and lock your editor." },
            { icon: "🤖", title: "AI Feedback", desc: "Get instant analysis of your code: logic, edge cases, and style — all powered by Claude." },
            { icon: "🧪", title: "Test Runner", desc: "Hidden and visible test cases run your code in real-time against expected outputs." },
            { icon: "🏆", title: "Leaderboard", desc: "Compete globally. See how your score stacks up against other developers." },
            { icon: "📈", title: "Track Progress", desc: "Login to save attempts, view history, and watch your average score improve." },
            { icon: "🎯", title: "3 Difficulties", desc: "Easy warm-ups, medium challenges, and hard brain-benders. Progress at your own pace." },
          ].map(({ icon, title, desc }) => (
            <div key={title} style={{
              background: S.cardBg, border: S.border,
              borderRadius: 12, padding: "24px 22px",
              transition: "border-color 0.2s, transform 0.2s",
            }}
              onMouseEnter={e => { e.currentTarget.style.borderColor = "rgba(0,255,65,0.3)"; e.currentTarget.style.transform = "translateY(-2px)"; }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = "#1a1a2e"; e.currentTarget.style.transform = "translateY(0)"; }}
            >
              <div style={{ fontSize: 28, marginBottom: 12 }}>{icon}</div>
              <div style={{ color: "#fff", fontWeight: 700, marginBottom: 8, fontSize: 15 }}>{title}</div>
              <div style={{ color: S.muted, fontSize: 13, lineHeight: 1.6 }}>{desc}</div>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div style={{
          position: "relative", zIndex: 1, textAlign: "center",
          padding: "60px 20px 80px",
          borderTop: "1px solid rgba(0,255,65,0.08)",
        }}>
          <h2 style={{ color: "#fff", fontSize: "clamp(24px,4vw,40px)", marginBottom: 16 }}>
            Ready to level up?
          </h2>
          <p style={{ color: S.muted, marginBottom: 32, fontSize: 14 }}>Free to use. No credit card. Start in seconds.</p>
          <button onClick={() => setScreen("login")} style={{
            background: S.accent, color: "#000", border: "none",
            padding: "16px 48px", borderRadius: 8, fontFamily: S.font,
            fontSize: 16, fontWeight: 700, cursor: "pointer",
            boxShadow: "0 0 40px rgba(0,255,65,0.25)",
          }}>Create Free Account</button>
        </div>
      </div>
    );
  }

  // =========================
  // LOGIN SCREEN
  // =========================
  if (screen === "login") {
    return (
      <div style={{
        minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center",
        background: "#050508", fontFamily: S.font,
        backgroundImage: `linear-gradient(rgba(0,255,65,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,65,0.03) 1px, transparent 1px)`,
        backgroundSize: "40px 40px",
      }}>
        <div style={{
          background: "#0a0a14", border: "1.5px solid #1a1a30",
          borderRadius: 14, padding: "44px 48px", width: "100%", maxWidth: 380,
          boxShadow: "0 8px 40px rgba(0,0,0,0.6)",
        }}>
          <div style={{ textAlign: "center", marginBottom: 32 }}>
            <div style={{ color: S.accent, fontSize: 20, fontWeight: 700, marginBottom: 6 }}>
              {"<"} InterviewSim {"/>"}
            </div>
            <p style={{ color: S.muted, fontSize: 13, margin: 0 }}>Practice DSA with AI feedback</p>
          </div>

          {[
            { placeholder: "Username", type: "text", val: username, set: setUsername },
            { placeholder: "Password", type: "password", val: password, set: setPassword },
          ].map(({ placeholder, type, val, set }) => (
            <input
              key={placeholder} type={type} placeholder={placeholder}
              value={val} onChange={(e) => set(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleLogin()}
              style={{
                display: "block", width: "100%", marginBottom: 12,
                padding: "11px 14px", background: "#060610", color: "#fff",
                border: "1.5px solid #1e1e35", borderRadius: 7, fontFamily: S.font,
                fontSize: 14, boxSizing: "border-box", outline: "none",
                transition: "border-color 0.2s",
              }}
              onFocus={e => e.target.style.borderColor = "rgba(0,255,65,0.5)"}
              onBlur={e => e.target.style.borderColor = "#1e1e35"}
            />
          ))}

          {authError && (
            <p style={{ color: "#ff4d4d", fontSize: 12, marginBottom: 10, marginTop: -4 }}>
              ⚠ {authError}
            </p>
          )}

          <div style={{ display: "flex", gap: 10, marginBottom: 12 }}>
            {[
              { label: authLoading ? "..." : "Login", fn: handleLogin, primary: true },
              { label: authLoading ? "..." : "Sign Up", fn: handleSignup, primary: false },
            ].map(({ label, fn, primary }) => (
              <button key={label} onClick={fn} disabled={authLoading} style={{
                flex: 1, padding: "11px 0",
                background: primary ? S.accent : "transparent",
                color: primary ? "#000" : S.accent,
                border: primary ? "none" : `1.5px solid ${S.accent}`,
                borderRadius: 7, fontFamily: S.font, fontSize: 14,
                fontWeight: primary ? 700 : 500, cursor: "pointer",
              }}>{label}</button>
            ))}
          </div>

          <button onClick={() => setScreen("main")} style={{
            width: "100%", padding: "10px 0", background: "transparent",
            color: S.muted, border: "1px solid #1e1e35", borderRadius: 7,
            fontFamily: S.font, fontSize: 12, cursor: "pointer",
          }}>Skip — continue as guest</button>

          <button onClick={() => setScreen("landing")} style={{
            width: "100%", padding: "8px 0", marginTop: 8, background: "transparent",
            color: "#333", border: "none", fontFamily: S.font, fontSize: 11, cursor: "pointer",
          }}>← Back to home</button>
        </div>
      </div>
    );
  }

  // =========================
  // MAIN SCREEN
  // =========================
  return (
    <div style={{
      display: "flex", flexDirection: "column",
      height: "100vh", background: "#050508",
      fontFamily: S.font, color: S.text, overflow: "hidden",
    }}>
      {/* TOP NAV */}
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "0 16px", height: 48, flexShrink: 0,
        borderBottom: "1px solid #12121f", background: "#07070f",
      }}>
        <span
          onClick={() => setScreen("landing")}
          style={{ color: S.accent, fontWeight: 700, fontSize: 14, cursor: "pointer", letterSpacing: "0.04em" }}>
          {"<"} InterviewSim {"/>"}
        </span>

        {/* Mobile panel toggle — only shown on mobile */}
        {isMobile && (
          <div style={{ display: "flex", gap: 4 }}>
            {[{ id: "left", label: "📋 Info" }, { id: "right", label: "💻 Code" }].map(p => (
              <button key={p.id} onClick={() => setMobilePanel(p.id)} style={{
                padding: "5px 13px", fontSize: 12, borderRadius: 5,
                background: mobilePanel === p.id ? "rgba(0,255,65,0.18)" : "transparent",
                color: mobilePanel === p.id ? S.accent : S.muted,
                border: `1px solid ${mobilePanel === p.id ? "rgba(0,255,65,0.4)" : "#1a1a2e"}`,
                cursor: "pointer", fontFamily: S.font, fontWeight: mobilePanel === p.id ? 700 : 400,
              }}>{p.label}</button>
            ))}
          </div>
        )}

        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          {token ? (
            <>
              <span style={{ color: S.accent, fontSize: 12 }}>✓ {loggedInUser}</span>
              <button onClick={handleLogout} style={{
                fontSize: 11, padding: "4px 10px", background: "transparent",
                border: "1px solid #2a2a3a", borderRadius: 4, color: S.muted, cursor: "pointer",
              }}>Logout</button>
            </>
          ) : (
            <button onClick={() => setScreen("login")} style={{
              fontSize: 11, padding: "4px 12px", background: "transparent",
              border: `1px solid ${S.accent}`, borderRadius: 4, color: S.accent, cursor: "pointer",
            }}>Log in</button>
          )}
        </div>
      </div>

      {/* BACKEND BANNERS */}
      {backendStatus === "waking" && (
        <div style={{
          background: "#1a1200", borderBottom: "1px solid #3a2a00",
          padding: "8px 16px", fontSize: 12, color: "#ffd600", flexShrink: 0,
          display: "flex", alignItems: "center", gap: 8,
        }}>
          <span style={{ animation: "spin 1s linear infinite", display: "inline-block" }}>⚙</span>
          <strong>Server waking up</strong> — free tier sleeps after inactivity. Ready in ~30s.
        </div>
      )}
      {backendStatus === "failed" && (
        <div style={{
          background: "#1a0008", borderBottom: "1px solid #3a0010",
          padding: "8px 16px", fontSize: 12, color: "#ff4d6d", flexShrink: 0,
        }}>
          ❌ <strong>Server unreachable.</strong>{" "}
          <button onClick={() => window.location.reload()} style={{
            marginLeft: 8, fontSize: 11, padding: "2px 8px",
            background: "#3a0010", border: "1px solid #ff4d6d", color: "#ff4d6d", borderRadius: 4, cursor: "pointer",
          }}>Retry</button>
        </div>
      )}
      {submitSuccess && (
        <div style={{
          background: "#001a08", borderBottom: "1px solid #00ff41",
          padding: "8px 16px", fontSize: 12, color: S.accent, flexShrink: 0,
        }}>
          ✅ Solution submitted successfully!
        </div>
      )}

      {/* MAIN CONTENT */}
      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>

        {/* LEFT PANEL */}
        <div style={{
          width: isMobile ? "100%" : "32%",
          minWidth: isMobile ? "unset" : 260,
          borderRight: isMobile ? "none" : "1px solid #12121f",
          overflowY: "auto", padding: "14px 16px", flexShrink: 0,
          paddingBottom: isMobile ? "70px" : "14px",
          display: isMobile && mobilePanel !== "left" ? "none" : "block",
        }}>
          {/* Difficulty */}
          <div style={{ marginBottom: 14 }}>
            <label style={{ fontSize: 10, color: S.muted, textTransform: "uppercase", letterSpacing: "0.1em" }}>Difficulty</label>
            <select value={difficulty} onChange={e => setDifficulty(e.target.value)}
              disabled={backendStatus === "waking"}
              style={{
                display: "block", marginTop: 6, width: "100%",
                background: "#0c0c1a", color: "#fff", border: "1px solid #1e1e35",
                borderRadius: 6, padding: "7px 10px", fontFamily: S.font, fontSize: 13, cursor: "pointer",
              }}>
              <option value="easy">🟢 Easy — 5 min</option>
              <option value="medium">🟡 Medium — 10 min</option>
              <option value="hard">🔴 Hard — 15 min</option>
            </select>
          </div>

          {/* Question */}
          <div style={{
            background: S.cardBg, border: S.border, borderRadius: 10,
            padding: "14px", marginBottom: 14,
          }}>
            {backendStatus === "waking" ? (
              <p style={{ color: S.muted, fontSize: 13, margin: 0, fontStyle: "italic" }}>⚙ Loading question...</p>
            ) : question ? (
              <>
                <div style={{ color: "#fff", fontWeight: 700, fontSize: 15, marginBottom: 8 }}>
                  {question.title}
                </div>
                <div style={{ color: S.text, fontSize: 13, lineHeight: 1.65 }}>
                  {question.description}
                </div>
              </>
            ) : (
              <p style={{ color: S.muted, fontSize: 13, margin: 0 }}>Loading...</p>
            )}
          </div>

          {/* Timer */}
          <div style={{
            background: S.cardBg, border: `1.5px solid ${timedOut ? "#dc3545" : timerColor === "#00ff41" ? "#1a1a2e" : timerColor + "44"}`,
            borderRadius: 10, padding: "10px 14px", marginBottom: 14,
            display: "flex", alignItems: "center", justifyContent: "space-between",
          }}>
            <span style={{ fontSize: 11, color: S.muted, textTransform: "uppercase", letterSpacing: "0.1em" }}>Timer</span>
            <span style={{ color: timerColor, fontWeight: 800, fontSize: 22, letterSpacing: "0.05em" }}>
              {formatTime(timeLeft)}
            </span>
          </div>
          {timedOut && (
            <div style={{
              background: "#1a0008", border: "1px solid #dc3545",
              borderRadius: 6, padding: "8px 12px", marginBottom: 14,
              color: "#ff4d6d", fontSize: 12, fontWeight: 600,
            }}>
              ⛔ Time's up! Click ⏭ Next for a new question.
            </div>
          )}

          {/* Output / Tests / Feedback Tabs */}
          <div style={{ marginBottom: 8 }}>
            <div style={{ display: "flex", gap: 2, marginBottom: 10 }}>
              {[
                { id: "output", label: "Output" },
                { id: "tests", label: `Tests${tests.length ? ` (${tests.length})` : ""}` },
                { id: "feedback", label: "AI" },
              ].map(tab => (
                <button key={tab.id} onClick={() => setActiveTab(tab.id)} style={{
                  flex: 1, padding: "6px 4px", fontSize: 11,
                  background: activeTab === tab.id ? "rgba(0,255,65,0.1)" : "transparent",
                  color: activeTab === tab.id ? S.accent : S.muted,
                  border: `1px solid ${activeTab === tab.id ? "rgba(0,255,65,0.3)" : "#1a1a2e"}`,
                  borderRadius: 5, cursor: "pointer", fontFamily: S.font,
                  transition: "all 0.15s",
                }}>{tab.label}</button>
              ))}
            </div>

            {/* Output tab */}
            {activeTab === "output" && (
              <pre style={{
                background: "#060610", color: "#00ff41", padding: "10px 12px",
                borderRadius: 8, fontSize: 12, margin: 0,
                border: "1px solid #1a1a2e", minHeight: 60,
                whiteSpace: "pre-wrap", wordBreak: "break-all",
                overflowX: "hidden", maxWidth: "100%", lineHeight: 1.6,
              }}>
                {outputLoading ? "Running..." : (output || "(no output yet)")}
              </pre>
            )}

            {/* Tests tab */}
            {activeTab === "tests" && (
              <div>
                {testsLoading ? (
                  <p style={{ color: S.muted, fontSize: 12 }}>Running tests...</p>
                ) : tests.length === 0 ? (
                  <p style={{ color: S.muted, fontSize: 12 }}>No test results yet. Click 🧪 Test.</p>
                ) : (
                  <>
                    {tests.map((t, i) => (
                      <div key={i} style={{
                        display: "flex", alignItems: "center", justifyContent: "space-between",
                        padding: "6px 10px", marginBottom: 4,
                        background: t.passed ? "rgba(0,255,65,0.05)" : "rgba(220,53,69,0.08)",
                        border: `1px solid ${t.passed ? "rgba(0,255,65,0.2)" : "rgba(220,53,69,0.25)"}`,
                        borderRadius: 6, fontSize: 12,
                      }}>
                        <span style={{ color: S.muted }}>{t.input != null ? `input: ${t.input}` : "Hidden test"}</span>
                        <span style={{ color: t.passed ? S.accent : "#ff4d6d", fontWeight: 700 }}>
                          {t.passed ? "✓ PASS" : "✗ FAIL"}
                        </span>
                      </div>
                    ))}
                    {score !== null && (
                      <div style={{
                        marginTop: 10, padding: "8px 12px",
                        background: "rgba(0,255,65,0.08)", border: "1px solid rgba(0,255,65,0.2)",
                        borderRadius: 6, color: S.accent, fontWeight: 700, fontSize: 14,
                        textAlign: "center",
                      }}>
                        Score: {score} / 100
                      </div>
                    )}
                  </>
                )}
              </div>
            )}

            {/* AI Feedback tab */}
            {activeTab === "feedback" && (
              <div style={{
                background: "#060610", border: "1px solid #1a1a2e",
                borderRadius: 8, padding: "10px 12px", fontSize: 12, lineHeight: 1.7,
                color: S.text, whiteSpace: "pre-wrap", minHeight: 60,
              }}>
                {feedbackLoading ? "🤖 Analyzing your code..." : (feedback || "Click 🤖 AI to get feedback on your solution.")}
              </div>
            )}
          </div>

          {/* Stats */}
          {stats && (
            <div style={{
              background: S.cardBg, border: S.border, borderRadius: 10,
              padding: "12px 14px", marginTop: 10, marginBottom: 10,
            }}>
              <div style={{ fontSize: 10, color: S.muted, textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 8 }}>Your Stats</div>
              <div style={{ display: "flex", gap: 20 }}>
                <div>
                  <div style={{ color: S.accent, fontWeight: 700, fontSize: 18 }}>{stats.total_attempts}</div>
                  <div style={{ color: S.muted, fontSize: 10 }}>Attempts</div>
                </div>
                <div>
                  <div style={{ color: S.accent, fontWeight: 700, fontSize: 18 }}>{stats.avg_score}</div>
                  <div style={{ color: S.muted, fontSize: 10 }}>Avg Score</div>
                </div>
              </div>
            </div>
          )}

          {/* History */}
          {history.length > 0 && (
            <div style={{ marginBottom: 10 }}>
              <div style={{ fontSize: 10, color: S.muted, textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 6 }}>History</div>
              {history.slice(0, 5).map((h, i) => (
                <div key={i} style={{
                  display: "flex", justifyContent: "space-between",
                  padding: "5px 0", borderBottom: "1px solid #0f0f1e",
                  fontSize: 11, color: S.muted,
                }}>
                  <span style={{ flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{h.question}</span>
                  <span style={{ color: S.accent, marginLeft: 8 }}>{h.score}</span>
                </div>
              ))}
            </div>
          )}

          {/* Leaderboard */}
          <div>
            <div style={{ fontSize: 10, color: S.muted, textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 6 }}>🏆 Leaderboard</div>
            {leaderboard.length === 0 ? (
              <p style={{ color: S.muted, fontSize: 12 }}>No entries yet.</p>
            ) : leaderboard.slice(0, 5).map((u, i) => (
              <div key={i} style={{
                display: "flex", justifyContent: "space-between", alignItems: "center",
                padding: "6px 10px", marginBottom: 4,
                background: i === 0 ? "rgba(0,255,65,0.06)" : "transparent",
                border: `1px solid ${i === 0 ? "rgba(0,255,65,0.15)" : "#0f0f1e"}`,
                borderRadius: 6, fontSize: 12,
              }}>
                <span style={{ color: i === 0 ? S.accent : S.muted }}>
                  {i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : `${i + 1}.`} {u.username}
                </span>
                <span style={{ color: S.accent, fontWeight: 700 }}>{u.score}</span>
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT PANEL — Editor */}
        <div style={{
          flex: 1, display: isMobile && mobilePanel !== "right" ? "none" : "flex",
          flexDirection: "column", padding: "14px",
          paddingBottom: isMobile ? "70px" : "14px",
          overflow: "hidden",
        }}>
          {/* Editor */}
          <div style={{ flex: 1, minHeight: 0, marginBottom: 12 }}>
            <CodeEditor
              value={code}
              onChange={setCode}
              disabled={actionsDisabled}
              timedOut={timedOut}
            />
          </div>

          {/* Action Buttons — Desktop only (mobile uses fixed bottom bar) */}
          {!isMobile && (
          <div style={{
            display: "flex", gap: 8, flexWrap: "wrap", flexShrink: 0,
          }}>
            {[
              { label: "▶ Run", fn: handleRun, disabled: actionsDisabled, style: {} },
              { label: "🧪 Test", fn: handleTest, disabled: actionsDisabled, style: {} },
              { label: "🤖 AI", fn: handleAI, disabled: actionsDisabled, style: {} },
              { label: "✅ Submit", fn: handleSubmit, disabled: actionsDisabled || !token, style: { background: "rgba(0,255,65,0.15)", border: "1px solid rgba(0,255,65,0.4)", color: S.accent } },
              { label: "⏭ Next", fn: loadQuestion, disabled: backendStatus === "waking", style: timedOut ? { background: S.accent, color: "#000", fontWeight: 700, border: "none" } : {} },
            ].map(({ label, fn, disabled, style }) => (
              <button key={label} onClick={fn} disabled={disabled} style={{
                padding: "9px 16px", fontSize: 12, borderRadius: 6,
                background: "#0c0c1a", color: disabled ? S.muted : S.text,
                border: "1px solid #1e1e35", cursor: disabled ? "not-allowed" : "pointer",
                fontFamily: S.font, transition: "all 0.15s", opacity: disabled ? 0.5 : 1,
                ...style,
              }}
                onMouseEnter={e => { if (!disabled) e.currentTarget.style.borderColor = "rgba(0,255,65,0.3)"; }}
                onMouseLeave={e => { if (!disabled) e.currentTarget.style.borderColor = "#1e1e35"; }}
              >{label}</button>
            ))}
          </div>
          )}
        </div>
      </div>

      {/* MOBILE FIXED BOTTOM ACTION BAR */}
      {isMobile && (
        <div style={{
          position: "fixed", bottom: 0, left: 0, right: 0, zIndex: 100,
          background: "#07070f", borderTop: "1px solid #1a1a2e",
          display: "flex", gap: 0, flexShrink: 0,
          paddingBottom: "env(safe-area-inset-bottom)",
        }}>
          {[
            { label: "▶ Run", fn: handleRun, disabled: actionsDisabled },
            { label: "🧪 Test", fn: handleTest, disabled: actionsDisabled },
            { label: "🤖 AI", fn: handleAI, disabled: actionsDisabled },
            {
              label: "✅ Submit", fn: handleSubmit,
              disabled: actionsDisabled || !token,
              highlight: true,
            },
            {
              label: "⏭ Next", fn: loadQuestion,
              disabled: backendStatus === "waking",
              pulse: timedOut,
            },
          ].map(({ label, fn, disabled, highlight, pulse }) => (
            <button
              key={label}
              onClick={fn}
              disabled={disabled}
              style={{
                flex: 1, padding: "11px 4px", fontSize: 11,
                background: pulse
                  ? S.accent
                  : highlight
                  ? "rgba(0,255,65,0.1)"
                  : "transparent",
                color: pulse ? "#000" : highlight ? S.accent : disabled ? S.muted : S.text,
                border: "none",
                borderRight: "1px solid #1a1a2e",
                cursor: disabled ? "not-allowed" : "pointer",
                fontFamily: S.font,
                fontWeight: pulse ? 700 : 400,
                opacity: disabled ? 0.4 : 1,
                transition: "all 0.15s",
              }}
            >{label}</button>
          ))}
        </div>
      )}

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&display=swap');
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #050508; }
        ::-webkit-scrollbar-thumb { background: #1e1e35; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #2e2e4a; }
        select option { background: #0a0a14; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
}

export default App;