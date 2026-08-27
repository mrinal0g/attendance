# views.py
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.views import View
from .models import Attendance
from .forms import AttendanceForm


class StudentAttendancePage(View):
    template_name = "attendance/student_attendance.html"

    def get_student(self, username):
        User = get_user_model()
        return get_object_or_404(User, username=username)

    def get(self, request, username):
        if not request.user.is_authenticated:
            return redirect("login")
        if request.user.username != username:
            return HttpResponseForbidden("You can only view your own attendance page.")
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
        # 1. Standard Session Check
        if not request.user.is_authenticated:
            return redirect("login")
            
        # 2. Identity Check: Prevent marking attendance for someone else
        if request.user.username != username:
            return HttpResponseForbidden("You can only mark your own attendance.")

        # 3. Pull the student directly from the verified session, not the URL
        student = request.user
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
