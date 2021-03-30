from app import api,mongo
#from typing import Optional
#from fastapi import FastAPI, Response, status
from pydantic import BaseModel

class Message(BaseModel):
	text: str

@api.put('/test')
async def put_message(msg:Message):	
	db = mongo["dbTest"]
	coll = db["collecTest"]
	coll.insert(msg)
	return {"status": "Message added successfully"}


