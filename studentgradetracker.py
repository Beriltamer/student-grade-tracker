[
  {
    "id": "S001",
    "name": "Ahmet Yılmaz",
    "email": "ahmet@example.com",
    "courses": ["CS101"]
  }
]

import json

def load_students(path: str) -> list:
    with open(path, "r") as f:
        return json.load(f)

def save_students(path: str, students: list) -> None:
    with open(path, "w") as f:
        json.dump(students, f, indent=4)

def add_student(students: list, student_data: dict) -> dict:
    students.append(student_data)
    return student_data

def update_student(students: list, student_id: str, updates: dict) -> dict:
    for st in students:
        if st["id"] == student_id:
            st.update(updates)
            return st
    return None

def enroll_student(course_roster: dict, student_id: str) -> dict:
    if student_id not in course_roster["students"]:
        course_roster["students"].append(student_id)
    return course_roster

def withdraw_student(course_roster: dict, student_id: str) -> dict:
    if student_id in course_roster["students"]:
        course_roster["students"].remove(student_id)
    return course_roster

