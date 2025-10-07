import os, numpy as np
from typing import List, Dict
from .utils import load_materia_medica, save_json, load_json
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

API_BASE = os.getenv("API_BASE", "https://api.openai.com/v1")
EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
INDEX_PATH = os.getenv("EMBED_INDEX_PATH", "./data/mm_index.json")
MM_DIR = os.getenv("MM_DIR", "../data/materia_medica")

def _client():
    if OpenAI is None:
        raise RuntimeError("openai package not installed")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=API_BASE)

def embed_texts(texts: List[str]) -> List[List[float]]:
    client = _client()
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]

def build_index() -> Dict:
    docs = load_materia_medica(MM_DIR)
    texts = [d["text"] for d in docs]
    vecs = embed_texts(texts)
    index = {"docs": docs, "vectors": vecs}
    save_json(INDEX_PATH, index)
    return index

def load_index() -> Dict:
    return load_json(INDEX_PATH, default={"docs": [], "vectors": []})

def search(query: str, k: int = 5) -> List[Dict]:
    index = load_index()
    if not index["docs"]:
        index = build_index()
    qvec = np.array(embed_texts([query])[0])
    scores = []
    for i, v in enumerate(index["vectors"]):
        vec = np.array(v)
        # cosine similarity
        sim = float(qvec @ vec / (np.linalg.norm(qvec) * np.linalg.norm(vec) + 1e-8))
        scores.append((i, sim))
    scores.sort(key=lambda x: x[1], reverse=True)
    out = []
    for i, sim in scores[:k]:
        doc = index["docs"][i]
        out.append({"id": doc["id"], "title": doc["title"], "similarity": sim, "excerpt": doc["text"][:600]})
    return out
