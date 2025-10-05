from django.urls import path
from . import views

app_name = "accounts"  # ✅ This registers the namespace

urlpatterns = [

    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    # add other routes here
]

