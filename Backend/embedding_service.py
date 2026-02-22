from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

# Load embedding model (Day-6 requirement)
model = SentenceTransformer("all-MiniLM-L6-v2")

index = None
stored_chunks = []


def create_embeddings(chunks):
    global index, stored_chunks

    stored_chunks = chunks

    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    return len(chunks)


def search_similar_chunks(query, top_k=3):
    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), top_k)

    results = [stored_chunks[i] for i in indices[0]]

    return results


def save_index(path="faiss_index"):
    if not os.path.exists(path):
        os.makedirs(path)

    faiss.write_index(index, f"{path}/index.faiss")

    with open(f"{path}/chunks.pkl", "wb") as f:
        pickle.dump(stored_chunks, f)


def load_index(path="faiss_index"):
    global index, stored_chunks

    index = faiss.read_index(f"{path}/index.faiss")

    with open(f"{path}/chunks.pkl", "rb") as f:
        stored_chunks = pickle.load(f)

def index_exists(path="faiss_index"):
    return os.path.exists(f"{path}/index.faiss")

