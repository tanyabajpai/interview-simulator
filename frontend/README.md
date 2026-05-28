# < InterviewSim />

> Practice DSA problems with AI-powered feedback, test cases, scoring, and a global leaderboard — no account required.

**Live Demo:** [interview-simulator-frontend.onrender.com](https://interview-simulator-frontend.onrender.com) &nbsp;|&nbsp; **Backend API:** [interview-simulator-backend-6ne6.onrender.com](https://interview-simulator-backend-6ne6.onrender.com/docs)

> ⚠️ Hosted on Render's free tier — the backend may take **20–30 seconds to wake up** on first load. The app will notify you while it's starting.

---

## Features

### 👨‍💻 Coding Environment
- Syntax-highlighted code editor
- Run code instantly and see output
- Structured test cases with pass/fail breakdown
- Name your function anything — the runner handles it automatically
- Works as a guest or logged-in user

### 🧠 AI Feedback
- Intelligent per-submission feedback via Claude
- Highlights logic gaps, edge cases, and optimizations

### 📊 Performance Tracking *(login required)*
- Total attempts and average score
- Full submission history

### 🏆 Leaderboard
- Global ranking across all users
- Updates in real time after each submission

### 🔐 Auth System
- JWT-based login/signup
- Guest mode — submit and get scored without an account
- Protected routes for stats and history

### ⏱️ Interview Simulation
- Built-in countdown timer per question
- Simulates real interview pressure

### 📚 Question Bank
- Easy / Medium / Hard difficulty levels
- Covers core DSA topics: arrays, strings, recursion, sorting, and more

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js, Axios, custom CSS |
| Backend | FastAPI (Python) |
| Database | MongoDB Atlas |
| Auth | JWT (JSON Web Tokens) |
| AI Feedback | Anthropic Claude API |
| Deployment | Render (frontend + backend) |

---

## Project Structure

```
interview-simulator/
├── frontend/
│   └── src/
│       ├── App.js           # Main app — all screens and logic
│       ├── api.js           # Axios API client + wakeUpBackend utility
│       └── App.css          # Global styles
├── backend/
│   ├── main.py              # FastAPI entry point + CORS + route registration
│   ├── routes/
│   │   ├── user.py          # Signup, login, stats, save attempt
│   │   ├── code.py          # Run code, run tests
│   │   ├── ai.py            # AI feedback endpoint
│   │   ├── questions.py     # Question bank by difficulty
│   │   ├── leaderboard.py   # Global leaderboard
│   │   └── attempts.py      # Submission history
│   └── services/
│       ├── auth_service.py  # Password hashing + JWT
│       ├── code_execution.py
│       ├── test_runner.py
│       ├── scorer.py
│       ├── question_bank.py
│       ├── db.py
│       └── deps.py
└── README.md
```

---

## Local Setup

### 1. Clone

```bash
git clone https://github.com/tanyabajpai/interview-simulator.git
cd interview-simulator
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in `/backend`:

```env
MONGO_URI=your_mongodb_atlas_connection_string
SECRET_KEY=your_jwt_secret
ANTHROPIC_API_KEY=your_claude_api_key
```

Run:

```bash
uvicorn main:app --reload
```

API docs available at `http://localhost:8000/docs`

### 3. Frontend

```bash
cd frontend
npm install
npm start
```

App runs at `http://localhost:3000`

> If running locally, update `BASE_URL` in `frontend/src/api.js` to `http://localhost:8000`

---

## API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/user/signup` | No | Register new user |
| POST | `/user/login` | No | Login, returns JWT |
| GET | `/user/stats` | Yes | Total attempts + avg score |
| POST | `/user/save` | Yes | Save a submission |
| GET | `/attempts/history` | Yes | Submission history |
| GET | `/questions/{difficulty}` | No | Get questions by difficulty |
| POST | `/code/run` | No | Execute code, return output |
| POST | `/code/test` | No | Run test cases, return score |
| POST | `/ai/feedback` | No | Get AI feedback on code |
| GET | `/leaderboard/leaderboard` | No | Global leaderboard |
| GET | `/health` | No | Health check (wake-up ping) |

---

## Deployment Notes (Render)

Both services are deployed on Render's free tier:

- **Backend** — Python/FastAPI web service. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Frontend** — Static site built with `npm run build`, served from the `build/` directory

The frontend calls `wakeUpBackend()` before login/signup attempts and on first load, polling `/health` every 3 seconds until the backend responds (up to 60s). This handles Render's cold start gracefully without the user hitting a silent failure.

---

## Roadmap

- [ ] Monaco editor with syntax highlighting
- [ ] Multi-language support (Java, C++)
- [ ] AI-generated question suggestions based on weak areas
- [ ] Real-time multiplayer contests
- [ ] Video interview simulation mode

---

## Author

**Tanya Bajpai** — [github.com/tanyabajpai](https://github.com/tanyabajpai)

---

⭐ If you found this useful, give it a star!