# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required

User = get_user_model()

def dashboard_view(request):
    # optional: get profile info
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/dashboard.html', {'profile': profile})

def education_level(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        profile.education_level = request.POST.get("education_level")
        profile.grade_level = request.POST.get("grade_level")
        profile.school_year = request.POST.get("school_year")
        profile.strand = request.POST.get("strand")
        profile.save()
        return redirect("accounts:dashboard")

    return render(request, "accounts/education-level.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")  # <-- changed from username
        password = request.POST.get("password")
        
        # authenticate using email and password
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("accounts:dashboard")  # your landing page
        else:
            messages.error(request, "Invalid email or password.")
    
    # For GET requests or failed login
    return render(request, "accounts/login.html")

def register_view(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        # Password validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:register")

        # Username / email uniqueness validation
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

        # Automatically create profile
        Profile.objects.create(user=user)

        # 🔹 Correct authentication using email
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)

        # Redirect to education-level page
        return redirect("accounts:education-level")

    return render(request, 'accounts/register.html')
