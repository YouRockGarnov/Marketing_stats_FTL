from pymongo import MongoClient

client = MongoClient("192.168.99.110", 27017)

db = client.hackaton_db
