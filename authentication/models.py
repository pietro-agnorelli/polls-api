from django.db import models
from django.contrib.auth.models import AbstractUser
from polls.models import Polls


# Create your models here.


class PollsUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    gender = models.CharField(max_length=10, blank=True)