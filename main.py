from storage import load_state, save_state
from roster import add_student
from grades import record_grade

DATA_DIR = "data"

students, courses, gradebook, settings = load_state(DATA_DIR)

while True:
    print("\n1) Add Student\n2) Add Grade\n3) Exit")
    choice = input("> ")

    if choice == "1":
        sid = input("ID: ")
        name = input("Name: ")
        email = input("Email: ")
        add_student(students, {"id": sid, "name": name, "email": email})

    elif choice == "2":
        cid = input("Course ID: ")
        sid = input("Student ID: ")
        aid = input("Assessment ID: ")
        score = float(input("Score: "))
        record_grade(gradebook, cid, sid, {"id": aid, "score": score, "type": "exam"})

    elif choice == "3":
        save_state(DATA_DIR, students, courses, gradebook, settings)
        break

