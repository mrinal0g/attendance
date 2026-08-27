# views.py
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from .models import Attendance
from .forms import AttendanceForm


class StudentAttendancePage(View):
    template_name = "attendance/student_attendance.html"

    def get_student(self, username):
        User = get_user_model()
        return get_object_or_404(User, username=username)

    def get(self, request, username):
        student = self.get_student(username)
        return render(
            request,
            self.template_name,
            {
                "student": student,
                "form": AttendanceForm(),
                "today": timezone.localdate(),
                "history": Attendance.objects.filter(student=student),
            },
        )

    def post(self, request, username):
        student = self.get_student(username)
        form = AttendanceForm(request.POST)
        if form.is_valid():
            try:
                Attendance.objects.create(
                    student=student,
                    date=timezone.localdate(),
                    **form.cleaned_data,
                )
            except IntegrityError:
                form.add_error(None, "Attendance has already been marked for today.")
            else:
                messages.success(request, "Attendance saved successfully.")
                return redirect("attendance:student-attendance", username=student.username)

        return render(
            request,
            self.template_name,
            {
                "student": student,
                "form": form,
                "today": timezone.localdate(),
                "history": Attendance.objects.filter(student=student),
            },
        )
