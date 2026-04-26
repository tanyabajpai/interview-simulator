# 🚀 AI Interview Simulator

A full-stack **Interview Preparation Platform** that simulates real coding interviews with **AI feedback, scoring, leaderboard, and user analytics**.

---

## 🌟 Features

### 👨‍💻 Coding Environment

* Real-time code editor
* Run code instantly
* Execute structured test cases (public + hidden)
* Supports multiple problem types

---

### 🧠 AI Feedback System

* Intelligent feedback on:

  * Code quality
  * Edge cases
  * Logic improvements
* Highlights missing conditions and optimizations

---

### 📊 Performance Tracking

* Total attempts
* Average score
* Real-time updates after submission

---

### 🏆 Leaderboard

* Global ranking system
* Tracks top performers
* Encourages competitive coding

---

### 🔐 Authentication System

* Secure login/signup using JWT
* Protected routes (stats, submissions)

---

### ⏱️ Interview Simulation

* Built-in timer for each question
* Simulates real interview pressure

---

### 📚 Question System

* Difficulty levels (Easy, Medium, Hard)
* Randomized questions
* Covers core DSA topics

---

### 📜 Submission History

* Track all previous attempts
* Analyze progress over time

---

## 🛠️ Tech Stack

### Frontend

* React.js
* Axios
* CSS (custom UI)

### Backend

* FastAPI
* Python

### Database

* MongoDB (Atlas)

### Authentication

* JWT (JSON Web Tokens)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone [https://github.com/tanyabajpai/interview-simulator]
cd interview-simulator
```

---

### 2️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file:

```env
MONGO_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key
```

Run backend:

```bash
uvicorn main:app --reload
```

---

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm start
```

---

## 🔐 API Endpoints

### Auth

* `POST /user/signup`
* `POST /user/login`

### Coding

* `POST /code/run`
* `POST /code/test`

### AI

* `POST /ai/feedback`

### User

* `POST /user/save`
* `GET /user/stats`

### Leaderboard

* `GET /leaderboard/leaderboard`

---

## 📸 Screenshots

### 🧑‍💻 Coding Interface

<img width="959" height="1022" alt="Screenshot 2026-04-26 132324" src="https://github.com/user-attachments/assets/24893b39-b91b-4960-9590-77049cfe6d37" />

### 📊 Stats Panel

<img width="959" height="1022" alt="Screenshot 2026-04-26 132343" src="https://github.com/user-attachments/assets/7653080d-0eb9-4b47-af11-6914b9aed6c5" />

### 🏆 Leaderboard &AI Feedback

<img width="959" height="1022" alt="Screenshot 2026-04-26 132335" src="https://github.com/user-attachments/assets/cd0c1393-88ad-410f-a059-ba8cf1941707" />

---

## 🚀 Future Improvements

* Multi-language support (Java, C++)
* Code editor with syntax highlighting (Monaco)
* Real-time contests
* AI-based question generation
* Video interview simulation

---

## 👩‍💻 Author

**Tanya Bajpai**

---

## 💡 Why This Project Stands Out

✔ Full-stack implementation
✔ Real-world interview simulation
✔ AI-powered feedback system
✔ Scalable backend design
✔ Clean API architecture

---

⭐ If you like this project, give it a star!
