from django.contrib import admin
from .models import StudentModel


@admin.register(StudentModel)
class StudentModelAdmin(admin.ModelAdmin):
	list_display = ('id', 'full_name', 'email', 'phone', 'batch_id')
	search_fields = ('full_name', 'email', 'phone', 'batch_id')
	list_filter = ('batch_id',)