"""
Django settings for GradeNest project.
"""

from pathlib import Path
import os
import dj_database_url               # ✅ add this
from dotenv import load_dotenv       # ✅ add this


# --------------------------
# BASE DIRECTORY & ENVIRONMENT
# --------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Load environment variables from .env
load_dotenv()

# --------------------------
# SECURITY
# --------------------------
SECRET_KEY = 'django-insecure-(0&@=_43$i(a@0x(pa#$=@o)7q8yd5r^by@-75se995xsrs6j%'
DEBUG = True
ALLOWED_HOSTS = []

# --------------------------
# INSTALLED APPS
# --------------------------
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Required by django-allauth
    'django.contrib.sites',

    # Allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Your app
    'accounts',
]

# --------------------------
# MIDDLEWARE
# --------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------------
# URLS / WSGI
# --------------------------
ROOT_URLCONF = 'GradeNest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # ✅ Make sure Django can find your templates
        'DIRS': [BASE_DIR / 'accounts' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'GradeNest.wsgi.application'

# --------------------------
# DATABASE (Supabase via Session Pooler)
# --------------------------
DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///db.sqlite3",  # fallback if DATABASE_URL not found
        conn_max_age=600,                # persistent connections
        ssl_require=True                 # enforce SSL (required by Supabase)
    )
}

# --------------------------
# PASSWORD VALIDATION
# --------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------
# INTERNATIONALIZATION
# --------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

# --------------------------
# STATIC FILES
# --------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "accounts" / "static"]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------------------------
# DJANGO-ALLAUTH CONFIG
# --------------------------
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Redirects after login/logout
LOGIN_REDIRECT_URL = '/accounts/post-login/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Google OAuth Credentials (replace with real ones)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '1014594358295-rvnslhldo7l999r6nju9m5jnl27m4hnf.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account',
        },
    }
}

# Optional — helps login on GET request
SOCIALACCOUNT_LOGIN_ON_GET = True
