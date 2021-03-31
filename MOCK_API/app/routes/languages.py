from app import api


@api.get('/languages')
async def get_languages():	
	return {"status": "Languages fetched successfully", "data":["python3", "c++", "c", "prolog"]}
