def grade_distribution(gradebook: dict, course_id: str, bins: list[int]) -> dict:
    distribution = {f"{bins[i]}-{bins[i+1]}": 0 for i in range(len(bins)-1)}
    for student in gradebook.get(course_id, {}).values():
        for a in student:
            for i in range(len(bins)-1):
                if bins[i] <= a["score"] < bins[i+1]:
                    distribution[f"{bins[i]}-{bins[i+1]}"] += 1
    return distribution
#grade_distribution (Not Dağılımı)

#Bu fonksiyon, öğrencilerin notlarını belirli aralıklara (bins) bölerek hangi aralıkta kaç öğrenci olduğunu sayar.

def top_performers(gradebook: dict, course_id: str, limit: int = 5) -> list:
    averages = []
    for sid in gradebook.get(course_id, {}):
        avg = sum(a["score"] for a in gradebook[course_id][sid]) / len(gradebook[course_id][sid])
        averages.append((sid, avg))
    averages.sort(key=lambda x: x[1], reverse=True)
    return averages[:limit]
    #top_performers (En Başarılı Öğrenciler)

#Belirli bir dersteki en yüksek ortalamaya sahip ilk n öğrenciyi bulur.

def student_progress_report(gradebook: dict, course_id: str, student_id: str) -> dict:
    grades = gradebook.get(course_id, {}).get(student_id, [])
    return {
        "completed": len(grades),
        "average": sum(a["score"] for a in grades) / len(grades) if grades else 0,
        "assessments": grades
    }
#student_progress_report (Öğrenci Gelişim Raporu)

#Tek bir öğrencinin o dersteki performans özetini çıkarır.

def export_report(report: dict, filename: str) -> str:
    with open(filename, "w") as f:
        for k, v in report.items():
            f.write(f"{k}: {v}\n")
    return filename
#export_report (Raporu Dışa Aktar)

#Oluşturulan rapor sözlüğünü bir metin dosyasına (.txt) alt alta yazar.

