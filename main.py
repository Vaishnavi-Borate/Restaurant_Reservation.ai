from database import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

app = FastAPI(title="Restaurant Reservation AI")

# ✅ Run DB init only on startup event (single process safe)
@app.on_event("startup")
def on_startup():
    init_db()

# CORS
origins = ["http://localhost:8001", "http://127.0.0.1:8001", "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Restaurant Reservation AI Backend Running"}
