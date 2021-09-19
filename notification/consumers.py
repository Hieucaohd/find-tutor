import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotifyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.accept()

    async def disconnect(self, close_code):
        pass
