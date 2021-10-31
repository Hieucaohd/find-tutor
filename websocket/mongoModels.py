from connection_to_mongodb import MongoBaseModel
from django.conf import settings

url = settings.MONGO_URL

db_name = "websocket"

class FriendModel(MongoBaseModel):
    fields = {
        "user_id": { "unique": True }, 
        "list_friends": {},
    }

    url = url
    db_name = db_name
    collection_name = "friends"


class FollowModel(MongoBaseModel):
    fields = {
        "user_id": { "unique": True }, 
        "following_groups": {}  # danh sach cac group ma user dang theo doi
    }

    url = url
    db_name = db_name
    collection_name = "follows"


class RoomNotificationModel(MongoBaseModel):
    fields = {
        "user_id_send": {
            "required": True,
            "type": int,
        },
        "user_id_receive": {
            "required": True,
            "type": int,
        },
        "room": {},
        "text": {},
        "is_click": {
            "default": False,
            "type": bool,
        },
        "is_new": { 
            "required": True,
            "default": True,
            "type": bool,
        },
        "try": "he",
    }

    url = url
    db_name = db_name
    collection_name = "roomNotifications"

class UserNotificationModel(MongoBaseModel):
    fields = {
        "user_id_send": {},
        "user_id_receive": {},
        "content": {},
        "is_seen": {},
    }

    url = url
    db_name = db_name
    collection_name = "userNotifications"


