from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    category = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.category


class ChatMessage(models.Model):
    context = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.context
