from app.agents.rag_fitness_agent import RagFitnessAgent
from app.agents.exercise_mapping_agent import ExerciseMappingAgent
from app.agents.facility_agent import FacilityAgent

class AIOrchestrator:

    def __init__(self):
        self.rag_agent = RagFitnessAgent()
        self.exercise_agent = ExerciseMappingAgent()
        self.facility_agent = FacilityAgent()

    def run(self, user_input, location):
        """
        1) RAG에서 유사 체력군 검색
        2) pres_note에서 운동 카테고리 추출
        3) 운동 카테고리 기반 시설 추천
        """
        # 1) 유사 체력 검색
        rag_result = self.rag_agent.run(user_input)

        # 2) 운동 매핑
        categories = self.exercise_agent.map_prescription(rag_result.prescription)

        # 3) 시설 추천
        facility_results = self.facility_agent.recommend(
            categories, 
            sido=location.sido,
            sigungu=location.sigungu
        )

        return {
            "similar_profile": rag_result.dict(),
            "exercise_categories": categories,
            "facility_recommendations": facility_results
        }
