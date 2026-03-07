import os
import json
import shutil
import chromadb
from openai import OpenAI
import tiktoken

DATASET_PATH = os.path.join(os.path.dirname(__file__), "fitness_data.jsonl")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "fr_chroma_db")

client = OpenAI()
enc = tiktoken.get_encoding("cl100k_base")

BATCH_SIZE = 1000
MAX_TOKENS = 8000
LIMIT = 10000   # ★ 1만 건 제한


def truncate_text(text, max_tokens=MAX_TOKENS):
    tokens = enc.encode(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return enc.decode(tokens)


def clean_metadata(meta):
    if isinstance(meta, dict):
        return meta
    return {"value": str(meta)}


def embed_batch(text_list):
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text_list
    )
    return [d.embedding for d in res.data]


def save_batch_in_chroma(collection, texts, metas, start_id, batch_index):
    print(f"[배치 {batch_index}] OpenAI 임베딩 요청 ({len(texts)}개)")

    vectors = embed_batch(texts)
    ids = [str(start_id + i) for i in range(len(texts))]

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metas,
        embeddings=vectors
    )

    print(f"[배치 {batch_index}] 저장 완료: {ids[0]} ~ {ids[-1]}")


def build_vector_db():

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"파일 없음: {DATASET_PATH}")

    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    chroma = chromadb.PersistentClient(CHROMA_DIR)
    collection = chroma.get_or_create_collection("fitness")

    buf_texts = []
    buf_metas = []
    current_id = 0
    batch_index = 0
    total_count = 0  # ★ 현재까지 저장한 개수 추적

    print("=== 1만 건 제한 인덱싱 시작 ===")

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if total_count >= LIMIT:
                break

            line = line.strip()
            if not line:
                continue

            item = json.loads(line)

            text = "\n".join([f"{k}: {v}" for k, v in item.items()])
            text = truncate_text(text)

            buf_texts.append(text)
            buf_metas.append(clean_metadata(item))
            total_count += 1  # ★ 증가

            # 배치 단위 처리
            if len(buf_texts) >= BATCH_SIZE:
                save_batch_in_chroma(collection, buf_texts, buf_metas, current_id, batch_index)
                current_id += len(buf_texts)
                batch_index += 1
                buf_texts = []
                buf_metas = []

        # 마지막 남은 문서 처리
        if buf_texts:
            save_batch_in_chroma(collection, buf_texts, buf_metas, current_id, batch_index)

    print("=== 1만 건 인덱싱 완료 ===")


if __name__ == "__main__":
    build_vector_db()
