import numpy as np
from sentence_transformers import SentenceTransformer
from app.services.cache_service import get_cache, set_cache

model = SentenceTransformer("all-MiniLM-L6-v2")

SIMILARITY_THRESHOLD = 0.90


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_semantic_cache(text):

    cache_data = get_cache("semantic_cache")

    if not cache_data:
        return None

    embedding = model.encode(text)

    for item in cache_data:

        stored_embedding = np.array(item["embedding"])
        similarity = cosine_similarity(embedding, stored_embedding)

        if similarity >= SIMILARITY_THRESHOLD:
            return item["suggestions"]

    return None


def set_semantic_cache(text, suggestions):

    cache_data = get_cache("semantic_cache") or []

    embedding = model.encode(text)

    cache_data.append({
        "text": text,
        "embedding": embedding.tolist(),
        "suggestions": suggestions
    })

    set_cache("semantic_cache", cache_data)