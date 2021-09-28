from django.conf import settings
from connection_to_mongodb import MongoBaseModel
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findTeacherProject.settings')

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
        "list_follower": {}, 
        "list_user_following": {}, 
        "list_room_following": {},
    }

    url = url
    db_name = db_name
    collection_name = "follows"


class FollowRoomModel(MongoBaseModel):
    fields = {
        "room_id": { "unique": True }, 
        "list_follower": {},
    }

    url = url
    db_name = db_name
    collection_name = "followRoom"


class ListGroupUserModel(MongoBaseModel):
    fields = {
        "user_id": { "unique": True },
        "my_group": { "unique": True },
        "following_groups": {},
    }

    url = url
    db_name = db_name
    collection_name = "listGroups"


class NotifyModel(MongoBaseModel):
    fields = {
        "user_id": {},
        "from_group": {},
        "user_send": {},
    }

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
