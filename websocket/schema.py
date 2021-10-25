import graphene

import pymongo

from authentication.types import UserType

from websocket.types import *
from websocket.mongoModels import *

import copy

from findTeacherProject.paginator import paginator_mongo_query


class Query(graphene.ObjectType):
    all_room_notification = graphene.List(RoomNotificationType, 
                                     page=graphene.Int(required=False),
                                     num_in_page=graphene.Int(required=False),
                                     token=graphene.String(required=True),)

    def resolve_all_room_notification(root, info, **kwargs):
        page = kwargs.get('page', 1)
        num_in_page = kwargs.get('num_in_page', 10)

        collection = RoomNotificationModel().collection

        user_id_receive = info.context.user.id
        
        cursor = collection.find({"user_id_receive": user_id_receive}).sort('create_at', pymongo.DESCENDING)

        return paginator_mongo_query(cursor=cursor, num_in_page=num_in_page, page=page)

    follow = graphene.Field(FollowType,
                            token=graphene.String(required=True),)

    def resolve_follow(root, info, **kwargs):
        collection = FollowModel().collection

        user_id = info.context.user.id

        follow = collection.find_one({"user_id": user_id})

        return follow




