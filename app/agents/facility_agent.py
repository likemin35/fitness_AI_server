import math
import os

import mysql.connector
import requests


EXERCISE_CATEGORY_MAP = {
    "헬스": ["헬스", "체력단련장", "피트니스", "PT"],
    "PT": ["헬스", "체력단련장", "피트니스", "PT"],
    "웨이트트레이닝": ["헬스", "체력단련장", "피트니스"],
    "크로스핏": ["크로스핏", "체력단련장", "피트니스"],
    "요가": ["요가"],
    "필라테스": ["필라테스"],
    "스트레칭": ["요가", "필라테스", "스트레칭"],
    "수영": ["수영", "수영장", "아쿠아"],
    "아쿠아로빅": ["수영", "수영장", "아쿠아"],
    "걷기": ["체력단련장", "헬스"],
    "조깅": ["체력단련장", "헬스"],
    "자전거": ["자전거", "사이클", "스피닝"],
}


class FacilityRecommendAgent:
    def __init__(self):
        self.base_config = {
            "host": os.getenv("MYSQL_HOST", "localhost"),
            "user": os.getenv("MYSQL_USER", "root"),
            "password": os.getenv("MYSQL_PASSWORD", "1234"),
            "database": "fitnessdb",
        }
        self.table_map = {
            "public_all": "facility_public",
            "public": "facility_public",
            "private": "facility_private",
            "onepass": "onepass_facility",
            "voucher_facility": "voucher_facility",
            "voucher_course": "voucher_course",
        }

    def geocode_address(self, address: str):
        kakao_key = os.getenv("KAKAO_REST_KEY") or os.getenv("KAKAO_REST_API_KEY")
        if not kakao_key:
            raise ValueError("Kakao REST API key is required.")

        response = requests.get(
            "https://dapi.kakao.com/v2/local/search/address.json",
            headers={"Authorization": f"KakaoAK {kakao_key}"},
            params={"query": address},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("documents"):
            raise ValueError("Address could not be geocoded.")

        document = data["documents"][0]
        return float(document["y"]), float(document["x"])

    def _calc_distance(self, lat1, lon1, lat2, lon2):
        radius_km = 6371
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = (
            math.sin(d_lat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(d_lon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return radius_km * c

    def recommend_facilities(
        self,
        exercise_name: str,
        user_lat: float,
        user_lon: float,
        facility_type: str = "public_all",
        limit: int = 5,
        max_distance_km: float = 10.0,
    ):
        if facility_type not in self.table_map:
            raise ValueError(f"Unsupported facility type: {facility_type}")

        table_name = self.table_map[facility_type]
        categories = EXERCISE_CATEGORY_MAP.get(exercise_name, [exercise_name])

        conn = mysql.connector.connect(**self.base_config)
        cursor = conn.cursor(dictionary=True)

        sql = f"""
            SELECT
                faci_nm AS name,
                ftype_nm AS facility_type_name,
                faci_lat,
                faci_lot,
                road_addr,
                jibun_addr,
                addr
            FROM {table_name}
            WHERE {" OR ".join(["ftype_nm LIKE %s" for _ in categories])}
        """

        try:
            cursor.execute(sql, [f"%{category}%" for category in categories])
            rows = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

        results = []
        for row in rows:
            try:
                distance_km = self._calc_distance(
                    user_lat,
                    user_lon,
                    float(row["faci_lat"]),
                    float(row["faci_lot"]),
                )
            except (TypeError, ValueError):
                continue

            if distance_km > max_distance_km:
                continue

            address = row["road_addr"] or row["jibun_addr"] or row["addr"] or ""
            rounded_distance = round(distance_km, 2)

            results.append(
                {
                    "name": row["name"],
                    "type": row["facility_type_name"],
                    "category": row["facility_type_name"],
                    "address": address,
                    "distanceKm": rounded_distance,
                    "distance_km": rounded_distance,
                }
            )

        return sorted(results, key=lambda item: item["distanceKm"])[:limit]


class FacilityAgent(FacilityRecommendAgent):
    pass
