from app import api
from typing import Optional,List
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
	lang: str
	profile: Optional[Profile]
	files: List[File]


@api.put('/compile')
async def put_request(dem: Demande):
	id = str(token_urlsafe(32))
	return {"status": "Compile request added successfully", "data":{"hash": id}}
