from mongo_model_base import MongoBaseModel
from django.conf import settings


url = settings.MONGO_URL

class SearchRoomModel(MongoBaseModel):
	fields = ['user_id', 'content_search']
	url = url
	db_name = "userSearch"
	collection_name = "searchRoom"


class SearchTutorModel(MongoBaseModel):
	fields = ['user_id', 'content_search']
	url = url
	db_name = "userSearch"
	collection_name = "searchTutor"


class SearchParentModel(MongoBaseModel):
	fields = ["user_id", "content_search"]
	url = url
	db_name = "userSearch"
	collection_name = "searchParent"

