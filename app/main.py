from fastapi import FastAPI
import redis
import requests

from app.api.routes import router
from app.config import REDIS_HOST, REDIS_PORT, OLLAMA_URL
from app.services.ai_service import call_ollama
from app.services.metrics import get_metrics

app = FastAPI(
    title="AI Text Improvement API",
    version="1.0"
)

app.include_router(router)


# ---------------------------------------
# Warm up Ollama model at startup
# ---------------------------------------

@app.on_event("startup")
async def warmup_model():
    try:
        await call_ollama("Hello")
    except Exception:
        pass


# ---------------------------------------
# Health Check Endpoint
# ---------------------------------------

@app.get("/health")
def health():

    status = {
        "api": "ok",
        "redis": "unknown",
        "ollama": "unknown"
    }

    # Check Redis
    try:
        r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True
        )
        r.ping()
        status["redis"] = "connected"
    except Exception:
        status["redis"] = "error"

    # Check Ollama
    try:
        requests.get("http://localhost:11434", timeout=2)
        status["ollama"] = "running"
    except Exception:
        status["ollama"] = "not reachable"

    return status

@app.get("/metrics")
def metrics():
    return get_metrics()