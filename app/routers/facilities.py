# app/routers/facilities.py

from fastapi import APIRouter
from app.agents.facility_agent import FacilityRecommendAgent
from app.models.facility_recommend_request import FacilityRecommendRequest

router = APIRouter(prefix="/api/facilities")

@router.post("/recommend")
def recommend_facilities(data: FacilityRecommendRequest):
    """
    시설 추천만 별도로 수행하는 API
    (주소 입력 → 위/경도 변환 → 시설 필터링)
    """
    agent = FacilityRecommendAgent()

    # 주소 기반 좌표 변환
    if data.address:
        lat, lon = agent.geocode_address(data.address)
    else:
        lat = data.lat or 37.5665
        lon = data.lon or 126.9780

    facilities = agent.recommend_facilities(
        exercise_name=data.exerciseName,
        user_lat=lat,
        user_lon=lon,
        facility_type=data.facilityType,
        limit=20,
        max_distance_km=data.distanceLimit or 10
    )

    return {"facilities": facilities}