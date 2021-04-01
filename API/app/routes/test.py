from app import api
from app.services.databases import db
#from typing import Optional
#from fastapi import FastAPI, Response, status
from pydantic import BaseModel

class Message(BaseModel):
	text: str

@api.put('/test')
async def put_message(msg:Message):	
	db.insert("dbTest",msg)
	return {"status": "Message added successfully"}


