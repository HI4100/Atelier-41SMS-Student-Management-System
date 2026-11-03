"""Unit tests for StudentManager using isolated temporary databases."""

import tempfile
import unittest
from pathlib import Path

from src.student_manager import StudentManager


class StudentManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.manager = StudentManager(Path(self.temp_dir.name) / "test_students.db")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def add_sample(self, roll: str = "IT001", name: str = "Aarav Shah") -> int:
        return self.manager.add_student(roll, name, "aarav@example.com", "Information Technology", 3)

    def test_add_and_list_student(self) -> None:
        self.add_sample()
        students = self.manager.list_students()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]["roll_number"], "IT001")

    def test_duplicate_roll_number_rejected(self) -> None:
        self.add_sample()
        with self.assertRaises(ValueError):
            self.manager.add_student("IT001", "Other Student", "other@example.com", "IT", 2)

    def test_duplicate_email_rejected(self) -> None:
        self.add_sample()
        with self.assertRaises(ValueError):
            self.manager.add_student("IT002", "Other Student", "aarav@example.com", "IT", 2)

    def test_invalid_email_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.manager.add_student("IT001", "Aarav Shah", "bad-email", "IT", 3)

    def test_invalid_semester_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.manager.add_student("IT001", "Aarav Shah", "", "IT", 9)

    def test_required_fields_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.manager.add_student("", "Aarav Shah", "", "IT", 3)

    def test_get_student(self) -> None:
        student_id = self.add_sample()
        self.assertEqual(self.manager.get_student(student_id)["full_name"], "Aarav Shah")
        self.assertIsNone(self.manager.get_student(999))

    def test_update_student(self) -> None:
        student_id = self.add_sample()
        changed = self.manager.update_student(student_id, "IT001", "Aarav S.", "", "Computer Engineering", 4)
        self.assertTrue(changed)
        self.assertEqual(self.manager.get_student(student_id)["course"], "Computer Engineering")

    def test_delete_student(self) -> None:
        student_id = self.add_sample()
        self.assertTrue(self.manager.delete_student(student_id))
        self.assertFalse(self.manager.delete_student(student_id))
        self.assertEqual(self.manager.total_students(), 0)

    def test_search_student(self) -> None:
        self.add_sample()
        self.assertEqual(len(self.manager.search_students("aarav")), 1)
        self.assertEqual(len(self.manager.search_students("Information")), 1)
        self.assertEqual(len(self.manager.search_students("missing")), 0)

    def test_empty_search_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.manager.search_students("  ")

    def test_course_summary(self) -> None:
        self.add_sample()
        self.manager.add_student("IT002", "Mira Patel", "mira@example.com", "Information Technology", 2)
        self.manager.add_student("CE001", "Dev Mehta", "dev@example.com", "Computer Engineering", 1)
        summary = {item["course"]: item["student_count"] for item in self.manager.course_summary()}
        self.assertEqual(summary["Information Technology"], 2)
        self.assertEqual(summary["Computer Engineering"], 1)

    def test_total_students(self) -> None:
        self.assertEqual(self.manager.total_students(), 0)
        self.add_sample()
        self.assertEqual(self.manager.total_students(), 1)


if __name__ == "__main__":
    unittest.main()
