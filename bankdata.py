import pymongo
databases = pymongo.MongoClient("mongodb://localhost:27017/")

db = databases["BlackBay"]

clients = db["clients"]
#{"user_id": INT, "user_name": STR}

wallets = db["wallets"]
#{"amount": FLOAT, "users": LIST[object_id], "channel_id": FLOAT"}

print("Datenbank initialisiert.")






#clients.insert_one({"user_id": "hallo", "amount": 123})
#clients.insert_one({"user_id": "adawdaw", "amount": 312313})
#print(clients.find_one({"user_id": "hallo"})["amount"])