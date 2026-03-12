import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

INTENT_LIBRARY = {
    "sick_leave": [
        "sick leave",
        "i am sick today",
        "not feeling well today",
        "i have fever today"
    ],
    "family_leave": [
        "family function",
        "family commitment",
        "family matter",
        "need leave for family"
    ],
    "meeting_absence": [
        "cannot attend meeting",
        "cant attend meeting",
        "unable to attend meeting",
        "miss meeting today"
    ]
}

phrases = []
labels = []

for intent, samples in INTENT_LIBRARY.items():
    for phrase in samples:
        phrases.append(phrase)
        labels.append(intent)

embeddings = model.encode(phrases)
embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)


def search_intent(text):

    query = model.encode([text]).astype("float32")

    distances, indices = index.search(query, 1)

    score = distances[0][0]
    intent = labels[indices[0][0]]

    if score < 1.2:
        return intent

    return None