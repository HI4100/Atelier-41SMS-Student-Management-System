"""Database-backed student record management."""

import re
import sqlite3
from pathlib import Path
from typing import Any


class StudentManager:
    """Create, retrieve, update, delete, and report student records."""

    def __init__(self, database_path: str | Path = "data/students.db") -> None:
        self.database_path = str(database_path)
        if self.database_path != ":memory:":
            Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll_number TEXT NOT NULL UNIQUE,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    course TEXT NOT NULL,
                    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )"""
            )

    @staticmethod
    def _validate_student(roll_number: str, full_name: str, email: str,
                          course: str, semester: int) -> tuple[str, str, str | None, str, int]:
        roll_number = roll_number.strip()
        full_name = full_name.strip()
        email = email.strip() or None
        course = course.strip()
        if not roll_number or not full_name or not course:
            raise ValueError("Roll number, full name, and course are required.")
        if email and not re.fullmatch(r"[^@\\s]+@[^@\\s]+\\.[^@\\s]+", email):
            raise ValueError("Enter a valid email address.")
        if isinstance(semester, bool) or not isinstance(semester, int) or not 1 <= semester <= 8:
            raise ValueError("Semester must be a whole number from 1 to 8.")
        return roll_number, full_name, email, course, semester

    def add_student(self, roll_number: str, full_name: str, email: str = "",
                    course: str = "", semester: int = 1) -> int:
        values = self._validate_student(roll_number, full_name, email, course, semester)
        try:
            with self._connect() as connection:
                cursor = connection.execute(
                    "INSERT INTO students (roll_number, full_name, email, course, semester) VALUES (?, ?, ?, ?, ?)",
                    values,
                )
                return int(cursor.lastrowid)
        except sqlite3.IntegrityError as exc:
            raise ValueError("Roll number or email already exists.") from exc

    def list_students(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT id, roll_number, full_name, email, course, semester, created_at FROM students ORDER BY roll_number COLLATE NOCASE"
            ).fetchall()
            return [dict(row) for row in rows]

    def get_student(self, student_id: int) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
            return dict(row) if row else None

    def update_student(self, student_id: int, roll_number: str, full_name: str,
                       email: str = "", course: str = "", semester: int = 1) -> bool:
        values = self._validate_student(roll_number, full_name, email, course, semester)
        try:
            with self._connect() as connection:
                cursor = connection.execute(
                    "UPDATE students SET roll_number=?, full_name=?, email=?, course=?, semester=? WHERE id=?",
                    (*values, student_id),
                )
                return cursor.rowcount > 0
        except sqlite3.IntegrityError as exc:
            raise ValueError("Roll number or email already exists.") from exc

    def delete_student(self, student_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM students WHERE id = ?", (student_id,))
            return cursor.rowcount > 0

    def search_students(self, keyword: str) -> list[dict[str, Any]]:
        keyword = keyword.strip()
        if not keyword:
            raise ValueError("Search keyword cannot be empty.")
        pattern = f"%{keyword}%"
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT * FROM students WHERE roll_number LIKE ? COLLATE NOCASE
                   OR full_name LIKE ? COLLATE NOCASE OR email LIKE ? COLLATE NOCASE
                   OR course LIKE ? COLLATE NOCASE ORDER BY full_name COLLATE NOCASE""",
                (pattern, pattern, pattern, pattern),
            ).fetchall()
            return [dict(row) for row in rows]

    def course_summary(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT course, COUNT(*) AS student_count FROM students GROUP BY course ORDER BY course COLLATE NOCASE"
            ).fetchall()
            return [dict(row) for row in rows]

    def total_students(self) -> int:
        with self._connect() as connection:
            return int(connection.execute("SELECT COUNT(*) FROM students").fetchone()[0])
