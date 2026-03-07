# test.py

from app.rag.rag_search_engine import FitnessRAGEngine

engine = FitnessRAGEngine()
print("🔥 검색 시작")

# --- 1) 간단한 검색 테스트 ---
res = engine.search(
    query="체력 테스트 결과가 유사한 사람 찾기",
    top_k=5
)

print("\n🔍 검색 결과 5개 출력:")
for i, item in enumerate(res):
    print(f"\n[{i+1}] ID={item['id']}")
    meta = item["metadata"]
    print("pres_note:", meta.get("pres_note", "(없음)"))

# --- 2) 전체 DB의 pres_note 통계 체크 ---
all_data = engine.collection.get(include=["metadatas"])

count_total = len(all_data["metadatas"])
count_with_note = sum(
    1 for m in all_data["metadatas"] 
    if "pres_note" in m and str(m["pres_note"]).strip() not in ("", "(운동 처방 없음)")
)

print("\n📊 전체 문서 수:", count_total)
print("📌 pres_note 있는 문서 수:", count_with_note)
print("📌 pres_note 비율:", f"{(count_with_note / count_total) * 100:.2f} %")
