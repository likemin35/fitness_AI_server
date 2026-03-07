# app/models/facility_recommend_request.py

from pydantic import BaseModel

class FacilityRecommendRequest(BaseModel):
    exerciseName: str
    address: str | None = None
    lat: float | None = None
    lon: float | None = None
    distanceLimit: float = 10
    facilityType: str = "public_all"
