import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SimpleVideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'video_room'  # Single room for testing
        self.room_group_name = f'video_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"Client connected: {self.channel_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"Client disconnected: {self.channel_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        # Forward all messages to everyone except sender
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'forward_message',
                'data': data,
                'sender': self.channel_name,
            }
        )

    async def forward_message(self, event):
        # Don't send back to the sender
        if self.channel_name != event['sender']:
            await self.send(text_data=json.dumps(event['data']))