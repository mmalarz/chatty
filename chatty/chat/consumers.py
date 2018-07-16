import datetime
from collections import defaultdict

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from chat.models import ChatMessage, Chat


class ChatConsumer(WebsocketConsumer):

    active_users = defaultdict(list)

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_{}'.format(self.room_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        ChatConsumer.active_users[self.room_name].append(self.scope['user'].first_name + ' ' + self.scope['user'].last_name)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'active_users_message',
                'users': ChatConsumer.active_users,
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        ChatConsumer.active_users[self.room_name].remove(self.scope['user'].first_name + ' ' + self.scope['user'].last_name)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'active_users_message',
                'users': ChatConsumer.active_users,
            }
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if message:
            username = self.scope['user'].username
            first_name = self.scope['user'].first_name
            last_name = self.scope['user'].last_name

            # save to database
            user = get_object_or_404(User, username=username)
            chat = get_object_or_404(Chat, category=self.room_name)
            ChatMessage.objects.create(context=message, chat=chat, user=user)

            print('SENDING MESSAGE')
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )

    def chat_message(self, event):
        print('event: ', event)
        message = event['message']
        username = event['username']
        first_name = event['first_name']
        last_name = event['last_name']

        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
        }))

    def active_users_message(self, event):
        users = event['users']

        self.send(text_data=json.dumps({
            'users': users,
        }))
