from pymongo import MongoClient
import urllib

url = "mongodb+srv://hieucao192:" + urllib.parse.quote("Caotrunghieu@192") + "@authenticationtest.6lh8w.mongodb.net/userSearch?retryWrites=true&w=majority"
client = MongoClient(url)
db = client.userSearch
