from rest_framework.serializers import ModelSerializer
from .models import StudentModel

class StudentSerializer(ModelSerializer):
    class Meta:
        model=StudentModel
        fields = "__all__"
    