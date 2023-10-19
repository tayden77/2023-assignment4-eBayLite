from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    