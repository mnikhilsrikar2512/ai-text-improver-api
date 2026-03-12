import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

REDIS_HOST = "localhost"
REDIS_PORT = 6379

CACHE_TTL = 3600

MAX_INPUT_LENGTH = 300
OLLAMA_TIMEOUT = 20
OLLAMA_RETRIES = 2