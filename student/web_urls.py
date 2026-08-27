from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path("register/", views.RegisterPage.as_view(), name="register"),
    path('logout/', views.LogoutPage.as_view(), name='logout'),
    # path("search/", views.StudentSearchPage.as_view(), name="student-search"),
]
