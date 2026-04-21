# AI Text Improver API

An AI-powered backend application that enhances user-provided text by improving grammar, clarity, tone, and overall readability.

## 🧠 How It Works

The system processes user input text and applies NLP-based transformations to:
1. Detect grammatical issues  
2. Improve sentence structure  
3. Adjust tone and readability  
4. Return optimized output  

# Features

- Local AI model (no external API keys required)
- FastAPI production architecture
- Redis caching for fast responses
- Semantic similarity cache
- Vector intent router
- Rule-based fast responses
- Adaptive learning from new requests
- LLM fallback for complex inputs
- Request metrics monitoring
- Rate limiting
- Latency tracking
- Swagger API documentation

## 📌 Use Cases

- AI assistants  
- Customer support automation  
- Knowledge base search  
- Content enhancement tools  

---

# Architecture

The API uses a **layered routing system** to minimize expensive LLM calls.

```
Client Request
      │
      ▼
Rate Limiter
      │
      ▼
Input Validation + Normalization
      │
      ▼
Redis Exact Cache
      │
      ▼
Rule Engine
      │
      ▼
Semantic Cache
      │
      ▼
Vector Intent Router
      │
      ▼
Local LLM (Ollama)
      │
      ▼
Deduplication
      │
      ▼
Cache + Metrics + Response
```

This architecture ensures that most requests are resolved in **under 50ms**.

---

# Tech Stack

| Component | Technology |
|----------|-------------|
| API Framework | FastAPI |
| Programming Language | Python |
| LLM | Ollama |
| Embeddings | Sentence Transformers |
| Cache | Redis |
| Public API Testing | ngrok |
| Metrics | Custom counters |

---

# Project Structure

```
ai-text-improver-api
│
├── app
│   ├── api
│   │   └── routes.py
│   │
│   ├── services
│   │   ├── ai_service.py
│   │   ├── cache_service.py
│   │   ├── semantic_cache.py
│   │   ├── rule_engine.py
│   │   ├── vector_index.py
│   │   ├── template_service.py
│   │   ├── validation_service.py
│   │   ├── deduplicator.py
│   │   ├── metrics.py
│   │   └── rate_limiter.py
│   │
│   ├── models
│   │   └── schemas.py
│   │
│   ├── utils
│   │   └── logger.py
│   │
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository.

```bash
git clone https://github.com/YOUR_USERNAME/ai-text-improver-api.git
cd ai-text-improver-api
```

Create a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Start Redis

Run Redis locally.

```bash
redis-server
```

---

# Start Ollama

Install Ollama if not installed.

```bash
brew install ollama
```

Run the model.

```bash
ollama run llama3
```

---

# Run the API

Start the FastAPI server.

```bash
uvicorn app.main:app --reload
```

Open Swagger UI.

```
http://127.0.0.1:8000/docs
```

---

# Public API Testing

Expose the API publicly using **ngrok**.

```bash
ngrok http 8000
```

Example public endpoint.

```
https://xxxxx.ngrok-free.app/improve-text
```

---

# API Usage

### Endpoint

```
POST /improve-text
```

### Request

```json
{
  "text": "I cant attend meeting today"
}
```

### Response

```json
{
  "original": "I cant attend meeting today",
  "suggestions": [
    "I will be unable to attend today's meeting.",
    "Unfortunately, I cannot attend the meeting today.",
    "I regret that I will not be able to attend today's meeting."
  ],
  "cached": false,
  "latency_ms": 320
}
```

---

# Performance Optimization

The system avoids unnecessary LLM calls using layered routing.

Typical production distribution:

| Source | Usage |
|------|------|
Cache | 40-60% |
Semantic cache | 15-25% |
Vector router | 10-20% |
Rule engine | 5-10% |
LLM | <10% |

This keeps the **average response latency extremely low**.

---

# Adaptive Learning

If the router cannot detect an intent, the request is processed by the LLM.

The system then stores the example in the vector index so future requests are routed instantly.

Example:

```
Input:
need leave for cousin wedding
```

First request → LLM

Second request → Vector Router

Latency drops from **~1s to ~20ms**.

---

# Monitoring

## Health Check

```
GET /health
```

Example response.

```json
{
  "api": "ok",
  "redis": "connected",
  "ollama": "running"
}
```

---

## Metrics

```
GET /metrics
```

Example output.

```json
{
  "requests_total": 120,
  "cache_hits": 70,
  "semantic_hits": 20,
  "router_hits": 15,
  "rule_hits": 10,
  "llm_calls": 5
}
```

---

# Integration Example (.NET)

This API is designed to integrate easily with enterprise portals.

Example request from a frontend.

```json
{
  "text": "family function"
}
```

The UI can cycle through suggestions using **Accept / Reject** buttons.

---

# Future Improvements

Possible upgrades:

- Persistent vector database (FAISS or pgvector)
- Prometheus metrics
- Request tracing
- Async Redis
- Kubernetes deployment
- Streaming responses
- Confidence scoring
- Intent classification model

---

# License

MIT License
