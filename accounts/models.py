from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    realname = models.TextField(max_length=20) # 이름
    department = models.TextField(max_length=20) # 부서
