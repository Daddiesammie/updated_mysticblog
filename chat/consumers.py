import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message, Notification
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"WebSocket connected: {self.channel_name} for user {self.user.username}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(f"Received message: {message} from user {self.user.username}")

        message_instance = await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
                'message_id': message_instance.id,
                'timestamp': message_instance.created_at.isoformat(),
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
        print(f"Sent message: {event['message']} to {self.channel_name}")

    @database_sync_to_async
    def save_message(self, content):
        chatroom = ChatRoom.objects.get(id=self.room_name)
        message = Message.objects.create(
            chatroom=chatroom,
            user=self.user,
            content=content
        )
        print(f"Saved message: {message.content} for user {self.user.username}")
        return message