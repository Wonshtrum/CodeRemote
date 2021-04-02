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

class Request(BaseModel):
	hash: Optional[str]
	state: Optional[int]
	lang: str
	profile: Optional[Profile]
	files: List[File]


@api.put('/compile')
async def put_request(req: Request):
	req=req.dict()
	with open(DEFAULT_PROFILE_PATH) as f:
  		profile = json.load(f)
	id = str(token_urlsafe(32))
	req["state"] = 0
	req["profile"]=profile	
	req["hash"] = id
	db.insert("requests",req)
	return {"status": "Compile request added successfully", "data":{"hash": id}}


