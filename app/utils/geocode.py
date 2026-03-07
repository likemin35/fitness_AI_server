import requests
import os

KAKAO_KEY = os.getenv("KAKAO_REST_API_KEY")

def geocode(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK " + KAKAO_KEY}
    params = {"query": address}

    res = requests.get(url, headers=headers, params=params)
    data = res.json()

    if len(data.get("documents", [])) == 0:
        return None

    doc = data["documents"][0]
    return {
        "lat": float(doc["y"]),
        "lon": float(doc["x"])
    }
