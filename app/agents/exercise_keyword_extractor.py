# app/agents/exercise_keyword_extractor.py

import re

class ExerciseKeywordExtractor:

    # pres_note에서 감지할 운동 키워드 사전 매핑
    KEYWORD_MAP = {
        # 유산소
        "수영": "수영",
        "걷기": "걷기",
        "트레드밀": "걷기",
        "조깅": "조깅",
        "자전거": "자전거",
        "실내 자전거": "자전거",

        # 근력/헬스 운동 → 모두 "헬스"로 정규화
        "스쿼트": "헬스",
        "윗몸": "헬스",
        "팔굽혀": "헬스",
        "덤벨": "헬스",
        "밴드": "헬스",
        "저항": "헬스",

        # 그룹운동
        "요가": "요가",
        "필라테스": "필라테스",
    }

    def extract(self, pres_note: str):
        pres_note = pres_note.lower()

        detected = []

        for key, mapped in self.KEYWORD_MAP.items():
            if key in pres_note:
                detected.append(mapped)

        # 중복 제거
        detected = list(set(detected))

        # 기본값 (아무것도 감지되지 않을 경우)
        if not detected:
            return "헬스"   # 가장 범용적인 운동종목

        # 첫 번째 종목 반환
        return detected[0]
