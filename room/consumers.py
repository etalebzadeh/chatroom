
import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')
django.setup()
import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async


from django.contrib.auth.models import User
from . models import *

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs'].get('room_name', '')
        self.room_group_name = 'chat_%s' % self.room_name       

        print(self.channel_layer)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data["username"]
        room = data['room']
        pk = uuid.uuid4().time_mid

        await self.save_message(pk, username, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "room": room,
                "message_id": pk
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        room = event['room']
        message_id=event["message_id"]

        # save db

        await self.send(text_data=json.dumps({
            "message": message,
            "username":username,
            "room":room,
            "message_id": message_id
        }))

    @sync_to_async
    def save_message(self, pk, username, room, message):
        user = User.objects.get(username=username)
        room_n = Room.objects.get(slug=room)
        Message.objects.create(pk=pk, user=user, room=room_n, content=message)
