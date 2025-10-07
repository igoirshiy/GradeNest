from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from .models import Profile
from django.contrib.auth.decorators import login_required


# ---------------- Register ----------------
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")

        # Password validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "accounts/register.html", {"username": username, "email": email})

        # Duplicate check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "accounts/register.html", {"email": email})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, "accounts/register.html", {"username": username})

        # ✅ Create user and log them in immediately
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        Profile.objects.create(user=user)

        # ✅ Specify backend since allauth is installed
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return redirect("accounts:education_level")

    return render(request, "accounts/register.html")


# ---------------- Login ----------------
def user_login(request):    
    if request.method == "POST":
        email = request.POST.get("username").strip()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "❌ Email not found. Please register first.")
            return render(request, "accounts/login.html", {"login_input": email})

        # Authenticate using username (since Django requires it)
        user_auth = authenticate(request, username=user.username, password=password)

        if user_auth is not None:
            auth_login(request, user_auth)
            profile, _ = Profile.objects.get_or_create(user=user_auth)

            # ✅ Check if education level is already set
            if not profile.education_level:
                return redirect("accounts:education_level")

    
            return redirect("accounts:dashboard")
        else:
            messages.error(request, "❌ Incorrect password. Please try again.")
            return render(request, "accounts/login.html", {"login_input": email})

    return render(request, "accounts/login.html")


# ---------------- Education Level ----------------
@login_required
def education_level(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # If already set, skip
    if profile.education_level:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        grade = request.POST.get("gradeLevel")
        strand = request.POST.get("strand")

        # ✅ Fix: Allow strand to be optional (for JHS)
        if not grade:
            messages.error(request, "Please select your grade level.")
            return render(request, "accounts/education-level.html")

        if "Grade 11" in grade or "Grade 12" in grade:
            if not strand:
                messages.error(request, "Please select your strand for SHS.")
                return render(request, "accounts/education-level.html")
            profile.education_level = f"{grade} - {strand}"
        else:
            profile.education_level = grade  # no strand for JHS

        profile.save()
        return redirect("accounts:dashboard")

    return render(request, "accounts/education-level.html")


# ---------------- Logout ----------------
def user_logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")


# ---------------- Dashboard ----------------
@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")


# ---------------- Post Google Login Redirect ----------------
def post_login(request):
    """
    Handles redirect logic after Google login.
    - If first-time Google login → go to education-level
    - If returning user → go to dashboard
    """
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    # Clear Google's success message
    storage = messages.get_messages(request)
    storage.used = True

    profile, _ = Profile.objects.get_or_create(user=request.user)

    # ✅ If first-time Google login (no education level)
    if not profile.education_level:
        return redirect("accounts:education_level")

    return redirect("accounts:dashboard")
