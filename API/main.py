from app import api
from app.config import *
import uvicorn


if __name__ == '__main__':
	uvicorn.run("main:api", host=HOST, port=PORT, reload=True)
