import threading
from .mongoConfig import db

def get_varname(varname):
	return f'{varname=}'.split('=')[0]

class MongoModelBase(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

class SearchRoomModel(MongoModelBase):
	fields_array = ['userId', 'contentSearch', 'createAt']
	def __init__(self):
		pass

	def run(self):
		pass

