import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

state = {"ready": False}

@asynccontextmanager
async def lifespan(app: FastAPI):
    state["ready"] = True
    yield
    state["ready"] = False

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok", "environment": os.getenv("APP_ENV", "unset"), "version": "v2"}

@app.get("/ready")
def readiness():
    return {"ready": state["ready"]}