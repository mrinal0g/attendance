from django.conf import settings
from django.db import migrations, models


DEFAULT_BATCH_ID = "FSD_Batch_64"


def create_student_records_for_users(apps, schema_editor):
    User = apps.get_model("auth", "User")
    StudentModel = apps.get_model("student", "StudentModel")

    for user in User.objects.all().iterator():
        full_name = f"{user.first_name} {user.last_name}".strip() or user.username
        StudentModel.objects.get_or_create(
            id=user.id,
            defaults={
                "full_name": full_name,
                "email": user.email,
                "phone": None,
                "batch_id": DEFAULT_BATCH_ID,
            },
        )


def reverse_sync(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("student", "0002_studentmodel_batch_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentmodel",
            name="phone",
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                unique=True,
            ),
        ),
        migrations.RunPython(create_student_records_for_users, reverse_sync),
    ]
