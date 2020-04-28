from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Tweet(models.Model):
    content = models.TextField(max_length=140, null=False, blank=False, verbose_name='Treść')
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disabled = models.BooleanField(default=False, verbose_name="Wyłączone")

    def __str__(self):
        return f'Tweet(from="{self.user.username}", content="{self.content[:5]}...")'


class Message(models.Model):
    content = models.TextField(max_length=140, null=False, blank=False, verbose_name='Treść')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    seen = models.BooleanField(default=False, verbose_name="Przeczytana")
    creation_date = models.DateTimeField(auto_now_add=True)
    disabled = models.BooleanField(default=False, verbose_name="Wyłączone")

    def __str__(self):
        return f'{self.sender.username} --> {self.receiver.username}'


class Comment(models.Model):
    content = models.TextField(max_length=140, null=False, blank=False, verbose_name='Treść')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    disabled = models.BooleanField(default=False, verbose_name="Wyłączone")

    def __str__(self):
        return f'Author={self.author}'
