# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

def education_level(request):
    return render(request, 'accounts/education-level.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")  # use username now
        password = request.POST.get("password")
        
        # authenticate using username and password
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("accounts:education-level")  # replace "home" with your landing page URL name
        else:
            messages.error(request, "Invalid username or password.")
    
    # For GET requests or failed login
    return render(request, "accounts/login.html")

def register_view(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")  # NEW
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")


        # Check passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:register")

        # Check username/email uniqueness
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("accounts:register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("accounts:register")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            firstname=firstname,
            lastname=lastname
        )
        user.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect("accounts:login")

    return render(request, 'accounts/register.html')

