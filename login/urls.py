from django.urls import path
from . import views

urlpatterns = [
    path('',views.StudentLogin.as_view(),name="login"),
    path('register/',views.StudentRegister.as_view(),name="register")
]