import json

import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from notification.mongoModels import ListGroupUserModel
from notification.models import ChannelNameModel

from multiprocessing import Process, Queue
from threading import Thread


class NotifyConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.user = self.scope["user"]

        await self.add_to_group()

        await database_sync_to_async(ChannelNameModel.objects.create)(user=self.user, 
                                                                channel_name=self.channel_name)

        if not self.user.is_authenticated:
            await self.close()
        else:
            await self.accept()


    async def add_to_group(self):
        collection = ListGroupUserModel().collection
        try:
            list_group = collection.find_one({ "user_id": self.user.id })
            self.following_groups = list_group.following_groups
        except:
            self.following_groups = []

        await asyncio.gather(*(self.channel_layer.group_add(group_name, self.channel_name) 
            for group_name in self.following_groups))


    async def disconnect(self, close_code):
        channel_item = await database_sync_to_async(ChannelNameModel.objects.get)(channel_name=self.channel_name)
        await database_sync_to_async(channel_item.delete)()

        await asyncio.gather(*(self.channel_layer.group_discard(group_name, self.channel_name) 
            for group_name in self.following_groups))

    async def notify_message(self, event):
        await self.send_json(
                event
            )
