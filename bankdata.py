import pymongo
databases = pymongo.MongoClient("mongodb://localhost:27017/")

db = databases["BlackBay"]
clients = db["clients"]
#{"user_id": INT, "user_name": STR}

wallets = db["wallets"]
#{"amount": FLOAT, "users": LIST[object_id], "channel_id": FLOAT"}

print("Datenbank initialisiert.")

def insert_bank_channel(channel_id, message_id):
    utils = db["utils"]
    print(utils)
    utils.insert_one({"channel_id": channel_id, "message_id": message_id})


def is_bankchannel(channel_id, message_id):
    utils = db["utils"]
    return utils.count_documents({"channel_id": channel_id, "message_id": message_id}) > 0









#clients.insert_one({"user_id": "hallo", "amount": 123})
#clients.insert_one({"user_id": "adawdaw", "amount": 312313})
#print(clients.find_one({"user_id": "hallo"})["amount"])