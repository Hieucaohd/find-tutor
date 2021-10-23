import graphene

from authentication.types import UserType
from authentication.models import User

from websocket.mongoModels import *
from websocket.groups import GroupName

from findTutor.types import ParentRoomType
from findTutor.models import ParentRoomModel

import json
from types import SimpleNamespace


class TextOfRoomNotificationType(graphene.ObjectType):
    id = graphene.String()
    user_send = graphene.Field(UserType)

    def resolve_id(root, info, **kwargs):
        return root["id"]

    def resolve_user_send(root, info, **kwargs):
        try:
            return User.objects.get(pk=root["user_send"]["id"])
        except User.DoesNotExist:
            return "User does not exist"


class RoomNotificationType(graphene.ObjectType):
    _id = graphene.ID()
    user_id_send = graphene.Int()
    user_send = graphene.Field(UserType)
    user_id_receive = graphene.Int()
    user_receive = graphene.Field(UserType)
    room = graphene.Field(ParentRoomType)
    is_seen = graphene.Boolean()
    text = graphene.Field(TextOfRoomNotificationType)
    create_at = graphene.DateTime()


    def resolve__id(root, info, **kwargs):
        return root['_id']


    def resolve_user_id_send(root, info, **kwargs):
        return root['user_id_send']


    def resolve_user_send(root, info, **kwargs):
        try:
            return User.objects.get(pk=root['user_id_send'])
        except User.DoesNotExist:
            return "User does not exist"


    def resolve_user_id_receive(root, info, **kwargs):
        return root['user_id_receive']


    def resolve_user_receive(root, info, **kwargs):
        try:
            return User.objects.get(pk=root['user_id_receive'])
        except User.DoesNotExist:
            return "User does not exist"


    def resolve_room(root, info, **kwargs):
        try:
            return ParentRoomModel.objects.get(pk=root['room']['id'])
        except ParentRoomModel.DoesNotExist:
            return "room does not exist"


    def resolve_is_seen(root, info, **kwargs):
        return root.get("is_seen", False)


    def resolve_text(root, info, **kwargs):
        return root['text']


    def resolve_create_at(root, info, **kwargs):
        return root['create_at']


class FollowType(graphene.ObjectType):
    _id = graphene.ID()
    user_id = graphene.Int()
    user = graphene.Field(UserType)
    following_groups = graphene.List(graphene.String)
    following_rooms = graphene.List(ParentRoomType,
                                    number_items=graphene.Int(required=False))
    following_users = graphene.Field(UserType,
                                    number_items=graphene.Int(required=False))

    def resolve__id(root, info, **kwargs):
        return root['_id']


    def resolve_user_id(root, info, **kwargs):
        return root['user_id']


    def resolve_user(root, info, **kwargs):
        try:
            return User.objects.get(pk=root['user_id'])
        except User.DoesNotExist:
            return "User does not exist"


    def resolve_following_groups(root, info, **kwargs):
        return root['following_groups']


    def resolve_following_rooms(root, info, **kwargs):
        following_groups = root['following_groups']
        number_items = kwargs.get("number_items", 6)

        rooms = []
        for group_name in following_groups:
            decoded_group = GroupName.decode_from_group_name(group_name)
            model_name, id = decoded_group['model_name'], decoded_group['id']

            if model_name == ParentRoomModel.__name__:
                try:
                    room = ParentRoomModel.objects.get(pk=id)
                    rooms.append(room)
                except:
                    pass

        return rooms[0:number_items]


    def resolve_following_users(root, info, **kwargs):
        following_groups = root['following_groups']
        number_items = kwargs.get("number_items", 6)

        users = []
        for group_name in following_groups:
            decoded_group = GroupName.decode_from_group_name(group_name)
            model_name, id = decoded_group['model_name'], decoded_group['id']

            if model_name == User.__name__:
                try:
                    room = User.objects.get(pk=id)
                    users.append(room)
                except:
                    pass

        return users[0:number_items]
