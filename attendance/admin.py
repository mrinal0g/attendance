from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.urls import path
from django.utils.encoding import iri_to_uri
import csv

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student_full_name", "student", "date", "time", "status")
    list_filter = ("status", "date")
    search_fields = ("student_full_name", "student__username", "student__first_name", "student__last_name")
    readonly_fields = ("student_full_name", "time")
    change_list_template = "admin/attendance/attendance/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "export-csv/",
                self.admin_site.admin_view(self.export_csv),
                name="attendance_attendance_export",
            ),
        ]
        return custom_urls + urls

    def save_model(self, request, obj, form, change):
        if "student" in form.changed_data:
            obj.student_full_name = (
                obj.student.get_full_name().strip() or obj.student.username
            )
        super().save_model(request, obj, form, change)

    def export_csv(self, request):
        """Export registered students as rows and recorded attendance dates as columns."""
        User = get_user_model()
        students = list(
            User.objects.filter(is_staff=False)
            .order_by("first_name", "last_name", "username")
        )
        records = Attendance.objects.select_related("student").order_by("date")
        dates = list(records.values_list("date", flat=True).distinct())
        status_codes = {"PRESENT": "P", "ABSENT": "A", "LATE": "L"}
        attendance_by_student_and_date = {
            (record.student_id, record.date): status_codes[record.status]
            for record in records
        }

        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = iri_to_uri(
            'attachment; filename="attendance-export.csv"'
        )
        writer = csv.writer(response)
        writer.writerow(["S No", "Learner Name", *[date.isoformat() for date in dates]])

        for serial_number, student in enumerate(students, start=1):
            full_name = student.get_full_name().strip() or student.username
            writer.writerow(
                [
                    serial_number,
                    full_name,
                    *[
                        attendance_by_student_and_date.get((student.id, date), "")
                        for date in dates
                    ],
                ]
            )

        return response
