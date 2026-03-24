import json

from fastapi import APIRouter

from app.agents.rag_fitness_agent import RagFitnessAgent
from app.agents.recommend_fitness_agent import RecommendFitnessAgent

router = APIRouter()


@router.post("/api/recommend/fitness")
@router.post("/api/rag/fitness")
def recommend_fitness(user_input: dict):
    rag_agent = RagFitnessAgent()
    rag_result = rag_agent.run(user_input or {})

    similar_users = rag_result.get("similar_users", [])
    prescriptions = rag_result.get("prescriptions", [])
    pres_note = prescriptions[0] if prescriptions else ""

    exercise_agent = RecommendFitnessAgent()
    exercise_json_str = exercise_agent.recommend_exercises(pres_note)

    try:
        exercise_json = json.loads(exercise_json_str)
    except json.JSONDecodeError:
        exercise_json = {"recommended_exercises": []}

    return {
        "similar_users": similar_users,
        "pres_note": pres_note,
        "exercise_recommendation": exercise_json,
    }
