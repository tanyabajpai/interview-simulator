from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.code import router as code_router
from routes.ai import router as ai_router
from routes.interview import router as interview_router
from routes.attempts import router as attempt_router
from routes.system import router as system_router
from routes.user import router as user_router
from routes.leaderboard import router as leaderboard_router
from routes.questions import router as question_router

app = FastAPI()

# =========================
# 🌐 CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 🚀 ROUTES (FIXED ORDER + PREFIX)
# =========================

# ✅ CORE
app.include_router(code_router, prefix="/code")
app.include_router(ai_router, prefix="/ai")

# ❌ REMOVE ROOT CONFLICT
# OLD (WRONG):
# app.include_router(interview_router, prefix="")

# ✅ FIX:
app.include_router(interview_router, prefix="/interview")

# ✅ QUESTIONS (NOW WILL WORK CORRECTLY)
app.include_router(question_router, prefix="/questions")

# OTHER ROUTES
app.include_router(attempt_router, prefix="/attempts")
app.include_router(system_router)
app.include_router(user_router, prefix="/user")
app.include_router(leaderboard_router, prefix="/leaderboard")


# =========================
# 🏠 HOME
# =========================
@app.get("/")
def home():
    return {"message": "Interview Simulator Backend Running"}


# =========================
# 🔍 DEBUG ROUTES
# =========================
@app.get("/debug/routes")
def list_routes():
    return [route.path for route in app.routes]