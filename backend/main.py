from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ROUTES
from routes.code import router as code_router
from routes.ai import router as ai_router
from routes.interview import router as interview_router
from routes.attempts import router as attempt_router
from routes.system import router as system_router
from routes.user import router as user_router
from routes.leaderboard import router as leaderboard_router
from routes.questions import router as question_router

app = FastAPI(
    title="Interview Simulator API",
    version="1.0.0"
)

# =========================
# 🌐 CORS (Frontend ready)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 🚀 ROUTES (CLEAN STRUCTURE)
# =========================

# CORE
app.include_router(code_router, prefix="/code", tags=["Code"])
app.include_router(ai_router, prefix="/ai", tags=["AI"])

# INTERVIEW FLOW
app.include_router(interview_router, prefix="/interview", tags=["Interview"])
app.include_router(question_router, prefix="/questions", tags=["Questions"])

# USER SYSTEM
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(leaderboard_router, prefix="/leaderboard", tags=["Leaderboard"])

# OTHER
app.include_router(attempt_router, prefix="/attempts", tags=["Attempts"])
app.include_router(system_router, tags=["System"])

# =========================
# 🏠 HOME
# =========================
@app.get("/")
def home():
    return {"message": "Interview Simulator Backend Running 🚀"}

# =========================
# 🔍 DEBUG ROUTES
# =========================
@app.get("/debug/routes")
def list_routes():
    return [route.path for route in app.routes]