# fitness-ai-server

체력 측정 기반 운동 추천과 주변 운동 시설 추천을 제공하는 FastAPI 서버입니다.  
RAG 검색으로 유사 사용자 처방을 찾고, OpenAI 기반 추천 로직으로 운동 종목을 제안한 뒤, MySQL에 저장된 시설 데이터에서 조건에 맞는 시설을 반환합니다.

## Deployment

- AWS EC2에 직접 배포해 운영
- 프론트엔드와는 별도 서버로 관리
- 백엔드 서버와도 별도 레포지토리로 운영

## Overview

- FastAPI 기반 AI API 서버
- ChromaDB 기반 RAG 검색
- OpenAI Embedding + 추천 로직 사용
- Kakao 주소 좌표 변환 사용
- MySQL 시설 데이터 조회 지원

## Tech Stack

- Python
- FastAPI
- Uvicorn
- ChromaDB
- OpenAI API
- MySQL Connector
- Requests

## Project Structure

```text
app/
  agents/        추천 로직, 시설 추천, 오케스트레이션
  models/        요청 DTO
  rag/           ChromaDB 생성/검색 스크립트
  routers/       FastAPI 엔드포인트
  utils/         주소 좌표 변환 등 공통 유틸
app/main.py      FastAPI 앱 진입점
test.py          RAG 검색 테스트 스크립트
```

## Main Endpoints

- `GET /`
  - 서버 상태 확인
- `POST /api/recommend/fitness`
  - 체력 입력값을 받아 유사 사용자, 처방 문구, 추천 운동 종목 반환
- `POST /api/rag/fitness`
  - `/api/recommend/fitness`와 동일한 추천 엔드포인트
- `POST /api/recommend/facility`
  - 주소, 운동 종목, 시설 유형을 받아 주변 시설 추천
- `POST /api/facilities/recommend`
  - `/api/recommend/facility`와 동일한 시설 추천 엔드포인트

## Environment Variables

`.env` 파일 또는 시스템 환경변수로 아래 값을 설정해야 합니다.

```env
OPENAI_API_KEY=your_openai_api_key
KAKAO_REST_API_KEY=your_kakao_rest_api_key
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=1234
```

참고:

- `OPENAI_API_KEY`가 없으면 서버 시작 시 예외가 발생합니다.
- Kakao 키는 `KAKAO_REST_API_KEY` 또는 `KAKAO_REST_KEY` 이름으로 읽습니다.
- 시설 추천은 `fitnessdb` 데이터베이스를 기준으로 동작합니다.

## Install

현재 루트의 `requirements.txt`는 비어 있고, 실제 의존성 목록은 `app/rag/requirements.txt`에 있습니다.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r app/rag/requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

브라우저 또는 Swagger 확인:

- `http://localhost:8000`
- `http://localhost:8000/docs`

## RAG Data

- ChromaDB 저장 경로: `app/rag/fr_chroma_db`
- RAG 검색 엔진: `app/rag/rag_search_engine.py`
- 데이터 적재 스크립트: `app/rag/insert_jsonl_to_mysql.py`
- 검색 테스트 스크립트: `python test.py`

## Facility Recommendation Notes

- 시설 추천은 운동 종목명을 시설 카테고리로 매핑한 뒤 MySQL 테이블을 조회합니다.
- 지원 시설 유형 키:
  - `public_all`
  - `public`
  - `private`
  - `onepass`
  - `voucher_facility`
  - `voucher_course`

## Example Request

운동 추천:

```json
{
  "age": 27,
  "sex": "F",
  "height": 165,
  "weight": 58
}
```

시설 추천:

```json
{
  "exerciseName": "수영",
  "address": "서울특별시 강남구 테헤란로 212",
  "distanceLimit": 10,
  "facilityType": "public"
}
```

## Notes

- 프론트엔드 프로젝트는 현재 로컬 개발 시 이 AI 서버의 `http://localhost:8000`을 직접 호출합니다.
- 운영 환경에서는 AI 서버를 EC2에 직접 배포해 사용 중입니다.
- 배포 전에는 API 키와 DB 접속 정보를 반드시 별도 환경설정으로 분리하는 것을 권장합니다.
