# app/agents/unified_fitness_agent.py

import json
from langchain_openai import ChatOpenAI
from app.rag.rag_search_engine import FitnessRAGEngine


class UnifiedFitnessAgent:

    def __init__(self):
        # RAG 엔진
        self.rag = FitnessRAGEngine()

        # 운동 추천 LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3
        )

    def run(self, user_input: dict):

        # 1) RAG 검색
        results = self.rag.search("체력 테스트 결과가 비슷한 사람", top_k=5)

        similar_users = []
        prescriptions = []

        for r in results:
            meta = r["metadata"]
            similar_users.append(meta)

            pres = meta.get("pres_note", "(운동 처방 없음)")
            prescriptions.append(pres)

        # 2) pres_note 선택
        if prescriptions:
            selected_pres_note = prescriptions[0]
        else:
            selected_pres_note = "기초 체력 증진이 필요한 사용자입니다."

        # 로그 출력
        print("🔥 selected_pres_note:", selected_pres_note)
        print("🔥 similar_users:", similar_users)

        # 3) LLM 운동 종목 추천
        prompt = f"""
        당신은 전문 운동처방사입니다.

        아래는 사용자의 운동 처방 기록입니다:

        [처방 내용]
        {selected_pres_note}

        ### 매우 중요한 규칙 ###
        당신이 추천해야 하는 것은 **운동 동작이 아니라 시설 종목**입니다.

        ### 출력 형식 (JSON ONLY) ###
        {{
          "recommended_exercises": [
              {{"name": "종목명1", "reason": "추천 이유"}},
              {{"name": "종목명2", "reason": "추천 이유"}},
              {{"name": "종목명3", "reason": "추천 이유"}}
          ]
        }}
        """

        llm_raw = self.llm.invoke(prompt).content

        try:
            exercise_recommendation = json.loads(llm_raw)
        except:
            exercise_recommendation = {"recommended_exercises": []}

        print("🔥 exercise_recommendation:", exercise_recommendation)

        # 4) 최종 응답
        return {
            "pres_note": selected_pres_note,
            "exercise_recommendation": exercise_recommendation,
            "similar_users": similar_users
        }
