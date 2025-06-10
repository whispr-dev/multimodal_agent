import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

def load_index(index_path):
    if os.path.exists(index_path):
        return faiss.read_index(index_path)
    else:
        return faiss.IndexFlatL2(384)  # use 384 or 768 depending on embedding model

class MemoryEngine:
    def __init__(self, index_path="data/memory.index"):
        self.index_path = index_path
        self.embeddings = SentenceTransformer("all-MiniLM-L6-v2")
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            self.index = faiss.IndexFlatL2(384)  # for MiniLM
        self.texts = []
        self.history = []

    def add_memory(self, text):
        embedding = self.embeddings.encode(text)
        self.index.add(np.array([embedding], dtype=np.float32))
        self.texts.append(text)
        self.history.append(text)
        self.save()

    def search_memory(self, query, k=5):
        query_embedding = self.embeddings.embed_query(query)
        D, I = self.index.search(np.array([query_embedding], dtype=np.float32), k)
        results = [self.texts[i] for i in I[0] if i < len(self.texts)]
        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)

    def store(self, speaker, input_text, emotion, response):
        content = f"{speaker}: {input_text}\nEmotion: {emotion}\nResponse: {response}"
        self.add_memory(content)

    def _save_index(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + '.pkl', 'wb') as f:
            pickle.dump(self.memory_data, f)

    def query_recent(self, prompt):
        if not self.history:
            return ""
        return "\n".join(self.history[-5:])  # Last 5 messages
