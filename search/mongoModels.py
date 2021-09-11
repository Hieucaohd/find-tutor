import threading, queue
from multiprocessing import Process, Queue
from .mongoConfig import client

# def get_varname(varname):
# 	return f'{varname=}'.split('=')[0]

class SearchBaseModel():
	def __init__(self):
		self.db = client.userSearch

	def create(self):
		pass

class SearchRoomModel(SearchBaseModel):
	def __init__(self):
		SearchBaseModel.__init__(self)
		self.collection = self.db.searchRoom

	def get(self):
		pass

	def create(self):
		pass

	def update(self):
		pass

	def delete(self):
		pass