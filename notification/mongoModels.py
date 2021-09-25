from django.conf import settings
from mongo_model_base import MongoBaseModel

url = settings.MONGO_URL

db_name = "notification"

class FriendModel(MongoBaseModel):
    fields = {
        "user_id": { unique: True }, 
        "list_friends": {},
    }

    url = url
    db_name = db_name
    collection_name = "friends"


class FollowModel(MongoBaseModel):
    fields = {
        "user_id": { unique: True }, 
        "list_follower": {}, 
        "list_user_following": {}, 
        "list_room_following": {},
    }

    url = url
    db_name = db_name
    collection_name = "follows"


class FollowRoomModel(MongoBaseModel):
    fields = {
        "room_id": { unique: True }, 
        "list_follower": {},
    }

    url = url
    db_name = db_name
    collection_name = "followRoom"


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
