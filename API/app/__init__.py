from fastapi import FastAPI
from app.config import *
import pymongo

mongo=pymongo.MongoClient(MONGO_URL,MONGO_PORT,username=MONGO_USER,password=MONGO_PWD)
db = mongo[MONGO_DATABASE]

api = FastAPI()

from app import routes