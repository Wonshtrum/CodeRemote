from app import api
from app.services.databases import db
from typing import Optional,List
#from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from secrets import token_urlsafe
from app.config import *
import json

class Profile(BaseModel):
	token: Optional[str]
	ram: float
	cpu: float
	time: float

class File(BaseModel):
	name: str
	content:str

class Demande(BaseModel):
	hash: Optional[str]
	state: Optional[int]
	lang: str
	profile: Profile
	files: List[File]


@api.put('/compile')
async def put_request(dem: Demande):
	with open(DEFAULT_PROFILE_PATH) as f:
  		profil = json.load(f)
	dem.state = 0
	dem.state=profil
	id = str(token_urlsafe(32))
	dem.hash = id
	db.insert("requests",dem.dict())
	return {"status": "Compile request added successfully", "hash": id}


