import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

SIMILARITY_THRESHOLD = 0.80


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def filter_meaning_preserved(original, suggestions):

    original_embedding = model.encode(original)

    valid_suggestions = []

    for s in suggestions:

        emb = model.encode(s)

        similarity = cosine_similarity(original_embedding, emb)

        if similarity >= SIMILARITY_THRESHOLD:
            valid_suggestions.append(s)

    return valid_suggestions