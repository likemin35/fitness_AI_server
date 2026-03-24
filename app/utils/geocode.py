import os

import requests


def geocode(address):
    kakao_key = os.getenv("KAKAO_REST_API_KEY") or os.getenv("KAKAO_REST_KEY")
    if not kakao_key or not address:
        return None

    response = requests.get(
        "https://dapi.kakao.com/v2/local/search/address.json",
        headers={"Authorization": f"KakaoAK {kakao_key}"},
        params={"query": address},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    documents = data.get("documents", [])
    if not documents:
        return None

    document = documents[0]
    return {
        "lat": float(document["y"]),
        "lon": float(document["x"]),
    }
