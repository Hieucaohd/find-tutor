from django.shortcuts import render

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication import serializers
from authentication.models import User

from findTutor.models import ParentRoomModel

from websocket.groups import GroupName
from websocket.channel_layer_custom import ChannelLayerHandler
from websocket.serializers import FollowRoomSerializer, FollowUserSerializer

# Create your views here.

class FollowRoomList(APIView):
    serializer_class = FollowRoomSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return Response(status=status.HTTP_200_OK)


class FollowRoomDetail(APIView):
    serializer_class = FollowRoomSerializer

    def delete(self, request, room_id, format=None):
        parent_room = ParentRoomModel.objects.get(pk=room_id)

        room_group = GroupName.generate_group_name_for_all(parent_room)
        ChannelLayerHandler.group_discard(user=request.user, group_name=room_group)

        return Response({"room_id": room_id} ,status=status.HTTP_200_OK)
    

class FollowUserList(APIView):
    serializer_class = FollowUserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user_send=request.user)

        return Response(status=status.HTTP_200_OK)


class FollowUserDetail(APIView):
    serializer_class = FollowUserSerializer

    def delete(self, request, user_id, format=None):
        user = User.objects.get(pk=user_id)

        user_group = GroupName.generate_group_name_for_all(user)

        ChannelLayerHandler.group_discard(user=request.user, group_name=user_group)

        return Response({"user_id": user_id}, status=status.HTTP_200_OK)