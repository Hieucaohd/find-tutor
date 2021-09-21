from django.conf import settings
from mongo_model_base import MongoBaseModel

url = settings.MONGO_URL

db_name = "notification"

class FriendModel(MongoBaseModel):
    fields = ["user_id", "list_friends"]
    url = url
    db_name = db_name
    collection_name = "friends"
