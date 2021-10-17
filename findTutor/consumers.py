import json

import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from notification.mongoModels import FollowModel
from notification.models import ChannelNameModel

from multiprocessing import Process, Queue
from threading import Thread

from notification.groups import GroupName

from findTutor.models import ParentRoomModel

import copy


class RoomConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group = await sync_to_async(GroupName.generate_group_name_for_realtime)(id=room_id, model=ParentRoomModel)
        await self.channel_layer.group_add(self.room_group, self.channel_name)

        # print("ban da thanh cong ket noi toi phong", self.room_group)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    async def room_message(self, event):
        event_copy = copy.deepcopy(event)
        del event_copy['type']
        await self.send_json(event_copy)


