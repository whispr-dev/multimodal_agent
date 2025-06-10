import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class MemoryEngine:
    def __init__(self, index_path="data/embeddings/memory.index"):
        os.makedirs("data/embeddings", exist_ok=True)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index_path = index_path
        self.index = faiss.IndexFlatL2(384)
        self.data = []

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)

    def embed(self, text):
        return self.model.encode([text])[0]

    def store(self, vision, audio, mood, reply):
        entry = f"[Vision] {vision} [Audio] {audio} [Mood] {mood} [Reply] {reply}"
        vec = self.embed(entry)
        self.index.add(np.array([vec]).astype("float32"))
        self.data.append(entry)

    def query_recent(self, context, k=3):
        vec = self.embed(context)
        D, I = self.index.search(np.array([vec]).astype("float32"), k)
        return "\\n".join([self.data[i] for i in I[0] if i < len(self.data)])

    def save(self):
        faiss.write_index(self.index, self.index_path)