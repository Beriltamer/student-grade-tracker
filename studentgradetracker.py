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

def add_student(students: list, student_data: dict) -> list:
    students.append(student_data)
    return students

def update_student(students: list, student_id: str, updates: dict) -> dict:
    for s in students:
        if s["id"] == student_id:
          s.update(updates) 
          return s
return {} 

def record_grade(gradebook: dict, course_id: str, student_id: str, assessment: dict) -> dict:
    course = gradebook.setdefault(course_id, {})
    student = course.setdefault(student_id, [])
    student.append(assessment)
    return gradebook

def update_grade(gradebook, course_id, student_id, assessment_id, new_score):
    for a in gradebook[course_id][student_id]:
        if a["id"] == assessment_id:
            a["score"] = new_score
            return a
    return {}

def delete_grade(gradebook, course_id, student_id, assessment_id):
    items = gradebook[course_id][student_id]
    gradebook[course_id][student_id] = [a for a in items if a["id"] != assessment_id]
    return gradebook

def calculate_student_average(gradebook, course_id, student_id):
    grades = gradebook.get(course_id, {}).get(student_id, [])
    if not grades:
        return 0
    total = sum(g["score"] for g in grades)
    return total / len(grades)

def calculate_course_average(gradebook, course_id):
    course = gradebook.get(course_id, {})
    if not course:
        return 0
    avgs = []
    for sid in course:
        avgs.append(calculate_student_average(gradebook, course_id,sid))
    return sum(avgs)/ len(avgs)
  def grade_distribution(gradebook, course_id, bins):
    course = gradebook.get(course_id, {})
    scores = []

    for sid in course:
        for a in course[sid]:
            scores.append(a["score"])

    dist = {b: 0 for b in bins}

    for s in scores:
        for b in bins:
            if s <= b:
                dist[b] += 1
                break

    return dist

def top_performers(gradebook, course_id, limit=3):
    course = gradebook.get(course_id, {})
    results = []

    for sid in course:
        total = sum(a["score"] for a in course[sid])
        count = len(course[sid])
        avg = total / count if count else 0
        results.append((sid, avg))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:limit]

def student_progress_report(gradebook, course_id, student_id):
    return gradebook.get(course_id, {}).get(student_id, [])
  
import json
import os

def load_state(base_dir: str):
    def read(name):
        path = os.path.join(base_dir, name)
        try:
            with open(path) as f:
                return json.load(f)
        except:
            return {}

    return (
        read("students.json"),
        read("courses.json"),
        read("grades.json"),
        read("settings.json")
    )

def save_state(base_dir, students, courses, gradebook, settings):
    def write(name, data):
        with open(os.path.join(base_dir, name), "w") as f:
            json.dump(data, f, indent=2)

    write("students.json", students)
    write("courses.json", courses)
    write("grades.json", gradebook)
    write("settings.json", settings)
  
  def assign_letter_grade(score):
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"

from roster import *
from grades import *
from storage import *
from config import *

BASE = "data"

students, courses, gradebook, settings = load_state(BASE)

def menu():
    while True:
        print("\n1) Öğrenci ekle")
        print("2) Not ekle")
        print("3) Ortalama bak")
        print("4) Çıkış")

        c = input("> ")

        if c == "1":
            sid = input("id: ")
            name = input("isim: ")
            students.append({"id": sid, "name": name})
            save_state(BASE, students, courses, gradebook, settings)

        elif c == "2":
            cid = input("course id: ")
            sid = input("student id: ")
            aid = input("assessment id: ")
            score = float(input("score: "))
            record_grade(gradebook, cid, sid, {"id": aid, "score": score})
            save_state(BASE, students, courses, gradebook, settings)

        elif c == "3":
            cid = input("course id: ")
            sid = input("student id: ")
            avg = calculate_student_average(gradebook, cid, sid)
            print("avg =", avg, "=>", assign_letter_grade(avg))

        else:
            save_state(BASE, students, courses, gradebook, settings)
            break

if __name__ == "__main__":
    menu()
