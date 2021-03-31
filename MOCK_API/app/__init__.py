from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import *

api = FastAPI()
api.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_methods=["*"],
	allow_headers=["*"]
)

from app import routes
