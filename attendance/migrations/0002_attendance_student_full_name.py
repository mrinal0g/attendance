from django.db import migrations, models


def copy_registered_student_names(apps, schema_editor):
    Attendance = apps.get_model("attendance", "Attendance")
    for attendance in Attendance.objects.select_related("student"):
        full_name = f"{attendance.student.first_name} {attendance.student.last_name}".strip()
        attendance.student_full_name = full_name or attendance.student.username
        attendance.save(update_fields=["student_full_name"])


class Migration(migrations.Migration):
    dependencies = [
        ("attendance", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance",
            name="student_full_name",
            field=models.CharField(default="", editable=False, max_length=301),
            preserve_default=False,
        ),
        migrations.RunPython(copy_registered_student_names, migrations.RunPython.noop),
    ]
