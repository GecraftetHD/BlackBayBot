import pymongo
from bson.objectid import ObjectId

databases = pymongo.MongoClient("mongodb://localhost:27017/")

db = databases["BlackBay"]
clients = db["clients"]

# {"user_id": INT, "user_name": STR}

wallets = db["wallets"]
# {"amount": FLOAT, "users": LIST[object_id], "channel_id": FLOAT"}

utils = db["utils"]

print("Datenbank initialisiert.")


def insert_bank_channel(channel_id, message_id):
    utils.insert_one({"channel_id": channel_id, "message_id": message_id})


def is_bankchannel(channel_id, message_id):
    return utils.find_one({"channel_id": channel_id, "message_id": message_id}) is not None


def insert_employee(role_id):
    utils.insert_one({"employee_id": role_id})


def get_employee():
    role_id = utils.find_one({})
    return role_id


def is_client(user_id):
    return clients.find_one({"user_id": user_id}) is not None


def create_client(user_id, member):
    client = clients.insert_one({"user_id": user_id, "name": str(member)})
    return get_client(user_id)


def insert_wallet(channel_id, owner_id, member, channel_name):
    if is_client(owner_id):
        client = get_client(owner_id)
    else:
        client = create_client(owner_id, member)

    wallets.insert_one(
        {"amount": 0.0, "users": [client], "channel_id": channel_id, "channel_name": channel_name, "status": "active"})


def get_client(user_id):
    client = clients.find_one({"user_id": user_id})
    return ObjectId(client["_id"])


def close_status(channel_id):
    wallet = wallets.find_one({"channel_id": channel_id})
    print(wallet)
    wallet.edit_one({"status": "closed"})
    wallet = wallets.find_one({"channel_id": channel_id})
    wallets.find_one_and_update()
    print(wallet)
