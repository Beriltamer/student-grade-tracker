[
  {
    "id": "S001",
    "name": "beril tamer",
    "email": "beril@example.com",
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
  
DEFAULT_MIN = 0
DEFAULT_MAX = 100


def validate_score(score: float) -> float:
    if score < DEFAULT_MIN or score > DEFAULT_MAX:
        raise ValueError("Score must be between 0 and 100")
    return score


def record_grade(gradebook: dict, course_id: str, student_id: str,
                 assessment_id: str, score: float, weight: float) -> dict:

    validate_score(score)

    course = gradebook.setdefault(course_id, {"students": {}})
    student = course["students"].setdefault(student_id, {"assessments": {}})

    student["assessments"][assessment_id] = {
        "score": score,
        "weight": weight
    }

    return gradebook


def update_grade(gradebook: dict, course_id: str, student_id: str,
                 assessment_id: str, new_score: float) -> dict:

    validate_score(new_score)

    gradebook[course_id]["students"][student_id]["assessments"][assessment_id]["score"] = new_score
    return gradebook


def delete_grade(gradebook: dict, course_id: str, student_id: str,
                 assessment_id: str) -> dict:

    student = gradebook[course_id]["students"][student_id]
    student["assessments"].pop(assessment_id, None)
    return gradebook


def calculate_student_average(gradebook: dict, course_id: str,
                              student_id: str) -> float:

    assessments = gradebook[course_id]["students"][student_id]["assessments"]

    if not assessments:
        return 0.0

    total = 0
    weight_sum = 0

    for a in assessments.values():
        total += a["score"] * a["weight"]
        weight_sum += a["weight"]

    return total / weight_sum if weight_sum > 0 else 0.0


def calculate_course_average(gradebook: dict, course_id: str) -> float:

    students = gradebook[course_id]["students"]

    if not students:
        return 0.0

    totals = []

    for student_id in students:
        totals.append(calculate_student_average(gradebook, course_id, student_id))

    return sum(totals) / len(totals)
  def grade_distribution(gradebook: dict, course_id: str, bins: list[int]) -> dict:
    """
    bins örnek: [0, 60, 70, 80, 90, 100]
    """
    distribution = {f"{bins[i]}-{bins[i+1]}": 0 for i in range(len(bins) - 1)}

    students = gradebook[course_id]["students"]

    for sid in students:
        avg = calculate_student_average(gradebook, course_id, sid)

        for i in range(len(bins) - 1):
            if bins[i] <= avg <= bins[i+1]:
                distribution[f"{bins[i]}-{bins[i+1]}"] += 1
                break

    return distribution


def top_performers(gradebook: dict, course_id: str, limit: int = 5) -> list:
    students = gradebook[course_id]["students"]

    ranking = []

    for sid in students:
        avg = calculate_student_average(gradebook, course_id, sid)
        ranking.append((sid, avg))

    ranking.sort(key=lambda x: x[1], reverse=True)

    return ranking[:limit]


def student_progress_report(gradebook: dict, course_id: str, student_id: str) -> dict:
    student = gradebook[course_id]["students"][student_id]
    avg = calculate_student_average(gradebook, course_id, student_id)

    return {
        "student_id": student_id,
        "assessments": student["assessments"],
        "average": avg,
        "status": "OK" if avg >= 60 else "At Risk"
    }


def export_report(report: dict, filename: str) -> str:
    with open(filename, "w") as f:
        for k, v in report.items():
            f.write(f"{k}: {v}\n")
        return filename
      import json
import csv
import os
import shutil
from typing import tuple, list, dict


def load_state(base_dir: str) -> tuple[list, list, dict, dict]:
    """
    base_dir içindeki JSON dosyalarını okuyarak sistemi geri yükler.

    Beklenen dosyalar:
      students.json
      courses.json
      gradebook.json
      settings.json
    """

    def _load_json(path, default):
        if not os.path.exists(path):
            return default
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    students = _load_json(os.path.join(base_dir, "students.json"), [])
    courses = _load_json(os.path.join(base_dir, "courses.json"), [])
    gradebook = _load_json(os.path.join(base_dir, "gradebook.json"), {})
    settings = _load_json(os.path.join(base_dir, "settings.json"), {})

    return students, courses, gradebook, settings


def save_state(
    base_dir: str,
    students: list,
    courses: list,
    gradebook: dict,
    settings: dict
) -> None:
    """
    Mevcut durumu JSON dosyalarına kaydeder.
    """

    os.makedirs(base_dir, exist_ok=True)

    def _save_json(path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    _save_json(os.path.join(base_dir, "students.json"), students)
    _save_json(os.path.join(base_dir, "courses.json"), courses)
    _save_json(os.path.join(base_dir, "gradebook.json"), gradebook)
    _save_json(os.path.join(base_dir, "settings.json"), settings)


def backup_state(base_dir: str, backup_dir: str) -> list[str]:
    """
    base_dir içindeki tüm JSON dosyalarını backup_dir içine kopyalar
    ve backup’a alınan dosyaların listesini döner.
    """

    os.makedirs(backup_dir, exist_ok=True)

    backed_up = []

    for filename in os.listdir(base_dir):
        if filename.endswith(".json"):
            src = os.path.join(base_dir, filename)
            dst = os.path.join(backup_dir, filename)
            shutil.copy2(src, dst)
            backed_up.append(filename)

    return backed_up


def import_from_csv(csv_path: str, course_id: str) -> dict:
    """
    CSV dosyasından notları içe aktarır.

    Beklenen CSV formatı:
        student_id, assessment_id, score
    """

    results = {
        "course_id": course_id,
        "entries": []
    }

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # basit doğrulama
            if not row.get("student_id") or not row.get("assessment_id"):
                continue

            entry = {
                "student_id": row["student_id"],
                "assessment_id": row["assessment_id"],
                "score": float(row.get("score", 0))
            }

            results["entries"].append(entry)
          return results
