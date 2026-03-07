import json
import os

DATASET_PATH = "fitness_dataset.jsonl"

all_keys = set()

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line.strip())
        for k in item.keys():
            all_keys.add(k)

print("전체 컬럼 목록:")
for k in sorted(all_keys):
    print(k)
