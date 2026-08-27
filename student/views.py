from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import StudentSerializer
# from .models import StudentModel
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views import View

from .forms import RegistrationForm


def home(request):
    return render(request, "home.html")

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View

class LoginPage(View):
    def get(self, request):
        # If the user is already logged in, send them straight to their attendance page
        if request.user.is_authenticated:
            return redirect("attendance:student-attendance", username=request.user.username)
            
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        # AuthenticationForm expects the data keyword argument for POST data
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            # The form automatically authenticates the user; we just extract them
            user = form.get_user()
            
            # Start the session
            login(request, user)
            
            # Redirect directly to their specific attendance tracking page
            return redirect("attendance:student-attendance", username=user.username)
            
        # If login fails, reload the page with error messages
        return render(request, "login.html", {"form": form})


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View

class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect("login") # Redirects them to the login page after logging out

    
class RegisterPage(View):
    def get(self, request):
        return render(request, "register.html", {"form": RegistrationForm()})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration complete. Login with your account to mark your attendance.")
            return redirect("login")
        return render(request, "register.html", {"form": form})


# class StudentSearchPage(View):
#     def get(self, request):
#         return render(request, "student_search.html")

#     def post(self, request):
#         username = request.POST.get("username", "").strip()
#         User = get_user_model()
#         try:
#             student = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return render(
#                 request,
#                 "student_search.html",
#                 {"error": "No registered student was found with that username.", "username": username},
#             )
        return redirect("attendance:student-attendance", username=student.username)

class Sanity(APIView):
    def get(self,req):
        return Response({"message":"API is up and running"})

# class AddStudent(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self,request):
#         serializer_data = StudentSerializer(data=request.data)
#         if serializer_data.is_valid():
#             serializer_data.save()
#             return Response(serializer_data.data,
#                 status=status.HTTP_201_CREATED)
#         return Response(serializer_data.errors,status = status.HTTP_400_BAD_REQUEST)

# class StudentSearch(APIView):
#     def post(self,request,phone=None):
#         username = phone or request.data.get('username')
#         if not username:
#             return Response(
#                 {"error": "Phone number is required either in the URL path or POST body."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         student = StudentModel.objects.get(username=username)
#         return Response(StudentSerializer(student).data)


# class StudentSearch(APIView):
#     def post(self,request):
#         username = request.data.get("username",None)
#         if username == None:
#             return Response(
#                             {"error": "username is required either in the URL path or POST body."},
#                             status=status.HTTP_400_BAD_REQUEST
#                         )
#         try:
#             student = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return Response(
#                 {"detail": "No registered student was found with that username."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         data = {
#                 "id": student.id,
#                 "username": student.username,
#                 "email": student.email,
#                 "first_name": student.first_name,
#                 "last_name": student.last_name,
#                 }
#         return Response(data)
            
    
# class AllStudents(APIView):
#     def get(self,request):
#         students = StudentSerializer(StudentModel.objects.all(),many=True)
#         return Response(students.data)
