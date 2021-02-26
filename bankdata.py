import pymongo
from bson.objectid import ObjectId
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

def insert_employee(id):
    utils = db["utils"]
    utils.insert_one({"employee_id": id})
    pass

def get_employee():
    utils =db["utils"]
    id = utils.find({"employee_id"})
    print(id)
    return id

def is_client(user_id):
    return clients.count_documents({"user_id": user_id}) == 1

def create_client(user_id, member):
    client = clients.insert_one({"user_id": user_id, "name": str(member)})
    return get_client(user_id)


def insert_wallet(channel_id, owner_id, member, channel_name):
    if is_client(owner_id):
        client = get_client(owner_id)
    else:
        client = create_client(owner_id, member)

    wallets.insert_one({"amount": 0.0, "users": [client], "channel_id": channel_id, "channel_name": channel_name})



def get_client(user_id):
    client = clients.find_one({"user_id": user_id})
    return ObjectId(client["_id"])








#clients.insert_one({"user_id": "hallo", "amount": 123})
#clients.insert_one({"user_id": "adawdaw", "amount": 312313})
#print(clients.find_one({"user_id": "hallo"})["amount"])