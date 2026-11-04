# ATELIER 41 | Student Management System

A Python command-line application for maintaining student records with an SQLite database. The project demonstrates CRUD operations, relational database fundamentals, input validation, SQL queries, and automated unit testing.

## Features

- Add student records with roll number, name, optional email, course, and semester
- View all registered students
- Search by roll number, name, email, or course
- Update and delete student records
- Enforce unique roll numbers and email addresses
- Validate required fields, email format, and semester range (1–8)
- View course-wise student counts and a dashboard summary
- Store records persistently in a local SQLite database
- Run automated tests with Python's built-in unittest framework

## Technology

- Python 3.10+
- SQLite (sqlite3, included with Python)
- unittest
- GitHub Actions

No third-party Python packages are required.

## Getting started

1. Install Python 3.10 or later.
2. Clone or download this repository.
3. Open a terminal in the project folder.
4. Run:

   python main.py

The application creates data/students.db automatically the first time it runs. The data/ folder and database files are excluded from Git by .gitignore so local student records are not accidentally committed.

## Run tests

   python -m unittest discover -s tests -v

Tests use temporary databases and do not modify your real application data.

## Project structure

    Student-Management-System/
    ├── .github/workflows/tests.yml
    ├── data/                       # Created automatically; ignored by Git
    ├── src/
    │   ├── __init__.py
    │   └── student_manager.py
    ├── tests/test_student_manager.py
    ├── .gitignore
    ├── main.py
    └── README.md

## Database design

The students table contains:

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| roll_number | TEXT | Required unique student identifier |
| full_name | TEXT | Required student name |
| email | TEXT | Optional unique email address |
| course | TEXT | Required course/program name |
| semester | INTEGER | Semester number from 1 to 8 |
| created_at | TEXT | Record creation timestamp |

SQL statements use parameterized queries. The application is intended as an educational, single-user local project; it is not an institutional student information system and does not include authentication, role-based access, or cloud hosting.

## Menu options

1. Add student
2. View all students
3. Search students
4. Update student
5. Delete student
6. Course-wise summary
7. Dashboard summary
8. Exit

## Future improvements

- Add marks and attendance modules
- Add CSV import/export
- Add a graphical interface or web dashboard
- Add database backup and restore

## License

No license has been added yet. All rights reserved by default.


---

## ✨ ATELIER 41 Signature

> **Build it clearly. Test it carefully. Document it honestly. Improve it continuously.**

This project is part of my **ATELIER 41** portfolio — a connected collection of practical projects built and documented by **Humza Warsi**.

🔗 GitHub: [@HI4100](https://github.com/HI4100) • ✨ **ATELIER 41**
