from django.shortcuts import render
from django.http import HttpResponse

def register(request):
    return render(request,'Authentication/register.html')

def login_user(request):
    return render(request,'Authentication/login.html')
