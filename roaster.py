import json

def load_students(path: str) -> list:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_students(path: str, students: list) -> None:
    with open(path, "w") as f:
        json.dump(students, f, indent=2)

def add_student(students: list, student_data: dict) -> dict:
    students.append(student_data)
    return student_data

def update_student(students: list, student_id: str, updates: dict) -> dict:
    for s in students:
        if s["id"] == student_id:
            s.update(updates)
            return s
    raise ValueError("Student not found")

def enroll_student(course_roster: dict, student_id: str) -> dict:
    course_roster.setdefault("students", [])
    if student_id not in course_roster["students"]:
        course_roster["students"].append(student_id)
    return course_roster

def withdraw_student(course_roster: dict, student_id: str) -> dict:
    if student_id in course_roster.get("students", []):
        course_roster["students"].remove(student_id)
    return course_roster

