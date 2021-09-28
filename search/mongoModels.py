from connection_to_mongodb import MongoBaseModel
from findTeacherProject import general_config

url = general_config.MONGO_URL

class SearchRoomModel(MongoBaseModel):
    fields = { 
        'user_id': {}, 
        'content_search': {}, 
    }

    url = url
    db_name = "userSearch"
    collection_name = "searchRoom"


class SearchTutorModel(MongoBaseModel):
    fields = {
        'user_id': {}, 
        'content_search': {},
    }

    url = url
    db_name = "userSearch"
    collection_name = "searchTutor"


class SearchParentModel(MongoBaseModel):
    fields = {
        "user_id": {}, 
        "content_search": {},
    }

    url = url
    db_name = "userSearch"
    collection_name = "searchParent"


