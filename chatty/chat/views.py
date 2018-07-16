from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
import json

from chat.models import ChatMessage, Chat


def index(request):
    context = {
        'chats': Chat.objects.all(),
    }
    return render(request, 'chat/index.html', context)


def room(request, room_name):
    chat = get_object_or_404(Chat, category=room_name)
    messages = ChatMessage.objects.filter(chat=chat).order_by('-timestamp')

    context = {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'user_json': mark_safe(json.dumps(request.user.username)),
        'chat': chat,
        'chats': Chat.objects.all(),
        'messages': messages,
    }

    return render(request, 'chat/room.html', context)
