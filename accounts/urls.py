# accounts/urls.py
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.login_view, name='login'),  # base accounts/ → login page
    path('register/', views.register_view, name='register'),
    path('education-level/', views.education_level, name='education-level'),
]
