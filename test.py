from pymongo import MongoClient
### Setup db connections
client = MongoClient('localhost', 27017)
db = client.test_database
collection = db.test_collection


username = "userName"
res = db.test_collection.find_one({"user_name": username}, {"pass": 1})


# print res.count()
print res

print res["pass"]


