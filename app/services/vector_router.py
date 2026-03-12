from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

INTENT_LIBRARY = {
    "sick_leave": [
        "sick leave",
        "I am sick today",
        "not feeling well today",
        "I have fever today"
    ],
    "family_leave": [
        "family function",
        "family matter",
        "family commitment",
        "need leave for family"
    ],
    "meeting_absence": [
        "cannot attend meeting",
        "can't attend meeting",
        "unable to attend meeting",
        "miss meeting today"
    ]
}


def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


intent_vectors = {}

for intent, phrases in INTENT_LIBRARY.items():
    intent_vectors[intent] = model.encode(phrases)


def detect_intent_vector(text):

    query = model.encode(text)

    best_intent = None
    best_score = 0

    for intent, vectors in intent_vectors.items():

        for vec in vectors:

            score = cosine(query, vec)

            if score > best_score:
                best_score = score
                best_intent = intent

    if best_score > 0.82:
        return best_intent

    return None