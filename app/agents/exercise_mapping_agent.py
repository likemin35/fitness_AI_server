class ExerciseMappingAgent:
    CATEGORY_MAP = {
        "걷기": ["걷기", "조깅", "자전거"],
        "조깅": ["조깅", "걷기", "자전거"],
        "수영": ["수영", "아쿠아로빅", "걷기"],
        "헬스": ["헬스", "PT", "필라테스"],
        "PT": ["PT", "헬스", "필라테스"],
        "요가": ["요가", "필라테스", "스트레칭"],
        "필라테스": ["필라테스", "요가", "스트레칭"],
    }

    def map_prescription(self, pres_note: str):
        note = pres_note or ""
        for keyword, mapped in self.CATEGORY_MAP.items():
            if keyword in note:
                return mapped
        return ["걷기", "헬스", "수영"]
