def grade_distribution(gradebook: dict, course_id: str, bins: list[int]) -> dict:
    distribution = {f"{bins[i]}-{bins[i+1]}": 0 for i in range(len(bins)-1)}
    for student in gradebook.get(course_id, {}).values():
        for a in student:
            for i in range(len(bins)-1):
                if bins[i] <= a["score"] < bins[i+1]:
                    distribution[f"{bins[i]}-{bins[i+1]}"] += 1
    return distribution

def top_performers(gradebook: dict, course_id: str, limit: int = 5) -> list:
    averages = []
    for sid in gradebook.get(course_id, {}):
        avg = sum(a["score"] for a in gradebook[course_id][sid]) / len(gradebook[course_id][sid])
        averages.append((sid, avg))
    averages.sort(key=lambda x: x[1], reverse=True)
    return averages[:limit]

def student_progress_report(gradebook: dict, course_id: str, student_id: str) -> dict:
    grades = gradebook.get(course_id, {}).get(student_id, [])
    return {
        "completed": len(grades),
        "average": sum(a["score"] for a in grades) / len(grades) if grades else 0,
        "assessments": grades
    }

def export_report(report: dict, filename: str) -> str:
    with open(filename, "w") as f:
        for k, v in report.items():
            f.write(f"{k}: {v}\n")
    return filename

