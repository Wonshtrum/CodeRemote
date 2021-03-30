from app import api, db
from typing import Optional,List
#from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from secrets import token_urlsafe

class Profile(BaseModel):
	token: str
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
	coll = db["requests"]
	dem.state = 0
	id = str(token_urlsafe(32))
	dem.hash = id
	coll.insert(dem.dict())
	return {"status": "Compile request added successfully", "hash": id}


