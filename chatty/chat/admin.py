from django.contrib import admin

from chat.models import ChatMessage, Chat

admin.site.register(Chat)
admin.site.register(ChatMessage)
