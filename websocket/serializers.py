from rest_framework import serializers, fields
from authentication.models import User

from findTutor.models import ParentRoomModel

from websocket.groups import GroupName
from websocket.channel_layer_custom import ChannelLayerHandler


class FollowRoomSerializer(serializers.Serializer):
    room_id = serializers.IntegerField(required=True)

    def validate(self, data):
        room_id = data.get("room_id")
        try:
            parent_room = ParentRoomModel.objects.get(pk=room_id)
        except ParentRoomModel.DoesNotExist:
            raise serializers.ValidationError("Room does not exists.")
        return data

    def create(self, validated_data):
        room_id = validated_data.get("room_id")
        user = validated_data.get("user")

        parent_room = ParentRoomModel.objects.get(pk=room_id)

        room_group = GroupName.generate_group_name_for_all(parent_room)

        ChannelLayerHandler.group_add(user=user, group_name=room_group)

        return room_id
    
    def update(self, instance, validated_data):
        pass


class FollowUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)

    def validate(self, data):
        user_id = data.get("user_id")

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exists.")
        return data
    
    def create(self, validated_data):
        user_id = validated_data.get("user_id")
        user = User.objects.get(pk=user_id)
        user_group = GroupName.generate_group_name_for_all(user)

        user_send = validated_data.get("user_send")

        ChannelLayerHandler.group_add(user=user_send, group_name=user_group)

        return user_id
    
    def update(self, instance, validated_data):
        pass
    







