"""Command-line interface for the Student Management System."""

from src.student_manager import StudentManager


def display_students(students: list[dict]) -> None:
    if not students:
        print("\nNo student records found.")
        return
    print("\n" + "-" * 100)
    print(f"{'ID':<5}{'Roll No.':<15}{'Name':<25}{'Email':<28}{'Course':<18}{'Sem':<5}")
    print("-" * 100)
    for student in students:
        print(f"{student['id']:<5}{student['roll_number']:<15}{student['full_name']:<25}{(student['email'] or '-'):<28}{student['course']:<18}{student['semester']:<5}")
    print("-" * 100)


def read_student_details() -> tuple[str, str, str, str, int]:
    roll = input("Roll number: ").strip()
    name = input("Full name: ").strip()
    email = input("Email (optional): ").strip()
    course = input("Course: ").strip()
    semester = int(input("Semester (1-8): ").strip())
    return roll, name, email, course, semester


def main() -> None:
    manager = StudentManager()
    while True:
        print("\n========== STUDENT MANAGEMENT SYSTEM ==========")
        print("1. Add student")
        print("2. View all students")
        print("3. Search students")
        print("4. Update student")
        print("5. Delete student")
        print("6. Course-wise summary")
        print("7. Dashboard summary")
        print("8. Exit")
        choice = input("Choose an option (1-8): ").strip()
        try:
            if choice == "1":
                details = read_student_details()
                student_id = manager.add_student(*details)
                print(f"Student added successfully. ID: {student_id}")
            elif choice == "2":
                display_students(manager.list_students())
            elif choice == "3":
                display_students(manager.search_students(input("Search roll/name/email/course: ")))
            elif choice == "4":
                student_id = int(input("Student ID to update: "))
                if not manager.get_student(student_id):
                    print("Student not found.")
                    continue
                details = read_student_details()
                print("Student updated." if manager.update_student(student_id, *details) else "Student not found.")
            elif choice == "5":
                student_id = int(input("Student ID to delete: "))
                confirm = input("Confirm deletion? (y/n): ").strip().lower()
                if confirm == "y":
                    print("Student deleted." if manager.delete_student(student_id) else "Student not found.")
                else:
                    print("Deletion cancelled.")
            elif choice == "6":
                summary = manager.course_summary()
                if not summary:
                    print("No records available.")
                else:
                    print("\nCourse-wise student count:")
                    for item in summary:
                        print(f"- {item['course']}: {item['student_count']}")
            elif choice == "7":
                print(f"\nTotal registered students: {manager.total_students()}")
                print(f"Courses represented: {len(manager.course_summary())}")
            elif choice == "8":
                print("Thank you for using Student Management System!")
                break
            else:
                print("Invalid option. Please choose from 1 to 8.")
        except ValueError as exc:
            print(f"Input error: {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\nApplication closed.")
            break


if __name__ == "__main__":
    main()
