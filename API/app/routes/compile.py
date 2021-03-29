from app import api,db
from typing import Optional,List
#from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from secrets import token_bytes

class Profile(BaseModel):
	token: str
	ram:float
	cpu:float
	time:float

class File(BaseModel):
	name:str
	content:str

class Demande(BaseModel):
	hash: Optional[str]
	state: Optional[int]
	lang: str
	profile: Profile
	files: List[File]


@api.put('/compile')
async def put_message(dem:Demande):
	coll=db["requests"]
	dem["state"]=0
	hash=str(token_bytes(32))
	dem["hash"]=hash
	coll.insert(dem)
	return {"status":"Compile request added successfully","hash":hash}


