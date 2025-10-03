# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()  # must be AFTER importing get_user_model

def login_view(request):
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("accounts:register")

        # create the user
        user = User.objects.create_user(
            email=email,
            password=password,
            firstname=firstname,
            lastname=lastname
        )
        user.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect("accounts:login")

    return render(request, 'accounts/register.html')


def education_level_view(request):
    return render(request, 'accounts/education_level.html')
