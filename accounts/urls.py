# accounts/urls.py
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("education-level/", views.education_level, name="education_level"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("post-login/", views.post_login, name="post_login"),  # 👈 add this
]
