from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from .models import Profile
from django.contrib.auth.decorators import login_required

# ---------------- Register -   ---------------
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "accounts/register.html", {"username": username, "email": email})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "accounts/register.html", {"email": email})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, "accounts/register.html", {"username": username})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        Profile.objects.create(user=user)  # create empty profile for new user

        messages.success(request, "✅ Account created successfully! Please log in.")
        return redirect("accounts:login")

    return render(request, "accounts/register.html")


# ---------------- Login ----------------
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("username").strip()
        password = request.POST.get("password")

        # Check if email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "❌ Email not found. Please register first.")
            return render(request, "accounts/login.html", {"login_input": email})

        # Authenticate user using username
        user_auth = authenticate(request, username=user.username, password=password)

        if user_auth is not None:
            auth_login(request, user_auth)

            # Check if the user has already selected an education level
            profile, created = Profile.objects.get_or_create(user=user_auth)
            if not profile.education_level:  # first-time login
                return redirect("accounts:education_level")

            messages.success(request, f"👋 Welcome back, {user.username}!")
            return redirect("accounts:dashboard")
        else:
            messages.error(request, "❌ Incorrect password. Please try again.")
            return render(request, "accounts/login.html", {"login_input": email})

    return render(request, "accounts/login.html")


# ---------------- Education Level ----------------
def education_level(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    profile, _ = Profile.objects.get_or_create(user=request.user)

    # If profile already has an education level, skip this step
    if profile.education_level:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        grade = request.POST.get("gradeLevel")
        strand = request.POST.get("strand")

        profile.education_level = f"{grade} - {strand}"
        profile.save()

        return redirect("accounts:dashboard")

    return render(request, "accounts/education-level.html")


# ---------------- Logout ----------------
def user_logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")


# ---------------- Dashboard ----------------
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
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

    # ✅ Clear unwanted "successfully signed in" messages from Google
    storage = messages.get_messages(request)
    storage.used = True  # this clears the existing messages

    profile, _ = Profile.objects.get_or_create(user=request.user)

    # First-time Google login (no education level yet)
    if not profile.education_level:
        return redirect("accounts:education_level")

    # Returning user
    return redirect("accounts:dashboard")

