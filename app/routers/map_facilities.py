from fastapi import APIRouter

router = APIRouter(prefix="/api/map-exercise")

EXERCISE_MAPPING = {
    "유산소": ["걷기", "조깅", "자전거", "수영"],
    "근력": ["헬스", "웨이트트레이닝", "크로스핏", "PT"],
    "유연성": ["요가", "필라테스", "스트레칭"],
    "재활": ["필라테스", "요가", "수중운동"],
}


@router.get("/mapping")
def map_exercise(exercise: str):
    return {"mapped": EXERCISE_MAPPING.get(exercise, [exercise])}
