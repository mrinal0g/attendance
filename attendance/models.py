# models.py
from django.conf import settings
from django.db import models
from django.utils import timezone


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
        ("LATE", "Late"),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendances",
    )
    # A snapshot of the student's name when the attendance record is created.
    student_full_name = models.CharField(max_length=301, editable=False)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="PRESENT"
    )

    class Meta:
        # Prevents a student from marking attendance multiple times on the same day
        constraints = [
            models.UniqueConstraint(
                fields=["student", "date"], name="unique_daily_student_attendance"
            )
        ]
        ordering = ["-date", "-time"]

    def __str__(self):
        return f"{self.student_full_name} - {self.date} ({self.status})"

    def save(self, *args, **kwargs):
        if self._state.adding or not self.student_full_name:
            full_name = self.student.get_full_name().strip()
            self.student_full_name = full_name or self.student.username
        super().save(*args, **kwargs)
