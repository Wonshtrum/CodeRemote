from app import api
import json
from app.config import CONFIG_PATH
#from typing import Optional
#from fastapi import FastAPI, Response, status


@api.get('/languages')
async def get_languages():	
	with open(CONFIG_PATH) as f:
  		data = json.load(f)
	res = [e["lang"] for e in data]
	return {"status": "Languages fetched successfully", "data": res}


