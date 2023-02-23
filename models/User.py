from pymongo import MongoClient
from env import *

CLIENT = MongoClient(env("mongo_uri"))
COLLECTION = CLIENT['jarvis']['users']

class User:
    first_name = ""
    username = ""
    last_name = ""
    telegram_id = 0
    email = ''

    def __init__(self, first_name=None,username=None,last_name=None,telegram_id=None):
        self.first_name = first_name
        self.username = username
        self.last_name = last_name
        self.telegram_id = telegram_id


    @staticmethod
    def save_from_telegram(telegram_user):
        user = User()
        user.telegram_id = telegram_user.id
        user.first_name = telegram_user.first_name
        user.username = telegram_user.username
        user.last_name = telegram_user.last_name


    def save(self):
        try:
            return COLLECTION.insert_one(self)
        except Exception as ex:
            return ex


    def update(self):
        try:
            return COLLECTION.update_one(self)
        except Exception as ex:
            return ex

    def delete(self):
        try:
            return COLLECTION.remove(self)
        except Exception as ex:
            return ex

