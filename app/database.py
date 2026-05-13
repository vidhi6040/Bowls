from pymongo import MongoClient

<<<<<<< HEAD
#client = MongoClient("mongodb://mongodb:27017")
=======
#client = MongoClient("mongodb://localhost:27017")
>>>>>>> 0e843842875e32be52dc497eb06e758b1b0595ab
#client = MongoClient("mongodb://host.docker.internal:27017")
client = MongoClient("mongodb://mongodb:27017")

db = client["bowls_db"]
item_master = db["item_master"]
user_master = db["user_master"]
cart_master = db["cart_master"]
