from app import config
from fastapi import FastAPI
from app.services.workers import Manager


api = FastAPI()
WorkManager = Manager(config.NUM_WORKERS)


import app.routes
