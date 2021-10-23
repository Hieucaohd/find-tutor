import graphene

import pymongo

from authentication.types import UserType

from websocket.types import *
from websocket.mongoModels import *

import copy


class Query(graphene.ObjectType):
    all_room_notification = graphene.List(RoomNotificationType, 
                                     number_notifications=graphene.Int(required=False),
                                     token=graphene.String(required=False),)

    def resolve_all_room_notification(root, info, **kwargs):
        collection = RoomNotificationModel().collection

        number_notifications = kwargs.get("number_notifications", 6)

        user_id_receive = info.context.user.id
        
        room_notifications = collection.find({"user_id_receive": user_id_receive}).sort('create_at', pymongo.DESCENDING)

        return copy.deepcopy(room_notifications)[0:number_notifications]

    follow = graphene.Field(FollowType,
                            token=graphene.String(required=False),)

    def resolve_follow(root, info, **kwargs):
        collection = FollowModel().collection

        user_id = info.context.user.id

        follow = collection.find_one({"user_id": user_id})

        return follow




