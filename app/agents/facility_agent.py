import os
import math
import requests
import mysql.connector


# -------------------------------------------------------------
# 추천 운동 → 시설 카테고리 매핑
# -------------------------------------------------------------
EXERCISE_CATEGORY_MAP = {
    "헬스": ["헬스", "체력단련장"],
    "웨이트": ["헬스", "체력단련장"],
    "PT": ["헬스", "체력단련장"],
    "크로스핏": ["크로스핏", "체력단련장"],
    "요가": ["요가"],
    "필라테스": ["필라테스"],
    "스트레칭": ["요가", "필라테스", "스트레칭"],
    "수영": ["수영", "아쿠아"],
    "아쿠아": ["수영", "아쿠아"],
    "에어로빅": ["에어로빅"],
    "런닝": ["헬스", "체력단련장"],  # 트레드밀이 헬스장에 있음
    "조깅": ["헬스", "체력단련장"],
    "스피닝": ["사이클", "스피닝"],
}


class FacilityRecommendAgent:

    def __init__(self):
        self.base_config = {
            "host": os.getenv("MYSQL_HOST", "localhost"),
            "user": os.getenv("MYSQL_USER", "root"),
            "password": os.getenv("MYSQL_PASSWORD", "1234"),
            "database": "fitnessdb"
        }

        # 테이블 매핑
        self.TABLE_MAP = {
            "public_all": "facility_public",        # 전국 체육시설 (기본값)
            "public": "facility_public",
            "private": "facility_private",
            "onepass": "onepass_facility",
            "voucher_facility": "voucher_facility",
            "voucher_course": "voucher_course"
        }

    # -------------------------------------------------------------
    # 주소 → 위도/경도 변환 (카카오 API)
    # -------------------------------------------------------------
    def geocode_address(self, address: str):
        KAKAO_KEY = os.getenv("KAKAO_REST_KEY")
        if not KAKAO_KEY:
            raise ValueError("카카오 REST API 키가 필요합니다.")

        url = "https://dapi.kakao.com/v2/local/search/address.json"
        headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}

        res = requests.get(url, headers=headers, params={"query": address})
        data = res.json()

        if "documents" not in data or len(data["documents"]) == 0:
            raise ValueError("주소를 변환할 수 없습니다.")

        lat = float(data["documents"][0]["y"])
        lon = float(data["documents"][0]["x"])
        return lat, lon

    # -------------------------------------------------------------
    # 거리 계산
    # -------------------------------------------------------------
    def _calc_distance(self, lat1, lon1, lat2, lon2):
        R = 6371
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = (math.sin(d_lat / 2) ** 2 +
             math.cos(math.radians(lat1)) *
             math.cos(math.radians(lat2)) *
             math.sin(d_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    # -------------------------------------------------------------
    # 시설 추천 메인 함수
    # -------------------------------------------------------------
    def recommend_facilities(
            self,
            exercise_name: str,
            user_lat: float,
            user_lon: float,
            facility_type: str = "public_all",
            limit: int = 5,
            max_distance_km: float = 10.0
    ):

        if facility_type not in self.TABLE_MAP:
            raise ValueError(f"지원하지 않는 시설 타입: {facility_type}")

        db_name = self.TABLE_MAP[facility_type]

        # 운동명 → 시설 카테고리 변환
        categories = EXERCISE_CATEGORY_MAP.get(exercise_name, [exercise_name])

        conn = mysql.connector.connect(**self.base_config)
        cursor = conn.cursor(dictionary=True)

        keyword_col = "ftype_nm"
        name_col = "faci_nm"

        sql = f"""
            SELECT 
                {name_col} AS name,
                {keyword_col} AS category,
                faci_lat,
                faci_lot,
                road_addr,
                jibun_addr,
                addr
            FROM {db_name}
            WHERE 
        """

        # 여러 카테고리를 OR 조건으로 추가
        sql_conditions = " OR ".join([f"{keyword_col} LIKE %s" for _ in categories])
        sql = sql + sql_conditions

        like_values = [f"%{c}%" for c in categories]
        cursor.execute(sql, like_values)

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        results = []

        for row in rows:
            try:
                dist = self._calc_distance(
                    user_lat, user_lon,
                    float(row["faci_lat"]), float(row["faci_lot"])
                )
            except:
                continue

            if dist > max_distance_km:
                continue  # 거리 필터

            address = row["road_addr"] or row["jibun_addr"] or row["addr"] or "주소 정보 없음"

            results.append({
                "name": row["name"],
                "category": row["category"],
                "address": address,
                "distance_km": round(dist, 2)
            })

        # 가까운 거리 순 정렬
        return sorted(results, key=lambda x: x["distance_km"])[:limit]
