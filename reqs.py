#this is for requests to server
import cryptic_sdk as cryptic
from dotenv import load_dotenv
import os


load_dotenv()
cryptic_user = os.getenv('env_user')
cryptic_password = os.getenv('env_password')

def login():
    client = cryptic.Client('wss://ws.cryptic-game.net')
    client.login(cryptic_user, cryptic_password)

def logout():
    cryptic.client.logout()