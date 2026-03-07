import requests
import json
import time

API_URL = "https://apis.data.go.kr/B551014/SRVC_NFA_TEST_RESULT/TODZ_NFA_TEST_RESULT_NEW"
SERVICE_KEY = "a936d525c913e311fc7d7789926e8fd9cd3c2f7aa41d52dc80ca90ac9983dcc1"

ROWS = 1000  # 최대 1000 유지


def fetch_page(page_no):
    """특정 페이지 JSON 호출"""
    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": page_no,
        "numOfRows": ROWS,
        "resultType": "json",
    }

    response = requests.get(API_URL, params=params)
    response.raise_for_status()

    data = response.json()

    items = data["response"]["body"]["items"]

    # 단일 item일 경우 list로 변환
    if isinstance(items, dict):
        items = [items]

    return items


def fetch_all_and_save(output_file="fitenss_data.jsonl", limit_pages=None):
    """전체 페이지 수집 후 JSONL 저장"""

    # 첫 페이지
    first_page = fetch_page(1)
    print("첫 페이지 로딩됨 (예시 1건):", first_page[0])

    # totalCount 요청
    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": 1,
        "numOfRows": 1,
        "resultType": "json",
    }
    resp = requests.get(API_URL, params=params)
    total_count = int(resp.json()["response"]["body"]["totalCount"])

    total_pages = total_count // ROWS + 1

    print(f"총 데이터 개수: {total_count:,}")
    print(f"총 필요한 페이지 수(pageNo): {total_pages:,}")

    if limit_pages:
        print(f"limit_pages 적용 → {limit_pages} 페이지만 수집합니다.")
        total_pages = limit_pages

    # 저장
    with open(output_file, "w", encoding="utf-8") as f:
        for page in range(1, total_pages + 1):
            try:
                items = fetch_page(page)

                for item in items:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")

                print(f"[{page}/{total_pages}] 저장 완료 ({len(items)}개)")
                time.sleep(0.05)

            except Exception as e:
                print(f"⚠ 페이지 {page} 오류:", e)

    print("✔ 전체 저장 완료!")
    print("파일 위치:", output_file)


if __name__ == "__main__":
    fetch_all_and_save("fitenss_data.jsonl", limit_pages=None)
