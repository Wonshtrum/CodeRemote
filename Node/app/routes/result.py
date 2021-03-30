from fastapi import Response
from app import api, WorkManager
from pydantic import BaseModel


class Request(BaseModel):
	hash: str


@api.post('/result')
def get_result(request: Request, response: Response):
	result = WorkManager.request(request.hash)
	if result is None:
		response.status_code = 404
		return { 'status': 'No job with this hash' }
	status, data = result
	return { 'status': status, 'data': data }
