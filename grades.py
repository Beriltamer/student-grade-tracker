def record_grade(gradebook: dict, course_id: str, student_id: str, assessment: dict) -> dict:
    gradebook.setdefault(course_id, {})
    gradebook[course_id].setdefault(student_id, [])
    gradebook[course_id][student_id].append(assessment)
    return assessment

def update_grade(gradebook: dict, course_id: str, student_id: str, assessment_id: str, new_score: float) -> dict:
    for a in gradebook[course_id][student_id]:
        if a["id"] == assessment_id:
            a["score"] = new_score
            return a
    raise ValueError("Assessment not found")

def delete_grade(gradebook: dict, course_id: str, student_id: str, assessment_id: str) -> dict:
    grades = gradebook[course_id][student_id]
    gradebook[course_id][student_id] = [g for g in grades if g["id"] != assessment_id]
    return gradebook

def calculate_student_average(gradebook: dict, course_id: str, student_id: str) -> float:
    scores = gradebook.get(course_id, {}).get(student_id, [])
    if not scores:
        return 0.0
    return sum(a["score"] for a in scores) / len(scores)

def calculate_course_average(gradebook: dict, course_id: str) -> float:
    students = gradebook.get(course_id, {})
    if not students:
        return 0.0
    return sum(calculate_student_average(gradebook, course_id, s) for s in students) / len(students)

