from fastapi import APIRouter

router = APIRouter(prefix="/api/map-exercise")

@router.get("/mapping")
def map_exercise(exercise: str):
    mapping = {
        "유산소": ["걷기", "조깅", "자전거"],
        "근력": ["스쿼트", "벤치프레스", "풀업"]
    }
    return {"mapped": mapping.get(exercise, [])}
