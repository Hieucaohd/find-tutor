from connection_to_mongodb import MongoBaseModel
from django.conf import settings

url = settings.MONGO_URL

db_name = "notification"

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
        "room_id": {},
        "content": {},
        "user_id_send": {},
        "user_id_receive": {},
        "is_seen": {},
        "room": {},
        "type_notify": {}
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


"""
tutor:
    - another people reply his/her comment
    - another want to be friend

    - parent kick him/her from waiting list 
    - parent accept/not accept him/her to teaching

    - parent change the room that tutor being.
    
    - parent invited him/her

parent:
    - another people reply his/her comment
    - another want to be friend

    - tutor apply to him/her room
    - tutor ok to teaching
"""
