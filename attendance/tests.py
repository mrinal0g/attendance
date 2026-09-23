import csv

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from .models import Attendance
from student.models import StudentModel


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

    def test_admin_csv_export_can_filter_by_batch_id(self):
        other_user = get_user_model().objects.create_user(
            username="student2",
            first_name="Bina",
            last_name="Patel",
            password="safe-password",
        )
        StudentModel.objects.create(
            id=self.user.id,
            full_name="Asha Sharma",
            email="asha@example.com",
            batch_id="batch-a",
        )
        StudentModel.objects.create(
            id=other_user.id,
            full_name="Bina Patel",
            email="bina@example.com",
            batch_id="batch-b",
        )
        first_date = timezone.localdate()
        second_date = first_date + timezone.timedelta(days=1)
        Attendance.objects.create(
            student=self.user, date=first_date, status="PRESENT"
        )
        Attendance.objects.create(
            student=other_user, date=second_date, status="ABSENT"
        )
        admin_user = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="safe-password"
        )
        self.client.force_login(admin_user)

        response = self.client.get(
            "/admin/attendance/attendance/export-csv/?batch_id=batch-a"
        )

        rows = list(csv.reader(response.content.decode().splitlines()))
        self.assertEqual(rows[0], ["S No", "Learner Name", first_date.isoformat()])
        self.assertEqual(rows[1], ["1", "Asha Sharma", "P"])
