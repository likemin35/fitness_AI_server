import json
import mysql.connector

# --- MySQL 연결 정보 ---------------------
config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "fitnessdb",
}
# ----------------------------------------

# JSONL 파일 경로
JSONL_FILE = "course_registration_dataset.jsonl"   # 또는 course_dataset.jsonl


TARGET = "voucher_facility"   # 또는 "voucher_course"


# ------------------------------
# 1) 바우처 시설 테이블 매핑
# ------------------------------
VOUCHER_FACILITY_FIELDS = [
    "facil_sn",
    "facil_nm",
    "road_addr",
    "faci_daddr",
    "city_nm",
    "local_nm",
    "main_event_nm",
    "main_event_cd",
    "faci_zip",
    "brno"
]

# ------------------------------
# 2) 바우처 강좌 테이블 매핑
# ------------------------------
VOUCHER_COURSE_FIELDS = [
    "course_no",
    "facil_sn",
    "course_nm",
    "item_nm",
    "item_cd",
    "lectr_nm",
    "start_tm",
    "equip_tm",
    "lectr_weekday_val",
    "course_seta_desc_cn",
    "settl_amt"
]


def load_jsonl_to_mysql():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    if TARGET == "facility":
        table_name = "voucher_facility"
        fields = VOUCHER_FACILITY_FIELDS
    else:
        table_name = "voucher_course"
        fields = VOUCHER_COURSE_FIELDS

    placeholders = ", ".join(["%s"] * len(fields))
    column_list = ", ".join(fields)

    query = f"""
        INSERT INTO {table_name} ({column_list})
        VALUES ({placeholders})
    """

    with open(JSONL_FILE, "r", encoding="utf-8") as f:
        count = 0
        for line in f:
            item = json.loads(line)

            values = [item.get(k) for k in fields]

            cursor.execute(query, values)
            count += 1

            if count % 1000 == 0:
                conn.commit()
                print(f"✔ {count}행 저장 완료 ({table_name})")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"🎉 모든 데이터 저장 완료 → {table_name}")


if __name__ == "__main__":
    load_jsonl_to_mysql()
