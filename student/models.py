from django.db import models

class StudentModel(models.Model):
    id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.full_name