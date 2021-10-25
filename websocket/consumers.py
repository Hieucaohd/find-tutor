import json

import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from websocket.mongoModels import FollowModel, RoomNotificationModel
from websocket.models import ChannelNameModel

from multiprocessing import Process, Queue
from threading import Thread

from websocket.groups import GroupName

import copy

import datetime


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
        await self.accept("Token")
        add_to_group.join()

    async def disconnect(self, close_code):
        if not self.user.is_authenticated:
            return

        # kiem tra xem con channel nao cua nguoi dung hay khong
        # neu khong con thi dua tat ca cac is_new cua thong bao ve false
        channel_names_of_user = await database_sync_to_async(ChannelNameModel.objects.filter)(user=self.user)
        if sync_to_async(len)(channel_names_of_user) == 1:
            # dua tat ca is_new cua cac thong bao co is_new = True la false
            threading.Thread(target=RoomNotificationModel().collection.update_many, kwargs={
                                                                                            "filter": { "is_new": True }, 
                                                                                            "update": { "is_new": False },
                                                                                            }).start()

        channel_item = await database_sync_to_async(ChannelNameModel.objects.get)(channel_name=self.channel_name)
        await database_sync_to_async(channel_item.delete)()

        await asyncio.gather(*(self.channel_layer.group_discard(group_name, self.channel_name) 
            for group_name in self.following_groups))

    async def notify_message(self, event):
        event_copy = copy.deepcopy(event)
        del event_copy['type']
        await self.send_json(event_copy)





