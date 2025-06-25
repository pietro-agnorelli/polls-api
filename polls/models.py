from django.db import models

# Create your models here.


class Polls(models.Model):
    question = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey('auth.User', related_name='polls', on_delete=models.CASCADE)


class Choices(models.Model):
    poll = models.ForeignKey(Polls, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)