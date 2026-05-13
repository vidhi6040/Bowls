from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
#client = MongoClient("mongodb://host.docker.internal:27017")

db = client["bowls_db"]
item_master = db["item_master"]
user_master = db["user_master"]
cart_master = db["cart_master"]
