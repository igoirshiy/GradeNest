"""
Django settings for GradeNest project.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# --------------------------
# BASE DIRECTORY & ENVIRONMENT
# --------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# --------------------------
# SECURITY
# --------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-(0&@=_43$i(a@0x(pa#$=@o)7q8yd5r^by@-75se995xsrs6j%")
DEBUG = True
ALLOWED_HOSTS = ["*"]

# --------------------------
# INSTALLED APPS
# --------------------------
INSTALLED_APPS = [
    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # custom app
    "accounts",
]

# --------------------------
# MIDDLEWARE
# --------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------
# URLS / WSGI
# --------------------------
ROOT_URLCONF = "GradeNest.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "accounts" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "GradeNest.wsgi.application"

# --------------------------
# DATABASE (Supabase)
# --------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL", "sqlite:///db.sqlite3"),
        conn_max_age=600,
        ssl_require=False,
    )
}

# --------------------------
# PASSWORD VALIDATION
# --------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------
# INTERNATIONALIZATION
# --------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True

# --------------------------
# STATIC FILES
# --------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "accounts" / "static"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------
# CUSTOM USER MODEL
# --------------------------
AUTH_USER_MODEL = "accounts.CustomUser"

# --------------------------
# LOGIN / LOGOUT REDIRECTS
# --------------------------
LOGIN_REDIRECT_URL = "/accounts/post-login/"
LOGOUT_REDIRECT_URL = "/accounts/login/"