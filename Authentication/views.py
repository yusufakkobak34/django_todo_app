from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_data_has_error = False

        if not(first_name and last_name and username and email and password and confirm_password):
            messages.error(request,'Tüm alanların doldurulması zorunludur')
            user_data_has_error = True

        if User.objects.filter(username = username).exists():
            messages.error(request, 'Mevcut kullanıcı adıyla sisteme kayıtlı kullanıcı mevcut')
            user_data_has_error = True
        
        if User.objects.filter(email = email).exists():
            messages.error(request, 'Mevcut e-posta ile sisteme kayıtlı kullanıcı mevcut')
            user_data_has_error = True
        
        if len(password) < 5:
            messages.error(request,'Şifreniz 5 karakterden az olamaz')
            user_data_has_error = True
        
        if password != confirm_password:
            messages.error(request,'Şifreler uyuşmuyor')
            user_data_has_error = True

        if user_data_has_error:
            return redirect('register')

        user = User.objects.create_user(
            username = username,
            email = email,
            password = password,
            first_name = first_name,
            last_name = last_name
        )
        user.save()
        messages.success(request,'Hesap başarıyla oluşturuldu')
        return redirect('login')    

    return render(request,'Authentication/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not(username and password):
            messages.error(request, 'Tüm alanların doldurulması zorunludur')
            return redirect('login')
        
        user = authenticate(request = request, username = username, password = password)

        if user is not None:
            login(request,user)

            # Redirect the user to home page
            return redirect('home')

        else: 
            messages.error(request,'Geçersiz kullanıcı adı veya şifre')
            return redirect('login')    
        

    return render(request,'Authentication/login.html')
@login_required

def home(request):
    return HttpResponse('Başarıyla yetkilendirildi')