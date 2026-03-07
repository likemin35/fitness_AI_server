import chromadb

client = chromadb.PersistentClient(path="./fr_chroma_db")
collection = client.get_collection("fitness")   # embedding_function 제거

res = collection.peek()
peek_dim = len(res["embeddings"][0])
print("현재 저장된 차원:", peek_dim)
