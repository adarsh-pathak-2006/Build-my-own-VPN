from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    otpid=models.CharField(max_length=6, null=True)

