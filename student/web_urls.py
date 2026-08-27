from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.RegisterPage.as_view(), name="register"),
    path("search/", views.StudentSearchPage.as_view(), name="student-search"),
]
