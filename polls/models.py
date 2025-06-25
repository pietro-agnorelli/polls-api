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


class Votes(models.Model):
    poll = models.ForeignKey(Polls, related_name='votes', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choices, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='votes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('choice', 'user')  # Ensure a user can vote only once per choice