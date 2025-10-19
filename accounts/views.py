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
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        # Split full name into first + last
        if fullname:
            parts = fullname.strip().split(" ", 1)
            firstname = parts[0]
            lastname = parts[1] if len(parts) > 1 else ""
        else:
            firstname = ""
            lastname = ""

        # Auto-generate username from email (before the @ symbol)
        username = email.split("@")[0]

        # Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:register")

        # Check email uniqueness
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("accounts:register")

        # Create the user
        user = User.objects.create_user(
            username=username,   # auto-generated
            email=email,
            password=password,
            firstname=firstname,
            lastname=lastname
        )
        Profile.objects.create(user=user)

        # Log the user in immediately after registration
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect("accounts:education-level")

    return render(request, "accounts/register.html")
