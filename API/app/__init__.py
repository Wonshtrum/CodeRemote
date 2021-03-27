from fastapi import FastAPI
from app import config
import pymongo

mongo=pymongo.MongoClient(config.MONGO_URL,config.MONGO_PORT)

print(mongo.list_database_names())
api = FastAPI()

from app import routes