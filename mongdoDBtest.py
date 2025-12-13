#import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['christmas_gifts_db']

gifts = db.gifts.find()

for gift in gifts:
  print(gift["title"])