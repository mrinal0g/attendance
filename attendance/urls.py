# urls.py
from django.urls import path
from .views import StudentAttendancePage

app_name = "attendance"

urlpatterns = [
    path("<str:username>/", StudentAttendancePage.as_view(), name="student-attendance"),
]
