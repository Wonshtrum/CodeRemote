from fastapi import FastAPI
from app.config import *

api = FastAPI()

from app import routes
