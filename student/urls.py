from django.urls import path
from . import views

urlpatterns = [
    path('',views.Sanity.as_view(),name='sanity'),
    # path('add/',views.AddStudent.as_view(),name='add_student'),
    # path('all/',views.AllStudents.as_view(),name='all_students'),
    path('search/', views.StudentSearch.as_view(), name='search-base'),
    path('search/<int:phone>/',views.StudentSearch.as_view(),name='search'),
]