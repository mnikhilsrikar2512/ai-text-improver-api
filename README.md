```markdown
# AI Text Improvement API

A production-ready AI service that improves short workplace messages such as leave reasons, explanations, and internal communication.  

The system is optimized for **speed, reliability, and minimal AI cost** using a multi-stage routing pipeline that reduces unnecessary LLM calls.

---

# Architecture

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

---

# Key Features

- Local AI model (no external API keys)
- Redis caching for fast responses
- Semantic similarity routing
- Rule-based fast responses
- Vector-based intent router
- Adaptive learning from new requests
- LLM fallback for complex inputs
- Rate limiting for API protection
- Request metrics tracking
- Latency monitoring
- Production-ready FastAPI architecture

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| API Framework | FastAPI |
| Language | Python |
| Local LLM | Ollama |
| Embeddings | Sentence Transformers |
| Cache | Redis |
| Public API Testing | ngrok |

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

````

---

# Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/ai-text-improver-api.git
cd ai-text-improver-api
````

Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Start Redis

```bash
redis-server
```

---

# Start Ollama

Install Ollama if not installed:

```bash
brew install ollama
```

Run the model:

```bash
ollama run llama3
```

---

# Run the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# Public API Testing

Expose the API publicly using ngrok:

```bash
ngrok http 8000
```

Example public endpoint:

```
https://xxxxx.ngrok-free.app/improve-text
```

---

# API Request

### Endpoint

```
POST /improve-text
```

### Request Body

```json
{
  "text": "I cant attend meeting today"
}
```

---

# API Response

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

Typical request distribution:

| Source         | Usage  |
| -------------- | ------ |
| Cache          | 40–60% |
| Semantic cache | 15–25% |
| Vector router  | 10–20% |
| Rule engine    | 5–10%  |
| LLM            | <10%   |

This keeps most responses under **50 ms**.

---

# Adaptive Learning

If the router cannot detect an intent, the request goes to the LLM.

After generating a response, the system stores the example in the vector index.

Future similar requests will be routed instantly without using the LLM.

Example:

```
Input:
need leave for cousin wedding
```

First request → LLM

Second request → Vector router (instant response)

---

# Monitoring

### Health Check

```
/health
```

Example:

```json
{
  "api": "ok",
  "redis": "connected",
  "ollama": "running"
}
```

### Metrics

```
/metrics
```

Example:

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

The API is designed to integrate easily with enterprise portals.

Example request:

```
POST /improve-text
```

Body:

```json
{
  "text": "family function"
}
```

The frontend cycles through suggestions using **Accept / Reject** behavior.

---

# License

MIT License

---

# Future Improvements

* Persistent vector database (FAISS / pgvector)
* Request tracing
* Prometheus monitoring
* Async Redis
* Kubernetes deployment
* Streaming responses
* Confidence scoring
* Intent classification model

```
```
