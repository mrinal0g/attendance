from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source="student.username")

    class Meta:
        model = Attendance
        fields = [
            "id",
            "student",
            "student_name",
            "student_full_name",
            "date",
            "time",
            "status",
        ]
        read_only_fields = ["id", "student", "student_name", "student_full_name", "time"]
