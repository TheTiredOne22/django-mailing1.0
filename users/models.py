from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# class CustomUser(AbstractUser):
#     username = None
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.CharField(unique=True)
#     USERNAME_FIELD = ['email']
#
#     def __str__(self):
#         return self.email
