# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 🔥 .env 로딩
load_dotenv()

# 🔥 FastAPI 인스턴스 생성
app = FastAPI()

# 🔥 CORS 미들웨어 (라우터 포함보다 반드시 위에 있어야 함)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 개발 단계 전체 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 라우터 Import는 미들웨어보다 아래
from app.routers import recommend, map_exercise, facilities

app.include_router(recommend.router)
app.include_router(map_exercise.router)
app.include_router(facilities.router)


@app.get("/")
def root():
    return {"status": "Fitness AI Server Running"}
