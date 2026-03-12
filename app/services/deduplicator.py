from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def deduplicate_suggestions(suggestions):

    unique = []

    embeddings = [model.encode(s) for s in suggestions]

    for i, s in enumerate(suggestions):

        duplicate = False

        for j, u in enumerate(unique):

            sim = cosine_similarity(
                embeddings[i],
                model.encode(u)
            )

            if sim > 0.95:
                duplicate = True
                break

        if not duplicate:
            unique.append(s)

    return unique[:3]