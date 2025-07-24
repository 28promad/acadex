from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        is_teacher = request.POST.get('is_teacher', False)
        
        # Basic validation
        if password1 != password2:
            messages.error(request, "Passwords don't match!")
            return render(request, 'accounts/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'accounts/signup.html')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        
        # Create profile
        Profile.objects.create(user=user, is_teacher=bool(is_teacher))
        
        # Log in user
        login(request, user)
        messages.success(request, f"Welcome to Acadex, {username}! 🎉")
        
        return redirect('dashboard')
    
    return render(request, 'accounts/signup.html')