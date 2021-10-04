import json

import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from notification.mongoModels import FollowModel
from notification.models import ChannelNameModel

from multiprocessing import Process, Queue
from threading import Thread


class DoInThead(Thread):
    def __init__(self, notify_consumer):
        self.notify_consumer = notify_consumer
        Thread.__init__(self)

    def run(self):
        collection = FollowModel().collection
        try:
            list_group = collection.find_one({ "user_id": self.notify_consumer.user.id })
            self.notify_consumer.following_groups = list_group.following_groups
        except:
            self.notify_consumer.following_groups = []

        for group_name in self.notify_consumer.following_groups:
            sync_to_async(self.notify_consumer.channel_layer.group_add)(group_name, self.notify_consumer.channel_name) 



class NotifyConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        add_to_group = DoInThead(self)
        add_to_group.start()

        await database_sync_to_async(ChannelNameModel.objects.create)(user=self.user, 
                                                                channel_name=self.channel_name)
        await self.accept()
        add_to_group.join()


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
        if not self.user.is_authenticated:
            return

        channel_item = await database_sync_to_async(ChannelNameModel.objects.get)(channel_name=self.channel_name)
        await database_sync_to_async(channel_item.delete)()

        await asyncio.gather(*(self.channel_layer.group_discard(group_name, self.channel_name) 
            for group_name in self.following_groups))

    async def receive_json(self, content, **kwargs):
        content['type'] = "notify.message"
        content['send message'] = "tôi là hiếu nhé"
        await self.channel_layer.send(self.channel_name, content)

    async def notify_message(self, event):
        del event['type']
        await self.send_json(event)



