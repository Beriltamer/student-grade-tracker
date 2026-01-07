import json, os, shutil

def load_state(base_dir: str):
    def load(name, default):
        try:
            with open(os.path.join(base_dir, name), "r") as f:
                return json.load(f)
        except:
            return default

    return (
        load("students.json", []),
        load("courses.json", []),
        load("grades.json", {}),
        load("settings.json", {})
    )

def save_state(base_dir: str, students, courses, gradebook, settings) -> None:
    os.makedirs(base_dir, exist_ok=True)
    for name, data in [
        ("students.json", students),
        ("courses.json", courses),
        ("grades.json", gradebook),
        ("settings.json", settings)
    ]:
        with open(os.path.join(base_dir, name), "w") as f:
            json.dump(data, f, indent=2)

def backup_state(base_dir: str, backup_dir: str) -> list[str]:
    os.makedirs(backup_dir, exist_ok=True)
    backups = []
    for file in os.listdir(base_dir):
        src = os.path.join(base_dir, file)
        dst = os.path.join(backup_dir, file)
        shutil.copy(src, dst)
        backups.append(dst)
    return backups

def import_from_csv(csv_path: str, course_id: str) -> dict:
    import csv
    gradebook = {}
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            gradebook.setdefault(course_id, {})
            gradebook[course_id].setdefault(row["student_id"], [])
            gradebook[course_id][row["student_id"]].append({
                "id": row["assessment_id"],
                "score": float(row["score"]),
                "type": row["type"]
            })
    return gradebook

