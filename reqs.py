# this is for requests to server
import cryptic_sdk as cryptic
import os
import atexit


class CrypticClient:
    def __init__(self):
        atexit.register(self.close)
        self.client: cryptic.Client = None

    def login(self, username, password):
        self.client = cryptic.Client('wss://ws.cryptic-game.net')
        self.client.login(username, password)

    def logout(self):
        self.client.logout()

    def get_all_money(self, uuid, key):
        wallet: cryptic.Wallet = self.client.getUser().getWallet(uuid, key)
        return wallet.amount

    def close(self):
        self.logout()
        self.client.websocket.close()
