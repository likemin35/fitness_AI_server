from app.agents.exercise_mapping_agent import ExerciseMappingAgent
from app.agents.facility_agent import FacilityAgent
from app.agents.rag_fitness_agent import RagFitnessAgent


class AIOrchestrator:
    def __init__(self):
        self.rag_agent = RagFitnessAgent()
        self.exercise_agent = ExerciseMappingAgent()
        self.facility_agent = FacilityAgent()

    def run(self, user_input, location):
        rag_result = self.rag_agent.run(user_input)
        prescriptions = rag_result.get("prescriptions", [])
        pres_note = prescriptions[0] if prescriptions else ""
        exercise_categories = self.exercise_agent.map_prescription(pres_note)

        facilities = []
        if exercise_categories and location:
            facilities = self.facility_agent.recommend_facilities(
                exercise_name=exercise_categories[0],
                user_lat=location.get("lat", 37.5665),
                user_lon=location.get("lon", 126.9780),
                facility_type=location.get("facilityType", "public_all"),
                max_distance_km=location.get("distanceLimit", 10),
            )

        return {
            "similar_profile": rag_result,
            "exercise_categories": exercise_categories,
            "facility_recommendations": facilities,
        }
