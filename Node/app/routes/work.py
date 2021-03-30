from fastapi import Response
from app import api, WorkManager
from typing import Optional, List
from pydantic import BaseModel


class Profile(BaseModel):
	token: str
	ram: float
	cpu: float
	time: float

class File(BaseModel):
	name: str
	content: str

class Request(BaseModel):
	hash: str
	lang: str
	profile: Profile
	files: List[File]


@api.put('/work', status_code = 202)
def put_work(request: Request, response: Response):
	if WorkManager.submit(request):
		return { 'status': 'Request submitted' }
	response.status_code = 503
	return { 'status': 'Node is overworked' }
