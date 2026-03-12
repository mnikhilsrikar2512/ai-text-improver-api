from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

INTENTS = {
    "sick_leave": [
        "sick leave",
        "not feeling well",
        "fever",
        "medical leave"
    ],
    "family_leave": [
        "family function",
        "family matter",
        "family commitment",
        "family emergency"
    ],
    "meeting_absence": [
        "cannot attend meeting",
        "miss meeting",
        "meeting absence",
        "unable to join meeting"
    ]
}

intent_vectors = {}

for intent, phrases in INTENTS.items():
    intent_vectors[intent] = model.encode(phrases)

SIMILARITY_THRESHOLD = 0.65


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search_intent(text):

    query_vector = model.encode(text)

    best_intent = None
    best_score = 0

    for intent, vectors in intent_vectors.items():

        for vec in vectors:

            score = cosine_similarity(query_vector, vec)

            if score > best_score:
                best_score = score
                best_intent = intent

    if best_score >= SIMILARITY_THRESHOLD:
        return best_intent

    return None


def learn_new_example(text, intent):

    if intent not in INTENTS:
        INTENTS[intent] = []
        intent_vectors[intent] = []

    INTENTS[intent].append(text)

    vector = model.encode(text)

    if isinstance(intent_vectors[intent], list):
        intent_vectors[intent].append(vector)
    else:
        intent_vectors[intent] = np.vstack([intent_vectors[intent], vector])