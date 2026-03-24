class ExerciseKeywordExtractor:
    KEYWORD_MAP = {
        "수영": "수영",
        "걷기": "걷기",
        "러닝": "조깅",
        "조깅": "조깅",
        "자전거": "자전거",
        "웨이트": "헬스",
        "헬스": "헬스",
        "근력": "헬스",
        "요가": "요가",
        "필라테스": "필라테스",
        "스트레칭": "스트레칭",
    }

    def extract(self, pres_note: str):
        note = (pres_note or "").lower()
        for keyword, mapped in self.KEYWORD_MAP.items():
            if keyword.lower() in note:
                return mapped
        return "걷기"
