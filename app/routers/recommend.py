# app/routers/recommend.py

from fastapi import APIRouter
from app.agents.rag_fitness_agent import RagFitnessAgent
from app.agents.recommend_fitness_agent import RecommendFitnessAgent
from app.agents.facility_agent import FacilityRecommendAgent
from app.utils.geocode import geocode
import json

router = APIRouter()


@router.post("/api/rag/fitness")
def recommend_fitness(user_input: dict):
    """
    1) RAG → 유사 체력 + pres_note
    2) 운동 추천
    3) 시설 추천(주소 → 위경도 변환 포함)
    """

    # ------------------------------------------------
    # 1) RAG 기반 운동 처방
    # ------------------------------------------------
    rag_agent = RagFitnessAgent()
    rag_result = rag_agent.run(user_input)

    similar_users = rag_result.get("similar_users", [])
    prescriptions = rag_result.get("prescriptions", [])

    if not prescriptions:
        return {
            "error": "유사한 데이터를 찾을 수 없습니다.",
            "similar_users": [],
            "prescriptions": []
        }

    pres_note = prescriptions[0]

    # ------------------------------------------------
    # 2) 운동 추천
    # ------------------------------------------------
    exercise_agent = RecommendFitnessAgent()
    exercise_json_str = exercise_agent.recommend_exercises(pres_note)
    exercise_json = json.loads(exercise_json_str)

    recommended_list = exercise_json.get("recommended_exercises", [])
    if not recommended_list:
        return {
            "similar_users": similar_users,
            "pres_note": pres_note,
            "exercise_recommendation": exercise_json,
            "facility_recommendation": []
        }

    top_exercise = recommended_list[0]["name"]

    # ------------------------------------------------
    # 3) 시설 추천 (주소 → 위경도 변환)
    # ------------------------------------------------
    facility_agent = FacilityRecommendAgent()

    # 3-1) 우선 주소 기반 변환
    user_lat = None
    user_lon = None

    if "address" in user_input and user_input["address"]:
        geo = geocode(user_input["address"])
        if geo:
            user_lat = geo["lat"]
            user_lon = geo["lon"]

    # 3-2) 주소 변환 실패 → lat/lon 직접 입력 사용
    if user_lat is None or user_lon is None:
        user_lat = float(user_input.get("lat", 37.5665))
        user_lon = float(user_input.get("lon", 126.9780))

    # 3-3) 거리 제한
    distance_limit = float(user_input.get("distanceLimit", 10))

    # 3-4) 시설 타입
    facility_type = user_input.get("facilityType", "public_all")

    # 3-5) 시설 추천 호출
    facilities = facility_agent.recommend_facilities(
        exercise_name=top_exercise,
        user_lat=user_lat,
        user_lon=user_lon,
        facility_type=facility_type,
        limit=20,               # 내부에서 거리로 필터링하므로 조회 수는 늘려도 됨
        max_distance_km=distance_limit
    )

    # ------------------------------------------------
    # 4) 최종 반환
    # ------------------------------------------------
    return {
        "similar_users": similar_users,
        "pres_note": pres_note,
        "exercise_recommendation": exercise_json,
        "facility_recommendation": facilities
    }
