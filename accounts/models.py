import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, firstname=None, lastname=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, firstname=firstname, lastname=lastname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, firstname=None, lastname=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, firstname, lastname, **extra_fields)

import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=150, unique=True)  # still stored
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, default='Student')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    # ✅ Use email for login instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'username'] # still required on creation

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email  # optional: now __str__ shows email



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    education_level = models.CharField(max_length=50, blank=True, null=True)
    grade_level = models.CharField(max_length=10, blank=True, null=True)
    school_year = models.CharField(max_length=20, blank=True, null=True)
    strand = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"