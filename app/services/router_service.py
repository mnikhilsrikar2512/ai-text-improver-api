from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


INTENT_PATTERNS = {
    "sick_leave": [
        "sick leave",
        "I am sick today",
        "not feeling well today"
    ],
    "family_leave": [
        "family function",
        "family matter",
        "family commitment"
    ],
    "meeting_absence": [
        "cannot attend meeting",
        "unable to attend meeting",
        "can't attend meeting"
    ]
}


def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


pattern_embeddings = {}

for key, patterns in INTENT_PATTERNS.items():
    pattern_embeddings[key] = model.encode(patterns)


def detect_intent(text):

    text_embedding = model.encode(text)

    best_intent = None
    best_score = 0

    for intent, embeds in pattern_embeddings.items():

        for emb in embeds:

            score = cosine(text_embedding, emb)

            if score > best_score:
                best_score = score
                best_intent = intent

    if best_score > 0.80:
        return best_intent

    return None