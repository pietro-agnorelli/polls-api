from django.db import models
from django.contrib.auth.models import User
from polls.models import Polls


# Create your models here.


class AuthUser(User):
    polls = models.ManyToManyField(Polls)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)