from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import StudentDB
# Create your views here.

class StudentLogin(generic.TemplateView):
    template_name = 'student/student_login.html'

class StudentRegistration(CreateView):
    model= StudentDB
    fields = ['s_name', 'dob', 'emailid', 'contactno', 'address', 'profile_pic']

