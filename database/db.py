from pymongo import MongoClient
from django.conf import settings


try:
    client = MongoClient("mongodb://localhost:27017/")
    client.admin.command("ping")

    db = client[settings.MONGO_DB["DATABASE"]]
    print("Connected !!")


except Exception as err:
    print("Database Conneciton Error")
