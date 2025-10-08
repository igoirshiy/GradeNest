from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade_level = models.CharField(max_length=50, blank=True, null=True)
    strand = models.CharField(max_length=100, blank=True, null=True)
    school_year = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username
