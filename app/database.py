import os
from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)

db = client["bowls_db"]

item_master = db["item_master"]
user_master = db["user_master"]
cart_master = db["cart_master"]