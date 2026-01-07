def set_grade_policy(course_settings: dict, course_id: str, policy: dict) -> dict:
    course_settings[course_id] = policy
    return policy

def compute_weighted_score(scores: list[dict], policy: dict) -> float:
    total = 0
    for s in scores:
        weight = policy.get(s["type"], 0)
        total += s["score"] * weight / 100
    return total

def assign_letter_grade(score: float, scale: dict) -> str:
    for letter, threshold in scale.items():
        if score >= threshold:
            return letter
    return "F"
