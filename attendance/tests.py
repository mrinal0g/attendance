import csv

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from .models import Attendance


class MarkAttendanceTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="student1",
            first_name="Asha",
            last_name="Sharma",
            password="safe-password",
        )

    def test_marks_attendance_from_the_django_form(self):
        response = self.client.post(
            "/attendance/student1/",
            {"date": "2000-01-01", "status": "PRESENT"},
        )

        self.assertRedirects(
            response, "/attendance/student1/", fetch_redirect_response=False
        )
        self.assertEqual(Attendance.objects.count(), 1)
        attendance = Attendance.objects.get()
        self.assertEqual(attendance.student, self.user)
        self.assertEqual(attendance.student_full_name, "Asha Sharma")
        self.assertEqual(attendance.date, timezone.localdate())

    def test_cannot_store_the_same_student_twice_for_one_date(self):
        Attendance.objects.create(student=self.user, date=timezone.localdate())

        with self.assertRaises(IntegrityError), transaction.atomic():
            Attendance.objects.create(student=self.user, date=timezone.localdate())

    def test_admin_csv_export_pivots_students_and_dates(self):
        admin_user = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="safe-password"
        )
        Attendance.objects.create(
            student=self.user, date=timezone.localdate(), status="PRESENT"
        )
        self.client.force_login(admin_user)

        response = self.client.get("/admin/attendance/attendance/export-csv/")

        self.assertEqual(response.status_code, 200)
        rows = list(csv.reader(response.content.decode().splitlines()))
        self.assertEqual(rows[0][:3], ["S No", "Learner Name", timezone.localdate().isoformat()])
        self.assertEqual(rows[1][:3], ["1", "Asha Sharma", "P"])
