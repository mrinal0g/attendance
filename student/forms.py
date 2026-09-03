from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import StudentModel


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "email")

    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=10)
    batch_id = forms.ChoiceField(
        choices=(
            ("FSD_Batch_64", "FSD_Batch_64"),
            ("FSD_Batch_63", "FSD_Batch_63"),
            ("FSD_Batch_62", "FSD_Batch_62"),
            ("FSD_Batch_61", "FSD_Batch_61"),
            ("FSD_Batch_60", "FSD_Batch_60"),
            ("FSD_Batch_59", "FSD_Batch_59"),
            ("FSD_Batch_58", "FSD_Batch_58"),
        )
    )

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if StudentModel.objects.filter(phone=phone).exists():
            raise forms.ValidationError("A student with this phone number already exists.")
        return phone
