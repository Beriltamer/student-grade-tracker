import json

def load_students(path: str) -> list:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
#load_students: JSON dosyasını okur. Eğer dosya henüz yoksa programın çökmemesi için boş bir liste ([]) döner. 
def save_students(path: str, students: list) -> None:
    with open(path, "w") as f:
        json.dump(students, f, indent=2)
#Güncel listeyi dosyaya yazar. indent=2 parametresi, JSON dosyasının insanlar tarafından kolayca okunabilmesini (girintili olmasını) sağlar.
def add_student(students: list, student_data: dict) -> dict:
    students.append(student_data)
    return student_data
#add_student: Yeni bir sözlüğü listeye ekler.
def update_student(students: list, student_id: str, updates: dict) -> dict:
    for s in students:
        if s["id"] == student_id:
            s.update(updates)
            return s
    raise ValueError("Student not found")
#update_student: Belirli bir ID'ye sahip öğrenciyi bulur ve s.update(updates) ile sadece değişmesi gereken alanları (isim, not, vb.) günceller.

def enroll_student(course_roster: dict, student_id: str) -> dict:
    course_roster.setdefault("students", [])
    if student_id not in course_roster["students"]:
        course_roster["students"].append(student_id)
    return course_roster

def withdraw_student(course_roster: dict, student_id: str) -> dict:
    if student_id in course_roster.get("students", []):
        course_roster["students"].remove(student_id)
    return course_roster

#enroll_student / withdraw_student: Bu fonksiyonlar ders kayıt sistemini yönetir. setdefault kullanımı çok pratiktir; eğer "students" anahtarı yoksa o an oluşturur.
