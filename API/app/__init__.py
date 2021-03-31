from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import *
import pymongo

mongo = pymongo.MongoClient(MONGO_URL, MONGO_PORT, username=MONGO_USER, password=MONGO_PWD)
db = mongo[MONGO_DATABASE]

api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app import routes