import threading, queue
from multiprocessing import Process, Queue
import datetime

from .mongoConfig import client, url
from pymongo import MongoClient
import copy


def get_varname(varname):
	return f'{varname=}'.split('=')[0]


def create_connection_to_mongo(db_name, collection_name):
	client = MongoClient(url)
	local_func = locals()
	exec(f"connected = client.{db_name}.{collection_name}", globals(), local_func)
	connected = local_func["connected"]
	return connected


class MongoBaseModel:
	def __init__(self):
		exec(f"self.db = client.{self.db_name}")
		exec(f"self.collection = self.db.{self.collection_name}")


class SearchBaseModel(MongoBaseModel):
	def __init__(self, **kwargs):
		self.db_name = "userSearch"
		self.data = copy.deepcopy(kwargs)
		self.create_thread = Process
		
		self.validate_data()
		MongoBaseModel.__init__(self)

	def create_in_thread(self, data):
		create_connection_to_mongo(self.db_name, self.collection_name).insert_one(data)

	def create(self, take_result=False):
		self.data['create_at'] = datetime.datetime.now()

		if take_result:
			return self.collection.insert_one(self.data)
		else:
			self.create_thread(target=self.create_in_thread, args=(self.data,)).start()

	def validate_data(self):
		for field in self.data:
			if field not in self.fields:
				del self.data[field]


class SearchRoomModel(SearchBaseModel):
	fields = ['user_id', 'content_search']
	def __init__(self, **kwargs):
		self.collection_name = "searchRoom"
		SearchBaseModel.__init__(self, **kwargs)


class SearchTutorModel(SearchBaseModel):
	fields = ['user_id', 'content_search']
	def __init__(self, **kwargs):
		self.collection_name = "searchTutor"
		SearchBaseModel.__init__(self, **kwargs)


class SearchParentModel(SearchBaseModel):
	fields = ["user_id", "content_search"]
	def __init__(self, **kwargs):
		self.collection_name = "searchParent"
		SearchBaseModel.__init__(self, **kwargs)





