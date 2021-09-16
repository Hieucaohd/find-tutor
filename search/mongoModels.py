from mongo_model_base import MongoBaseModel

import urllib

url = "mongodb+srv://hieucao192:" + urllib.parse.quote("Caotrunghieu@192") + "@authenticationtest.6lh8w.mongodb.net/userSearch?retryWrites=true&w=majority"

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

