import json


class RecommendFitnessAgent:
    RULES = [
        (
            ("수영", "수중", "swim"),
            [
                {"name": "수영", "reason": "관절 부담을 줄이면서 심폐지구력을 높이기 좋습니다."},
                {"name": "아쿠아로빅", "reason": "물속에서 전신 운동을 하며 체력 향상에 도움이 됩니다."},
                {"name": "걷기", "reason": "일상에서 가장 쉽게 실천할 수 있는 유산소 운동입니다."},
            ],
        ),
        (
            ("걷기", "조깅", "러닝", "run", "walk"),
            [
                {"name": "걷기", "reason": "부담이 적고 꾸준히 지속하기 좋은 기본 유산소 운동입니다."},
                {"name": "조깅", "reason": "심폐지구력 향상에 도움이 되는 대표적인 운동입니다."},
                {"name": "자전거", "reason": "하체 지구력 강화와 유산소 운동을 함께 기대할 수 있습니다."},
            ],
        ),
        (
            ("근력", "웨이트", "헬스", "weight", "gym", "근지구력"),
            [
                {"name": "헬스", "reason": "근력과 근지구력을 단계적으로 강화하기 좋습니다."},
                {"name": "PT", "reason": "개인별 체력 수준에 맞춘 운동 강도 조절이 쉽습니다."},
                {"name": "필라테스", "reason": "코어 안정성과 자세 개선에 도움이 됩니다."},
            ],
        ),
        (
            ("요가", "유연성", "스트레칭", "rehab"),
            [
                {"name": "요가", "reason": "유연성과 균형감 향상에 도움이 됩니다."},
                {"name": "필라테스", "reason": "코어 강화와 자세 보완에 적합합니다."},
                {"name": "스트레칭", "reason": "부상 예방과 가동범위 확대에 효과적입니다."},
            ],
        ),
    ]

    DEFAULT_RECOMMENDATIONS = [
        {"name": "걷기", "reason": "대부분의 사용자가 안전하게 시작하기 좋은 운동입니다."},
        {"name": "헬스", "reason": "근력과 체력을 균형 있게 관리하기 좋습니다."},
        {"name": "수영", "reason": "전신 운동과 심폐지구력 향상에 도움이 됩니다."},
    ]

    def recommend_exercises(self, pres_note: str) -> str:
        note = (pres_note or "").lower()

        recommendations = self.DEFAULT_RECOMMENDATIONS
        for keywords, items in self.RULES:
            if any(keyword.lower() in note for keyword in keywords):
                recommendations = items
                break

        return json.dumps(
            {"recommended_exercises": recommendations},
            ensure_ascii=False,
        )
