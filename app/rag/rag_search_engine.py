# app/rag/rag_search_engine.py

import chromadb
from app.rag.rag_engine import CHROMA_DIR
from openai import OpenAI

COLLECTION_NAME = "fitness"
client = OpenAI()

class FitnessRAGEngine:

    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_DIR)
        self.collection = self.client.get_or_create_collection(COLLECTION_NAME)

    def _embed(self, text: str):
        res = client.embeddings.create(
            model="text-embedding-3-small",
            input=[text]
        )
        return res.data[0].embedding

    def search(self, query: str, top_k: int = 5):
        embedding = self._embed(query)

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )

        output = []
        for i in range(len(results["documents"][0])):
            output.append({
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i]
            })
        return output
