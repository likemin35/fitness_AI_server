from app.rag.rag_search_engine import FitnessRAGEngine


class RagFitnessAgent:
    def __init__(self):
        self.rag = FitnessRAGEngine()

    def _build_query(self, user_input: dict) -> str:
        parts = []

        age_class = user_input.get("ageClass")
        test_sex = user_input.get("testSex")
        test_ym = user_input.get("testYm")

        if age_class is not None:
            parts.append(f"ageClass={age_class}")
        if test_sex:
            parts.append(f"testSex={test_sex}")
        if test_ym:
            parts.append(f"testYm={test_ym}")

        metric_items = []
        for key in sorted(user_input.keys()):
            value = user_input.get(key)
            if key.startswith("item") and value is not None:
                metric_items.append(f"{key}={value}")

        parts.extend(metric_items[:12])

        if not parts:
            return "국민체력100 운동 처방 추천"

        return " | ".join(parts)

    def run(self, user_input: dict):
        query = self._build_query(user_input)

        try:
            results = self.rag.search(query, top_k=5)
        except Exception:
            return {
                "query": query,
                "similar_users": [],
                "prescriptions": [],
            }

        similar_users = []
        prescriptions = []

        for result in results:
            metadata = result.get("metadata") or {}
            similar_users.append(metadata)

            pres_note = str(metadata.get("pres_note", "")).strip()
            if pres_note:
                prescriptions.append(pres_note)

        return {
            "query": query,
            "similar_users": similar_users,
            "prescriptions": prescriptions,
        }
