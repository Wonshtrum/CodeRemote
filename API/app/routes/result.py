from app import api
from app.services.databases import db
from fastapi import Response, status
from pydantic import BaseModel
from app.config import *

class Data(BaseModel):
	hash: str
	

@api.post('/result')
async def post_result(data: Data,response: Response):
    h=data.hash
    res=db.find_one("results",hash=h)

    if res is None:
        check=db.find_one("requests",hash=h)
        if check is None:
            response.status_code=status.HTTP_404_NOT_FOUND
            return {"status":"Request with this hash not found"}
        for e in db.watch('results'):
            if e["hash"] == h:
                del e["_id"]
                res=e
                break
    return {"status": "Result successfully returned", "data":res}


